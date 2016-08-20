# -*- coding:utf-8 -*-

from torcms.model.ext_tab import *
from torcms.model.ext_tab import TabApp
from torcms.model.mrelation import MRelation


class MAppRel(MRelation):
    def __init__(self):
        self.tab_relation = TabAppRelation
        self.tab_post = TabApp
        try:
            TabAppRelation.create_table()
        except:
            pass


class MRelPost2App(MRelation):
    def __init__(self):
        MRelation.__init__(self)
        self.tab_relation = RabPost2App
        self.tab_post = TabApp
        try:
            self.tab_relation.create_table()
        except:
            pass


class MRelApp2Post(MRelation):
    def __init__(self):
        MRelation.__init__(self)
        self.tab_relation = RabApp2Post
        self.tab_post = CabPost
        try:
            self.tab_relation.create_table()
        except:
            pass
