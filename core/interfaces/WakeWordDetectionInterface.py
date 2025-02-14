from abc import ABC, abstractmethod


class WakeWordDetectionInterface(ABC):
    def __init__(self, signals: object, **kwargs):
        self.signals = signals
        self.kwargs = kwargs

    def run(self): ...
