from baidu_spider.baidu_spider.spider import Spider
from baidu_spider.baidu_spider.settings.settings_manage import SettingsManger
from baidu_spider.baidu_spider.core.engine import Engine
from baidu_spider.baidu_spider.stats_collector import StatsCollector
from baidu_spider.baidu_spider.utils.project import merge_settings
from baidu_spider.baidu_spider.exceptions import SpiderTypeError
from baidu_spider.baidu_spider.utils.log import get_loger
from typing import Type, Final, Set, Optional
import asyncio
import signal
logger = get_loger(__name__)


class Crawler:
    def __init__(self, spider_cls, settings):
        self.spider_cls = spider_cls
        self.spider: Optional[Spider] = None
        self.engine: Optional[Engine] = None
        self.stats: Optional[StatsCollector] = None
        self.settings: SettingsManger = settings.copy()



    async def crawl(self):
        self.spider = self._create_spider()
        self.engine = await self._create_engine()
        self.stats = self._create_stats()
        await self.engine.start_spider(self.spider)

    def _create_stats(self):
        stats = StatsCollector(self)
        return stats

    def _create_spider(self) -> Spider:
        spider = self.spider_cls.create_instance(self)
        self._set_spider(spider)
        return spider

    def _set_spider(self, spider):
        merge_settings(spider, self.settings)

    async def _create_engine(self):
        engine = Engine(self)
        return engine

    async def close(self, reason='finished'):
        self.stats.close_spider(self.spider, reason)


class CrawlerProcess:
    def __init__(self, settings):
        self.settings = settings
        self.crawls: Final[Set] = set()
        self._active: Final[Set] = set()
        signal.signal(signal.SIGINT, self._shutdowm)

    async def crawl(self, spider: Type[Spider]):
        crawler: Crawler = self._create_crawler(spider)
        self.crawls.add(crawler)
        task = await self._craw(crawler)
        self._active.add(task)

    async def start(self):
        await asyncio.gather(*self._active)

    @staticmethod
    async def _craw(crawler):
        return asyncio.create_task(crawler.crawl())

    def _create_crawler(self, spider_cls) -> Crawler:
        if isinstance(spider_cls, str):
            raise SpiderTypeError(f'{self}.crawl args: String is not supported')
        crawler = Crawler(spider_cls, self.settings)
        return crawler

    def _shutdowm(self, _signum, _frame):
        for crawler in self.crawls:
            crawler.engine.running = False
        logger.warning(f'spiders received signal `ctrl c` signal, closed.')



