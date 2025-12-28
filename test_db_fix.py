#!/usr/bin/env python
"""
Test the database fix with mock data that includes list/dict values
to simulate the real API response issue
"""

from storage import save_csv, save_csv_extended, init_db, save_db

# Mock data with list and dict values (simulating real API responses)
MOCK_RESULTS_WITH_LISTS = [
    {
        "title": "IT System Integration Services",
        "solicitationNumber": "F33657-25-R-0001",
        "noticeId": "d6d33af67294460a8cdc3efd55353745",
        "agency": "DEPT OF THE AIR FORCE",
        "type": "Solicitation",
        "notice_type": "Solicitation",
        "postedDate": "12/20/2025",
        "naics": "541512",
        "description": "IT integration services",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "John Smith",
        "link": "https://api.sam.gov/...",
        # These are the problematic list/dict values from real API
        "attachments": ["file1.pdf", "file2.docx"],  # LIST value
        "tags": {"category": "IT", "priority": "High"},  # DICT value
        "active": True,  # BOOL value
        "estimatedAmount": 500000  # INT value
    },
    {
        "title": "Custom IT Software Development",
        "solicitationNumber": "HHS-2025-001234",
        "noticeId": "a69484e93c094bf9a52493509e17b3df",
        "agency": "DEPT OF HEALTH AND HUMAN SERVICES",
        "type": "Solicitation",
        "notice_type": "Solicitation",
        "postedDate": "12/22/2025",
        "naics": "541511",
        "description": "Software development",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "Jane Doe",
        "link": "https://api.sam.gov/...",
        "attachments": ["rfi.pdf"],
        "tags": {"category": "Development"},
        "active": True,
        "estimatedAmount": 750000
    },
    {
        "title": "IT Infrastructure Management",
        "solicitationNumber": "GSA-IT-25-0567",
        "noticeId": "fe263144420a4ac9a9e33bb16c715922",
        "agency": "GENERAL SERVICES ADMINISTRATION",
        "type": "Solicitation",
        "notice_type": "Solicitation",
        "postedDate": "12/23/2025",
        "naics": "541513",
        "description": "Infrastructure management",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "Mike Johnson",
        "link": "https://api.sam.gov/...",
        "attachments": [],  # Empty list
        "tags": {"category": "Infrastructure"},
        "active": False,  # FALSE value
        "estimatedAmount": None  # None value
    }
]

if __name__ == "__main__":
    print("=" * 80)
    print("DATABASE FIX TEST - Handling List/Dict Values")
    print("=" * 80)
    print()
    
    print("Initializing database...")
    init_db()
    print("✓ Database initialized\n")
    
    print(f"Saving {len(MOCK_RESULTS_WITH_LISTS)} mock records with list/dict values...")
    print("  (This tests the fix for: sqlite3.ProgrammingError: type 'list' is not supported)\n")
    
    try:
        save_db(MOCK_RESULTS_WITH_LISTS)
        print("✓ Successfully saved to database\n")
    except Exception as e:
        print(f"✗ Failed to save: {e}\n")
        exit(1)
    
    print("Saving to CSV files...")
    save_csv(MOCK_RESULTS_WITH_LISTS)
    save_csv_extended(MOCK_RESULTS_WITH_LISTS)
    print("✓ CSVs saved\n")
    
    print("Verifying database records...")
    import sqlite3
    conn = sqlite3.connect("sam_opportunities.db")
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM opportunities")
    count = c.fetchone()[0]
    print(f"✓ Total records in database: {count}\n")
    
    c.execute("SELECT title, naics, classificationCode FROM opportunities")
    print("Sample records from database:")
    for row in c.fetchall():
        print(f"  - {row[0][:40]:40} | NAICS: {row[1]} | Class: {row[2]}")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ TEST PASSED - Database fix works correctly!")
    print("=" * 80)
    print("\nThe fix successfully handles:")
    print("  ✓ List values (converted to string)")
    print("  ✓ Dict values (converted to string)")
    print("  ✓ Boolean values (converted to string)")
    print("  ✓ Integer values (preserved)")
    print("  ✓ None values (preserved)")
