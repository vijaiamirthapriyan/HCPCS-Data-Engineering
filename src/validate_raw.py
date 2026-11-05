import json
from pathlib import Path
from collections import Counter


def main():
    raw_file = Path("/opt/airflow/project_raw/hcpcs_raw.json")

    with raw_file.open("r", encoding="utf-8") as file:
        records = json.load(file)

    codes = [record["hcpcs_code"] for record in records]
    duplicates = [
        code for code, count in Counter(codes).items()
        if count > 1
    ]

    missing_code = sum(
        1 for record in records
        if not record.get("hcpcs_code")
    )

    missing_description = sum(
        1 for record in records
        if not record.get("long_description")
    )

    print("Total records:", len(records))
    print("Unique HCPCS codes:", len(set(codes)))
    print("Duplicate codes:", len(duplicates))
    print("Missing codes:", missing_code)
    print("Missing descriptions:", missing_description)
    print("Sample record:", records[0])


if __name__ == "__main__":
    main()