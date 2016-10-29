# -*- coding:utf-8 -*-

import json
import tornado.escape
import tornado.web
import config
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.label_model import MPost2Label
from torcms.model.post_model import MPost
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_hist_model import MPostHist
from torcms.model.relation_model import MRelation
from config import router_post


class PostHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mpost = MPost()
        self.mcat = MCategory()
        self.cats = self.mcat.query_all()
        self.mpost_hist = MPostHist()
        self.mpost2catalog = MPost2Catalog()
        self.mpost2label = MPost2Label()
        self.mrel = MRelation()
        self.kind = '1'

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_str == '':
            self.index()
        elif len(url_arr) == 1 and url_str.endswith('.html'):
            self.view_or_add(url_str.split('.')[0])
        elif url_arr[0] in ['add_document', '_add']:
            self.to_add()
        elif url_str == 'recent':
            self.recent()
        elif url_str == '_refresh':
            self.refresh()
        elif url_arr[0] in ['modify', 'edit']:
            self.to_edit(url_arr[1])
        elif url_arr[0] == 'delete':
            self.delete(url_arr[1])
        elif url_arr[0] == 'ajax_count_plus':
            self.ajax_count_plus(url_arr[1])
        elif len(url_arr) == 1:
            self.view_or_add(url_str)
        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )



    def post(self, url_str=''):
        print('post url:', url_str)
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['modify', 'edit', '_edit']:
            self.update(url_arr[1])
        elif url_arr[0] in ['add_document', '_add']:
            self.add()
        elif len(url_arr) == 1:
            if len(url_str) in [4, 5]:
                self.add(url_str)
        else:
            self.redirect('html/404.html')

    def index(self):
        print('index', self.kind)
        self.render('post_{0}/index.html'.format(self.kind),
                    userinfo=self.userinfo,
                    kwd={'uid': '',}
                    )
    def ajax_count_plus(self, uid):
        output = {
            'status': 1 if self.mpost.update_view_count_by_uid(uid) else 0,
        }
        return json.dump(output, self)

    @tornado.web.authenticated
    def extra_data(self, ext_dic, post_data):
        '''
        The additional information.
        :param post_data:
        :return: directory.
        '''
        return ext_dic

    def recent(self, with_catalog=True, with_date=True):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '最近文档',
            'with_catalog': with_catalog,
            'with_date': with_date,
        }
        self.render('post_{0}/post_list.html'.format(self.kind),
                    kwd=kwd,
                    view=self.mpost.query_recent(num=20, kind=self.kind),
                    postinfo=self.mpost.query_recent(num=20, kind=self.kind),
                    # view_all=self.mpost.query_all(),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    cfg=config.cfg,
                    )

    @tornado.web.authenticated
    def __could_edit(self, postid):

        post_rec = self.mpost.get_by_uid(postid)
        if not post_rec:
            return False
        if self.check_post_role(self.userinfo)['EDIT'] or post_rec.user_name == self.userinfo.user_name:
            return True
        else:
            return False

    def refresh(self):

        kwd = {
            'pager': '',
            'title': '最近文档',
        }
        self.render('post_{0}/post_list.html'.format(self.kind),
                    kwd=kwd,
                    userinfo=self.userinfo,
                    view=self.mpost.query_dated(10),
                    postrecs=self.mpost.query_dated(10),
                    format_date=tools.format_date,
                    unescape=tornado.escape.xhtml_unescape,
                    cfg=config.cfg, )

    # def get_random(self):
    #     return self.mpost.query_random()

    def view_or_add(self, uid):
        print('self.kind:', self.kind, uid)
        if self.mpost.get_by_id(uid):
            self.view_post(uid)
        else:
            self.to_add(uid)

    @tornado.web.authenticated
    def to_add(self, uid=''):
        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        kwd = {
            'pager': '',
            'cats': self.cats,
            'uid': '',

        }
        self.render('post_{0}/post_add.html'.format(self.kind),
                    kwd=kwd,
                    tag_infos=self.mcat.query_all(),
                    userinfo=self.userinfo,
                    cfg=config.cfg,
                    )

    @tornado.web.authenticated
    def update(self, uid):
        if self.__could_edit(uid):
            pass
        else:
            return False

        postinfo = self.mpost.get_by_id(uid)
        if postinfo.kind == self.kind:
            pass
        else:
            return False

        post_data = self.get_post_data()

        post_data['user_name'] = self.get_current_user()
        post_data['kind'] = self.kind
        is_update_time = True if post_data['is_update_time'][0] == '1' else False

        cnt_old = tornado.escape.xhtml_unescape(postinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            self.mpost_hist.insert_data(postinfo)

        print('upadte, ', uid)
        print('post_data:', post_data)
        self.mpost.update(uid, post_data, update_time=is_update_time)
        self.update_category(uid)
        self.update_tag(uid)
        self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], uid))

    @tornado.web.authenticated
    def update_tag(self, signature):
        current_tag_infos = self.mpost2label.get_by_id(signature, kind=self.kind)
        post_data = self.get_post_data()
        if 'tags' in post_data:
            pass
        else:
            return False

        print('tags: {0}'.format(post_data['tags']))
        tags_arr = [x.strip() for x in post_data['tags'].split(',')]
        for tag_name in tags_arr:
            if tag_name == '':
                pass
            else:
                self.mpost2label.add_record(signature, tag_name, 1)

        for cur_info in current_tag_infos:
            print(cur_info.tag.name)
            if cur_info.tag.name in tags_arr:
                pass
            else:
                self.mpost2label.remove_relation(signature, cur_info.tag)

    @tornado.web.authenticated
    def update_category(self, uid):
        post_data = self.get_post_data()

        current_infos = self.mpost2catalog.query_by_entity_uid(uid)
        new_tag_arr = []
        # HTML中预定义的
        def_cate_arr = ['gcat{0}'.format(x) for x in range(10)]
        # todo: next line should be deleted. keep here for historical reason.
        def_cate_arr.append('def_cat_uid')

        for key in def_cate_arr:
            if key in post_data:
                pass
            else:
                continue
            print('a' * 4)
            print(post_data[key])
            if post_data[key] == '' or post_data[key] == '0':
                continue
            # if len(post_data[key]) != 4:
            #     continue
            print(post_data[key])
            print(new_tag_arr)
            # 有可能选重复了。保留前面的
            if post_data[key] in new_tag_arr:
                continue

            new_tag_arr.append(post_data[key] + ' ' * (4 - len(post_data[key])))

        for idx, val in enumerate(new_tag_arr):
            self.mpost2catalog.add_record(uid, val, idx)

        # 对原来的进行处理，如果不在现有中，则删除
        for cur_info in current_infos:
            if str(cur_info.tag.uid).strip() not in new_tag_arr:
                self.mpost2catalog.remove_relation(uid, cur_info.tag)

    @tornado.web.authenticated
    def to_edit(self, id_rec):
        if self.__could_edit(id_rec):
            pass
        else:
            return False

        kwd = {
            'pager': '',
            'cats': self.cats,

        }
        self.render('post_{0}/post_edit.html'.format(self.kind),
                    kwd=kwd,
                    unescape=tornado.escape.xhtml_unescape,
                    tag_infos=self.mcat.query_all(kind=self.kind),
                    app2label_info=self.mpost2label.get_by_id(id_rec),
                    app2tag_info=self.mpost2catalog.query_by_entity_uid(id_rec, self.kind),
                    dbrec=self.mpost.get_by_id(id_rec),
                    userinfo=self.userinfo,
                    cfg=config.cfg,
                    )

    def get_cat_str(self, cats):
        cat_arr = cats.split(',')
        out_str = ''
        for xx in self.cats:
            if str(xx.uid) in cat_arr:
                tmp_str = '''<li><a href="/category/{0}" style="margin:10px auto;"> {1} </a></li>
                '''.format(xx.slug, tornado.escape.xhtml_escape(xx.name))
                out_str += tmp_str

        return (out_str)

    def get_cat_name(self, id_cat):
        for x in self.cats:
            if x['id_cat'] == id_cat:
                return (x['name'])

    def __gen_last_current_relation(self, post_id):
        '''
        Generate the relation for the post and last post viewed.
        :param post_id:
        :return:
        '''
        last_post_id = self.get_secure_cookie('last_post_uid')
        if last_post_id:
            last_post_id = last_post_id.decode('utf-8')
        self.set_secure_cookie('last_post_uid', post_id)

        if last_post_id and self.mpost.get_by_id(last_post_id):
            self.add_relation(last_post_id, post_id)

    def view_post(self, post_id):
        self.__gen_last_current_relation(post_id)

        cats = self.mpost2catalog.query_by_entity_uid(post_id)
        # replys = self.mpost2reply.get_by_id(post_id)
        tag_info = self.mpost2label.get_by_id(post_id)

        postinfo = self.mpost.get_by_id(post_id)


        if postinfo.kind == self.kind:
            pass
        else:
            self.set_status(301)
            self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], post_id))


        if not postinfo:
            kwd = {
                'info': '您要查看的页面不存在。',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo)
            return False

        if cats.count() == 0:
            cat_id = ''
        else:
            cat_id = cats.get().tag
        kwd = {
            'pager': '',
            'editable': self.editable(),
            'cat_id': cat_id
        }

        rel_recs = self.mrel.get_app_relations(postinfo.uid, 4)

        rand_recs = self.mpost.query_random(4 - rel_recs.count() + 2)

        self.render('post_{0}/post_view.html'.format(self.kind),
                    view=postinfo,
                    postinfo=postinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    tag_info=tag_info,
                    relations=rel_recs,
                    rand_recs=rand_recs,
                    replys=[],
                    cfg=config.cfg,
                    )

    def add_relation(self, f_uid, t_uid):
        if self.mpost.get_by_id(t_uid) is False:
            return False
        if f_uid == t_uid:
            '''
            关联其本身
            '''
            return False
        # 双向关联，但权重不一样.
        self.mrel.add_relation(f_uid, t_uid, 2)
        self.mrel.add_relation(t_uid, f_uid, 1)
        return True

    @tornado.web.authenticated
    def add(self, uid=''):
        print('adding:', uid)
        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        post_data = self.get_post_data()
        if not ('title' in post_data):
            self.set_status(400)
            return False
        else:
            pass

        id_post = uid
        if id_post == '':
            id_post = self.gen_uid()

        post_data['user_name'] = self.userinfo.user_name
        post_data['kind'] = self.kind
        cur_post_rec = self.mpost.get_by_id(id_post)
        if cur_post_rec:
            pass
        else:
            if self.mpost.insert_data(id_post, post_data):
                self.update_tag(id_post)
                self.update_category(id_post)
        self.redirect('/{0}/{1}'.format(router_post[self.kind], id_post))

    def gen_uid(self):
        cur_uid = tools.get_uu5d()
        while self.mpost.get_by_id(cur_uid):
            cur_uid = tools.get_uu5d()
        return cur_uid

    @tornado.web.authenticated
    def delete(self, del_id):
        if self.check_post_role(self.userinfo)['DELETE']:
            pass
        else:
            return False
        is_deleted = self.mpost.delete(del_id)
        if is_deleted:
            self.redirect('/{0}/recent'.format(router_post[self.kind]))
        else:
            return False


class PostAjaxHandler(PostHandler):
    def initialize(self):
        self.init()
        self.mpost = MPost()
        self.mcat = MCategory()
        self.cats = self.mcat.query_all()
        self.mpost_hist = MPostHist()
        self.mpost2catalog = MPost2Catalog()
        # self.mpost2reply = MPost2Reply()
        self.mpost2label = MPost2Label()
        self.mrel = MRelation()
        self.tmpl_dir = 'admin'
        self.tmpl_router = 'post_ajax'

    @tornado.web.authenticated
    def delete(self, del_id):
        if self.check_post_role(self.userinfo)['DELETE']:
            pass
        else:
            return False
        is_deleted = self.mpost.delete(del_id)

        if is_deleted:
            output = {
                'del_info ': 1,
            }
        else:
            output = {
                'del_info ': 0,
            }
        return json.dump(output, self)
