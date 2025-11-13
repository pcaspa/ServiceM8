import requests
import csv
import os

# === CONFIG ===
API_KEY = ""  # ServiceM8 → Settings → API Keys (read access required)
BASE_URL = "https://api.servicem8.com/api_1.0/company.json"
OUTPUT_FILE = "servicem8_companies.csv"
HEADERS = {"X-API-Key": API_KEY}

def fetch_all_companies():
    cursor = "-1"
    all_companies = []

    while cursor:
        print(f"Fetching page with cursor: {cursor}")
        r = requests.get(f"{BASE_URL}?cursor={cursor}", headers=HEADERS, timeout=30)
        if r.status_code != 200:
            raise SystemExit(f"company.json -> HTTP {r.status_code}: {r.text}")

        batch = r.json()
        all_companies.extend(batch)
        cursor = r.headers.get("x-next-cursor")  # Continue until None

    print(f"✅ Total companies fetched: {len(all_companies)}")
    return all_companies

def save_to_csv(records):
    if not records:
        print("No company data found.")
        return

    fieldnames = sorted({k for record in records for k in record.keys()})

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"💾 Exported {len(records)} companies → {OUTPUT_FILE}")

if __name__ == "__main__":
    companies = fetch_all_companies()
    save_to_csv(companies)
