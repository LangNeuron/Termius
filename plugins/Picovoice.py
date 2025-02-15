from core.interfaces.WakeWordDetectionInterface import WakeWordDetectionInterface
import pvporcupine
import struct
from pvrecorder import PvRecorder
from datetime import datetime


class WakeWordDetection(WakeWordDetectionInterface):

    def __init__(self, signals, **kwargs):
        super().__init__(signals, **kwargs)

        self.porcupine = None
        if not kwargs.get("token"):
            raise ValueError("Please configure your Porcupine (Picovoice) token")
        self.token = kwargs.get("token")

        self.sensitivity = kwargs.get("sensitivity", 0.7)
        self.keywords = kwargs.get("keywords", "jarvis")

        if self.sensitivity is None:
            self.sensitivity = 0.7
        if self.keywords is None:
            self.keywords = "jarvis"

        print(self.keywords)

        try:
            # Инициализация Porcupine
            self.porcupine = pvporcupine.create(
                access_key=self.token,
                keywords=self.keywords,
                sensitivities=[self.sensitivity] * len(self.keywords),
            )
        except Exception as e:
            print("Error initializing Porcupine: %s" % e)

    def run(self):
        """
        Запускает детекцию wake word в реальном времени.
        """
        recorder = PvRecorder(frame_length=self.porcupine.frame_length)
        recorder.start()

        print("Listening for wake word...")

        try:
            while self.signals.ai_run is True:
                pcm = recorder.read()
                result = self.porcupine.process(pcm)

                if result >= 0:
                    print(
                        "[%s] Detected %s"
                        % (str(datetime.now()), self.keywords[result])
                    )
                    return True
        except KeyboardInterrupt:
            print("Stopping ...")
            return False
        finally:
            recorder.delete()
            self.porcupine.delete()
