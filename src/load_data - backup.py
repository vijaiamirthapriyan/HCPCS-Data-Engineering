import json
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "raw" / "hcpcs_transformed.json"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "hcpcs_db",
    "user": "postgres",
    "password": "Vijai@2212"
}


def main():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        records = json.load(file)

    rows = [
        (
            record["hcpcs_code"],
            record["group_code"],
            record["long_description"],
            record["desc_hash"]
        )
        for record in records
    ]

    insert_sql = """
        INSERT INTO hcpcs_codes (
            hcpcs_code,
            group_code,
            long_description,
            desc_hash
        )
        VALUES %s
    """

    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:
            execute_values(cursor, insert_sql, rows, page_size=1000)

    print(f"Successfully loaded {len(rows)} records into hcpcs_codes")


if __name__ == "__main__":
    main()