# -*- coding:utf-8 -*-


from torcms.model.core_tab import CabPost, CabCatalog, CabPost2Catalog
from torcms.model.post2catalog_model import MPost2Catalog


class MInfor2Catalog(MPost2Catalog):
    def __init__(self):
        self.tab_post2catalog = CabPost2Catalog
        self.tab_catalog = CabCatalog
        self.tab_post = CabPost
        try:
            CabPost2Catalog.create_table()
        except:
            pass
