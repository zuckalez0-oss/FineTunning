class SummarizeContextUseCase:
    def execute(self, text: str) -> str:
        if len(text) <= 280:
            return text
        return f"{text[:277]}..."
