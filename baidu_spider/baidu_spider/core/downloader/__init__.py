from contextlib import asynccontextmanager
from abc import ABCMeta
from typing import Set, Final, Optional
from abc import abstractmethod
from baidu_spider.baidu_spider.http.request import Request
from baidu_spider.baidu_spider.http.response import Response
from baidu_spider.baidu_spider.utils.log import get_loger
# aiohttp httpx 插件化：插拔性 即插即用


class ActiveRequestManger:
    def __init__(self):
        self._active: Final[Set] = set()

    def add(self, request):
        self._active.add(request)

    def remove(self, request):
        self._active.remove(request)

    @asynccontextmanager
    async def __call__(self, request):
        self.add(request)
        try:
            yield
        finally:
            self.remove(request)

    def __len__(self):
        return len(self._active)


class DownloaderMeta(ABCMeta):
    def __subclasscheck__(self, subclass):
        required_method = ('create_instance', 'fetch', 'fetch', 'close', 'idle')
        is_subclass = all(
            hasattr(subclass, method) and callable(getattr(subclass, method, None)) for method in required_method
        )
        return is_subclass


class DownloaderBase(metaclass=DownloaderMeta):
    def __init__(self, crawler):
        self._active = ActiveRequestManger()
        self.crawler = crawler
        self.logger = get_loger(self.__class__.__name__, self.crawler.settings.get('LOG_LEVEL'))

    def open(self):
        self.logger.info(
            f'{self.crawler.spider} <downloader class: {type(self).__name__}>'
            f'concurrency: {self.crawler.settings.getint("CONCURRENCY")}'
        )

    @classmethod
    def create_instance(cls, *args, **kwargs):
        return cls(*args, **kwargs)


    async def fetch(self, request) -> Optional[Response]:
        async with self._active(request):
            response = await self.download(request)
            if not response:
                return None
            return response

    @abstractmethod
    async def download(self, request:Request) -> Optional[Response]:
        pass

    def idle(self) -> bool:
        return len(self) == 0

    def __len__(self) -> int:
        return len(self._active)

    async def close(self) -> None:
        pass




