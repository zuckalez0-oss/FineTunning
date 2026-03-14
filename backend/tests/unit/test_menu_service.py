from app.application.services.menu_service import MenuService


def test_main_menu_contains_required_actions() -> None:
    items = MenuService().build_main_menu()
    actions = [item.action for item in items]

    assert "create_prompt" in actions
    assert "manage_reference_prompts" in actions
    assert "manage_personas" in actions
    assert "exit" in actions
