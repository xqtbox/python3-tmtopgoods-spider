# 加载url管理器、下载器、解析器、输出器
from autohome_spider import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    # 初始化各个对象
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        # 记录当前爬取的是第几个url
        count = 1
        # 将入口url添加进url管理器，这样url管理器就有了待爬取的url,我们就可以启动爬虫的循环
        self.urls.add_new_url(root_url)
        # 当url管理器有新的url时，启动循环
        while self.urls.has_new_url():
            try:
                # 获取待爬取的url
                new_url = self.urls.get_new_url()
                # 实时打印爬取数和爬取url
                print('craw %s : %s' % (count, new_url))
                # 下载器下载页面
                html_cont = self.downloader.download(new_url)
                # print(html_cont)

                # 解析器解析url和页面，得到新的url和数据(返回两个值)
                new_urls, new_data = self.parser.parse(new_url, html_cont)

                # 获得的新的url添加进url管理器
                self.urls.add_new_urls(new_urls)
                # 收集数据
                self.outputer.collect_data(new_data)

                # 设置爬取数
                if count == 100:
                    break

                count = count + 1
            except Exception as e:
                print(str(e))

        # 输出收集好的数据
        self.outputer.output_html()

if __name__ == '__main__':
    # 爬虫入口url
    root_url = 'http://www.autohome.com.cn/78/#pvareaid=103177'
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
