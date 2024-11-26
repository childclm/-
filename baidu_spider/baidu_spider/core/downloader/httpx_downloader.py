from typing import Optional
import httpx
from baidu_spider.baidu_spider.core.downloader import DownloaderBase
from baidu_spider.baidu_spider.http.response import Response


class HTTPXDownloader(DownloaderBase):
    def __init__(self, crawler):
        super().__init__(crawler)
        self._timeout: Optional[httpx.Timeout] = None

    def open(self):
        super().open()
        request_timeout = self.crawler.settings.getint('REQUEST_TIMEOUT')
        self._timeout = httpx.Timeout(timeout=request_timeout)

    async def fetch(self, request) -> Optional[Response]:
        async with self._active(request):
            response = await self.download(request)
            if not response:
                return None
            return response

    async def download(self, request) -> Optional[Response]:
        try:
            proxies = request.proxy
            async with httpx.AsyncClient(timeout=self._timeout, proxies=proxies) as client:
                self.logger.debug(f'Request downloading:{request.url}, method:{request.method}')
                response = await client.request(
                    request.method, request.url, headers=request.headers, cookies=request.cookies, data=request.body
                )
                body = await response.aread()
        except Exception as e:
            self.logger.error(f'Error during request: {e}')
            return None
        return self.structure_response(request, response, body)

    @staticmethod
    def structure_response(request, response, body) -> Response:
        """
        构建response对象给你
        :param request:
        :param response:
        :param body:
        :return:
        """
        return Response(
            url=request.url,
            headers=dict(response.headers),
            status=response.status_code,
            body=body,
            request=request,
        )

