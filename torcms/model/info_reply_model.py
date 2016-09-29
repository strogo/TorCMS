# -*- coding:utf-8 -*-

from torcms.model.core_tab import CabPost2Reply
from torcms.model.post2reply_model import MPost2Reply


class MInfor2Reply(MPost2Reply):
    def __init__(self):
        self.tab = CabPost2Reply
        try:
            CabPost2Reply.create_table()
        except:
            pass
