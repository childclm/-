from inspect import isasyncgen, isgenerator
from baidu_spider.baidu_spider.exceptions import TransformTypeError


async def transform(func_result):
    if isgenerator(func_result):
        for r in func_result:
            yield r
    elif isasyncgen(func_result):
        async for r in func_result:
            yield r
    else:
        raise TransformTypeError('callback return value must be `generator` or `async generator`')