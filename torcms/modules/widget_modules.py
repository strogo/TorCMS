# -*- coding:utf-8 -*-

import bs4
import tornado.escape
import tornado.web
from torcms.model.post_model import MPost
from torcms.model.link_model import MLink
from torcms.model.post2catalog_model import MPost2Catalog
import config
import tornado.web
from torcms.model.category_model import MCategory
from torcms.core.tools import constant
from torcms.model.info_model import MInfor as  MInfor
from torcms.model.label_model import MPost2Label

from torcms.model.reply_model import MReply
from torcms.model.page_model import MPage

mreply = MReply()
mpage = MPage()


class userinfo_widget(tornado.web.UIModule, tornado.web.RequestHandler):
    def render(self, signature):
        if self.get_secure_cookie("user"):
            self.render('modules/widget/loginfo.html',
                        username=self.get_secure_cookie("user"))
        else:
            self.render('modules/widget/tologinfo.html')

class widget_editor(tornado.web.UIModule):
    def render(self,router, uid, userinfo):
        kwd  = {'router': router,
                'uid': uid,
                }
        return self.render_string('modules/widget/widget_editor.html',
                                  kwd  = kwd,
                                  userinfo=userinfo,

                                  )

class widget_search(tornado.web.UIModule):
    def render(self, ):
        self.mcat = MCategory()

        return self.render_string('modules/widget/widget_search.html', cat_enum=self.mcat.query_pcat())