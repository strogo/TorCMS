# -*- coding:utf-8 -*-
from torcms.handlers.post2reply_handler import Post2ReplyHandler
from torcms.model.app_reply_model import MApp2Reply
from torcms.model.mreply import MReply
from torcms.model.mreply2user import MReply2User


class Info2ReplyHandler(Post2ReplyHandler):
    def initialize(self):
        self.init()
        self.mreply = MReply()
        self.mreply2user = MReply2User()
        self.mpost2reply = MApp2Reply()
