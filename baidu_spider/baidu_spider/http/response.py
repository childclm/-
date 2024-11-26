import re
import json
from typing import Dict
from typing import Optional
from parsel import Selector
from urllib.parse import urljoin as _urljoin
from baidu_spider.baidu_spider.http.request import Request
from baidu_spider.baidu_spider.exceptions import DecodeError



class Response:
    def __init__(
            self, url: str, *,
            request: Request,
            headers: Optional[Dict] = None,
            body: bytes = b"",
            status: int = 200
    ):
        self.url = url
        self.headers = headers if headers is not None else {}
        self.body = body
        self.request = request
        self.status = status
        self.encoding = self.request.encoding
        # 缓存机制，如果出现多次response.text只走一遍text逻辑
        self._text_cache = None
        self._selector = None

    @property
    def text(self):
        if self._text_cache:
            return self._text_cache
        try:
            self._text_cache = self.body.decode(self.encoding)
        except UnicodeDecodeError:
            try:
                _encoding_re = re.compile(r"charset([\w-]+)", flags=re.I)
                _encoding_string = self.headers.get('content-type', '') or self.headers.get('Content-Type', '')
                _encoding = _encoding_re.search(_encoding_string)
                if _encoding:
                    _encoding = _encoding.groups()[1]
                    self._text_cache = self.body.decode(_encoding)
                else:
                    raise DecodeError(
                        f'{self.request} {self.request.encoding} error.'
                    )
            except UnicodeDecodeError as exc:
                raise UnicodeDecodeError(
                    exc.encoding, exc.object, exc.start, exc.end, f'{self.request}'
                )
        return self._text_cache

    def json(self):
        """
        str类型json类型
        :return:
        """
        return json.loads(self.text)

    def urljoin(self, url):
        """
        url拼接
        :param url:
        :return:
        """
        return _urljoin(self.url, url)

    def xpath(self, xpath_string):
        """
        :param xpath_string:
        :return:
        """
        if not self._selector:
            self._selector = Selector(self.text)
        return self._selector.xpath(xpath_string)

    def __str__(self):
        return f'<{self.status}  {self.url}>'

    @property
    def meta(self):
        return self.request.meta

