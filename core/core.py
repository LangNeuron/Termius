# core/core.py


from .loger import get_logger


class Core:
    def __init__(self):
        self.logger = get_logger()
        self.logger.info("Core initialized")

    def run(self): ...
