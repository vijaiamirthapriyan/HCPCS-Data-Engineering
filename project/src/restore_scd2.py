import psycopg2

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
            # Expire the temporary test version
            cur.execute("""
                UPDATE hcpcs_codes
                SET is_current = FALSE,
                    end_date = CURRENT_DATE
                WHERE hcpcs_code = 'A0021'
                  AND is_current = TRUE
                  AND long_description LIKE '%SCD2 TEST%'
            """)

            # Restore the original description as the current version
            cur.execute("""
                INSERT INTO hcpcs_codes (
                    hcpcs_code, group_code, category_name,
                    long_description, desc_hash,
                    effective_date, is_current, version
                )
                SELECT
                    hcpcs_code, group_code, category_name,
                    'Ambulance service, outside state per mile, transport (medicaid only)',
                    desc_hash,
                    CURRENT_DATE, TRUE, 3
                FROM hcpcs_codes
                WHERE hcpcs_code = 'A0021'
                  AND version = 1
            """)

    print("Original A0021 description restored as version 3.")

finally:
    conn.close()