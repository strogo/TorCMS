# -*- coding:utf-8 -*-

import json

import tornado.escape
import tornado.web
from torcms.model.app2label_model import MApp2Label
from torcms.model.app_model import MApp
from torcms.model.app_rel_model import MAppRel
from torcms.model.app_reply_model import MApp2Reply
from torcms.model.evaluation_model import MEvaluation
from torcms.model.minforcatalog import MInforCatalog
from torcms.model.usage_model import MUsage

from  config import cfg
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.model.app2catalog_model import MApp2Catalog


class MetaHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mappcat = MInforCatalog()
        self.mevaluation = MEvaluation()
        self.mapp2catalog = MApp2Catalog()
        self.mapp2tag = MApp2Label()
        self.mapp = MApp()
        self.musage = MUsage()
        self.mtag = MInforCatalog()
        self.mrel = MAppRel()
        self.mreply = MApp2Reply()
        if 'app_url_name' in cfg:
            self.app_url_name = cfg['app_url_name']
        else:
            self.app_url_name = 'info'

    def get(self, url_str=''):

        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'cat_add':
            self.user_to_add(url_arr[1])
        elif url_arr[0] == 'catalog':
            self.catalog()
        elif len(url_arr) == 1 and len(url_str) == 4:
            self.redirect('/{0}/{1}'.format(self.app_url_name, url_arr[0]))
        elif len(url_arr) == 2:
            if url_arr[0] == 'edit':
                self.to_edit_app(url_arr[1])
            elif url_arr[0] == 'add':
                self.to_add_app(url_arr[1])
            elif url_arr[0] == 'delete':
                self.to_del_app(url_arr[1])


            else:
                '''
                从相关计算中过来的。
                '''
                self.mrel.update_relation(url_arr[1], url_arr[0])
                self.redirect('/{0}/{1}'.format(self.app_url_name, url_arr[0]))
        else:
            kwd = {
                'title': '',
                'info': '',
            }
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, url_str=''):

        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'to_add':
            self.add()
        elif url_arr[0] == 'rel':
            if self.get_current_user():
                self.add_relation(url_arr[1])
            else:
                self.redirect('/user/login')
        elif url_arr[0] == 'comment_add':
            self.add_comment(url_arr[1])
        elif url_arr[0] == 'edit':
            self.update(url_arr[1])
        elif url_arr[0] == 'add':
            self.add(url_arr[1])
        else:
            return False

    def catalog(self):
        self.render('infor/app/catalog.html',
                    userinfo=self.userinfo,
                    kwd={'uid': '',}
                    )

    @tornado.web.authenticated
    def user_to_add(self, catid):

        uid = tools.get_uu4d()
        while self.mapp.get_by_uid(uid):
            uid = tools.get_uu4d()
        kwd = {
            'uid': uid,
            'userid': self.userinfo.user_name,
            'def_cat_uid': catid,
            'parentname': self.mtag.get_by_id(catid[:2] + '00').name,
            'catname': self.mtag.get_by_id(catid).name,
        }
        self.render('autogen/add/add_{0}.html'.format(catid),
                    userinfo=self.userinfo,
                    kwd=kwd)

    def check_priv(self, userinfo, cat_id):
        cat_rec = self.mappcat.get_by_uid(cat_id)
        priv_mask_idx = cat_rec.priv_mask.index('1')
        priv_dic = {'ADD': False, 'EDIT': False, 'DELETE': False, 'ADMIN': False}
        if userinfo.privilege[priv_mask_idx] >= '1':
            priv_dic['ADD'] = True
        if userinfo.privilege[priv_mask_idx] >= '2':
            priv_dic['EDIT'] = True
        if userinfo.privilege[priv_mask_idx] >= '4':
            priv_dic['DELETE'] = True
        if userinfo.privilege[priv_mask_idx] >= '8':
            priv_dic['ADMIN'] = True
        return priv_dic

    @tornado.web.authenticated
    def to_add_app(self, uid):
        if self.mapp.get_by_uid(uid):
            self.redirect('/{0}/edit/{1}'.format(self.app_url_name, uid))
        else:
            self.render('infor/app/add.html',
                        tag_infos=self.mtag.query_all(),
                        userinfo=self.userinfo,
                        kwd={'uid': uid,}
                        )

    @tornado.web.authenticated
    def to_del_app(self, uid):
        current_infor = self.mapp.get_by_uid(uid)
        if self.check_priv(self.userinfo, current_infor.extinfo['def_cat_uid'])['DELETE']:
            pass
        else:
            return False

        if self.mapp.delete(uid):
            self.redirect('/list/{0}'.format(current_infor.extinfo['def_cat_uid']))
        else:
            self.redirect('/info/{0}'.format(uid))

    @tornado.web.authenticated
    def to_edit_app(self, infoid):

        rec_info = self.mapp.get_by_uid(infoid)

        if rec_info:
            pass
        else:
            self.render('html/404.html')
            return
        if 'def_cat_uid' in rec_info.extinfo:
            catid = rec_info.extinfo['def_cat_uid']
        else:
            catid = ''

        kwd = {
            'def_cat_uid': catid,
            'parentname': self.mtag.get_by_id(catid[:2] + '00').name if catid != '' else '',
            'catname': self.mtag.get_by_id(catid).name if catid != '' else '',
            'parentlist': self.mtag.get_parent_list(),
            'userip': self.request.remote_ip
        }

        if catid:
            tmpl = 'autogen/edit/edit_{0}.html'.format(catid)
        else:
            tmpl = 'infor/app/edit.html'

        self.render(tmpl,
                    kwd=kwd,
                    calc_info=rec_info,
                    post_info=rec_info,
                    userinfo=self.userinfo,
                    app_info=rec_info,
                    unescape=tornado.escape.xhtml_unescape,
                    cat_enum=self.mappcat.get_qian2(catid[:2]),
                    tag_infos=self.mappcat.query_all(by_order=True),
                    app2tag_info=self.mapp2catalog.query_by_entry_uid(infoid),
                    app2label_info=self.mapp2tag.get_by_id(infoid), )

    @tornado.web.authenticated
    def update(self, uid):
        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)

        post_data['user_name'] = self.userinfo.user_name

        current_info = self.mapp.get_by_uid(uid)

        if current_info.user_name == self.userinfo.user_name:
            pass
        elif self.userinfo.privilege[4] >= '1':
            pass
        elif 'def_cat_uid' in post_data and self.check_priv(self.userinfo, post_data['def_cat_uid'][0])['EDIT']:
            pass
        else:
            return False

        ext_dic['def_uid'] = str(uid)
        if 'def_cat_uid' in post_data:
            ext_dic['def_cat_uid'] = post_data['def_cat_uid'][0]
            ext_dic['def_cat_pid'] = '{0}00'.format(post_data['def_cat_uid'][0][:2])

        ext_dic['def_tag_arr'] = [x.strip() for x in post_data['tags'][0].strip().strip(',').split(',')]
        ext_dic = self.extra_data(ext_dic, post_data)
        self.mapp.modify_meta(uid,
                              post_data,
                              extinfo=ext_dic)
        self.update_catalog(uid)
        self.update_tag(uid)
        self.redirect('/{0}/{1}'.format(self.app_url_name, uid))

    @tornado.web.authenticated
    def add(self, uid=''):

        ext_dic = {}
        post_data = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)

        if self.check_priv(self.userinfo, post_data['def_cat_uid'][0])['ADD']:
            pass
        else:
            return False

        if uid == '':
            uid = tools.get_uu4d()
            while self.mapp.get_by_uid(uid):
                uid = tools.get_uu4d()
            post_data['uid'][0] = uid

        post_data['user_name'] = self.userinfo.user_name

        ext_dic['def_uid'] = str(uid)
        if 'def_cat_uid' in post_data:
            ext_dic['def_cat_pid'] = '{0}00'.format(post_data['def_cat_uid'][0][:2])
            ext_dic['def_cat_uid'] = post_data['def_cat_uid'][0]

        ext_dic['def_tag_arr'] = [x.strip() for x in post_data['tags'][0].strip().strip(',').split(',')]
        ext_dic = self.extra_data(ext_dic, post_data)
        print(post_data)
        self.mapp.modify_meta(ext_dic['def_uid'],
                              post_data,
                              extinfo=ext_dic)
        self.update_catalog(ext_dic['def_uid'])
        self.update_tag(ext_dic['def_uid'])

        self.redirect('/list/{0}'.format(ext_dic['def_cat_uid']))

    @tornado.web.authenticated
    def extra_data(self, ext_dic, post_data):
        '''
        The additional information.
        :param post_data:
        :return: directory.
        '''
        return ext_dic

    @tornado.web.authenticated
    def update_tag(self, signature):

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        current_tag_infos = self.mapp2tag.get_by_id(signature)
        tags_arr = [x.strip() for x in post_data['tags'][0].split(',')]
        for tag_name in tags_arr:
            if tag_name == '':
                pass
            else:
                self.mapp2tag.add_record(signature, tag_name, 1)

        for cur_info in current_tag_infos:
            if cur_info.tag.name in tags_arr:
                pass
            else:
                self.mapp2tag.remove_relation(signature, cur_info.tag)

    @tornado.web.authenticated
    def update_catalog(self, signature):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        current_catalog_infos = self.mapp2catalog.query_by_entry_uid(signature)

        new_tag_arr = []
        for idx, key in enumerate(['cat_1', 'cat_2', 'cat_3', 'cat_4', 'cat_5', 'def_cat_uid']):
            if key in post_data:
                vv = post_data[key][0]
                if vv == '':
                    pass
                else:
                    new_tag_arr.append(vv)
                    self.mapp2catalog.add_record(signature, vv, idx)
            else:
                pass

        for cur_info in current_catalog_infos:
            if str(cur_info.catalog.uid).strip() in new_tag_arr:
                pass
            else:
                self.mapp2catalog.remove_relation(signature, cur_info.catalog)

    @tornado.web.authenticated
    def add_comment(self, id_post):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        post_data['user_id'] = self.userinfo.uid
        post_data['user_name'] = self.userinfo.user_name
        comment_uid = self.mreply.insert_data(post_data, id_post)
        if comment_uid:
            output = {
                'pinglun': comment_uid,
            }
        else:
            output = {
                'pinglun': 0,
            }
        return json.dump(output, self)

    def add_relation(self, f_uid, t_uid):
        if False == self.mapp.get_by_uid(t_uid):
            return False
        if f_uid == t_uid:
            '''
            关联其本身
            '''
            return False
        self.mrel.add_relation(f_uid, t_uid, 2)
        self.mrel.add_relation(t_uid, f_uid, 1)
        return True
