#!/usr/bin/env python3
import sys
import traceback
from datetime import datetime

print(f"[{datetime.now()}] Starting main.py execution...")
sys.stdout.flush()

try:
    from sam_api import search_sam
    from storage import save_csv, save_csv_extended, init_db, save_db
    
    print(f"[{datetime.now()}] Imports successful, initializing database...")
    sys.stdout.flush()
    
    init_db()
    print(f"[{datetime.now()}] Database initialized")
    sys.stdout.flush()

    print(f"[{datetime.now()}] Starting SAM.gov API search for IT opportunities...")
    sys.stdout.flush()
    
    results = search_sam(
        keyword="IT",
        naics=["541511", "541512", "541513", "541519"],
        agencies=None
    )
    
    print(f"[{datetime.now()}] Search completed. Found {len(results)} opportunities")
    sys.stdout.flush()

    print(f"[{datetime.now()}] Saving to CSV (extended format)...")
    sys.stdout.flush()
    save_csv_extended(results)
    
    print(f"[{datetime.now()}] Saving to database...")
    sys.stdout.flush()
    save_db(results)

    print(f"[{datetime.now()}] ✅ Successfully saved {len(results)} results")
    sys.stdout.flush()

except Exception as e:
    print(f"[{datetime.now()}] ❌ ERROR: {str(e)}")
    print(traceback.format_exc())
    sys.stdout.flush()
    sys.exit(1)
