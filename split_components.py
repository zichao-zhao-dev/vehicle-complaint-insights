import re
import sqlite3
from pathlib import Path

DB_PATH = Path("data/complaints.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS complaint_components (
    odi_number INTEGER NOT NULL,
    component  TEXT    NOT NULL,
    PRIMARY KEY (odi_number, component)
)
"""

conn = sqlite3.connect(DB_PATH)
conn.execute("DROP TABLE IF EXISTS complaint_components")
conn.execute(SCHEMA)

pairs = []
for odi_number, components in conn.execute(
    "SELECT odi_number, components FROM complaints"
):
    if not components:
        continue
    for part in re.split(r",(?! )", components):
        part = part.strip()
        if part:
            pairs.append((odi_number, part))

before = conn.total_changes
conn.executemany(
    "INSERT OR IGNORE INTO complaint_components (odi_number, component) VALUES (?, ?)",
    pairs,
)
inserted = conn.total_changes - before
conn.commit()

total = conn.execute("SELECT COUNT(*) FROM complaint_components").fetchone()[0]
print(f"{len(pairs)} pairs found, {inserted} inserted")
print(f"Total rows in complaint_components: {total}")
conn.close()
