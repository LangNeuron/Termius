from google import genai
from core.loger import get_logger
import requests

class AiLLM:
    def __init__(self, signals, **kwargs):
        self.logger = get_logger()
        # Change on super.__init__(self, signals, **kwargs):
        self.signals = signals
        self.kwargs = kwargs

        if kwargs.get("google", None) is None:
            self.api_key = self.kwargs.get("google_api", "")
            self.model = self.kwargs.get("google_model", "gemini-2.0-flash")
            self.ai = "google"

        if kwargs.get("ollama", None) is not None:
            self.model = self.kwargs.get("model", "llama2-7b-chat")
            self.ollama_serve = self.kwargs.get("ollama_serve", "http://127.0.0.1:11434/api/generate")
            self.api_key = self.kwargs.get("ollama", False)
            self.ai = "ollama"

    def run_google(self, prompt):
        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(model=self.model, contents=prompt)
        self.logger.info(response.text)
        return response.text

    def run_ollama(self, prompt):
        headers = {"Content-Type": "application/json"}
        if self.api_key:  # Only add auth header if API key exists
            headers["Authorization"] = f"Bearer {self.api_key}"

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False  # for non-streaming response
        }

        try:
            response = requests.post(self.ollama_serve, headers=headers,
                                     json=data)
            response.raise_for_status()  # Raise HTTP errors
            result = response.json()
            self.logger.info(result.get("response", ""))
            return result.get("response")
        except Exception as e:
            self.logger.error(f"Ollama error: {str(e)}")
            raise



    def run(self, **kwargs):

        data = kwargs.get("data", "")

        if data == "":
            return None

        match self.ai:
            case "google":
                return self.run_google(data)
            case "ollama":
                return self.run_ollama(data)
            case _:
                raise ValueError("Invalid AI")
