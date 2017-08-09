#! /usr/bin/ python
# coding:utf8
'''
管理网页链接
'''
class UrlManager(object):
    def __init__(self):
        self.new_urls = list()
        self.old_urls = list()
        pass

    def has_new_url(self):
        return len(self.new_urls) > 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.append(new_url)
        return new_url

    def add_new_url(self, root_url):
        if root_url is None:
            return
        if (root_url not in self.new_urls) and (root_url not in self.old_urls):
            self.new_urls.append(root_url)

    def add_new_urls(self, new_urls):
        for url in new_urls:
            self.add_new_url(url)
        pass


if __name__ == '__main__':
    pass
