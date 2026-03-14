from dataclasses import dataclass


@dataclass(frozen=True)
class MenuOption:
    key: str
    label: str
    action: str


class MenuService:
    def build_main_menu(self) -> list[MenuOption]:
        return [
            MenuOption(key="1", label="Criar Novo Prompt", action="create_prompt"),
            MenuOption(
                key="2",
                label="Gerenciar Prompts de Referencia",
                action="manage_reference_prompts",
            ),
            MenuOption(key="3", label="Gerenciar Personas", action="manage_personas"),
            MenuOption(key="0", label="Sair", action="exit"),
        ]
