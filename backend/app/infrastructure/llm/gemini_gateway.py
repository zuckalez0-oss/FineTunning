from google import genai

from app.core.config import get_settings
from app.core.exceptions import ConfigurationError


class GeminiGateway:
    def __init__(self) -> None:
        self.settings = get_settings()

    def generate_text(self, prompt: str) -> str:
        if not self.settings.gemini_api_key:
            raise ConfigurationError("GEMINI_API_KEY must be configured.")

        client = genai.Client(api_key=self.settings.gemini_api_key)
        response = client.models.generate_content(
            model=self.settings.default_llm_model,
            contents=prompt,
        )
        return response.text
