from core.interfaces.SpeechToTextInterface import SpeechToTextInterface

import queue
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
from core.loger import get_logger


class Vosk(SpeechToTextInterface):

    def select_device(self):
        self.device_info = sd.query_devices(None, "input")
        self.samplerate = int(self.device_info["default_samplerate"])

        self.rec = KaldiRecognizer(self.model, self.samplerate)

    def create_module(self, model_path=None, language=None):
        self.model = Model(model_path=model_path, lang=language)

    def __init__(self, signals, **kwargs):
        super().__init__(signals, **kwargs)
        self.logger = get_logger()

        self.rec = None
        self.device_info = None
        self.samplerate = None
        self.model = None

        if not kwargs.get("model_path", False) and not kwargs.get("languages", False):
            self.signals.ai_run = False
            self.signals.apps_run = False
            raise ValueError(
                "Model path not found. Please select model_path or languages"
            )

        if kwargs.get("languages", False):
            self.languages = kwargs.get("languages")
            self.model_path = None
            self.create_module("vosk")
        else:
            self.languages = None
            self.model_path = kwargs.get("model_path")
            self.create_module(model_path=self.model_path)

        self.select_device()
        self.q = queue.Queue()

    def audio_callback(self, indata, frames, time, status):
        if status:
            self.logger.debug(status, flush=True)
        self.q.put(bytes(indata))

    def run(self, **kwargs):

        with sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self.audio_callback,
        ):
            self.logger.info("VOSK is start listening...")

            while self.signals.ai_run:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    self.logger.info("Recognized speech: %s", result.get("text", ""))
                    return {"status": True, "message": result.get("text", "")}
