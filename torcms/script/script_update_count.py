# -*- coding: utf-8

import sys

from torcms.model.postcatalog_model import MPostCatalog
from torcms.model.inforcatalog_model import MInforCatalog
from torcms.model.infor_model import MInfor
from torcms.model.infor2catalog_model import MInfor2Catalog as MApp2Catalog

def run_update_count():
    mapp2cat = MApp2Catalog()
    mappcat = MInforCatalog()
    mapp = MInfor()
    for rec in mappcat.query_all():
        uid= rec.uid
        # uuvv = mapp.query_extinfo_by_cat(uid)
        uuvv = mapp2cat.query_by_catid(rec.uid)
        print(uid, uuvv.count())
        mappcat.update_count(uid, uuvv.count())
