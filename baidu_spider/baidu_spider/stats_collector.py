from baidu_spider.baidu_spider.utils.log import get_loger
from pprint import pformat


class StatsCollector:
    def __init__(self, crawler):
        self.crawler = crawler
        self._stats = {}
        self.logger = get_loger(self.__class__.__name__, 'INFO')

    def inc_value(self, key, count=1, start=0):
        self._stats[key] = self._stats.setdefault(key, start) + count

    def get_value(self, key, default=None):
        return self._stats[key, default]

    def get_stats(self):
        return self._stats

    def set_stats(self, stats):
        self._stats = stats

    def clear_stats(self):
        self._stats.clear()

    def close_spider(self, spider, reason):
        self._stats['reason'] = reason
        self.logger.info(f"{spider} stats: \n" + pformat(self._stats))
