# -*- coding:utf-8 -*-


import random
import tornado.escape
import tornado.web
import tornado.gen

from torcms.core import tools
from torcms.model.infor2label_model import MInfor2Label
from torcms.model.info_model import MInfor
from torcms.model.info_relation_model import MInforRel
from torcms.model.evaluation_model import MEvaluation
from torcms.model.category_model import MCategory
from torcms.model.usage_model import MUsage
from torcms.model.infor2catalog_model import MInfor2Catalog
from torcms.model.reply_model import MReply
from torcms.handlers.post_handler import PostHandler
from torcms.model.info_hist_model import MInfoHist
from config import router_post

class InfoHandler(PostHandler):
    def initialize(self, hinfo=''):
        self.init()
        self.mevaluation = MEvaluation()
        self.mpost2label = MInfor2Label()
        self.mpost2catalog = MInfor2Catalog()
        self.mpost = MInfor()
        self.musage = MUsage()
        self.mcat = MCategory()
        self.mrel = MInforRel()
        self.mreply = MReply()
        self.mpost_hist = MInfoHist()
        self.kind = '2'
        self.sig = '2'  # '1' for maplet,  '2' for drr

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_str == '':
            self.index()
        elif url_arr[0] in ['cat_add', '_cat_add']:
            self.to_add_with_category(url_arr[1])
        elif url_arr[0] in ['_add', 'add_document']:
            self.to_add()
        # elif url_arr[0] == 'catalog':
        #     self.catalog()
        elif len(url_arr) == 2:
            if url_arr[0] in ['edit', 'modify', '_edit']:
                self.to_edit(url_arr[1])
            elif url_arr[0] == 'add':
                self.to_add(url_arr[1])
            elif url_arr[0] == 'delete':
                self.to_del_app(url_arr[1])
            else:
                '''
                从相关计算中过来的。
                '''
                pass
                # self.mrel.update_relation(url_arr[1], url_arr[0])
                # self.redirect('/{0}/{1}'.format(self.app_url_name, url_arr[0]))

        elif len(url_arr) == 1:
            if len(url_str) in [4, 5]:
                self.view_info(url_str)

        else:
            kwd = {
                'title': '',
                'info': '',
            }
            self.set_status(404)
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, url_str=''):

        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['to_add', '_add']:
            self.add()
        elif url_arr[0] == 'rel':
            if self.get_current_user():
                self.add_relation(url_arr[1])
            else:
                self.redirect('/user/login')
        # elif url_arr[0] == 'comment_add':
        #     self.add_comment(url_arr[1])
        elif url_arr[0] in ['edit', '_edit']:
            self.update(url_arr[1])
        elif url_arr[0] == 'add':
            self.add(url_arr[1])

        elif url_arr[0] == 'rel':
            if self.get_current_user():
                self.add_relation(url_arr[1], url_arr[2])
            else:
                self.redirect('/user/login')
        # elif url_arr[0] == 'comment_add':
        #     self.add_comment(url_arr[1])
        else:
            return False

    # @tornado.web.authenticated
    # def add_comment(self, id_post):
    #     post_data = {}
    #     for key in self.request.arguments:
    #         post_data[key] = self.get_arguments(key)
    #     post_data['user_id'] = self.userinfo.uid
    #     post_data['user_name'] = self.userinfo.user_name
    #     comment_uid = self.mreply.insert_data(post_data, id_post)
    #     if comment_uid:
    #         output = {
    #             'pinglun': comment_uid,
    #         }
    #     else:
    #         output = {
    #             'pinglun': 0,
    #         }
    #     return json.dump(output, self)


    def view_info(self, info_id):
        '''
        Render the info
        :param info_id:
        :return: Nonthing.
        '''
        postinfo = self.mpost.get_by_uid(info_id)
        if postinfo.kind == self.kind:
            pass
        else:
            return

        if postinfo:
            pass
        else:
            kwd = {
                'info': '您要找的信息不存在。',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo, )
            return False
        #
        cats = self.mpost2catalog.query_by_entity_uid(info_id, kind=postinfo.kind)
        cat_uid_arr = []
        for cat_rec in cats:
            cat_uid = cat_rec.tag.uid
            cat_uid_arr.append(cat_uid)
        print('info category:', cat_uid_arr)

        rel_recs = self.mrel.get_app_relations(postinfo.uid, 8, kind=postinfo.kind)
        print('rel_recs count:', rel_recs.count())
        if len(cat_uid_arr) > 0:
            rand_recs = self.mpost.query_cat_random(cat_uid_arr[0], 4 - rel_recs.count() + 4)
        else:
            rand_recs = self.mpost.query_random(num=4 - rel_recs.count() + 4, kind=postinfo.kind)

        self.chuli_cookie_relation(info_id)
        cookie_str = tools.get_uuid()

        if 'def_cat_uid' in postinfo.extinfo:
            ext_catid = postinfo.extinfo['def_cat_uid']
        else:
            ext_catid = ''

        if len(ext_catid) == 4:
            pass
        else:
            ext_catid = ''

        # parent_name = ''
        # cat_name = ''
        # parentname = ''
        # catname = ''
        catinfo = None
        p_catinfo = None
        if ext_catid != '':
            catinfo = self.mcat.get_by_uid(ext_catid)
            p_catinfo = self.mcat.get_by_uid(catinfo.pid)

        kwd = {
            'pager': '',
            'url': self.request.uri,
            'cookie_str': cookie_str,
            'daohangstr': '',
            'signature': info_id,
            'tdesc': '',
            'eval_0': self.mevaluation.app_evaluation_count(info_id, 0),
            'eval_1': self.mevaluation.app_evaluation_count(info_id, 1),
            'login': 1 if self.get_current_user() else 0,
            'has_image': 0,
            'parentlist': self.mcat.get_parent_list(),
            'parentname': '',
            'catname': '',
        }
        self.mpost.view_count_increase(info_id)
        if self.get_current_user():
            self.musage.add_or_update(self.userinfo.uid, info_id, postinfo.kind)
        self.set_cookie('user_pass', cookie_str)
        tmpl = self.ext_tmpl_name(postinfo) if self.ext_tmpl_name(postinfo) else self.get_tmpl_name(postinfo)

        print('info tmpl: ' + tmpl)
        ext_catid2 = postinfo.extinfo['def_cat_uid'] if 'def_cat_uid' in postinfo.extinfo else None

        if self.userinfo:
            recent_apps = self.musage.query_recent(self.userinfo.uid, postinfo.kind, 6)[1:]
        else:
            recent_apps = []
        self.render(tmpl,
                    kwd=dict(kwd, **self.extra_kwd(postinfo)),
                    calc_info=postinfo,  # Deprecated
                    post_info=postinfo,  # Deprecated
                    postinfo=postinfo,
                    userinfo=self.userinfo,
                    catinfo=catinfo,
                    pcatinfo=p_catinfo,

                    relations=rel_recs,
                    rand_recs=rand_recs,
                    unescape=tornado.escape.xhtml_unescape,
                    ad_switch=random.randint(1, 18),
                    tag_info=self.mpost2label.get_by_id(info_id),

                    recent_apps=recent_apps,
                    cat_enum=self.mcat.get_qian2(ext_catid2[:2]) if ext_catid else [],
                    )

    def extra_kwd(self, info_rec):
        '''
        The additional information.
        :param info_rec:
        :return: directory.
        '''
        return {}

    def chuli_cookie_relation(self, app_id):
        '''
        The current Info and the Info viewed last should have some relation.
        And the last viewed Info could be found from cookie.
        :param app_id: the current app
        :return: None
        '''
        last_app_uid = self.get_secure_cookie('use_app_uid')
        if last_app_uid:
            last_app_uid = last_app_uid.decode('utf-8')
        self.set_secure_cookie('use_app_uid', app_id)
        if last_app_uid and self.mpost.get_by_uid(last_app_uid):
            self.add_relation(last_app_uid, app_id)

    def ext_tmpl_name(self, rec):
        return None

    def get_tmpl_name(self, rec):
        '''
        According to the application, each info of it's classification could has different temaplate.
        :param rec: the App record.
        :return: the temaplte path.
        '''
        if 'def_cat_uid' in rec.extinfo and rec.extinfo['def_cat_uid'] != '':
            cat_id = rec.extinfo['def_cat_uid']
        else:
            cat_id = False
        if cat_id and self.sig == '2':
            tmpl = 'autogen/view/view_{0}.html'.format(cat_id)
        else:
            tmpl = 'post_{0}/show_map.html'.format(self.kind)
        return tmpl

    def add_relation(self, f_uid, t_uid):
        '''
        Add the relation. And the from and to, should have different weight.
        :param f_uid:
        :param t_uid:
        :return: return True if the relation has been succesfully added.
        '''
        if self.mpost.get_by_uid(t_uid):
            pass
        else:
            return False
        if f_uid == t_uid:
            return False

        # 针对分类进行处理。只有落入相同分类的，才加1
        f_cats = self.mpost2catalog.query_by_entity_uid(f_uid)
        t_cats = self.mpost2catalog.query_by_entity_uid(t_uid)
        flag = False

        for f_cat in f_cats:
            print(f_cat.tag)
            for t_cat in t_cats:
                print(t_cat.tag)
                if f_cat.tag == t_cat.tag:
                    flag = True
        if flag:
            pass
        else:
            return False

        self.mrel.add_relation(f_uid, t_uid, 2)
        self.mrel.add_relation(t_uid, f_uid, 1)
        return True

    # def add_relation(self, f_uid, t_uid):
    #     if False == self.mpost.get_by_uid(t_uid):
    #         return False
    #     if f_uid == t_uid:
    #         '''
    #         关联其本身
    #         '''
    #         return False
    #     self.mrel.add_relation(f_uid, t_uid, 2)
    #     self.mrel.add_relation(t_uid, f_uid, 1)
    #     return True

    #
    #
    # def catalog(self):
    #     self.render('post{0}/catalog.html'.format(self.kind),
    #                 userinfo=self.userinfo,
    #                 kwd={'uid': '',}
    #                 )


    def gen_uid(self):
        cur_uid = self.kind + tools.get_uu4d()
        while self.mpost.get_by_id(cur_uid):
            cur_uid = self.kind + tools.get_uu4d()
        return cur_uid

    @tornado.web.authenticated
    def to_add_with_category(self, catid):
        '''
        Used for OSGeo
        :param catid:
        :param sig:
        :return:
        '''
        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        catinfo = self.mcat.get_by_uid(catid)
        kwd = {
            'uid': self.gen_uid(),
            'userid': self.userinfo.user_name,
            'def_cat_uid': catid,
            'parentname': self.mcat.get_by_id(catinfo.pid).name,
            'catname': self.mcat.get_by_id(catid).name,
        }

        self.render('autogen/add/add_{0}.html'.format(catid),
                    userinfo=self.userinfo,
                    kwd=kwd)

    @tornado.web.authenticated
    def to_add(self, uid=''):
        # Used for yunsuan, maplet
        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        if uid != '' and self.mpost.get_by_uid(uid):
            # todo:
            # self.redirect('/{0}/edit/{1}'.format(self.app_url_name, uid))
            pass
        self.render('post{0}/add.html'.format(self.kind),
                    tag_infos=self.mcat.query_all(by_order=True, kind=self.kind),
                    userinfo=self.userinfo,
                    kwd={'uid': uid,}
                    )

    @tornado.web.authenticated
    def to_del_app(self, uid):
        current_infor = self.mpost.get_by_uid(uid)

        if self.check_post_role(self.userinfo)['DELETE']:
            pass
        else:
            return False

        if self.mpost.delete(uid):
            self.redirect('/list/{0}'.format(current_infor.extinfo['def_cat_uid']))
        else:
            self.redirect('/{0}/{1}'.format(router_post[self.kind], uid))

    @tornado.web.authenticated
    def to_edit(self, infoid):

        if self.check_post_role(self.userinfo)['EDIT']:
            pass
        else:
            return False

        rec_info = self.mpost.get_by_uid(infoid)

        if rec_info:
            pass
        else:
            self.render('html/404.html')
            return
        if 'def_cat_uid' in rec_info.extinfo:
            catid = rec_info.extinfo['def_cat_uid']
        else:
            catid = ''

        if len(catid) == 4:
            pass
        else:
            catid = ''

        # p_name = ''
        # if catid != '':
        #     if self.mcat.get_by_id(catid[:2] + 'zz'):
        #         p_name = self.mcat.get_by_id(catid[:2] + 'zz').name
        # c_name = ''
        # if catid != '':
        #     if self.mcat.get_by_id(catid):
        #         c_name = self.mcat.get_by_id(catid).name

        catinfo = None
        p_catinfo = None
        if catid != '':
            catinfo = self.mcat.get_by_uid(catid)
            p_catinfo = self.mcat.get_by_uid(catinfo.pid)

        kwd = {
            'def_cat_uid': catid,
            'parentname': '',
            'catname': '',
            'parentlist': self.mcat.get_parent_list(),
            'userip': self.request.remote_ip
        }

        if self.sig == '2':
            tmpl = 'autogen/edit/edit_{0}.html'.format(catid)
        else:
            tmpl = 'post_{0}/edit.html'.format(self.kind)

        # print('site_type: ', cfg['site_type'])
        # print('Meta template:', tmpl)

        self.render(tmpl,
                    kwd=kwd,
                    calc_info=rec_info,  # Deprecated
                    post_info=rec_info,  # Deprecated
                    app_info=rec_info,  # Deprecated
                    postinfo=rec_info,

                    catinfo=catinfo,
                    pcatinfo=p_catinfo,


                    userinfo=self.userinfo,

                    unescape=tornado.escape.xhtml_unescape,
                    cat_enum=self.mcat.get_qian2(catid[:2]),
                    tag_infos=self.mcat.query_all(by_order=True, kind=self.kind),
                    tag_infos2=self.mcat.query_all(by_order=True, kind=self.kind),
                    app2tag_info=self.mpost2catalog.query_by_entity_uid(infoid, kind=self.kind),
                    app2label_info=self.mpost2label.get_by_id(infoid, kind=self.kind + '1'))

    def get_def_cat_uid(self, post_data):
        # 下面两种处理方式，上面是原有的，暂时保留以保持兼容
        ext_cat_uid = {}
        if 'def_cat_uid' in post_data:
            ext_cat_uid['def_cat_uid'] = post_data['def_cat_uid']
            ext_cat_uid['def_cat_pid'] =  self.mcat.get_by_uid( post_data['def_cat_uid']).pid
        if 'gcat0' in post_data:
            ext_cat_uid['def_cat_uid'] = post_data['gcat0']
            ext_cat_uid['def_cat_pid'] =  self.mcat.get_by_uid( post_data['gcat0']).pid
        print(ext_cat_uid)
        return ext_cat_uid

    @tornado.web.authenticated
    def update(self, uid):

        if self.check_post_role(self.userinfo)['EDIT']:
            pass
        else:
            return False

        postinfo = self.mpost.get_by_uid(uid)
        if postinfo.kind == self.kind:
            pass
        else:
            return False

        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)[0]

        post_data['user_name'] = self.userinfo.user_name
        # post_data['kind'] = self.kind



        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = postinfo.valid

        ext_dic['def_uid'] = str(uid)
        print(post_data)

        ext_dic = dict(ext_dic, **self.get_def_cat_uid(post_data))

        ext_dic['def_tag_arr'] = [x.strip() for x in post_data['tags'].strip().strip(',').split(',')]
        ext_dic = self.extra_data(ext_dic, post_data)

        cnt_old = tornado.escape.xhtml_unescape(postinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            self.mpost_hist.insert_data(postinfo)

        self.mpost.modify_meta(uid,
                               post_data,
                               extinfo=ext_dic)
        self.update_category(uid)
        self.update_tag(uid)

        print('post kind:' + self.kind)
        print('update jump to:', '/{0}/{1}'.format(router_post[self.kind], uid))

        # Todo: won't work with self.kind
        self.redirect('/{0}/{1}'.format(router_post[postinfo.kind], uid))

    @tornado.web.authenticated
    def add(self, uid=''):

        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False

        ext_dic = {}
        post_data = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)[0]

        if uid == '':
            uid = self.gen_uid()

        post_data['user_name'] = self.userinfo.user_name
        post_data['kind'] = self.kind

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = 1

        ext_dic['def_uid'] = uid

        ext_dic = dict(ext_dic, **self.get_def_cat_uid(post_data))

        ext_dic['def_tag_arr'] = [x.strip() for x in post_data['tags'].strip().strip(',').split(',')]
        ext_dic = self.extra_data(ext_dic, post_data)

        self.mpost.modify_meta(ext_dic['def_uid'],
                               post_data,
                               extinfo=ext_dic)
        self.update_category(ext_dic['def_uid'])
        self.update_tag(ext_dic['def_uid'])

        self.redirect('/{0}/{1}'.format(router_post[self.kind], uid))
