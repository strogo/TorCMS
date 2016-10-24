# # -*- coding:utf-8 -*-
#
# import json
#
# import tornado.escape
# import tornado.web
# from torcms.model.infor2label_model import MInfor2Label
# from torcms.model.info_model import MInfor
# from torcms.model.info_relation_model import MInforRel
# from torcms.model.evaluation_model import MEvaluation
# from torcms.model.category_model import MCategory
#
# from torcms.model.usage_model import MUsage
#
# from  config import cfg
# from torcms.core import tools
# from torcms.handlers.post_handler import PostHandler
# from torcms.model.infor2catalog_model import MInfor2Catalog
# from torcms.model.info_hist_model import MInfoHist
# from config import router_post
#
#
# class MetaHandler(PostHandler):
#     def initialize(self):
#         self.init()
#         self.mpost = MInfor()
#         self.mcat = MCategory()
#         self.cats = self.mcat.query_all()
#         self.mpost_hist = MInfoHist()
#         self.mpost2catalog = MInfor2Catalog()
#         self.mpost2label = MInfor2Label()
#         self.mrel = MInforRel()
#         self.musage = MUsage()
#         self.mevaluation = MEvaluation()
#         self.kind = '2'
#         # if 'app_url_name' in cfg:
#         #     self.app_url_name = cfg['app_url_name']
#         # else:
#         #     self.app_url_name = 'info'
#
#
#
