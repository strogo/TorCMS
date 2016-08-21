# -*- coding:utf-8 -*-

import peewee
from playhouse.postgres_ext import BinaryJSONField
from torcms.core.base_model import BaseModel
from torcms.model.core_tab import CabMember
from torcms.model.core_tab import CabPost
from torcms.model.core_tab import CabReply

class TabApp(BaseModel):
    uid = peewee.CharField(max_length=4, null=False, unique=True, help_text='', primary_key=True)
    title = peewee.CharField(null=False, help_text='标题', )
    keywords = peewee.CharField(null=True, default='')
    user_name = peewee.CharField(null=False, default = '', max_length=36, help_text='UserName', )
    logo = peewee.CharField(default='')
    date = peewee.DateTimeField(null=False, help_text='显示出来的日期时间')
    run_count = peewee.IntegerField(null=False, default=0, help_text='运行次数')
    view_count = peewee.IntegerField(null=False, default=0, help_text='查看次数')
    run_time = peewee.IntegerField(null=False, default=0, help_text='上次运行时间')
    create_time = peewee.IntegerField(null=False, default=0, help_text='创建时间')
    time_update = peewee.IntegerField(null=False, default=0, help_text='更新时间')
    type = peewee.IntegerField(null=False, default=1)
    html_path = peewee.CharField(default='')
    cnt_md = peewee.TextField(null=True)
    cnt_html = peewee.TextField(null=True)
    extinfo = BinaryJSONField()


class TabCatalog(BaseModel):
    uid = peewee.CharField(null=False, max_length=4, index=True, unique=True, primary_key=True, help_text='', )
    slug = peewee.CharField(null=False, index=True, unique=True, max_length=36, help_text='', )
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    order = peewee.IntegerField()
    priv_mask = peewee.CharField(null=False, default='00100', help_text='Member Privilege')
    count = peewee.IntegerField(default=0)


class TabApp2Catalog(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    catalog = peewee.ForeignKeyField(TabCatalog, related_name='catalog_id')
    post = peewee.ForeignKeyField(TabApp, related_name='app_id')
    order = peewee.IntegerField()


class TabLabel(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, help_text='', max_length=8)
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    count = peewee.IntegerField()


class TabApp2Label(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    tag = peewee.ForeignKeyField(TabLabel, related_name='tag_app_id')
    app = peewee.ForeignKeyField(TabApp, related_name='app_tag_id')
    order = peewee.IntegerField()


class TabCollect(BaseModel):
    '''
    用户收藏
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app = peewee.ForeignKeyField(TabApp, related_name='collect_app_rel')
    user = peewee.ForeignKeyField(CabMember, related_name='collect_user_rel')
    timestamp = peewee.IntegerField()


class TabEvaluation(BaseModel):
    '''
    用户评价
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app = peewee.ForeignKeyField(TabApp, related_name='evaluation_app_rel')
    user = peewee.ForeignKeyField(CabMember, related_name='evaluation_user_rel')
    value = peewee.IntegerField()  # 用户评价， 1 或 0, 作为计数

class TabRating(BaseModel):
    '''
    Rating for App of each user.
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    user = peewee.ForeignKeyField(CabMember, related_name='rating_user_rel')
    app = peewee.ForeignKeyField(TabApp, related_name='rating_app_rel')
    value = peewee.IntegerField(null = False)  # 用户评价， 1 或 0, 作为计数
    timestamp = peewee.IntegerField(null = False)

class TabUsage(BaseModel):
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    signature = peewee.ForeignKeyField(TabApp, related_name='equa_id')
    user = peewee.ForeignKeyField(CabMember, related_name='user_id')
    count = peewee.IntegerField()
    catalog_id = peewee.CharField(null=True)
    timestamp = peewee.IntegerField()


class TabAppRelation(BaseModel):
    '''
    相关应用
    我们认为，相关性，并非是对称操作
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app_f = peewee.ForeignKeyField(TabApp, related_name='app_f')
    app_t = peewee.ForeignKeyField(TabApp, related_name='app_t')
    count = peewee.IntegerField()


class TabToolbox(BaseModel):
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    title = peewee.CharField()
    app = peewee.CharField()
    cnt = peewee.CharField()
    user = peewee.ForeignKeyField(CabMember, related_name='user_tbx_id')
    order = peewee.IntegerField()


class TabApp2Reply(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    post_id = peewee.ForeignKeyField(TabApp, related_name='app_post_reply_id')
    reply_id = peewee.ForeignKeyField(CabReply, related_name='app_reply_post_id')
    timestamp = peewee.IntegerField()


class RabPost2App(BaseModel):
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app_f = peewee.ForeignKeyField(CabPost, related_name='rel_post2app_post')
    app_t = peewee.ForeignKeyField(TabApp, related_name='rel_post2app_app')
    count = peewee.IntegerField()


class RabApp2Post(BaseModel):
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app_f = peewee.ForeignKeyField(TabApp, related_name='rel_app2post_app')
    app_t = peewee.ForeignKeyField(CabPost, related_name='rel_app2post_post')
    count = peewee.IntegerField()
