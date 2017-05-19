# -*- coding: utf-8 -*-
import scrapy
from topgoods.items import TopgoodsItem

class TmgoodsSpiderSpider(scrapy.Spider):
    name = "tmgoods_spider"
    allowed_domains = ["tmall.com"]
    start_urls = ['https://www.tmall.com']
    count = 0
    def start_requests(self):  # 循环页码，就在这个函数中实现。
        reqs = []   # 每个页面的request
        cookies = {
            'miid':'1279809970704864021',
            'thw':'cn',
            't':'7349beda1fac2771e1b07173a388c1a7',
            'cookie2':'169e58df275871365bf763a04f83945d',
            '_tb_token_':'f5836335bbbed',
            'l':'As7Ol7pcpNOglmJtnYezXP/Fnq6RuZJB',
            'isg':'AuTkU7_eYUo5n5WHgkykUP1IteI6RAjnXtEpK_4Ehq96qYZzJ431dp1BH7ZL',
            'cna':'xxqjEU4BaTMCAXLV6R/2cfxq',
            'sca':'49d5174e',
            'atpsida':'b8147f8d3acd3709988ab26d_1495089785_1',
            'aimx':'xxqjEYvEdQcCAXLV6R9iOoQn_1495089785',
            'cad':'k95WugY3Sgew+2KIuDSUxTOnySH07xok1SSfrDICn3k=0001',
            'cap':'41cf',
            '_med':'dw:1366&dh:768&pw:1366&ph:768&ist:0',
            'res':'scroll%3A1349*6611-client%3A1349*637-offset%3A1349*6611-screen%3A1366*768',
            'pnm_cku822':'043UW5TcyMNYQwiAiwQRHhBfEF8QXtHcklnMWc%3D%7CUm5Ockt%2FR3pPe0F5QndJdCI%3D%7CU2xMHDJ7G2AHYg8hAS8XIgwsAl4%2FWTVSLFZ4Lng%3D%7CVGhXd1llXGhQbVhsVm5VYF5jVGlLcEx2SHxBf0F0QH5AekF%2FQG44%7CVWldfS0RMQ01DDQUKBMzHWxSPAIrFioSKhI4Az0YLlV7LXs%3D%7CVmhIGCUFOBgkGiMXNww3CzcXKxUuFTUPNAEhHSMYIwM5BjNlMw%3D%3D%7CV25Tbk5zU2xMcEl1VWtTaUlwJg%3D%3D',
            'cq':'ccp%3D1'
        }
        for i in range(0, 2): # 代表从0到1页
            req = scrapy.Request("https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.wH40GN&s="+str(i*60)+"&q=%C4%D0%D7%B0&sort=d&style=g&from=nanzhuang..pc_1_suggest&suggest=0_1&type=pc#J_Filter",cookies=cookies )
            reqs.append(req)
        return reqs

    def parse(self, response):
        TmgoodsSpiderSpider.count += 1
        divs = response.xpath("//*[@id='J_ItemList']/div/div")
        if not divs:
            self.log("List Page error--%s" % response.url)
        # 打印获取到的商品数
        print ("Goods numbers: ",len(divs))
        for div in divs:
            item = TopgoodsItem()
            # 商品价格
            item["GOODS_PRICE"] = div.xpath("p[@class='productPrice']/em/@title")[0].extract()#//*[@id="J_ItemList"]/div[1]/div/p[1]/em
            # 商品名称
            item["GOODS_NAME"] = div.xpath("p[@class='productTitle']/a/@title")[0].extract()
            # 商品连接
            pre_goods_url = div.xpath("p[@class='productTitle']/a/@href")[0].extract()
            item["GOODS_URL"] = pre_goods_url if "http:" in pre_goods_url else ("http:" + pre_goods_url)

            # 图片链接
            try:
                file_urls = div.xpath('div[@class="productImg-wrap"]/a[1]/img/@src|'
                                      'div[@class="productImg-wrap"]/a[1]/img/@data-ks-lazyload').extract()[0]
                item['file_urls'] = ["http:" + file_urls]
            except Exception as e:
                print("Error:",e)
                import pdb;pdb.set_trace()

            yield scrapy.Request(url=item["GOODS_URL"], meta={'item': item}, callback=self.parse_detail,dont_filter=True)


    def parse_detail(self,response):
        div = response.xpath('//*[@id="shopExtra"]/div[1]')
        if not div:
            self.log( "Detail Page error--%s"%response.url )

        item = response.meta['item']
        div = div[0]
        # 店铺名称
        item["SHOP_NAME"] = div.xpath("a/strong/text()")[0].extract()#//*[@id="shopExtra"]/div[1]/a/strong
        # 店铺连接
        item["SHOP_URL"] = div.xpath("a/@href")[0].extract()
        # # 公司名称
        # item["COMPANY_NAME"] = div.xpath("li[3]/div/text()")[0].extract().strip()
        # # 公司所在地
        # item["COMPANY_ADDRESS"] = div.xpath("li[4]/div/text()")[0].extract().strip()

        yield item