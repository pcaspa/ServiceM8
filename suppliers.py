# export_servicem8_suppliers.py
import requests, csv, sys

API_KEY = ""
BASE = "https://api.servicem8.com/api_1.0/supplier.json"
HEADERS = {"X-API-Key": API_KEY}
OUT = "servicem8_suppliers.csv"

def fetch_all():
    cursor = "-1"; rows = []
    while cursor:
        r = requests.get(f"{BASE}?cursor={cursor}", headers=HEADERS, timeout=30)
        if r.status_code == 400 and "requires addon activation" in r.text:
            sys.exit("Suppliers add-on is OFF. Enable it in Settings → ServiceM8 Add-ons, then retry.")
        if r.status_code == 403:
            sys.exit("API key lacks supplier read permission (read_suppliers). Use a key with access.")
        if r.status_code != 200:
            sys.exit(f"HTTP {r.status_code}: {r.text}")
        rows.extend(r.json())
        cursor = r.headers.get("x-next-cursor")
    return rows

def to_csv(rows):
    if not rows:
        print("No suppliers found."); return
    cols = sorted({k for r in rows for k in r.keys()})
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print(f"Exported {len(rows)} suppliers -> {OUT}")

if __name__ == "__main__":
    to_csv(fetch_all())
