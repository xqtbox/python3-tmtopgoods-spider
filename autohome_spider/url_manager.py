class UrlManager(object):
    # 初始化存放新的url列表和爬取过的url列表
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    # 向url管理器添加一个新的url
    def add_new_url(self, url):
        # url是否是空
        if url is None:
            return
        # url是否存在在新的url列表和爬取过的url列表中
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    # 向url管理器添加新的url(urls是 解析器 返回的新的url列表)
    def add_new_urls(self, urls):
        # urls是否是空
        if urls is None or len(urls) == 0:
            return
        # 逐一添加url
        for url in urls:
            self.add_new_url(url)

    # url管理器是否有新的待爬取url
    def has_new_url(self):
        return len(self.new_urls) != 0

    # 从url管理器中获取新的待爬取url
    def get_new_url(self):
        # 获取url并从new_urls中移除
        new_url = self.new_urls.pop()
        # 添加进已爬取old_urls中
        self.old_urls.add(new_url)
        # 返回新的url
        return new_url
