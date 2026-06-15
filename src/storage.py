import json
from pathlib import Path


INDEX_PATH = Path("data/index.json")
SCREENSHOT_DIR = Path("data/screenshots")

SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_index() -> list[dict]:
    if not INDEX_PATH.exists():
        return []

    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_index(records: list[dict]) -> None:
    with open(INDEX_PATH, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def save_uploaded_file(uploaded_file) -> str:
    file_path = SCREENSHOT_DIR / uploaded_file.name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return str(file_path)
