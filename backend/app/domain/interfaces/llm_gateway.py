from typing import Protocol


class LlmGateway(Protocol):
    def generate_text(self, prompt: str) -> str: ...
