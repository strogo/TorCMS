# -*- coding:utf-8 -*-

from torcms.model.core_tab import CabCatalog
from torcms.model.postcatalog_model import MPostCatalog

class MInforCatalog(MPostCatalog):
    def __init__(self):
        self.tab = CabCatalog
        try:
            CabCatalog.create_table()
        except:
            pass

