import hashlib
import json
import psycopg2
from psycopg2.extras import execute_values

# Read the original transformed data
with open("raw/hcpcs_transformed.json", "r", encoding="utf-8") as file:
    records = json.load(file)

# Find A0021 and make a temporary description change in memory
record = next(row for row in records if row["hcpcs_code"] == "A0021")

original_description = record["long_description"]
test_description = original_description + " - SCD2 TEST"

record["long_description"] = test_description
record["desc_hash"] = hashlib.sha256(
    test_description.encode("utf-8")
).hexdigest()

# Update these connection details to match your local setup.
# Do not share your password here.
conn = psycopg2.connect(
    host="localhost",
    database="hcpcs_db",
    user="postgres",
    password="Vijai@2212",
    port=5432
)

try:
    with conn:
        with conn.cursor() as cur:
            # Expire the existing current version
            cur.execute("""
                UPDATE hcpcs_codes
                SET is_current = FALSE,
                    end_date = CURRENT_DATE
                WHERE hcpcs_code = %s
                  AND is_current = TRUE
                  AND desc_hash <> %s
            """, (record["hcpcs_code"], record["desc_hash"]))

            # Insert the changed description as a new version
            cur.execute("""
                INSERT INTO hcpcs_codes (
                    hcpcs_code, group_code, category_name,
                    long_description, desc_hash,
                    effective_date, is_current, version
                )
                SELECT %s, %s, %s, %s, %s,
                       CURRENT_DATE, TRUE,
                       COALESCE(MAX(version), 0) + 1
                FROM hcpcs_codes
                WHERE hcpcs_code = %s
            """, (
                record["hcpcs_code"],
                record.get("group_code"),
                record.get("category_name"),
                record["long_description"],
                record["desc_hash"],
                record["hcpcs_code"]
            ))

            cur.execute("""
                SELECT hcpcs_code, version, is_current,
                       effective_date, end_date, long_description
                FROM hcpcs_codes
                WHERE hcpcs_code = 'A0021'
                ORDER BY version
            """)

            for row in cur.fetchall():
                print(row)

    print("Test completed. The test version is saved in the database.")

finally:
    conn.close()