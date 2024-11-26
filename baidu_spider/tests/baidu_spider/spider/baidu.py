from baidu_spider.baidu_spider.spider import Spider
from baidu_spider.baidu_spider.http.request import Request
from baidu_spider.tests.baidu_spider.items import BaiduItem


class BaiduSpider(Spider):
    start_urls = ['http://www.baidu.com', 'http://www.baidu.com']

    async def parse(self, response):
        # print('parse', response)
        for i in range(2):
            url = 'http://www.baidu.com'
            request = Request(url, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        # print('parse_page', response)
        for i in range(10):
            url = 'http://www.baidu.com'
            request = Request(url, callback=self.parse_detail)
            yield request

    @staticmethod
    def parse_detail(response):
        item = BaiduItem()
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').get()
        yield item







