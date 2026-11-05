from pathlib import Path
import json


def test_raw_data_file_exists():
    raw_file = Path("raw/hcpcs_raw.json")
    assert raw_file.exists(), f"Raw data file not found: {raw_file}"


def test_transformed_data_file_exists():
    transformed_file = Path("raw/hcpcs_transformed.json")
    assert transformed_file.exists(), f"Transformed data file not found: {transformed_file}"


def test_raw_data_file_contains_records():
    raw_file = Path("raw/hcpcs_raw.json")

    with raw_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) > 0, "Raw HCPCS data file is empty"


def test_raw_records_have_required_fields():
    raw_file = Path("raw/hcpcs_raw.json")

    with raw_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    required_fields = {"hcpcs_code", "group_code", "long_description"}

    for record in data:
        assert required_fields.issubset(record.keys())


def test_transformed_records_have_required_fields():
    transformed_file = Path("raw/hcpcs_transformed.json")

    with transformed_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    required_fields = {
        "hcpcs_code",
        "group_code",
        "category_name",
        "long_description",
        "desc_hash",
        "processed_at",
    }

    for record in data:
        assert required_fields.issubset(record.keys())


def test_hcpcs_codes_are_not_empty():
    raw_file = Path("raw/hcpcs_raw.json")

    with raw_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    for record in data:
        assert record["hcpcs_code"], "HCPCS code is empty"

def test_hcpcs_codes_are_unique():
    raw_file = Path("raw/hcpcs_raw.json")

    with raw_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    codes = [record["hcpcs_code"] for record in data]

    assert len(codes) == len(set(codes)), "Duplicate HCPCS codes found"

def test_category_names_are_not_empty():
    transformed_file = Path("raw/hcpcs_transformed.json")

    with transformed_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    for record in data:
        assert record["category_name"], "Category name is empty"

def test_descriptions_are_not_empty():
    transformed_file = Path("raw/hcpcs_transformed.json")

    with transformed_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    for record in data:
        assert record["long_description"], "Description is empty"

def test_description_hashes_are_not_empty():
    transformed_file = Path("raw/hcpcs_transformed.json")

    with transformed_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    for record in data:
        assert record["desc_hash"], "Description hash is empty"

def test_processed_timestamps_are_not_empty():
    transformed_file = Path("raw/hcpcs_transformed.json")

    with transformed_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    for record in data:
        assert record["processed_at"], "Processed timestamp is empty"

def test_raw_and_transformed_record_counts_match():
    raw_file = Path("raw/hcpcs_raw.json")
    transformed_file = Path("raw/hcpcs_transformed.json")

    with raw_file.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    with transformed_file.open("r", encoding="utf-8") as file:
        transformed_data = json.load(file)

    assert len(raw_data) == len(transformed_data), (
        "Raw and transformed record counts do not match"
    )

