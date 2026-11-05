import json
import os
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values

project_dir = Path(__file__).resolve().parent.parent
data_file = project_dir / "raw" / "hcpcs_transformed.json"

with data_file.open("r", encoding="utf-8") as f:
    records = json.load(f)

rows = [(r["hcpcs_code"], r["category_name"]) for r in records]

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="hcpcs_db",
    user="postgres",
    password=os.environ["HCPCS_DB_PASSWORD"]
)

try:
    with conn:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """
                UPDATE hcpcs_codes AS t
                SET category_name = v.category_name
                FROM (VALUES %s) AS v(hcpcs_code, category_name)
                WHERE t.hcpcs_code = v.hcpcs_code
                  AND t.is_current = TRUE
                """,
                rows,
                page_size=1000
            )
    print(f"Updated category names for {len(rows)} current codes.")
finally:
    conn.close()
