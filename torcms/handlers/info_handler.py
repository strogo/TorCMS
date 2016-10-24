# -*- coding:utf-8 -*-

import json
import random
import tornado.escape
import tornado.web

import config
from torcms.core import tools
from torcms.model.infor2label_model import MInfor2Label
from torcms.model.info_model import MInfor
from torcms.model.info_relation_model import MInforRel
from torcms.model.evaluation_model import MEvaluation
from torcms.model.category_model import MCategory
from torcms.model.usage_model import MUsage
from torcms.model.infor2catalog_model import MInfor2Catalog
from torcms.model.reply_model import MReply
from config import router_post
from config import cfg
from torcms.handlers.post_handler import PostHandler
from torcms.model.info_hist_model import MInfoHist

import tornado.gen
import tornado.web


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
            #  分类方式
            self.user_to_add(url_arr[1])
        elif url_arr[0] in ['_add', 'add_document']:
            # 直接添加
            self.add_app()
        elif url_arr[0] == 'catalog':
            self.catalog()

        elif len(url_arr) == 2:
            if url_arr[0] in ['edit', 'modify', '_edit']:
                self.to_edit_app(url_arr[1])
            elif url_arr[0] == 'add':
                self.to_add_app(url_arr[1])
            elif url_arr[0] == 'delete':
                self.to_del_app(url_arr[1])
            else:
                '''
                从相关计算中过来的。
                '''
                pass
                # self.mrel.update_relation(url_arr[1], url_arr[0])
                # self.redirect('/{0}/{1}'.format(self.app_url_name, url_arr[0]))

        elif len(url_arr) == 1 and len(url_str) == 4:
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

    def index(self):
        self.render('post{0}/index.html'.format(self.kind),
                    userinfo=self.userinfo,
                    kwd={'uid': '',}
                    )

    def post(self, url_str=''):

        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'to_add':
            self.add()
        elif url_arr[0] == 'rel':
            if self.get_current_user():
                self.add_relation(url_arr[1])
            else:
                self.redirect('/user/login')
        # elif url_arr[0] == 'comment_add':
        #     self.add_comment(url_arr[1])
        elif url_arr[0] == 'edit':
            self.update(url_arr[1])
        elif url_arr[0] == 'add':
            self.add(url_arr[1])
        elif url_arr[0] == '_add':
            self.map_add()

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
        cats = self.mpost2catalog.query_by_entity_uid(info_id, kind=self.kind)
        cat_uid_arr = []
        for cat_rec in cats:
            cat_uid = cat_rec.tag.uid
            cat_uid_arr.append(cat_uid)
        print('info category:', cat_uid_arr)
        replys = []  # self.mreply.get_by_id(info_id)
        rel_recs = self.mrel.get_app_relations(postinfo.uid, 0, kind=self.kind)
        if len(cat_uid_arr) > 0:
            rand_recs = self.mpost.query_cat_random(cat_uid_arr[0], 4 - rel_recs.count() + 4)
        else:
            rand_recs = self.mpost.query_random(4 - rel_recs.count() + 4)

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
        parent_name = self.mcat.get_by_id(ext_catid[:2] + '00').name if ext_catid != '' else ''
        if ext_catid != '':
            cat_rec = self.mcat.get_by_uid(ext_catid)
            role_mask_idx = cat_rec.role_mask.index('1')
            cat_name = cat_rec.name
        else:
            role_mask_idx = 0
            cat_name = ''

        parentname = '<a href="/list/{0}">{1}</a>'.format(ext_catid[:2] + '00', parent_name)

        catname = '<a href="/list/{0}">{1}</a>'.format(ext_catid, cat_name)

        kwd = {
            'pager': '',
            'url': self.request.uri,
            'cookie_str': cookie_str,
            'daohangstr': '',
            'signature': info_id,
            'tdesc': '',
            'eval_0': self.mevaluation.app_evaluation_count(info_id, 0),
            'eval_1': self.mevaluation.app_evaluation_count(info_id, 1),
            'site_url': config.site_url,
            'login': 1 if self.get_current_user() else 0,
            'has_image': 0,
            'parentlist': self.mcat.get_parent_list(),
            'parentname': parentname,
            'catname': catname,
        }
        self.mpost.view_count_increase(info_id)
        if self.get_current_user():
            self.musage.add_or_update(self.userinfo.uid, info_id)
        self.set_cookie('user_pass', cookie_str)
        tmpl = self.ext_tmpl_name(postinfo) if self.ext_tmpl_name(postinfo) else self.get_tmpl_name(postinfo)

        print('info tmpl: ' + tmpl)
        ext_catid2 = postinfo.extinfo['def_cat_uid'] if 'def_cat_uid' in postinfo.extinfo else None

        self.render(tmpl,
                    kwd=dict(kwd, **self.extra_kwd(postinfo)),
                    calc_info=postinfo,  # Deprecated
                    post_info=postinfo,  # Deprecated
                    postinfo=postinfo,
                    userinfo=self.userinfo,
                    relations=rel_recs,
                    rand_recs=rand_recs,
                    unescape=tornado.escape.xhtml_unescape,
                    ad_switch=random.randint(1, 18),
                    tag_info=self.mpost2label.get_by_id(info_id),
                    recent_apps=self.musage.query_recent(self.get_current_user(), 6)[1:],
                    replys=[],  # replys,
                    cat_enum=self.mcat.get_qian2(ext_catid2[:2], kind=self.kind ) if ext_catid else [],
                    role_mask_idx=role_mask_idx,
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
        if cat_id:
            tmpl = 'autogen/view/view_{0}.html'.format(cat_id)
        else:
            tmpl = 'post{0}/show_map.html'.format(self.kind)
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



    def catalog(self):
        self.render('post{0}/catalog.html'.format(self.kind),
                    userinfo=self.userinfo,
                    kwd={'uid': '',}
                    )

    @tornado.web.authenticated
    def user_to_add(self, catid, sig=''):
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
        uid = sig + tools.get_uu4d()
        while self.mpost.get_by_uid(uid):
            uid = sig + tools.get_uu4d()

        kwd = {
            'uid': uid,
            'userid': self.userinfo.user_name,
            'def_cat_uid': catid,
            'parentname': self.mcat.get_by_id(catid[:2] + '00').name,
            'catname': self.mcat.get_by_id(catid).name,
        }

        self.render('autogen/add/add_{0}.html'.format(catid),
                    userinfo=self.userinfo,
                    kwd=kwd)

    @tornado.web.authenticated
    def add_app(self):
        # Used for yunsuan, maplet
        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        self.render('post{0}/add.html'.format(self.kind),
                    tag_infos=self.mcat.query_all(by_order=True, kind=self.kind),
                    userinfo=self.userinfo,

                    )

    @tornado.web.authenticated
    def to_add_app(self, uid):
        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False

        if self.mpost.get_by_uid(uid):
            # todo:
            # self.redirect('/{0}/edit/{1}'.format(self.app_url_name, uid))
            pass
        else:
            self.render('post{0}/add.html'.format(self.kind),
                        tag_infos=self.mcat.query_all(),
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
    def to_edit_app(self, infoid):

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

        kwd = {
            'def_cat_uid': catid,
            'parentname': self.mcat.get_by_id(catid[:2] + '00').name if catid != '' else '',
            'catname': self.mcat.get_by_id(catid).name if catid != '' else '',
            'parentlist': self.mcat.get_parent_list(),
            'userip': self.request.remote_ip
        }

        if self.sig == '2':
            tmpl = 'autogen/edit/edit_{0}.html'.format(catid)
        else:
            tmpl = 'post{0}/edit.html'.format(self.kind)

        # print('site_type: ', cfg['site_type'])
        # print('Meta template:', tmpl)

        self.render(tmpl,
                    kwd=kwd,
                    calc_info=rec_info,  # Deprecated
                    post_info=rec_info,  # Deprecated
                    app_info=rec_info,  # Deprecated
                    postinfo=rec_info,
                    userinfo=self.userinfo,

                    unescape=tornado.escape.xhtml_unescape,
                    cat_enum=self.mcat.get_qian2(catid[:2], kind=self.kind ),
                    tag_infos=self.mcat.query_all(by_order=True, kind=self.kind ),
                    tag_infos2=self.mcat.query_all(by_order=True, kind=self.kind ),
                    app2tag_info=self.mpost2catalog.query_by_entity_uid(infoid, kind=self.kind ),
                    app2label_info=self.mpost2label.get_by_id(infoid, kind=self.kind + '1'))

    def get_def_cat_uid(self, post_data):
        # 下面两种处理方式，上面是原有的，暂时保留以保持兼容
        ext_cat_uid = {}
        if 'def_cat_uid' in post_data:
            ext_cat_uid['def_cat_uid'] = post_data['def_cat_uid']
            ext_cat_uid['def_cat_pid'] = '{0}00'.format(post_data['def_cat_uid'][:2])
        if 'gcat0' in post_data:
            ext_cat_uid['def_cat_uid'] = post_data['gcat0']
            ext_cat_uid['def_cat_pid'] = '{0}00'.format(post_data['gcat0'][:2])
        print(ext_cat_uid)
        return ext_cat_uid

    @tornado.web.authenticated
    def update(self, uid):

        if self.check_post_role(self.userinfo)['EDIT']:
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

        current_info = self.mpost.get_by_uid(uid)

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = current_info.valid

        ext_dic['def_uid'] = str(uid)
        print(post_data)

        ext_dic = dict(ext_dic, **self.get_def_cat_uid(post_data))

        ext_dic['def_tag_arr'] = [x.strip() for x in post_data['tags'].strip().strip(',').split(',')]
        ext_dic = self.extra_data(ext_dic, post_data)
        self.mpost_hist.insert_data(self.mpost.get_by_id(uid))

        self.mpost.modify_meta(uid,
                               post_data,
                               extinfo=ext_dic)
        self.update_catalog(uid)
        self.update_tag(uid)

        print('post kind:' + self.kind)
        print('update jump to:', '/{0}/{1}'.format(router_post[self.kind], uid))

        # Todo: won't work with self.kind
        self.redirect('/{0}/{1}'.format(router_post[current_info.kind], uid))

    @tornado.web.authenticated
    def map_add(self, uid='', sig=''):

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

        post_data['kind'] = self.kind

        if uid == '':
            uid = sig + tools.get_uu4d()
            while self.mpost.get_by_uid(uid):
                uid = sig + tools.get_uu4d()
            post_data['uid'] = uid

        post_data['user_name'] = self.userinfo.user_name
        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = 1

        ext_dic['def_uid'] = ext_dic['ext_map_uid']

        ext_dic = dict(ext_dic, **self.get_def_cat_uid(post_data))

        ext_dic['def_tag_arr'] = [x.strip() for x in post_data['tags'].strip().strip(',').split(',')]
        ext_dic = self.extra_data(ext_dic, post_data)

        self.mpost.modify_meta(ext_dic['def_uid'],
                               post_data,
                               extinfo=ext_dic)
        self.update_catalog(ext_dic['def_uid'])
        self.update_tag(ext_dic['def_uid'])

        self.redirect('/{0}/{1}'.format(router_post[self.kind], ext_dic['def_uid']))

    @tornado.web.authenticated
    def add(self, uid='', sig=''):

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
            uid = sig + tools.get_uu4d()
            while self.mpost.get_by_uid(uid):
                uid = sig + tools.get_uu4d()
            post_data['uid'] = uid

        post_data['user_name'] = self.userinfo.user_name
        post_data['kind'] = self.kind

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = 1

        ext_dic['def_uid'] = str(uid)

        ext_dic = dict(ext_dic, **self.get_def_cat_uid(post_data))

        ext_dic['def_tag_arr'] = [x.strip() for x in post_data['tags'].strip().strip(',').split(',')]
        ext_dic = self.extra_data(ext_dic, post_data)

        self.mpost.modify_meta(ext_dic['def_uid'],
                               post_data,
                               extinfo=ext_dic)
        self.update_catalog(ext_dic['def_uid'])
        self.update_tag(ext_dic['def_uid'])

        self.redirect('/{0}/{1}'.format(router_post[self.kind], uid))

    @tornado.web.authenticated
    def extra_data(self, ext_dic, post_data):
        '''
        The additional information.
        :param post_data:
        :return: directory.
        '''
        return ext_dic
