from abc import ABC, abstractmethod


class WakeWordDetectionInterface(ABC):

    @abstractmethod
    def __init__(self, signals, **kwargs):
        self.signals = signals
        self.kwargs = kwargs

    @abstractmethod
    def run(self, **kwargs): ...
