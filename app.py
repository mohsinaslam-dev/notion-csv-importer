"""Import a CSV into a Notion database. A JSON mapping says which column becomes which property type."""
import argparse
import csv
import json
import os
import time

import requests


def build_properties(row, mapping):
    props = {}
    for col, kind in mapping.items():
        v = (row.get(col) or "").strip()
        if kind == "title":
            props[col] = {"title": [{"text": {"content": v}}]}
        elif not v:
            continue
        elif kind == "rich_text":
            props[col] = {"rich_text": [{"text": {"content": v}}]}
        elif kind == "number":
            props[col] = {"number": float(v)}
        elif kind == "select":
            props[col] = {"select": {"name": v}}
        elif kind == "date":
            props[col] = {"date": {"start": v}}
        elif kind == "checkbox":
            props[col] = {"checkbox": v.lower() in ("1", "true", "yes", "y")}
        elif kind == "url":
            props[col] = {"url": v}
        else:
            raise ValueError(f"unsupported type {kind!r} for column {col!r}")
    return props


def create_page(token, db_id, props):
    r = requests.post("https://api.notion.com/v1/pages", timeout=20,
                      headers={"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28"},
                      json={"parent": {"database_id": db_id}, "properties": props})
    r.raise_for_status()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv_file")
    p.add_argument("--mapping", required=True, help='JSON file, e.g. {"Name":"title","Priority":"number"}')
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    mapping = json.load(open(a.mapping, encoding="utf-8"))
    token, db = os.environ.get("NOTION_TOKEN"), os.environ.get("NOTION_DATABASE_ID")
    if not a.dry_run and not (token and db):
        raise SystemExit("Set NOTION_TOKEN and NOTION_DATABASE_ID (or use --dry-run)")
    n = 0
    with open(a.csv_file, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            props = build_properties(row, mapping)
            if a.dry_run:
                print(json.dumps(props)[:120])
            else:
                create_page(token, db, props)
                time.sleep(0.35)  # Notion allows ~3 requests/second
            n += 1
    print(f"imported {n} row(s)")


if __name__ == "__main__":
    main()
