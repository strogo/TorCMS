# -*- coding:utf-8 -*-

import datetime
import time

import tornado
import tornado.escape
from torcms.core import tools
from torcms.model.core_tab import CabPage
from torcms.model.msingle_table import MSingleTable


class MPage(MSingleTable):
    def __init__(self):
        self.tab = CabPage
        try:
            CabPage.create_table()
        except:
            pass

    def update(self, slug, post_data):
        if len(post_data['title'][0].strip()) == 0:
            return False
        entry = CabPage.update(
            title=post_data['title'][0],
            date=datetime.datetime.now(),
            cnt_html=tools.markdown2html(post_data['cnt_md'][0]),
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=time.time(),
        ).where(CabPage.slug == slug)
        entry.execute()

    def insert_data(self, post_data):
        if len(post_data['title'][0].strip()) == 0:
            return False
        slug = post_data['slug'][0]
        uu = self.get_by_slug(slug)
        if uu is None:
            pass
        else:
            return (False)

        try:
            CabPage.create(
                title=post_data['title'][0],
                date=datetime.datetime.now(),
                slug=slug,
                cnt_html=tools.markdown2html(post_data['cnt_md'][0]),
                time_create=time.time(),
                id_user= post_data['user_name'],
                cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
                time_update=time.time(),
                view_count=1,
            )
            return slug
        except:
            return ''

    def query_by_cat(self, cat_str):
        tt = CabPage.select().where((CabPage.id_cats.contains(str(cat_str))) & ((CabPage.type == 1))).order_by(
            'time_update')
        return tt
    def query_all(self):

        return self.tab.select()
    def view_count_plus(self, slug):

        entry = CabPage.update(
            view_count=CabPage.view_count + 1,
        ).where(CabPage.slug == slug)
        entry.execute()

    def get_by_slug(self, slug):

        tt = CabPage.select().where(CabPage.slug == slug).count()
        if tt == 0:
            return None
        else:
            return CabPage.get(CabPage.slug == slug)
