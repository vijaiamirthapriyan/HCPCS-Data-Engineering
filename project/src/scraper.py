import json
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://hcpcsdata.com"
GROUPS_URL = f"{BASE_URL}/Codes"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    )
}

RAW_DIR = RAW_DIR = (
    Path("/opt/airflow/project_raw")
    if Path("/opt/airflow/project_src").exists()
    else Path(__file__).resolve().parent.parent / "raw"
)
RAW_DIR.mkdir(parents=True, exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)


def get_soup(url):
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_code_groups():
    soup = get_soup(GROUPS_URL)
    groups = []

    for link in soup.select("a[href^='/Codes/']"):
        href = link.get("href", "").strip()
        text = link.get_text(" ", strip=True)

        # Group links look like /Codes/A, /Codes/B, etc.
        parts = href.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "Codes":
            group_code = parts[1]
            if group_code.isalpha() and len(group_code) == 1:
                groups.append(group_code)

    return sorted(set(groups))


def scrape_group(group_code):
    url = f"{BASE_URL}/Codes/{group_code}"
    soup = get_soup(url)

    table = soup.find("table")
    if not table:
        print(f"No table found for group {group_code}")
        return []

    records = []

    for row in table.find_all("tr"):
        cells = row.find_all(["th", "td"])
        if len(cells) < 2:
            continue

        code = cells[0].get_text(" ", strip=True)
        description = cells[1].get_text(" ", strip=True)

        if code.lower() == "code":
            continue

        if code and description:
            records.append({
                "hcpcs_code": code,
                "group_code": group_code,
                "long_description": description
            })

    return records


def main():
    groups = get_code_groups()
    print("Groups found:", groups)

    all_records = []

    for group in groups:
        print(f"Scraping group {group}...")
        try:
            records = scrape_group(group)
            all_records.extend(records)
            print(f"  Records collected: {len(records)}")
            time.sleep(1)  # Be polite to the source website
        except requests.RequestException as error:
            print(f"  Failed group {group}: {error}")

    output_file = RAW_DIR / "hcpcs_raw.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(all_records, file, indent=2, ensure_ascii=False)

    print("\nTotal records:", len(all_records))
    print("Raw snapshot saved to:", output_file)


if __name__ == "__main__":
    main()