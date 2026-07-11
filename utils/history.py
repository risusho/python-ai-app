import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
HISTORY_FILE = DATA_DIR / "history.json"


def _ensure_file() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("[]", encoding="utf-8")


def load_history() -> list[dict]:
    _ensure_file()
    return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))


def add_history(category: str, input_summary: str, output_text: str) -> None:
    history = load_history()
    history.insert(
        0,
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "category": category,
            "input_summary": input_summary,
            "output_text": output_text,
        },
    )
    HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


def clear_history() -> None:
    _ensure_file()
    HISTORY_FILE.write_text("[]", encoding="utf-8")
