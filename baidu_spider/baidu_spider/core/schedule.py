from typing import Optional
from baidu_spider.baidu_spider.utils.pqueue import SpiderQueue


class Schedule:
    def __init__(self, crawler):
        self.crawler = crawler
        self.request_queue: Optional[SpiderQueue] = None

    def open(self):
        self.request_queue = SpiderQueue()

    async def next_request(self):
        request = await self.request_queue.get()
        return request

    async def enqueue_request(self, request):
        await self.request_queue.put(request)
        self.crawler.stats.inc_value("request_schedule_count")

    def __len__(self):
        return self.request_queue.qsize()

    def idle(self) -> bool:
        return len(self) == 0
