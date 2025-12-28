import csv
import sqlite3

from config import DB_FILE, CSV_FILE

FIELDS = [
    "title", "solicitationNumber", "agency", "type",
    "postedDate", "naics", "description"
]

# Extended fields that might be in the API response
EXTENDED_FIELDS = [
    "title", "solicitationNumber", "noticeId", "agency", "type", "notice_type",
    "postedDate", "naics", "description", "opportunityStatus",
    "classificationCode", "pointOfContact", "uiLink"
]

def save_csv(results, filename=CSV_FILE):
    """Save results to CSV file with standard fields"""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore')
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k, "") for k in FIELDS})


def save_csv_extended(results, filename="sam_results_extended.csv"):
    """Save results to extended CSV file with all available fields"""
    if not results:
        print(f"No results to save")
        return
    
    # Get all unique keys from results
    all_keys = set()
    for r in results:
        all_keys.update(r.keys())
    
    fieldnames = sorted(list(all_keys))
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k, "") for k in fieldnames})
    
    print(f"✓ Saved {len(results)} results to {filename}")
    print(f"  Fields saved: {', '.join(fieldnames[:10])}{'...' if len(fieldnames) > 10 else ''}")
    return len(all_keys)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Check if table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='opportunities'")
    table_exists = c.fetchone()
    
    if table_exists:
        # Drop and recreate table with new schema
        c.execute("DROP TABLE IF EXISTS opportunities")
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            solicitationNumber TEXT,
            noticeId TEXT,
            agency TEXT,
            type TEXT,
            notice_type TEXT,
            postedDate TEXT,
            naics TEXT,
            description TEXT,
            opportunityStatus TEXT,
            classificationCode TEXT,
            pointOfContact TEXT,
            link TEXT
        )
    """)
    conn.commit()
    conn.close()


def _convert_value(value):
    """Convert value to string, handling lists and dicts"""
    if value is None:
        return None
    if isinstance(value, (list, dict)):
        return str(value)
    if isinstance(value, bool):
        return str(value)
    return value


def save_db(results):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    for r in results:
        # Extract all available fields and convert list/dict values to strings
        try:
            c.execute("""
                INSERT INTO opportunities 
                (title, solicitationNumber, noticeId, agency, type, notice_type, postedDate, naics, description, 
                 opportunityStatus, classificationCode, pointOfContact, link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                _convert_value(r.get("title")),
                _convert_value(r.get("solicitationNumber")),
                _convert_value(r.get("noticeId")),
                _convert_value(r.get("agency")),
                _convert_value(r.get("type")),
                _convert_value(r.get("notice_type")),
                _convert_value(r.get("postedDate")),
                _convert_value(r.get("naicsCode")),
                _convert_value(r.get("description")),
                _convert_value(r.get("opportunityStatus")),
                _convert_value(r.get("classificationCode")),
                _convert_value(r.get("pointOfContact")),
                _convert_value(r.get("uiLink"))
            ))
        except sqlite3.ProgrammingError as e:
            print(f"Warning: Failed to insert record: {e}")
            continue

    conn.commit()
    conn.close()
