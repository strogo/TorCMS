# -*- coding:utf-8 -*-

import os

from torcms.core.base_handler import BaseHandler


class JavascriptHandler(BaseHandler):
    def get(self, url_str=''):
        if len(url_str) > 0:
            url_arr = url_str.split(r'/')
        else:
            self.redirect('/')

        if os.path.exists(('templates/jshtml/{0}_js.html').format(format('/'.join(url_arr[:-1])))):
            self.render('jshtml/{0}_js.html'.format('/'.join(url_arr[:-1])), )
        else:
            return None
