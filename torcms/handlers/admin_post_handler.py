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
from torcms.core.tools import logger


class AdminPostHandler(PostHandler):
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


    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_str == '':
            self.index()
        elif len(url_arr) == 2:
            if url_arr[0] in ['_edit']:
                self.to_edit(url_arr[1])
        else:
            return False

    def to_edit(self, post_uid):
        postinfo = self.mpost.get_by_uid(post_uid)
        print('gotit')
        self.render('man_post/admin_post.html',
                    postinfo = postinfo,
                    sig_dic = router_post,
                    tag_infos=self.mcat.query_all(),
                    tag_infos2=self.mcat.query_all(),
                    unescape=tornado.escape.xhtml_unescape,
                    userinfo = self.userinfo,
                    )


    # def post(self, url_str=''):
    #
    #     url_arr = self.parse_url(url_str)
    #
    #     if url_arr[0] in ['to_add', '_add', 'add']:
    #         if len(url_arr) == 2:
    #             self.add(uid=url_arr[1])
    #         else:
    #             self.add()
    #
    #     elif url_arr[0] in ['cat_add', '_cat_add']:
    #         self.add(catid=url_arr[1])
    #     elif url_arr[0] == 'rel':
    #         if self.get_current_user():
    #             self.add_relation(url_arr[1])
    #         else:
    #             self.redirect('/user/login')
    #     # elif url_arr[0] == 'comment_add':
    #     #     self.add_comment(url_arr[1])
    #     elif url_arr[0] in ['edit', '_edit']:
    #         self.update(url_arr[1])
    #
    #
    #     elif url_arr[0] == 'rel':
    #         if self.get_current_user():
    #             self.add_relation(url_arr[1], url_arr[2])
    #         else:
    #             self.redirect('/user/login')
    #
    #     else:
    #         return False
    #
