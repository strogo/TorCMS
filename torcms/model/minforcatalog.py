# -*- coding:utf-8 -*-

from torcms.model.ext_tab import TabCatalog
from torcms.model.mcatalog import MCatalog

class MInforCatalog(MCatalog):
    def __init__(self):
        self.tab = TabCatalog
        try:
            TabCatalog.create_table()
        except:
            pass

