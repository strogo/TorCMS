# -*- coding:utf-8 -*-


from torcms.model.ext_tab import *
from torcms.model.ext_tab import TabApp
from torcms.model.mpost2catalog import MPost2Catalog


class MApp2Catalog(MPost2Catalog):
    def __init__(self):
        self.tab_post2catalog = TabApp2Catalog
        self.tab_catalog = TabCatalog
        self.tab_post = TabApp
        try:
            TabApp2Catalog.create_table()
        except:
            pass
