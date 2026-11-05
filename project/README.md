# HCPCS Data Engineering Project

## Overview
This project builds an end-to-end data pipeline to collect, validate, transform, and load HCPCS code data into PostgreSQL. It also includes an Airflow workflow, data quality checks, SCD Type 2 history tracking, automated tests, and a Power BI dashboard.

## Architecture
Source Data → Scraping → Raw JSON → Validation → Transformation → Data Quality Checks → PostgreSQL → Power BI

## Technologies
- Python
- Apache Airflow
- Docker
- PostgreSQL
- SQL
- Power BI
- pytest

## Project Structure
- `airflow/dags/` – Airflow DAGs
- `src/` – Pipeline source code
- `raw/` – Raw and transformed JSON files
- `tests/` – Pipeline tests
- `HCPCS_Dashboard.pbix` – Power BI dashboard
- `requirements.txt` – Python dependencies

## Pipeline Workflow
1. Scrape HCPCS data.
2. Validate the raw data.
3. Transform and standardize records.
4. Run data quality checks.
5. Load data into PostgreSQL using SCD Type 2 logic.
6. Visualize data in Power BI.

## Data Quality and Testing
The pipeline includes checks for required fields, non-empty values, unique HCPCS codes, and matching raw and transformed record counts.

Automated tests are implemented using pytest.

## Running the Project
1. Install dependencies using `pip install -r requirements.txt`.
2. Start Airflow from the `airflow` directory using Docker Compose.
3. Trigger the HCPCS pipeline from the Airflow UI.
4. Review the loaded data in PostgreSQL.
5. Open the Power BI dashboard to explore the results.

## Security
Sensitive credentials should be stored in environment variables or `.env` files and not committed to version control.

## Author
Data Engineering Project