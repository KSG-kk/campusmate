import json
from datetime import date, datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

calendar_events = json.loads((DATA_DIR / "calendar.json").read_text(encoding="utf-8"))
offices = json.loads((DATA_DIR / "offices.json").read_text(encoding="utf-8"))


def search_calendar_event(keyword: str) -> dict:
    matches = [e for e in calendar_events if keyword in e["name"] or keyword in e["description"]]
    return {"tool": "search_calendar_event", "input": keyword, "matches": matches[:5]}


def calculate_date_gap(start_date: str, end_date: str) -> dict:
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    return {"tool": "calculate_date_gap", "start_date": start_date, "end_date": end_date, "days": (end - start).days}


def lookup_office_hours(name: str) -> dict:
    for office_name, info in offices.items():
        if name in office_name or office_name in name:
            return {"tool": "lookup_office_hours", "office": office_name, **info}
    return {"tool": "lookup_office_hours", "office": name, "error": "没有找到该部门"}


def today_iso() -> str:
    return date.today().isoformat()
