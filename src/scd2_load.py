import json
import os
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values

if Path("/opt/airflow/project_src").exists():
    DATA_FILE = Path("/opt/airflow/project_raw/hcpcs_transformed.json")
else:
    DATA_FILE = Path(__file__).resolve().parent.parent / "raw" / "hcpcs_transformed.json"

DB_CONFIG = {
    "host": "host.docker.internal",
    "port": 5432,
    "database": "hcpcs_db",
    "user": "postgres",
    "password": os.environ["HCPCS_DB_PASSWORD"]
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

    with psycopg2.connect(**DB_CONFIG) as connection:
        with connection.cursor() as cursor:

            # Stage the incoming snapshot
            cursor.execute("""
                CREATE TEMP TABLE stg_hcpcs (
                    hcpcs_code VARCHAR(50),
                    group_code VARCHAR(10),
                    long_description TEXT,
                    desc_hash CHAR(64)
                ) ON COMMIT DROP;
            """)

            execute_values(
                cursor,
                """
                INSERT INTO stg_hcpcs
                (hcpcs_code, group_code, long_description, desc_hash)
                VALUES %s
                """,
                rows,
                page_size=1000
            )

            # Expire current records whose description hash changed
            cursor.execute("""
                UPDATE hcpcs_codes AS target
                SET
                    is_current = FALSE,
                    end_date = CURRENT_DATE - 1
                FROM stg_hcpcs AS source
                WHERE target.hcpcs_code = source.hcpcs_code
                  AND target.is_current = TRUE
                  AND target.desc_hash <> source.desc_hash;
            """)

            expired_count = cursor.rowcount

            # Insert new codes and changed versions
            cursor.execute("""
                INSERT INTO hcpcs_codes (
                    hcpcs_code,
                    group_code,
                    long_description,
                    desc_hash,
                    effective_date,
                    end_date,
                    is_current,
                    version
                )
                SELECT
                    source.hcpcs_code,
                    source.group_code,
                    source.long_description,
                    source.desc_hash,
                    CURRENT_DATE,
                    NULL,
                    TRUE,
                    COALESCE(history.max_version, 0) + 1
                FROM stg_hcpcs AS source
                LEFT JOIN (
                    SELECT hcpcs_code, MAX(version) AS max_version
                    FROM hcpcs_codes
                    GROUP BY hcpcs_code
                ) AS history
                  ON history.hcpcs_code = source.hcpcs_code
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM hcpcs_codes AS target
                    WHERE target.hcpcs_code = source.hcpcs_code
                      AND target.is_current = TRUE
                      AND target.desc_hash = source.desc_hash
                );
            """)

            inserted_count = cursor.rowcount

    print("Changed versions expired:", expired_count)
    print("New/current versions inserted:", inserted_count)


if __name__ == "__main__":
    main()