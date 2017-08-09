#! /usr/bin/ python
# coding:utf-8
import html_downloader
import html_outputer
import html_parser
import url_manager

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.page_downloader = html_downloader.HtmlDownloader()
        self.page_parser = html_parser.HtmlPaser()
        self.page_outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():

            new_url = self.urls.get_new_url()
            page_cont = self.page_downloader.downloader(new_url)
            new_urls, new_data = self.page_parser.parser(new_url, page_cont)
            if new_url == root_url:
                self.urls.add_new_urls(new_urls)
            self.page_outputer.collect_data(new_data)
            # break

        self.page_outputer.output_html()
        self.page_outputer.save_db()

        pass


if __name__ == '__main__':
    root_url = 'https://baike.baidu.com/item/Python'
    spider_obj = SpiderMain()
    spider_obj.craw(root_url)
    pass
