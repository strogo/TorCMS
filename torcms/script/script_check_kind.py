# -*- coding:utf-8 -*-

import tornado.escape


# from torcms.model.post_model import MPost

from torcms.model.info_model import MInfor

from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.wiki_model import MWiki
from torcms.model.category_model import MCategory
from torcms.model.label_model import MLabel

mcat = MCategory()
mlabel = MLabel()
mpost = MInfor()
mpost2tag = MPost2Catalog()
mwiki = MWiki()

# for catid in ['2101', '2102', '2103', '2104', '2105','a001', 'a002', 'a003' , 'w005']:
#     catinfo  = mcat.get_by_uid(catid)
#     recs = mpost2tag.query_by_catid(catid)
#     for rec in recs:
#         postinfo = mpost.get_by_uid(rec.post.uid)
#         print(postinfo.title)
#         print(postinfo.kind)
#         mpost.update_kind(postinfo.uid, catinfo.kind)
#


import sys
from config import router_post
from torcms.model.category_model import MCategory

from torcms.model.infor2catalog_model import MInfor2Catalog
def run_check_kind():
    mapp2cat = MInfor2Catalog()
    mappcat = MCategory()

    for kd in router_post.keys():
        for rec in mappcat.query_all( kind = kd ):
            catid= rec.uid
            # print(rec.name)
            # # uuvv = mapp.query_extinfo_by_cat(uid)
            # uuvv = mapp2cat.query_by_catid(rec.uid)
            # print(uid, uuvv.count())
            # mappcat.update_count(uid, uuvv.count())


            catinfo  = mcat.get_by_uid(catid)
            recs = mpost2tag.query_by_catid(catid)
            for rec in recs:
                postinfo = mpost.get_by_uid(rec.post.uid)
                if postinfo.kind == catinfo.kind:
                    pass
                else:
                    print(postinfo.uid)
                # print(postinfo.title)
                # print(postinfo.kind)
                # extjson =       {
                #     'def_cat_uid': catinfo.uid,
                #     'def_cat_pid' : catinfo.pid,
                # }
                # mpost.update_jsonb(postinfo.uid, extjson)
                # mpost.update_kind(postinfo.uid, catinfo.kind)



