# export_servicem8_materials.py
import requests, csv, os

API_KEY   = ""  # ServiceM8 → Settings → API Keys (must allow read of Job Materials)
BASE_URL  = "https://api.servicem8.com/api_1.0/jobmaterial.json"
OUT_FILE  = "servicem8_materials.csv"
HEADERS   = {"X-API-Key": API_KEY}

def fetch_all_materials():
    cursor = "-1"
    rows = []
    while cursor:
        r = requests.get(f"{BASE_URL}?cursor={cursor}", headers=HEADERS, timeout=30)
        if r.status_code != 200:
            raise SystemExit(f"jobmaterial.json -> HTTP {r.status_code}: {r.text}")
        batch = r.json()
        rows.extend(batch)
        cursor = r.headers.get("x-next-cursor")
    return rows

def write_csv(rows, path):
    if not rows:
        open(path, "w", encoding="utf-8").close()
        print("No materials found."); return
    cols = sorted({k for row in rows for k in row.keys()})
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)
    print(f"Exported {len(rows)} materials → {path}")

if __name__ == "__main__":
    materials = fetch_all_materials()
    write_csv(materials, OUT_FILE)
