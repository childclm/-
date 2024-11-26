from baidu_spider.baidu_spider.utils.project import get_settings
from baidu_spider.baidu_spider.crawler import CrawlerProcess
from baidu_spider.tests.baidu_spider.spider.baidu import BaiduSpider
from baidu_spider.tests.baidu_spider.spider.baidu2 import BaiduSpider2
from baidu_spider.baidu_spider.utils import system
import asyncio
import time


async def main():
    settings = get_settings('settings')
    # print(settings)
    process = CrawlerProcess(settings)
    await process.crawl(BaiduSpider)
    # await process.crawl(BaiduSpider2)
    await process.start()

t = time.time()
asyncio.run(main())
print(f'总时间{time.time() - t}')