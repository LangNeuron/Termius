# core/core.py

from core.loger import get_logger
from threading import Thread
from .manager_plugins import ManagerPlugins


class Core:
    def __init__(self, signals):
        self.logger = get_logger()
        self.signals = signals  # signals is a list of Signal objects
        self.manager_plugins = ManagerPlugins(self.signals)
        self.process = Thread(target=self.manager_plugins.run)

        self.logger.info("Core initialized")

    def run(self):
        self.process.start()
        while self.signals.ai_run:
            self.signals.put_task("WWD")
            out = self.signals.get_output()
            if out:
                self.signals.put_task("STT")
                self.signals.get_output()
                """self.logger.info("Core running")
        # load base model
        if self.manager_plugins.table_plugins["WWD"]["loaded"]:
            wake_word_detection = self.manager_plugins.table_plugins["WWD"]["loaded"]
            print(wake_word_detection)
        else:
            wake_word_detection = self.manager_plugins.table_plugins["WWD"]

        while self.signals.ai_run:
            self.logger.debug("Core working")
            wake_word_detection()"""
