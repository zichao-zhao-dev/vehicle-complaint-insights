import json
import sqlite3
from datetime import datetime
from pathlib import Path

RAW_DIR = Path("data/raw")
DB_PATH = Path("data/complaints.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS complaints (
    odi_number     INTEGER NOT NULL,
    make           TEXT    NOT NULL,
    model          TEXT    NOT NULL,
    model_year     INTEGER NOT NULL,
    crash          INTEGER,
    fire           INTEGER,
    injuries       INTEGER,
    deaths         INTEGER,
    incident_date  TEXT,
    filed_date     TEXT,
    components     TEXT,
    summary        TEXT,
    PRIMARY KEY (odi_number, make, model, model_year)
);
"""


def to_iso(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


conn = sqlite3.connect(DB_PATH)
conn.execute(SCHEMA)

for path in sorted(RAW_DIR.glob("*.json")):
    make, model, year = path.stem.split("_")
    records = json.loads(path.read_text())
    rows = [
        (
            rec["odiNumber"], make, model, int(year),
            int(rec["crash"]), int(rec["fire"]),
            rec["numberOfInjuries"], rec["numberOfDeaths"],
            to_iso(rec.get("dateOfIncident")),
            to_iso(rec.get("dateComplaintFiled")),
            rec.get("components"), rec.get("summary"),
        )
        for rec in records
    ]
    before = conn.total_changes
    conn.executemany(
        "INSERT OR IGNORE INTO complaints VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        rows,
    )
    inserted = conn.total_changes - before
    print(f"{path.name}: {len(rows)} records, {inserted} inserted")

conn.commit()
total = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
print(f"Total rows in database: {total}")
conn.close()
