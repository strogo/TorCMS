# -*- coding:utf-8 -*-

import tornado.escape
import tornado.web
import tornado.web
from torcms.model.category_model import MCategory


from torcms.model.reply_model import MReply
from torcms.model.page_model import MPage
from torcms.model.rating_model import MRating

mreply = MReply()
mpage = MPage()
mrating = MRating()


class baidu_share(tornado.web.UIModule):
    def render(self):
       #  out_str = '''<div class="bdsharebuttonbox"><a class="bds_more" href="#" data-cmd="more"></a><a title="分享到QQ空间" class="bds_qzone" href="#" data-cmd="qzone"></a><a title="分享到新浪微博" class="bds_tsina" href="#" data-cmd="tsina"></a><a title="分享到腾讯微博" class="bds_tqq" href="#" data-cmd="tqq"></a><a title="分享到人人网" class="bds_renren" href="#" data-cmd="renren"></a><a title="分享到微信" class="bds_weixin" href="#" data-cmd="weixin"></a></div>
       # <script>window._bd_share_config={"common":{"bdSnsKey":{},"bdText":"","bdMini":"2","bdPic":"","bdStyle":"0","bdSize":"16"},"share":{}};with(document)0[(getElementsByTagName('head')[0]||body).appendChild(createElement('script')).src='http://bdimg.share.baidu.com/static/api/js/share.js?v=89860593.js?cdnversion='+~(-new Date()/36e5)];</script>'''
       #  return out_str

        return self.render_string('modules/widget/baidu_share.html')

class reply_panel(tornado.web.UIModule):
    def render(self, uid, userinfo):
        return self.render_string('modules/widget/reply_panel.html',
                                  uid=uid,
                                  replys=mreply.query_by_post(uid),
                                  userinfo=userinfo,
                                  unescape=tornado.escape.xhtml_unescape,
                                  linkify=tornado.escape.linkify,
                                  )


class userinfo_widget(tornado.web.UIModule, tornado.web.RequestHandler):
    def render(self, signature):
        if self.get_secure_cookie("user"):
            self.render('modules/widget/loginfo.html',
                        username=self.get_secure_cookie("user"))
        else:
            self.render('modules/widget/tologinfo.html')


class widget_editor(tornado.web.UIModule):
    def render(self, router, uid, userinfo):
        kwd = {'router': router,
               'uid': uid,
               }
        return self.render_string('modules/widget/widget_editor.html',
                                  kwd=kwd,
                                  userinfo=userinfo,
                                  )


class widget_search(tornado.web.UIModule):
    def render(self, ):
        self.mcat = MCategory()
        tag_enum = self.mcat.query_pcat(kind='2')
        return self.render_string('modules/widget/widget_search.html',
                                  cat_enum=tag_enum,
                                  tag_enum = tag_enum)


class star_rating(tornado.web.UIModule):
    def render(self, postinfo, userinfo):
        rating = False
        if userinfo:
            rating = mrating.get_rating(postinfo.uid, userinfo.uid)
        if rating:
            pass
        else:
            rating = postinfo.rating
        return self.render_string('modules/widget/star_rating.html',
                                  unescape=tornado.escape.xhtml_unescape,
                                  postinfo=postinfo,
                                  userinfo=userinfo,
                                  rating=rating,
                                  )
