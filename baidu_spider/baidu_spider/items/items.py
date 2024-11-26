from baidu_spider.baidu_spider.exceptions import ItemInitError, ItemAttributeError
from baidu_spider.baidu_spider.items import Field, ItemMeta


class Item(metaclass=ItemMeta):
    FIELDS: dict

    def __init__(self, *args, **keyword_args):
        self._values = {}
        if args:
            raise ItemInitError(
                f"{self.__class__.__name__}: positional arguments are not supported, use keyword arguments."
            )
        if keyword_args:
            for k, v in keyword_args.items():
                self[k] = v
        # print(self.FIELDS)

    def __setitem__(self, key, value):
        if key in self.FIELDS:
            self._values[key] = value
        else:
            raise KeyError(f'{self.__class__.__name__} does not support field {key}')

    def __getitem__(self, item):
        return self._values[item]

    def __delitem__(self, key):
        del self._values[key]

    def __setattr__(self, key, value):
        if not key.startswith('_'):
            raise AttributeError(
                f'use item [{key!r}] = [{value!r}] to set field value'
            )
        super().__setattr__(key, value)


    # 属性不存在就会进入__getattr__
    # 属性存不存在都会进入__getattribute__
    # 抛出AttributeError异常会调用__getattr__


    def __getattr__(self, item):
        raise AttributeError(
            f'use item[{item!r}] to get field value2'
        )

    def __getattribute__(self, item):
        field = super().__getattribute__('FIELDS')
        if item in field:
            raise ItemAttributeError(
                f'use item[{item!r}] to get field value1'
            )
        else:
            return super().__getattribute__(item)


    def __repr__(self):
        return str(self._values)

    __str__ = __repr__


if __name__ == '__main__':
    class TestItem(Item):
        url = Field()
        title = Field()
    test_item = TestItem()
    print(test_item.url)
