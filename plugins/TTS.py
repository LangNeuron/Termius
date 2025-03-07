from core.loger import get_logger
import pyttsx3
from gtts import gTTS
import playsound

class TTS:
    def __init__(self, signals, **kwargs):
        self.logger = get_logger()
        self.signals = signals

        self.kwargs = kwargs
        
        if kwargs.get("pyttsx3", None) is not None:
            self.tts_engine = pyttsx3.init()
            self.tts_provider = "pyttsx3"

        
        if kwargs.get("gtts", None) is not None:
            self.gtts_engine = gTTS
            self.language = kwargs.get("language", "en")
            self.file_output_path = kwargs.get("file_output_path", "tmp/output.mp3")  # Default path

            self.tts_provider = "gTTS"

    def run(self, **kwargs):
        match self.tts_provider:
            case "pyttsx3":
                return self.run_pyttsx3(kwargs.get("data", ""))
            case "gTTS":
                return self.run_gtts(kwargs.get("data", ""))
            case _:
                raise ValueError("Invalid TTS provider")
            
    def run_pyttsx3(self, text):
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return {"status": "success", "audio": True}
        except Exception as e:
            self.logger.error(f"pyttsx3 error: {str(e)}")
            raise
        
    def run_gtts(self, text):
        try:
            tts = self.gtts_engine(text=text, lang=self.language)
            tts.save(self.file_output_path)
            playsound.playsound(self.file_output_path)
        except Exception as e:
            self.logger.error(f"gTTS error: {str(e)}")
            raise