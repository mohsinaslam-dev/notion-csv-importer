# Notion CSV Importer

**Platform:** Notion API

Imports CSV rows into a Notion database. A JSON mapping chooses the property type per column (title, rich_text, number, select, date, checkbox, url).

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # then fill in your values
```
Environment variables: NOTION_TOKEN, NOTION_DATABASE_ID (share the database with your integration)

Load them before running (for example `export $(grep -v '^#' .env | xargs)` on Linux/macOS, or set them in your shell on Windows).

## Usage
```bash
python app.py tasks.sample.csv --mapping mapping.sample.json --dry-run
python app.py tasks.csv --mapping mapping.json
```
Use `--dry-run` where available to see what would happen without calling the real API.

## Tests
The core logic is covered by tests that need no internet or credentials:
```bash
pip install pytest && pytest
```

## License
MIT
