# core/core.py

from core.loger import get_logger
from threading import Thread
from .manager_plugins import ManagerPlugins
import asyncio


class Core:
    def __init__(self, signals):
        self.logger = get_logger()
        self.signals = signals  # signals is a list of Signal objects
        self.manager_plugins = ManagerPlugins(self.signals)

        self.logger.info("Core initialized")

    async def _run(self):
        while self.signals.ai_run:
            await self.signals.add_task("WWD")
            result = await self.signals.get_result()
            self.logger.debug(result)
            if result["status"]:
                await self.signals.add_task("open_browser")
                result = await self.signals.get_result()
                self.logger.debug(result)

    async def run(self):
        asyncio.create_task(self.manager_plugins.run())
        await self._run()
