PROJECT_NAME = "baidu_spider"
CONCURRENCY = 32
TEST = 111

LOG_LEVEL = 'INFO'

VERIFY_SSL = True

REQUEST_TIMEOUT = 60

USE_SESSION = True

DOWNLOADER = 'baidu_spider.baidu_spider.core.downloader.aiohttp_downloader.AioDownloader'