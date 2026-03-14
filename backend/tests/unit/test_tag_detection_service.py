from app.application.services.tag_detection_service import TagDetectionService


def test_detects_tags_from_text_and_category() -> None:
    service = TagDetectionService()
    tags = service.detect("Projeto de frontend com python e automacao", category="Engineering")
    assert "frontend" in tags
    assert "python" in tags
    assert "engineering" in tags
