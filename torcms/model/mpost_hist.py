# -*- coding:utf-8 -*-


from torcms.core import tools
from torcms.model.core_tab import CabPostHist
from torcms.model.msingle_table import MSingleTable


class MPostHist(MSingleTable):
    def __init__(self):
        self.tab = CabPostHist
        try:
            CabPostHist.create_table()
        except:
            pass

    def insert_data(self, raw_data):
        uid = tools.get_uuid()
        try:
            CabPostHist.create(
                uid=uid,
                title=raw_data.title,
                date=raw_data.date,
                post_id=raw_data.uid,
                time_create=raw_data.time_create,
                user_name=raw_data.user_name,
                cnt_md=raw_data.cnt_md,
                time_update=raw_data.time_update,
                id_spec=raw_data.id_spec,
                logo=raw_data.logo,
            )
            return (uid)
        except:
            return False
