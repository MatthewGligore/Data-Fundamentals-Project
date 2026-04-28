import csv
from collections import Counter
from pathlib import Path


INPUT_CSV = Path("fema_disasters.csv")
SELECTED_CSV = Path("fema_selected_columns.csv")
GULF_STATES = {"TX", "LA", "MS", "AL", "FL"}


def print_columns(header: list[str]) -> None:
    print("\n1) Showing dataset columns")
    for idx, name in enumerate(header, start=1):
        print(f"{idx:>2}  {name}")


def write_selected_columns(rows: list[list[str]]) -> None:
    print(f"\n2) Extracting selected columns to {SELECTED_CSV}")
    with SELECTED_CSV.open("w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerows(rows)


def main() -> None:
    print("=== HW1 FEMA Analysis (Python Version) ===")

    if not INPUT_CSV.exists():
        print(f"Input file '{INPUT_CSV}' not found.")
        print("Download it with:")
        print("curl 'https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv' > fema_disasters.csv")
        raise SystemExit(1)

    with INPUT_CSV.open("r", newline="", encoding="utf-8") as in_file:
        reader = csv.reader(in_file)
        header = next(reader)
        rows = list(reader)

    print_columns(header)

    # Column indices are based on the original HW1 selection:
    # state(3), declarationType(4), fyDeclared(6), incidentType(7), designatedArea(20)
    selected_rows = [header[2], header[3], header[5], header[6], header[19]]
    extracted_rows = [selected_rows]
    for row in rows:
        extracted_rows.append([row[2], row[3], row[5], row[6], row[19]])
    write_selected_columns(extracted_rows)

    state_counter: Counter[str] = Counter()
    gulf_incident_counter: Counter[str] = Counter()

    for row in extracted_rows[1:]:
        state = row[0]
        incident_type = row[3]
        state_counter[state] += 1
        if state in GULF_STATES:
            gulf_incident_counter[incident_type] += 1

    print("\n3) Top 15 states by declaration count")
    for count, state in sorted(((v, k) for k, v in state_counter.items()), reverse=True)[:15]:
        print(f"{count:>6}  {state}")

    print("\n4) Incident counts for Gulf Coast states (TX, LA, MS, AL, FL)")
    for count, incident in sorted(((v, k) for k, v in gulf_incident_counter.items()), reverse=True):
        print(f"{count:>6}  {incident}")

    print(f"\nDone. Output file updated: {SELECTED_CSV}")


if __name__ == "__main__":
    main()
