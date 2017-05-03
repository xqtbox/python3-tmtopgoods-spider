from urllib import request
from urllib import parse
### 使用urllib库进行下载HTML页面

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        values = {'name': 'voidking', 'language': 'Python'}
        data = parse.urlencode(values).encode(encoding='utf-8', errors='ignore')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0','Content-Length': '0'}
        request1 = request.Request(url=url, data=data, headers=headers, method='GET')
        response = request.urlopen(request1)

        if response.getcode() != 200:
            return None

        buff = response.read()
        html = buff.decode("gb2312",errors='ignore')
        return html