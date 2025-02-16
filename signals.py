# signals.py
from core.loger import get_logger
from queue import SimpleQueue
import asyncio


class Signals:
    def __init__(self):
        self.logger = get_logger()

        self._apps_run: bool = True
        self._ai_run: bool = True
        self._task_queue = asyncio.Queue()
        self._result_queue = asyncio.Queue()

        self.logger.info("Signals class initialized")

    @property
    def apps_run(self) -> bool:
        return self._apps_run

    @apps_run.setter
    def apps_run(self, value: bool) -> None:
        self.logger.info("Method Set apps_run = %s", value)
        if value is False:
            self.logger.debug(" ai run = False")
            self._ai_run: bool = value
        self._apps_run: bool = value

    @property
    def ai_run(self) -> bool:
        return self._ai_run

    @ai_run.setter
    def ai_run(self, value: bool):
        self.logger.debug("Method Set ai_run = %s", value)
        self._ai_run: bool = value

    async def add_task(self, task):
        """Добавляет задачу в очередь"""
        await self._task_queue.put(task)

    async def get_task(self):
        """Получает следующую задачу (блокирующий вызов)"""
        return await self._task_queue.get()

    async def add_result(self, result):
        """Добавляет результат в очередь"""
        await self._result_queue.put(result)

    async def get_result(self):
        """Получает результат (блокирующий вызов)"""
        return await self._result_queue.get()
