import json
import re
from pathlib import Path


if Path("/opt/airflow/project_src").exists():
    DATA_FILE = Path("/opt/airflow/project_raw/hcpcs_transformed.json")
else:
    DATA_FILE = (
        Path(__file__).resolve().parent.parent
        / "raw"
        / "hcpcs_transformed.json"
    )


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    if not records:
        raise ValueError("Data quality failed: dataset is empty")

    required_fields = ["hcpcs_code", "long_description"]
    seen_codes = set()
    errors = []

    for row_number, record in enumerate(records, start=1):
        for field in required_fields:
            if not record.get(field):
                errors.append(
                    f"Row {row_number}: missing {field}"
                )

        code = record.get("hcpcs_code")

        if code:
            if code in seen_codes:
                errors.append(
                    f"Row {row_number}: duplicate HCPCS code {code}"
                )
            seen_codes.add(code)

            if not re.fullmatch(r"[A-Z0-9]{5}", str(code)):
                errors.append(
                    f"Row {row_number}: invalid HCPCS code format {code}"
                )

    print("Total records:", len(records))
    print("Unique HCPCS codes:", len(seen_codes))
    print("Quality errors:", len(errors))

    if errors:
        for error in errors[:20]:
            print(error)

        raise ValueError(
            f"Data quality check failed with {len(errors)} error(s)"
        )

    print("Data quality checks passed.")


if __name__ == "__main__":
    main()
