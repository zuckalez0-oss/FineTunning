import typer

from app.application.services.menu_service import MenuService

app = typer.Typer(help="PromptMaster CLI")


@app.command()
def menu() -> None:
    service = MenuService()
    typer.echo("PromptMaster CLI")
    typer.echo("================")
    for option in service.build_main_menu():
        typer.echo(f"[{option.key}] {option.label}")


if __name__ == "__main__":
    app()
