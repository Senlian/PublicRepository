#! /usr/bin/ python
# coding:utf8
import os
import urllib2
# import urllib
'''
下载html网页
'''

class HtmlDownloader(object):
    def downloader(self, page_url):
        if page_url is None:
            return None

        request = urllib2.Request(page_url)
        response = urllib2.urlopen(request)

        if response.getcode() != 200:
            print 'response exitcode is', response.getcode()
            return None

        page = response.read()
        html_name = os.path.join(os.getcwd(), 'output', 'demo_page_' + os.path.basename(page_url) + '.html')
        if not os.path.exists(os.path.dirname(html_name)):
            os.makedirs(os.path.dirname(html_name))
        # local_html = open(html_name, 'w').write(page)
        return page


if __name__ == '__main__':
    pass
