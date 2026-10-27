import json
import time
from pathlib import Path

import requests

URL = "https://api.nhtsa.gov/complaints/complaintsByVehicle"
RAW_DIR = Path("data/raw")

VEHICLES = [
    ("honda", "civic", 2018),
    ("toyota", "corolla", 2018),
    ("toyota", "camry", 2018),
    ("honda", "cr-v", 2018),
    ("toyota", "rav4", 2018),
]


def fetch_complaints(make, model, year, max_retries=3):
    params = {"make": make, "model": model, "modelYear": year}
    for attempt in range(1, max_retries + 1):
        try:
            r = requests.get(URL, params=params, timeout=30)
            r.raise_for_status()
            return r.json()["results"]
        except requests.RequestException as e:
            print(f"  attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
    print(f"  giving up on {year} {make} {model}")
    return []


RAW_DIR.mkdir(parents=True, exist_ok=True)

for make, model, year in VEHICLES:
    results = fetch_complaints(make, model, year)
    out_file = RAW_DIR / f"{make}_{model}_{year}.json"
    out_file.write_text(json.dumps(results, indent=2))
    print(f"{year} {make} {model}: {len(results)} complaints -> {out_file}")
    time.sleep(1)
