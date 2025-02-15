# signals.py
from core.loger import get_logger
from queue import SimpleQueue


class Signals:
    def __init__(self):
        self.logger = get_logger()

        self._apps_run: bool = True
        self._ai_run: bool = True
        self._tasks: SimpleQueue = SimpleQueue()
        self._output: SimpleQueue = SimpleQueue()

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

    def get_task(self):
        element = self._tasks.get()
        self.logger.debug("Method Get task %s", element)
        return element

    def put_task(self, task):
        self.logger.debug("Method Add task %s", task)
        self._tasks.put(task)

    def clear_task(self):
        self._tasks = SimpleQueue()

    def print_task(self):
        print(self._tasks)

    def get_task_nowait(self):
        return self._tasks.get_nowait()

    def get_output(self):
        element = self._output.get()
        self.logger.debug("Method Get output %s", element)
        return element

    def put_output(self, output):
        self.logger.debug("Method Add output %s", output)
        self._output.put(output)

    def clear_output(self):
        self._output = SimpleQueue()

    def print_output(self):
        print(self._output)

    def get_output_nowait(self):
        return self._output.get_nowait()
