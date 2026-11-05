import os
import psycopg2


def main():
    conn = psycopg2.connect(
        host="localhost",
        database="hcpcs_db",
        user="postgres",
        password=os.environ["HCPCS_DB_PASSWORD"],
        port=5432
    )

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*) AS total_versions,
                    COUNT(*) FILTER (WHERE is_current = TRUE) AS current_records,
                    COUNT(*) FILTER (WHERE is_current = FALSE) AS historical_records,
                    MAX(inserted_at) AS latest_load_time
                FROM hcpcs_codes;
            """)

            result = cur.fetchone()

            print("HCPCS Warehouse Report")
            print("----------------------")
            print("Total versions:", result[0])
            print("Current records:", result[1])
            print("Historical records:", result[2])
            print("Latest load time:", result[3])

    finally:
        conn.close()


if __name__ == "__main__":
    main()