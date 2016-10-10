# -*- coding: utf-8 -*-

import config
from torcms.core import tools
from torcms.model.post_model import MPost
from torcms.model.post_hist_model import MPostHist
from difflib import HtmlDiff
from torcms.core.tool.send_email import send_mail
from config import smtp_cfg
from config import site_url
from config_email import post_emails
import os
import re

import datetime

now = datetime.datetime.now()

datestr = now.strftime('%Y-%m-%d %H:%M:%S')

def run_edit_diff():
    email_cnt = '''<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title></title>
    <style type="text/css">
        table.diff {font-family:Courier; border:medium;}
        .diff_header {background-color:#e0e0e0}
        td.diff_header {text-align:right}
        .diff_next {background-color:#c0c0c0}
        .diff_add {background-color:#aaffaa}
        .diff_chg {background-color:#ffff77}
        .diff_sub {background-color:#ffaaaa}
    </style></head><body>'''
    mpost = MPost()
    mposthist = MPostHist()
    recent_posts = mpost.query_recent_edited( tools.timestamp() - 24 * 60 * 60)

    email_cnt = email_cnt + '<table border=1>'
    idx = 1
    for recent_post in recent_posts:
        hist_rec = mposthist.get_last(recent_post.uid)
        if hist_rec:
            foo_str = '''
                <tr><td>{0}</td><td class="diff_chg">Edit</td><td>{1}</td>
                <td><a href="{2}">{2}</a></td></tr>
                '''.format(idx, recent_post.title, os.path.join(site_url, 'post', recent_post.uid + '.html'))
            email_cnt = email_cnt + foo_str
        else:
            foo_str = '''
                <tr><td>{0}</td><td class="diff_add">New </td><td>{1}</td>
                <td><a href="{2}">{2}</a></td></tr>
                '''.format(idx, recent_post.title, os.path.join(site_url, 'post', recent_post.uid + '.html'))
            email_cnt = email_cnt + foo_str
        idx = idx + 1
    email_cnt = email_cnt + '</table>'

    recent_posts = mpost.query_recent_edited(tools.timestamp() - 24 * 60 * 60)
    diff_str = ''
    for recent_post in recent_posts:
        hist_rec = mposthist.get_last(recent_post.uid)
        if hist_rec:
            print('=' * 10)

            print(recent_post.title)

            raw_title = hist_rec.title
            new_title = recent_post.title

            test = HtmlDiff.make_file(HtmlDiff(), [raw_title], [new_title])

            # if len(test) > 1:
            start = test.find('<table class="diff"')  # 起点记录查询位置
            end = test.find('</table>')
            infobox = test[start:end] + '</table>'
            if ('diff_add' in infobox) or ('diff_chg' in infobox) or ('diff_sub' in infobox):
                diff_str = diff_str + '<h2 style="color:red; font-size:larger; font-weight:70;">TITLE: {0}</h2> TITLE'.format(
                    recent_post.title) + infobox

            raw_md = hist_rec.cnt_md.split('\n')
            new_md = recent_post.cnt_md.split('\n')
            test = HtmlDiff.make_file(HtmlDiff(), raw_md, new_md)

            # if len(test) >1 :
            start = test.find('<table class="diff"')  # 起点记录查询位置
            end = test.find('</table>')

            infobox = test[start:end] + '</table>'
            if ('diff_add' in infobox) or ('diff_chg' in infobox) or ('diff_sub' in infobox):
                diff_str = diff_str + '<h2 style="color:red; font-size:larger; font-weight:70;">TITLE: {0}</h2> CONTENT'.format(
                    recent_post.title) + infobox + '</hr>'


        else:
            continue
    if len(diff_str) < 8000:
        email_cnt = email_cnt + diff_str 
    email_cnt = email_cnt + '''<table class="diff" summary="Legends">
        <tr> <th colspan="2"> Legends </th> </tr>
        <tr> <td> <table border="" summary="Colors">
                      <tr><th> Colors </th> </tr>
                      <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
                      <tr><td class="diff_chg">Changed</td> </tr>
                      <tr><td class="diff_sub">Deleted</td> </tr>
                  </table></td>
             <td> <table border="" summary="Links">
                      <tr><th colspan="2"> Links </th> </tr>
                      <tr><td>(f)irst change</td> </tr>
                      <tr><td>(n)ext change</td> </tr>
                      <tr><td>(t)op</td> </tr>
                  </table></td> </tr>
    </table></body>'''

    # print (email_cnt)
    idx > 1:
        send_mail( post_emails , "{0}|{1}|{2}".format(smtp_cfg['name'], '文档更新情况', datestr), email_cnt)


