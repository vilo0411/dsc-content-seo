"""
Fetch Google Search Console data via API and cache to CSV.

Usage:
    python scripts/sync_gsc.py              # fetch 30 days, skip if cache < 7 days
    python scripts/sync_gsc.py --days=90   # fetch 90 days
    python scripts/sync_gsc.py --force     # ignore cache TTL
    python scripts/sync_gsc.py --site https://www.dsc.com.vn/
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

CREDENTIALS_PATH = Path(".antigravity/config/gsc-credentials.json")
TOKEN_PATH = Path(".antigravity/config/gsc-token.json")
CACHE_DIR = Path("knowledge/raw/gsc")
QUERIES_CSV = CACHE_DIR / "queries.csv"
PAGES_CSV = CACHE_DIR / "pages.csv"
META_FILE = CACHE_DIR / "cache-meta.json"

CACHE_TTL_HOURS = 168  # 7 days
DEFAULT_SITE = os.environ.get("GSC_SITE", "https://www.dsc.com.vn/")
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def get_credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                print(f"[ERROR] Credentials file not found: {CREDENTIALS_PATH}")
                print("Follow setup guide: .antigravity/config/gsc-config.md")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_PATH.write_text(creds.to_json())

    return creds


def is_cache_fresh():
    if not META_FILE.exists():
        return False
    meta = json.loads(META_FILE.read_text())
    cached_at = datetime.fromisoformat(meta.get("cached_at", "2000-01-01"))
    age_hours = (datetime.now() - cached_at).total_seconds() / 3600
    return age_hours < CACHE_TTL_HOURS


def fetch_gsc_data(service, site, days):
    end_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")  # GSC lags ~3 days
    start_date = (datetime.now() - timedelta(days=days + 3)).strftime("%Y-%m-%d")

    print(f"[INFO] Fetching GSC data: {start_date} → {end_date} (site: {site})")

    queries_rows = []
    pages_rows = []

    # Fetch query + page dimension (for keyword-to-page mapping)
    start_row = 0
    while True:
        body = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["page", "query"],
            "rowLimit": 25000,
            "startRow": start_row,
        }
        response = service.searchanalytics().query(siteUrl=site, body=body).execute()
        rows = response.get("rows", [])
        if not rows:
            break
        for row in rows:
            queries_rows.append({
                "page": row["keys"][0],
                "query": row["keys"][1],
                "clicks": int(row["clicks"]),
                "impressions": int(row["impressions"]),
                "ctr": round(row["ctr"], 4),
                "position": round(row["position"], 1),
            })
        if len(rows) < 25000:
            break
        start_row += 25000
        time.sleep(0.5)

    print(f"[INFO] Fetched {len(queries_rows)} query rows")

    # Fetch page-only dimension (for page-level metrics)
    start_row = 0
    while True:
        body = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["page"],
            "rowLimit": 25000,
            "startRow": start_row,
        }
        response = service.searchanalytics().query(siteUrl=site, body=body).execute()
        rows = response.get("rows", [])
        if not rows:
            break
        for row in rows:
            pages_rows.append({
                "page": row["keys"][0],
                "clicks": int(row["clicks"]),
                "impressions": int(row["impressions"]),
                "ctr": round(row["ctr"], 4),
                "position": round(row["position"], 1),
            })
        if len(rows) < 25000:
            break
        start_row += 25000
        time.sleep(0.5)

    print(f"[INFO] Fetched {len(pages_rows)} page rows")
    return queries_rows, pages_rows


def write_csv(filepath, rows, fieldnames):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[OK] Saved: {filepath} ({len(rows)} rows)")


def main():
    parser = argparse.ArgumentParser(description="Sync GSC data to CSV cache")
    parser.add_argument("--days", type=int, default=30, help="Days of data to fetch (default: 30)")
    parser.add_argument("--force", action="store_true", help="Ignore cache TTL")
    parser.add_argument("--site", default=DEFAULT_SITE, help="GSC site property URL")
    args = parser.parse_args()

    if not args.force and is_cache_fresh():
        meta = json.loads(META_FILE.read_text())
        print(f"[SKIP] Cache is fresh (last synced: {meta['cached_at']}). Use --force to refresh.")
        return

    try:
        from googleapiclient.discovery import build
    except ImportError:
        print("[ERROR] Missing dependencies. Run:")
        print("  pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        sys.exit(1)

    creds = get_credentials()
    service = build("searchconsole", "v1", credentials=creds)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    queries_rows, pages_rows = fetch_gsc_data(service, args.site, args.days)

    write_csv(QUERIES_CSV, queries_rows, ["page", "query", "clicks", "impressions", "ctr", "position"])
    write_csv(PAGES_CSV, pages_rows, ["page", "clicks", "impressions", "ctr", "position"])

    META_FILE.write_text(json.dumps({
        "cached_at": datetime.now().isoformat(),
        "days": args.days,
        "site": args.site,
        "query_rows": len(queries_rows),
        "page_rows": len(pages_rows),
    }, indent=2))

    print(f"\n[DONE] GSC cache updated. Run 'python scripts/process_gsc.py' to generate opportunities report.")


if __name__ == "__main__":
    main()
