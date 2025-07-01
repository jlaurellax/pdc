import json
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime


DB_FILE = Path("journal.json")
DB_FILE.touch(exist_ok=True)


@dataclass(slots=True)
class JournalEntry:

    title: str
    content: str
    date: str


def load_entries() -> list[JournalEntry]:
    """Load journal entries from the JSON file."""

    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            return [
                JournalEntry(
                    title=entry.get("title", "Untitled"),
                    content=entry.get("content", ""),
                    date=entry.get("date", "Unknown date"),
                )
                for entry in data
                if isinstance(entry, dict)  # extra safety
            ]
    except json.JSONDecodeError:
        return []


def save_entries(entries: list[JournalEntry]) -> None:
    """Save journal entries to the JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump([asdict(entry) for entry in entries], f, indent=4)


def add_entry(title: str, content: str) -> None:
    """Create and save a new journal entry."""
    entries = load_entries()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = JournalEntry(title=title, content=content, date=now)
    entries.append(entry)
    save_entries(entries)


def list_entries(entries: list[JournalEntry]) -> None:
    """Print all journal entries."""
    if not entries:
        print("No journal entries found.")
        return

    for entry in entries:
        print(f"{entry.date}")
        print(f"{entry.title}")
        print(entry.content)
        print("-" * 40)


if __name__ == "__main__":
    # quick interactive program (entry point) to validate the above
    title = input("Title: ")
    content = input("Content: ")
    add_entry(title, content)
    print("✅ Entry saved.")
    print("\n📘 Your Journal:")
    list_entries(load_entries())
