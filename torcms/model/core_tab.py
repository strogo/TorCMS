# -*- coding:utf-8 -*-

import peewee

from torcms.core.base_model import BaseModel


class CabCatalog(BaseModel):
    uid = peewee.CharField(null=False, max_length=4, index=True, unique=True, primary_key=True, help_text='', )
    slug = peewee.CharField(null=False, index=True, unique=True, max_length=36, help_text='', )
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    order = peewee.IntegerField()
    # post_count = peewee.IntegerField(default=0)
    count = peewee.IntegerField(default=0)


class CabLink(BaseModel):
    uid = peewee.CharField(null=False, index=False, unique=True, primary_key=True, default='0000',
                           max_length=4, help_text='', )
    link = peewee.CharField(null=False, max_length=36, help_text='', )
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    logo = peewee.CharField(null=False, max_length=255, help_text='', )
    order = peewee.IntegerField()


class CabClass(BaseModel):
    uid = peewee.CharField(null=False, index=False, unique=True, primary_key=True, default='00000',
                           max_length=5, help_text='', )
    slug = peewee.CharField(null=False, index=True, unique=True, max_length=36, help_text='', )
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    order = peewee.IntegerField()


class CabPage(BaseModel):
    title = peewee.CharField(null=False, max_length=255, )
    slug = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    date = peewee.DateTimeField()
    cnt_html = peewee.TextField()
    time_create = peewee.IntegerField()
    id_user = peewee.CharField()
    cnt_md = peewee.TextField()
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()


class CabPost(BaseModel):
    uid = peewee.CharField(null=False, index=False, unique=True, primary_key=True, default='00000',
                           max_length=5, help_text='', )
    title = peewee.CharField(null=False, help_text='Title')
    keywords = peewee.CharField(null=False, help_text='Keywords')
    date = peewee.DateTimeField()
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(null=False, max_length=36, help_text='UserName', )
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()
    logo = peewee.CharField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()


class CabWiki(BaseModel):
    uid = peewee.CharField(null=False, index=False,
                           unique=True,
                           primary_key=True,
                           default='00000',
                           max_length=8, help_text='', )
    title = peewee.CharField(null=False, unique=True, help_text='Title')
    date = peewee.DateTimeField()
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(null=False, max_length=36, help_text='UserName', )
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()


class CabPostHist(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, help_text='', primary_key=True, max_length=36)
    title = peewee.CharField(null=False, max_length=255, help_text='', )
    date = peewee.DateTimeField()
    post_id = peewee.CharField(null=False, max_length=5, help_text='', )
    time_create = peewee.IntegerField()
    user_name = peewee.CharField()
    cnt_md = peewee.TextField()
    time_update = peewee.IntegerField()
    logo = peewee.CharField()


class CabWikiHist(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, help_text='', primary_key=True, max_length=36)
    title = peewee.CharField(null=False, max_length=255, help_text='', )
    date = peewee.DateTimeField()
    wiki_id = peewee.CharField(null=False, max_length=8, help_text='', )
    time_create = peewee.IntegerField()
    user_name = peewee.CharField()
    cnt_md = peewee.TextField()
    time_update = peewee.IntegerField()


class CabMember(BaseModel):
    # user_id = peewee.CharField()
    '''
    privilege:
    11111
    read,add,edit,delete,manage
    [0]: read
    [1]: add
    [2]: edit
    [3]: delete
    [4]: manage
    And, could be extended.
    '''
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    user_name = peewee.CharField(null=False, index=True, unique=True, max_length=16, help_text='', )
    privilege = peewee.CharField(null=False, default='10000', help_text='Member Privilege', )
    user_pass = peewee.CharField(null=False, max_length=255, )
    user_email = peewee.CharField(null=False, max_length=255, )
    reset_passwd_timestamp = peewee.IntegerField(null=False, default=0)


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


class CabLabel(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, help_text='', max_length=8)
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    count = peewee.IntegerField()


class CabPost2Label(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, max_length=36, help_text='', )
    tag = peewee.ForeignKeyField(CabLabel, related_name='tag_post_rel')
    app = peewee.ForeignKeyField(CabPost, related_name='post_tag_rel')
    order = peewee.IntegerField()


class CabRelation(BaseModel):
    '''
    相关应用
    相关性，并非是对称操作
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    app_f = peewee.ForeignKeyField(CabPost, related_name='post_from')
    app_t = peewee.ForeignKeyField(CabPost, related_name='post_to')
    count = peewee.IntegerField()
