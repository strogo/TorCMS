# -*- coding:utf-8 -*-
import json
import tornado.web
from torcms.model.app_model import MApp
from torcms.model.evaluation_model import MEvaluation
from torcms.model.usage_model import MUsage
from torcms.core.base_handler import BaseHandler
from torcms.model.app_rel_model import MAppRel


class EvaluationHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mequa = MApp()
        self.musage = MUsage()
        self.mrel = MAppRel()
        self.mcollect = MEvaluation()


    def get(self, url_str=''):
        if len(url_str) > 0:
            url_arr = url_str.split('/')
        else:
            return False

        # 形如  /evalucate/0123/1
        if len(url_arr) == 2 and len(url_arr[0]) == 4 and ( url_arr[1] in ['0', '1']):
            if self.get_current_user():
                self.add_or_update(url_arr[0], url_arr[1])
            else:
                self.set_status('403')
                return False
        return None



    @tornado.web.authenticated
    def add_or_update(self, app_id, value):
        self.mcollect.add_or_update(self.userinfo.uid, app_id, value)

        out_dic = {
            'eval0': self.mcollect.app_evaluation_count(app_id, 0),
            'eval1': self.mcollect.app_evaluation_count(app_id, 1)
        }
        uu = json.dumps(out_dic)
        self.write(uu)
