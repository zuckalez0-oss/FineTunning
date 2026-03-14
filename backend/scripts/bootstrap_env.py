from pathlib import Path


def main() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    example_path = Path(__file__).resolve().parents[1] / ".env.example"
    if env_path.exists():
        print(".env already exists.")
        return

    env_path.write_text(example_path.read_text(encoding="utf-8"), encoding="utf-8")
    print("Created .env from .env.example")


if __name__ == "__main__":
    main()
