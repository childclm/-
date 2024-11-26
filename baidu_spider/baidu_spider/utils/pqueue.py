from asyncio import PriorityQueue, TimeoutError
import asyncio


class SpiderQueue(PriorityQueue):
    def __init__(self, maxsize=0):
        super(SpiderQueue, self).__init__(maxsize=maxsize)

    async def get(self):
        f = super().get()
        try:
            return await asyncio.wait_for(f, timeout=0.1)
        except TimeoutError:
            return None