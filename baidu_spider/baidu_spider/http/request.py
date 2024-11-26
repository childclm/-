from typing import Dict, Optional, Callable


class Request:
    def __init__(
            self, url: str, *,
            callback: Optional[Callable] = None,
            headers: Optional[Dict] = None,
            method: str = 'GET',
            priority: int = 0,
            cookies: Optional[Dict] = None,
            proxy: Optional[Dict] = None,
            body='',
            encoding='utf-8',
            meta: Optional[Dict] = None,
    ):
        self.url = url
        self.callback = callback
        self.headers = headers if headers is not None else {}
        self.method = method
        self.priority = priority
        self.cookies = cookies
        self.proxy = proxy
        self.body = body
        self.encoding = encoding
        self._meta = meta if meta is not None else {}

    def __lt__(self, other):
        return self.priority < other.priority

    def __str__(self):
        return f'{self.url} {self.method}'

    @property
    def meta(self):
        return self._meta