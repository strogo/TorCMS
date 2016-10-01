# -*- coding:utf-8 -*-

import time
from torcms.model.core_tab import g_Image
from torcms.model.supertable_model import MSuperTable

class MEntity(MSuperTable):
    def __init__(self):
        self.tab = g_Image
        try:
            g_Image.create_table()
        except:
            pass

    def getall(self):
        return g_Image.select()

    def get_id_by_impath(self, imgpath):
        uu = g_Image.select().where(g_Image.imgpath == imgpath)
        if uu.count() == 1:
            return uu.get().uid
        elif uu.count() > 1:
            return False
        else:
            return False

    def insert_data(self, signature, impath):
        entry = g_Image.create(
            uid=signature,
            imgpath=impath,
            create_timestamp=time.time()
        )
        return entry
