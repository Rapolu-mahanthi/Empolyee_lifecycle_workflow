import argparse
import csv
import json
from pathlib import Path
from generator import validate

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data")
    args = parser.parse_args()
    directory = Path(args.data)
    names = ["departments", "roles", "managers", "employees", "onboarding_cases", "tasks", "dependencies", "access_roles", "access_grants", "assets", "offboarding_cases", "audit_events", "ground_truth"]
    tables = {name: read_csv(directory / f"{name}.csv") for name in names}
    result = validate(tables)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
