from abc import ABC, abstractmethod


class SpeechToTextInterface(ABC):
    @abstractmethod
    def __init__(self, signals, **kwargs) -> None:
        self.signals = signals
        self.kwargs = kwargs

    @abstractmethod
    def run(self, **kwargs): ...
