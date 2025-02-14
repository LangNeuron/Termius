# signals.py
from core.loger import get_logger


class Signals:
    def __init__(self):
        self.logger = get_logger()

        self._apps_run: bool = True
        self._ai_run: bool = False

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
