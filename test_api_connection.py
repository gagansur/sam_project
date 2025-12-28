#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta
from config import API_KEY

BASE_URL = "https://api.sam.gov/opportunities/v2/search"

def format_date(dt):
    return dt.strftime("%m/%d/%Y")

posted_from = format_date(datetime.today() - timedelta(days=30))
posted_to = format_date(datetime.today())

params = {
    "api_key": API_KEY,
    "limit": 10,
    "offset": 0,
    "noticeType": "Solicitation",
    "postedFrom": posted_from,
    "postedTo": posted_to,
    "q": "IT",
    "naics": "541511,541512,541513,541519"
}

print(f"[{datetime.now()}] Testing SAM.gov API with timeout=30 seconds...")
print(f"URL: {BASE_URL}")
print(f"Query: keyword=IT, NAICS codes provided")
print()

try:
    response = requests.get(BASE_URL, params=params, timeout=30)
    print(f"[{datetime.now()}] Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        opportunities = data.get("opportunitiesData", [])
        print(f"[{datetime.now()}] ✅ API Response received!")
        print(f"[{datetime.now()}] Found {len(opportunities)} opportunities")
        if opportunities:
            print(f"\nFirst opportunity:")
            print(f"  Title: {opportunities[0].get('title', 'N/A')}")
            print(f"  Agency: {opportunities[0].get('agency', 'N/A')}")
            print(f"  NAICS: {opportunities[0].get('naics', 'N/A')}")
    else:
        print(f"[{datetime.now()}] ❌ Error: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except requests.Timeout:
    print(f"[{datetime.now()}] ❌ Request timed out after 30 seconds")
except Exception as e:
    print(f"[{datetime.now()}] ❌ Error: {str(e)}")
