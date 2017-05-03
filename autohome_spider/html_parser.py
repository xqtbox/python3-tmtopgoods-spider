from bs4 import BeautifulSoup
import re
from urllib import parse


class HtmlParser(object):

    # 获取html中的新的连接
    def _get_new_urls(self, page_url, soup):
        # 结果存入列表
        new_urls = set()
        # 正则匹配：<a href="/3589/#pvareaid=101201" title="博瑞">博瑞</a>
        links = soup.find_all('a', href=re.compile(r'/\d+/#pvareaid=\d+'),title=re.compile(r'\S'))
        for link in links:
            # 获取相对url
            new_url = link['href']
            # 拼接为完整url
            new_full_url = parse.urljoin(page_url, new_url)
            # print(new_full_url)
            new_urls.add(new_full_url)
        # print(new_urls)
        return new_urls

    # 获取当前页面 汽车的名字以及评分
    def _get_new_data(self, page_url, soup):
        # 存放数据
        res_data = {}
        # url
        res_data['url'] = page_url

        # 获取html中的车名
        # <div class="subnav-title-name">   <a href="/78/">广汽本田-<h1>雅阁</h1></a>     </div>
        title_node = soup.find(
            'div', class_='subnav-title-name').find('a')
        # 转换成字符串 并去除<h1>标签
        res_data['title'] = title_node.get_text().strip('<h1>').strip('</h1>')

        # 获取html中的汽车评分
        # <a class="font-score" href="http://k.autohome.com.cn/78/8369/#pvareaid=101486">4.38</a>
        summary_node = soup.find('a', class_='font-score')
        res_data['summary'] = summary_node.get_text()
        print(res_data)
        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        soup2 = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup2)
        return new_urls, new_data
