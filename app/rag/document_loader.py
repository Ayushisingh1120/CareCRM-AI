from pathlib import Path


def load_markdown(file_path: str) -> str:
    """
    Load a Markdown file and return its contents as text.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    return path.read_text(
        encoding="utf-8"
    )