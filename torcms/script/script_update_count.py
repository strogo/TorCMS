# -*- coding: utf-8

import sys

from torcms.model.category_model import MCategory

from torcms.model.infor2catalog_model import MInfor2Catalog
def run_update_count():
    mapp2cat = MInfor2Catalog()
    mappcat = MCategory()

    for kd in ['1', '2', 'm', 's', 'w']:
        for rec in mappcat.query_all( kind = kd ):
            uid= rec.uid
            print(rec.name)
            # uuvv = mapp.query_extinfo_by_cat(uid)
            uuvv = mapp2cat.query_by_catid(rec.uid)
            print(uid, uuvv.count())
            mappcat.update_count(uid, uuvv.count())
