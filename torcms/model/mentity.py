# -*- coding:utf-8 -*-

import time
from torcms.model.core_tab import CabPic


class MEntity():
    def __init__(self):
        try:
            CabPic.create_table()
        except:
            pass

    def getall(self):
        return CabPic.select()

    def insert_data(self, signature, impath):
        entry = CabPic.create(
            uid=signature,
            imgpath=impath,
            create_timestamp=time.time()
        )
        return entry
