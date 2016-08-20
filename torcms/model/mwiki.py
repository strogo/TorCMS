# -*- coding:utf-8 -*-

import datetime

import tornado.escape

from torcms.core import tools
from torcms.model.core_tab import CabWiki
from torcms.model.msingle_table import MSingleTable


class MWiki(MSingleTable):

    def __init__(self):
        self.tab = CabWiki
        try:
            CabWiki.create_table()
        except:
            pass

    def update(self, uid, post_data):


        cnt_html = tools.markdown2html(post_data['cnt_md'][0])

        entry = CabWiki.update(
            title=post_data['title'][0],
            date=datetime.datetime.now(),
            cnt_html=cnt_html,
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=tools.timestamp(),
        ).where(CabWiki.uid == uid)
        entry.execute()

    def insert_data(self, post_data):
        title = post_data['title'][0]
        uu = self.get_by_wiki(title)
        if uu is None:
            pass
        else:
            return (False)


        cnt_html = tools.markdown2html(post_data['cnt_md'][0])

        entry = CabWiki.create(
            title=post_data['title'][0],
            date=datetime.datetime.now(),
            cnt_html=cnt_html,
            uid=tools.get_uu8d(),
            time_create=tools.timestamp(),
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=tools.timestamp(),
            view_count=1,
        )
        return (entry.uid)



    def get_by_title(self, in_title):
        try:
            return CabWiki.get(CabWiki.title == in_title)
        except:
            return None
    def query_dated(self, num = 10):
        return CabWiki.select().order_by(CabWiki.time_update.desc()).limit(num)

    def query_most(self, num=8):
        return CabWiki.select().order_by(CabWiki.view_count.desc()).limit(num)

    def update_view_count(self, citiao):
        entry = CabWiki.update(view_count=CabWiki.view_count + 1).where(CabWiki.title == citiao)
        entry.execute()

    def update_view_count_by_uid(self, uid):
        entry = CabWiki.update(view_count=CabWiki.view_count + 1).where(CabWiki.uid == uid)
        entry.execute()

    def get_by_wiki(self, citiao):
        tt = CabWiki.select().where(CabWiki.title == citiao).count()
        if tt == 0:
            return None
        else:
            self.update_view_count(citiao)
            return CabWiki.get(CabWiki.title == citiao)


