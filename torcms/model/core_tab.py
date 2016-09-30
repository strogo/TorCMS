# -*- coding:utf-8 -*-

import peewee
from playhouse.postgres_ext import BinaryJSONField

from torcms.core.base_model import BaseModel


class CabCatalog(BaseModel):
    uid = peewee.CharField(null=False, max_length=4, index=True, unique=True, primary_key=True, help_text='', )
    slug = peewee.CharField(null=False, index=True, unique=True, max_length=36, help_text='', )
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    order = peewee.IntegerField()
    count = peewee.IntegerField(default=0)
    type = peewee.IntegerField(default=1)
    priv_mask = peewee.CharField(null=False, default='00100', help_text='Member Privilege')


class CabLink(BaseModel):
    uid = peewee.CharField(null=False, index=False, unique=True, primary_key=True, default='0000',
                           max_length=4, help_text='', )
    link = peewee.CharField(null=False, max_length=36, help_text='', )
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    logo = peewee.CharField(null=False, max_length=255, help_text='', )
    order = peewee.IntegerField()


class CabPost(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, default='00000',
                           max_length=5, help_text='', )
    title = peewee.CharField(null=False, help_text='Title')
    keywords = peewee.CharField(null=False, default='', help_text='Keywords')
    date = peewee.DateTimeField(null=False, help_text='')
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(null=False, default='', max_length=36, help_text='UserName', )
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()
    logo = peewee.CharField(default='')
    valid = peewee.IntegerField(null=False, default=1, help_text='Whether the infor would show.')
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    type = peewee.IntegerField(null=False, default=1)
    extinfo = BinaryJSONField(default={})


class CabWiki(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    title = peewee.CharField(null=False, unique=True, index=True, help_text='Title')
    date = peewee.DateTimeField()
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(null=False, max_length=36, help_text='UserName', )
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    type = peewee.IntegerField(null=False, default=1)  # 1 for wiki, 2 for page.


class CabPostHist(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, help_text='', primary_key=True, max_length=36)
    title = peewee.CharField(null=False, max_length=255, help_text='', )
    post_id = peewee.CharField(null=False, max_length=5, help_text='', )
    user_name = peewee.CharField()
    cnt_md = peewee.TextField()
    time_update = peewee.IntegerField()
    logo = peewee.CharField()


class CabWikiHist(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, help_text='', primary_key=True, max_length=36)
    title = peewee.CharField(null=False, max_length=255, help_text='', )
    wiki_id = peewee.CharField(null=False, max_length=8, help_text='', )
    user_name = peewee.CharField()
    cnt_md = peewee.TextField()
    time_update = peewee.IntegerField()


class CabMember(BaseModel):
    '''
    privilege:
    11111
    read,add,edit,delete,manage
    [0]: read
    [1]: for post, page, wiki,
    [2]: for infor.
    [3]: keep
    [4]: keep
    And, could be extended.
    '''
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    user_name = peewee.CharField(null=False, index=True, unique=True, max_length=16, help_text='User Name', )
    user_email = peewee.CharField(null=False, unique=True, max_length=255, help_text='User Email', )
    user_pass = peewee.CharField(null=False, max_length=255, help_text='User Password')
    privilege = peewee.CharField(null=False, default='10000', help_text='Member Privilege', )
    time_reset_passwd = peewee.IntegerField(null=False, default=0)
    time_login = peewee.IntegerField(null=False, default=0)
    time_create = peewee.IntegerField(null=False, default=0)
    time_update = peewee.IntegerField(null=False, default=0)
    time_email = peewee.IntegerField(null=False, default=0, help_text='Time auto send email.')


class CabPic(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, )
    imgpath = peewee.CharField(null=False, unique=True, max_length=255, help_text='', )
    create_timestamp = peewee.IntegerField()


class CabPost2Catalog(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    catalog = peewee.ForeignKeyField(CabCatalog, related_name='cat_id')
    post = peewee.ForeignKeyField(CabPost, related_name='post_id')
    order = peewee.IntegerField()


class CabReply(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    create_user_id = peewee.ForeignKeyField(CabMember, related_name='reply_member_id')
    user_name = peewee.TextField()
    timestamp = peewee.IntegerField()
    date = peewee.DateTimeField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    vote = peewee.IntegerField()


class CabPost2Reply(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    post_id = peewee.ForeignKeyField(CabPost, related_name='post_reply_id')
    reply_id = peewee.ForeignKeyField(CabReply, related_name='reply_post_id')
    timestamp = peewee.IntegerField()


class CabVoter2Reply(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    reply_id = peewee.ForeignKeyField(CabReply, related_name='reply_voter_id')
    voter_id = peewee.ForeignKeyField(CabMember, related_name='voter_reply_id')
    timestamp = peewee.IntegerField()


class CabRelation(BaseModel):
    '''
    相关应用
    相关性，并非是对称操作
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app_f = peewee.ForeignKeyField(CabPost, related_name='post_from')
    app_t = peewee.ForeignKeyField(CabPost, related_name='post_to')
    count = peewee.IntegerField()


class TabCollect(BaseModel):
    '''
    用户收藏
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app = peewee.ForeignKeyField(CabPost, related_name='collect_app_rel')
    user = peewee.ForeignKeyField(CabMember, related_name='collect_user_rel')
    timestamp = peewee.IntegerField()


class TabEvaluation(BaseModel):
    '''
    用户评价
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app = peewee.ForeignKeyField(CabPost, related_name='evaluation_app_rel')
    user = peewee.ForeignKeyField(CabMember, related_name='evaluation_user_rel')
    value = peewee.IntegerField()  # 用户评价， 1 或 0, 作为计数


class TabRating(BaseModel):
    '''
    Rating for App of each user.
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    user = peewee.ForeignKeyField(CabMember, related_name='rating_user_rel')
    app = peewee.ForeignKeyField(CabPost, related_name='rating_app_rel')
    value = peewee.IntegerField(null=False)  # 用户评价， 1 或 0, 作为计数
    timestamp = peewee.IntegerField(null=False)


class TabUsage(BaseModel):
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    signature = peewee.ForeignKeyField(CabPost, related_name='equa_id')
    user = peewee.ForeignKeyField(CabMember, related_name='user_id')
    count = peewee.IntegerField()
    catalog_id = peewee.CharField(null=True)
    timestamp = peewee.IntegerField()


class CabPostRelation(BaseModel):
    '''
    相关应用
    我们认为，相关性，并非是对称操作
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app_f = peewee.ForeignKeyField(CabPost, related_name='app_f')
    app_t = peewee.ForeignKeyField(CabPost, related_name='app_t')
    count = peewee.IntegerField()


class TabToolbox(BaseModel):
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    title = peewee.CharField()
    app = peewee.CharField()
    cnt = peewee.CharField()
    user = peewee.ForeignKeyField(CabMember, related_name='user_tbx_id')
    order = peewee.IntegerField()


class RabPost2App(BaseModel):
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app_f = peewee.ForeignKeyField(CabPost, related_name='rel_post2app_post')
    app_t = peewee.ForeignKeyField(CabPost, related_name='rel_post2app_app')
    count = peewee.IntegerField()


class RabApp2Post(BaseModel):
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app_f = peewee.ForeignKeyField(CabPost, related_name='rel_app2post_app')
    app_t = peewee.ForeignKeyField(CabPost, related_name='rel_app2post_post')
    count = peewee.IntegerField()
