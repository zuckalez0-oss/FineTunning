class TagDetectionService:
    def detect(self, idea: str, category: str | None = None) -> list[str]:
        seed_words = set((idea or "").lower().replace(",", " ").split())
        tags = []

        for candidate in ("frontend", "backend", "dados", "automacao", "marketing", "python"):
            if candidate in seed_words:
                tags.append(candidate)

        if category:
            tags.append(category.lower())

        return sorted(set(tags))
