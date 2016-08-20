# -*- coding:utf-8 -*-

import tornado.web
from torcms.model.app_model import MApp
from torcms.model.app_rel_model import MAppRel
from torcms.model.usage_model import MUsage
from torcms.core.base_handler import BaseHandler
from torcms.model.collect_model import MCollect


class CollectHandler(BaseHandler, ):
    def initialize(self):
        self.init()
        self.mequa = MApp()
        self.musage = MUsage()
        self.mrel = MAppRel()
        self.mcollect = MCollect()

    def get(self, url_str=''):
        if len(url_str) > 0:
            url_arr = self.parse_url(url_str)
        else:
            return False

        if url_str == 'list':
            self.list()
        elif len(url_arr) == 1 and len(url_str) == 4 :
            if self.get_current_user():
                self.add_or_update(url_str)
            else:
                self.set_status('403')
                return False

    @tornado.web.authenticated
    def add_or_update(self, app_id):
        self.mcollect.add_or_update(self.userinfo.uid, app_id)

    @tornado.web.authenticated
    def list(self):
        self.render('user/collect/list.html',
                    recs_collect = self.mcollect.query_recent(self.userinfo.uid, 20),
                    userinfo = self.userinfo,
                    )