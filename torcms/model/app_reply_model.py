# -*- coding:utf-8 -*-

from torcms.model.ext_tab import TabApp2Reply
from torcms.model.mpost2reply import MPost2Reply


class MApp2Reply(MPost2Reply):
    def __init__(self):
        self.tab = TabApp2Reply
        try:
            TabApp2Reply.create_table()
        except:
            pass
