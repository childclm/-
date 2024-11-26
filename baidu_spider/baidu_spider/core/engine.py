from typing import Optional, Generator, Callable
from baidu_spider.baidu_spider.core.downloader import DownloaderBase
from baidu_spider.baidu_spider.core.processor import Processor
from baidu_spider.baidu_spider.core.schedule import Schedule
from baidu_spider.baidu_spider.exceptions import OutPutError
from baidu_spider.baidu_spider.http.request import Request
from baidu_spider.baidu_spider.items.items import Item
from baidu_spider.baidu_spider.task_manage import TaskManager
from baidu_spider.baidu_spider.utils.log import get_loger
from baidu_spider.baidu_spider.utils.project import load_class
from baidu_spider.baidu_spider.utils.spider import transform
from inspect import iscoroutine
import asyncio



class Engine:
    def __init__(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings
        self.logger = get_loger(self.__class__.__name__)
        self.downloader: Optional[DownloaderBase] = None
        self.start_requests: Optional[Generator] = None
        self.schedule: Optional[Schedule] = None
        self.spider: Optional[Generator] = None
        self.processor: Optional[Processor] = None
        # print(f"当前的并发数{self.crawler.settings.getint('CONCURRENCY')}")
        self.task_manager: TaskManager = TaskManager(self.settings.getint('CONCURRENCY'))
        self.running = False

    def _get_downloader_cls(self):
        downloader_cls = load_class(self.settings.get('DOWNLOADER'))
        if not issubclass(downloader_cls, DownloaderBase):
            raise TypeError(
                f"The downloader class({self.settings.get('DOWNLOADER')}) doesn't fully implemented required interface"
            )
        return downloader_cls

    async def start_spider(self, spider):
        self.running = True
        self.logger.info(f"baidu_spider started. (project name: {self.settings.get('PROJECT_NAME')})")
        self.spider = spider
        downloader_cls = self._get_downloader_cls()
        self.downloader = downloader_cls(self.crawler)
        if hasattr(self.downloader, 'open'):
            self.downloader.open()
        self.schedule = Schedule(self.crawler)
        self.processor = Processor(self.crawler)
        if hasattr(self.schedule, 'open'):
            # 创建一个任务队列，等下方Request
            self.schedule.open()
        self.start_requests = iter(spider.start_requests())
        await self._open_spder()

    async def _open_spder(self):
        crawling = asyncio.create_task(self.craw(), name='crawling')
        # 这里可以干其他的事情
        await crawling


    async def craw(self):
        """主逻辑:return:"""
        while self.running:
            if (request := await self._get_next_request()) is not None:
                await self._carw(request)

            else:
                try:
                    start_request = next(self.start_requests)
                except StopIteration:
                    self.start_requests = None
                except Exception as e:
                    if not await self._exit():
                        continue
                    self.running = False
                    if self.start_requests is not None:
                        self.logger.error(f"Error during start_requests: {e}")
                else:
                    # 入队
                    await self.enqueue_request(start_request)
        if not self.running:
            await self.close_spider()

    async def _carw(self, request):
        # todo 实现并发
        async def craw_task():
            outputs = await self._fetch(request)
            if outputs:
                await self._handle_spider_output(outputs)
        await self.task_manager.semaphore.acquire()
        self.task_manager.create_task(craw_task())


    async def _fetch(self, request):
        async def _success(_response):
            callback: Optional[Callable] = request.callback or self.spider.parse  # noqa
            if _outputs := callback(_response):
                if iscoroutine(_outputs):
                    await _outputs
                else:
                    return transform(_outputs)
        _response = await self.downloader.fetch(request)
        if not _response:
            return None
        outputs = await _success(_response)
        return outputs

    async def enqueue_request(self, request):
        await self._schedule_request(request)

    async def _schedule_request(self, request):
        # todo  去重
        await self.schedule.enqueue_request(request)

    async def _get_next_request(self):
        return await self.schedule.next_request()

    async def _handle_spider_output(self, outputs):
        async for spider_output in outputs:
            if isinstance(spider_output, (Request, Item)):
                await self.processor.enqueue(spider_output)
            else:
                raise OutPutError(f'{type(self.spider)} return must `Request` or `item`')

    async def _exit(self):
        # 调度器，下载器，下载请求， output都空闲
        if self.schedule.idle() and self.downloader.idle() and self.task_manager.all_done() and self.processor.idle():
            return True
        else:
            return False

    async def close_spider(self):
        await asyncio.gather(*self.task_manager.current_task)
        await self.downloader.close()
        await self.crawler.close()




