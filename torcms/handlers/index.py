# -*- coding:utf-8 -*-

import tornado.escape
import tornado.web

import config
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.mcatalog import MCatalog
from torcms.model.mlink import MLink
from torcms.model.mpage import MPage
from torcms.model.mpost import MPost


class IndexHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mpost = MPost()
        self.mcat = MCatalog()
        self.mpage = MPage()
        self.mlink = MLink()

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self, input=''):
        if input == '':
            self.index()
        else:
            self.render('html/404.html', kwd={}, userinfo=self.userinfo)

    def index(self):
        cstr = tools.get_uuid()
        self.set_cookie('user_pass', cstr)
        kwd = {
            'cookie_str': cstr
        }
        self.render('index/index.html',
                    userinfo=self.userinfo,
                    catalog_info=self.mcat.query_all(by_order=True),
                    link=self.mlink.query_all(),
                    unescape=tornado.escape.xhtml_unescape,
                    cfg=config.cfg,
                    view=self.mpost.query_most_pic(20),
                    kwd=kwd, )
