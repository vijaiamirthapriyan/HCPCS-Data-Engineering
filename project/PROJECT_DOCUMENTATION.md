 
# HCPCS Project Documentation

## 1. Project Objective

Build an end-to-end data engineering pipeline for HCPCS code data, from source extraction through transformation, validation, database loading, and reporting.

## 2. Pipeline Components

### Data Extraction
- Collect HCPCS data from the source website.
- Save the extracted records as JSON in the `raw` folder.

### Data Validation
- Check that required fields are present.
- Verify that the raw data contains records before processing.

### Data Transformation
- Standardize and transform the extracted data.
- Generate a description hash and processing timestamp.
- Save transformed records as JSON.

### Data Quality
- Check required fields and non-empty values.
- Validate HCPCS code uniqueness.
- Confirm raw and transformed record counts match.

### Database Loading
- Load transformed records into PostgreSQL.
- Use SCD Type 2 logic to preserve historical changes.
- Maintain current and historical versions of records.

### Orchestration
- Use Apache Airflow to orchestrate the pipeline.
- Run tasks in sequence:
  1. Scrape HCPCS data
  2. Validate raw data
  3. Transform data
  4. Run data quality checks
  5. Load data into PostgreSQL

## 3. Technology Stack

- Python
- Apache Airflow
- Docker
- PostgreSQL
- SQL
- Power BI
- pytest

## 4. Testing

Automated tests are available in the `tests` folder.

Run tests from the project root:

```powershell
pytest -v
```

The current test suite validates file availability, record structure, required values, uniqueness, and record-count consistency.

## 5. Starting Airflow

From the `airflow` folder, run:

```powershell
docker compose up -d
```

Check container status:

```powershell
docker compose ps
```

Open the Airflow UI at:

`http://localhost:8080`

## 6. Project Outputs

- Raw HCPCS JSON data
- Transformed JSON data
- PostgreSQL table with current and historical records
- Power BI dashboard
- Automated test results

## 7. Security

- Store credentials in environment variables or `.env` files.
- Do not commit credentials or secrets to source control.
- Restrict access to database and cloud resources.

## 8. Future Improvements

- Add CI automation to run tests on code changes.
- Improve logging and failure notifications.
- Add monitoring for pipeline execution and data quality.
- Expand cloud deployment using GCP services.
