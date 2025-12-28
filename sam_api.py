import requests
from datetime import datetime, timedelta
from config import API_KEY, DEFAULT_DAYS, DEFAULT_LIMIT

BASE_URL = "https://api.sam.gov/opportunities/v2/search"

def format_date(dt):
    return dt.strftime("%m/%d/%Y")

def search_sam(
    keyword=None,
    naics=None,
    agencies=None,
    notice_type="Solicitation",
    posted_from=None,
    posted_to=None,
    limit=DEFAULT_LIMIT,
    timeout=30
):
    if not posted_from:
        posted_from = format_date(datetime.today() - timedelta(days=DEFAULT_DAYS))
    if not posted_to:
        posted_to = format_date(datetime.today())

    offset = 0
    all_results = []

    while True:
        params = {
            "api_key": API_KEY,
            "limit": limit,
            "offset": offset,
            "noticeType": notice_type,
            "postedFrom": posted_from,
            "postedTo": posted_to,
        }

        if keyword:
            params["q"] = keyword
        if naics:
            params["naics"] = ",".join(naics) if isinstance(naics, list) else naics
        if agencies:
            params["agency"] = ",".join(agencies)

        try:
            print(f"[{datetime.now()}] Fetching page {offset // limit + 1} (offset={offset})...")
            response = requests.get(BASE_URL, params=params, timeout=timeout)

            if response.status_code != 200:
                print(f"[{datetime.now()}] Error: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                break

            data = response.json()
            batch = data.get("opportunitiesData", [])
            print(f"[{datetime.now()}] Got {len(batch)} records from this page")

            if not batch:
                break
            yield batch

            # all_results.extend(batch)
            #
            if len(batch) < limit:
                break

            offset += limit

        except requests.Timeout:
            print(f"[{datetime.now()}] Error: Request timeout after {timeout} seconds")
            break
        except requests.RequestException as e:
            print(f"[{datetime.now()}] Request error: {str(e)}")
            break
        except Exception as e:
            print(f"[{datetime.now()}] Unexpected error: {str(e)}")
            break

    #return all_results
