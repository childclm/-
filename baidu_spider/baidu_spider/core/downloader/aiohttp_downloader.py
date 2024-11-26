from aiohttp import ClientSession, BaseConnector, ClientTimeout, TraceConfig, TCPConnector, ClientResponse
from baidu_spider.baidu_spider.core.downloader import DownloaderBase
from typing import Optional
from baidu_spider.baidu_spider.http.response import Response


class AioDownloader(DownloaderBase):
    def __init__(self, crawler):
        super().__init__(crawler)
        self.session: Optional[ClientSession] = None
        self.connector: Optional[BaseConnector] = None
        self._timeout: Optional[ClientTimeout] = None
        self._verify_ssl: Optional[bool] = None
        self._use_session: Optional[bool] = None
        self.trace_config: Optional[TraceConfig] = None
        self.request_methods = {
            'get': self._get,
            'post': self._post
        }

    def open(self):
        super().open()
        request_timeout = self.crawler.settings.getint('REQUEST_TIMEOUT')
        self._verify_ssl = self.crawler.settings.getbool('VERIFY_SSL')
        self._use_session = self.crawler.settings.getbool('USE_SESSION')
        self._timeout = ClientTimeout(total=request_timeout)
        self.trace_config = TraceConfig()
        self.trace_config.on_request_start.append(self.request_start)
        if self._use_session:
            self.connector = TCPConnector(verify_ssl=self._verify_ssl)
            self.session = ClientSession(
                connector=self.connector, timeout=self._timeout, trace_configs=[self.trace_config]
            )


    async def request_start(self, _session, _trace_config, params):
        self.logger.debug(f'Request downloading:{params.url}, method:{params.method}')

    async def download(self, request) -> Optional[Response]:
        try:
            if self._use_session:
                response = await self.send_request(self.session, request)
                # 返回类型为bytes类型
                body = await response.content.read()
            else:
                connector = TCPConnector(verify_ssl=self._verify_ssl)
                async with ClientSession(
                        connector=connector, timeout=self._timeout, trace_configs=[self.trace_config]
                ) as session:
                    response = await self.send_request(session, request)
                    # 返回类型为bytes类型
                    body = await response.content.read()
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
            status=response.status,
            body=body,
            request=request,
        )


    async def send_request(self, session, request) -> ClientResponse:
        return await self.request_methods[request.method.lower()](session, request)

    @staticmethod
    async def _get(session, request) -> ClientResponse:
        response = await session.get(
            url=request.url, headers=request.headers, cookies=request.cookies, proxy=request.proxy
        )
        return response

    @staticmethod
    async def _post(session, request) -> ClientResponse:
        response = await session.post(
            url=request.url, headers=request.headers, data=request.body, cookies=request.cookies, proxy=request.proxy
        )
        return response


    async def fetch(self, request) -> Optional[Response]:
        async with self._active(request):
            response = await self.download(request)
            if not response:
                return None
            return response

    async def close(self):
        if self.connector:
            await self.connector.close()
        if self.session:
            await self.session.close()