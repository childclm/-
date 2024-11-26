from typing import Set, Final
from asyncio import Task, Semaphore
import asyncio


class TaskManager:
    def __init__(self, total_concurrence=8):
        self.current_task: Final[Set] = set()
        self.semaphore: Semaphore = Semaphore(total_concurrence)

    def create_task(self, coroutine) -> Task:
        task = asyncio.create_task(coroutine)
        self.current_task.add(task)


        def done_callback(_fut: Task):
            self.semaphore.release()
            self.current_task.remove(task)
        task.add_done_callback(done_callback)
        return task

    def all_done(self):
        return len(self.current_task) == 0
