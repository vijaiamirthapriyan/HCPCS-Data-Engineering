import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

if Path("/opt/airflow/project_src").exists():
    RAW_DIR = Path("/opt/airflow/project_raw")
else:
    RAW_DIR = Path(__file__).resolve().parent.parent / "raw"

RAW_FILE = RAW_DIR / "hcpcs_raw.json"
PROCESSED_FILE = RAW_DIR / "hcpcs_transformed.json"

def create_description_hash(description):
    normalized_description = " ".join(description.strip().split()).lower()
    return hashlib.sha256(
        normalized_description.encode("utf-8")
    ).hexdigest()


def transform_records(records):
    transformed_records = []

    for record in records:
        code = record["hcpcs_code"].strip().upper()
        group_code = record["group_code"].strip().upper()
        description = " ".join(
            record["long_description"].strip().split()
        )

        transformed_records.append({
            "hcpcs_code": code,
            "group_code": group_code,
            "long_description": description,
            "desc_hash": create_description_hash(description),
            "processed_at": datetime.now(timezone.utc).isoformat()
        })

    return transformed_records


def main():
    with RAW_FILE.open("r", encoding="utf-8") as file:
        raw_records = json.load(file)

    transformed_records = transform_records(raw_records)

    with PROCESSED_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            transformed_records,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("Raw records:", len(raw_records))
    print("Transformed records:", len(transformed_records))
    print("Output file:", PROCESSED_FILE)
    print("Sample transformed record:")
    print(json.dumps(transformed_records[0], indent=2))


if __name__ == "__main__":
    main()