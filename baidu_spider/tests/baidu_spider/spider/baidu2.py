from baidu_spider.baidu_spider.spider import Spider  # noqa
from baidu_spider.baidu_spider.http.request import Request


class BaiduSpider2(Spider):
    start_urls = ['https://www.baidu.com', 'https://www.baidu.com']
    custom_settings = {'CONCURRENCY': '64'}

    async def parse(self, response):
        print('parse2', response)
        for i in range(2):
            url = 'https://www.baidu.com'
            request = Request(url, callback=self.parse_page)
            yield request

    def parse_page(self, response):
        print('parse2_page', response)
        for i in range(10):
            url = 'https://www.baidu.com'
            request = Request(url, callback=self.parse_detail)
            yield request

    def parse_detail(self, response):
        print('parse2_detail', response)

