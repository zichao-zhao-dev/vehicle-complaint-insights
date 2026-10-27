# Vehicle Complaint Insights

A small end-to-end data pipeline that pulls vehicle safety complaints from NHTSA's public API, loads them into SQLite, and uses SQL to find what goes wrong with five popular 2018 models.

## Why

In grad school I cleaned and categorized an auto body shop's repair records by hand with SQL and Python. This project rebuilds that kind of work as an automated, reproducible pipeline on public data.

## Pipeline

    fetch.py  ->  load.py  ->  split_components.py  ->  analysis.sql
    extract       load         transform                report

- **fetch.py** calls the NHTSA complaints API for each vehicle, with a timeout, retries with exponential backoff, and a pause between requests. Raw JSON is saved to disk.
- **load.py** normalizes dates to ISO 8601 and loads everything into SQLite with parameterized queries. A composite primary key plus `INSERT OR IGNORE` makes it idempotent: rerunning inserts nothing new.
- **split_components.py** transforms the multi-label `components` field inside the database into a junction table, one row per complaint and component.
- **analysis.sql** holds every analysis query; the output goes to `reports/summary.txt`.

Run everything with one command:

    python -m pip install -r requirements.txt
    ./run.sh

## Findings (data pulled October 2026, 3,976 complaints)

- **Each model's problems are concentrated and different.** Steering leads for the Civic, electrical for the RAV4, airbags for the Corolla, and engine for the CR-V.
- **Volume is not severity.** The CR-V has by far the most complaints but the lowest crash (2.1%) and fire (0.1%) rates; most are reliability issues.
- **The RAV4's fire rate (9.9%) is about ten times the others.** About 70% of its fire complaints are tagged Electrical System.
- **Complaints peaked in 2024, six years after launch.** Both Hondas spiked that year in "FUEL SYSTEM, GASOLINE" while the Toyotas didn't, matching Honda's expanded fuel-pump recall for 2018-2020 models, announced to owners in early 2024. Complaint volume tracks awareness, not just failures.

## Data quality notes

- Some NHTSA component names contain commas themselves (e.g. "SERVICE BRAKES, HYDRAULIC"). A naive split silently broke over 400 rows into fragments; a row-count sanity check caught it, and the split now breaks only on commas not followed by a space.
- Child-seat part lists use the opposite convention and stay merged. This affects 3 complaints and is left as is.
- NHTSA renamed some categories over time (e.g. "ENGINE" vs "ENGINE AND ENGINE COOLING"); they are not merged here.
- The Civic shows zero complaints filed in 2026 so far, which looks unusual and is not yet explained.

## Limitations

- Raw counts aren't comparable across models without sales volume, so comparisons focus on rates and category mix.
- Complaints are self-reported, so they reflect people who chose to file, not all owners.
- Small samples (the Corolla has 135 complaints) make percentages noisy.
