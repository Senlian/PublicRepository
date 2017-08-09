#! /usr/bin/ python
# coding:utf8
'''
解析网页内容
'''
import re
import urlparse

from bs4 import BeautifulSoup


class HtmlPaser(object):
    def parser(self, page_url, page_cont):
        if (page_url is None) or (page_cont is None):
            return None
        soup = BeautifulSoup(page_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # links = soup.find_all('a', href=re.compile(r'^/item/(\S)+'))
        links = soup.find_all('a', href=re.compile(r'^/item/[a-zA-Z0-9%#/]+'))
        for link in links:
            new_url_suf = link['href']
            # print new_url_suf
            new_url = urlparse.urljoin(page_url, new_url_suf)
            # print new_url
            new_urls.add(new_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        lable_cont = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        title = lable_cont.get_text()
        new_data = {title: page_url}
        return new_data


if __name__ == '__main__':
    pass
