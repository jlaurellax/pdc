import json
from pathlib import Path
from dataclasses import dataclass, asdict, field
from datetime import datetime
import uuid
import typer

app = typer.Typer()

DB_FILE = Path("journal.json")
DB_FILE.touch(exist_ok=True)


@dataclass(slots=True)
class JournalEntry:

    title: str
    content: str
    date: str
    tags: list[str] = field(default_factory=list)
    uuid: str = field(default_factory=lambda: uuid.uuid4().hex)


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
                    tags=entry.get("tags", []),
                    uuid=entry.get("uuid", uuid.uuid4().hex),
                )
                for entry in data
                if isinstance(entry, dict)
            ]
    except json.JSONDecodeError:
        return []


def save_entries(entries: list[JournalEntry]) -> None:
    """Save journal entries to the JSON file."""

    try:
        with open(DB_FILE, "w") as f:
            json.dump([asdict(entry) for entry in entries], f, indent=4)

    except IOError as error:
        print(f"Failed to save entries: {error}.")


@app.command(name="add")
def add_entry(title: str, content: str) -> None:
    """Create and save a new journal entry or update an entry with a UUID."""
    entries = load_entries()
    tags_input = input("Tags (comma separated, optional): ")
    parsed_tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = JournalEntry(title=title, content=content, date=now)
    entries.append(entry)
    save_entries(entries)
    print(f"✅ Entry added with UUID: {entry.uuid}")


@app.command(name="list")
def list_entries() -> None:
    """Print all journal entries."""

    entries = load_entries()
    if not entries:
        print("No journal entries found.")
        return

    for entry in entries:
        print(f"{entry.date}")
        print(f"{entry.title}")
        print(entry.content)
        print(f"This is the uuid for the entry: {entry.uuid}.")
        print("-" * 40)


@app.command(name="delete")
def delete_entries(uuid: str) -> None:
    """Find the entry with the given UUID and remove it."""
    entries = load_entries()
    updated_entries = [entry for entry in entries if entry.uuid != uuid]

    # If no entries were deleted, print a message
    if len(updated_entries) == len(entries):
        print(f"No entry found with UUID: {uuid}")
    else:
        # Save the updated entries back to the file
        save_entries(updated_entries)
        print(f"Entry with UUID {uuid} has been deleted.")


if __name__ == "__main__":
    # quick interactive program (entry point) to validate the above

    title = input("Title: ")
    content = input("Content: ")
    add_entry(title, content)
    print("✅ Entry saved.")
    print("\n📘 Your Journal:")
    list_entries()
