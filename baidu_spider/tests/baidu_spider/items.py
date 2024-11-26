from baidu_spider.baidu_spider.items import Field
from baidu_spider.baidu_spider.items.items import Item


class BaiduItem(Item):
    url = Field()
    title = Field()