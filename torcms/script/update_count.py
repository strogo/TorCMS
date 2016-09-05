__author__ = 'bukun'

import sys

from torcms.model.mcatalog import MCatalog
from torcms.model.minforcatalog import MInforCatalog
from torcms.model.app_model import MApp


def update_app_count():

    mappcat = MInforCatalog()
    mapp = MApp()
    for rec in mappcat.query_all():
        uid= rec.uid
        uuvv = mapp.query_extinfo_by_cat(uid)
        print(uid, uuvv.count())
        mappcat.update_count(uid, uuvv.count())