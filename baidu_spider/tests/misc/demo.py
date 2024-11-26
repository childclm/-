import asyncio
from asyncio import Semaphore
semaphore = Semaphore(4)


async def fetch():
    semaphore.release()
    semaphore.release()
    semaphore.release()
    print(semaphore._value)

asyncio.run(fetch())
