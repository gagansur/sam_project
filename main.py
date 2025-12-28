#!/usr/bin/env python3
"""
Main script that streams SAM.gov API results and saves them incrementally.
Uses generator pattern to process batches as they arrive.
"""
from pathlib import Path

from sam_api import search_sam
from storage import save_csv_extended, init_db, save_db
from datetime import datetime

# Mock data - simulates SAM.gov API responses for IT opportunities (for fallback)
MOCK_OPPORTUNITIES = [
    {
        "title": "Cloud Computing Infrastructure Services RFP",
        "solicitationNumber": "DOD-CLOUD-25-001",
        "agency": "DEPARTMENT OF DEFENSE",
        "noticeType": "Solicitation",
        "description": "Request for Proposal to provide cloud computing infrastructure services for DoD operations.",
        "postedDate": "2025-12-20",
        "deadlineDate": "2026-01-15",
        "naics": "541512",
        "attachments": ["Spec_Sheet.pdf", "RFP_Guidelines.pdf"],
        "opportunityStatus": "Posted",
        "naicsDescription": "Computer Systems Design Services"
    },
    {
        "title": "IT Software Development Services RFQ",
        "solicitationNumber": "HHS-IT-25-002",
        "agency": "DEPARTMENT OF HEALTH AND HUMAN SERVICES",
        "noticeType": "Solicitation",
        "description": "Request for Quote for custom IT software development for federal health systems.",
        "postedDate": "2025-12-22",
        "deadlineDate": "2026-01-10",
        "naics": "541511",
        "attachments": ["Tech_Requirements.pdf"],
        "opportunityStatus": "Posted",
        "naicsDescription": "Custom Computer Programming Services"
    },
    {
        "title": "Cybersecurity Solutions Implementation RFI",
        "solicitationNumber": "GSA-SEC-25-003",
        "agency": "GENERAL SERVICES ADMINISTRATION",
        "noticeType": "Solicitation",
        "description": "Request for Information on cybersecurity solution providers for federal agencies.",
        "postedDate": "2025-12-18",
        "deadlineDate": "2026-01-05",
        "naics": "541513",
        "attachments": [],
        "opportunityStatus": "Posted",
        "naicsDescription": "Computer Facilities Management Services"
    },
    {
        "title": "Enterprise Data Analytics Platform RFP",
        "solicitationNumber": "NOAA-DATA-25-004",
        "agency": "NATIONAL OCEANIC AND ATMOSPHERIC ADMINISTRATION",
        "noticeType": "Solicitation",
        "description": "Major RFP for enterprise-wide data analytics and reporting platform.",
        "postedDate": "2025-12-21",
        "deadlineDate": "2026-01-20",
        "naics": "541512",
        "attachments": ["Data_Schema.pdf", "Integration_Requirements.pdf"],
        "opportunityStatus": "Posted",
        "naicsDescription": "Computer Systems Design Services"
    },
    {
        "title": "Network Infrastructure IT Services Contract",
        "solicitationNumber": "VA-NET-25-005",
        "agency": "DEPARTMENT OF VETERANS AFFAIRS",
        "noticeType": "Solicitation",
        "description": "Ongoing IT services for network infrastructure maintenance and upgrades.",
        "postedDate": "2025-12-19",
        "deadlineDate": "2026-01-15",
        "naics": "541519",
        "attachments": ["Network_Specs.pdf"],
        "opportunityStatus": "Posted",
        "naicsDescription": "Other Computer Related Services"
    }
]

def save_mock_data():
    print(f"[{datetime.now()}] No results from API search. Using mock data for demonstration...")
    print(f"[{datetime.now()}] Processing {len(MOCK_OPPORTUNITIES)} mock IT opportunities...")
    print()

    save_db(MOCK_OPPORTUNITIES)
    save_csv_extended(MOCK_OPPORTUNITIES)
    total_count = len(MOCK_OPPORTUNITIES)
    return total_count

def save_sam_data():
    total_count = 0
    batch_num = 0
    data_path = Path(r"C:\Users\gagan\source\repos\sam_project\data")

    # Use generator to process batches as they arrive
    search_generator = search_sam(
        keyword="IT",
        naics=["541511", "541512", "541513", "541519"],
        agencies=None
    )


    for batch in search_generator:
        batch_num += 1
        batch_count = len(batch)
        total_count += batch_count

        print(f"[{datetime.now()}] Processing batch {batch_num} ({batch_count} records)...")

        # Update CSV file with all records so far
        print(f"[{datetime.now()}]   → Updating CSV file...")

        save_csv_extended(results=batch, filename=data_path.joinpath(f"sam_results_extended_{batch_num}.csv"))
        print(f"[{datetime.now()}]   ✅ Batch {batch_num} saved (Total so far: {total_count})")
        print()
    return total_count


if __name__ == "__main__":


    print(f"[{datetime.now()}] Starting main.py execution...")
    print()

    try:
        print(f"[{datetime.now()}] Initializing database...")
        init_db()
        print(f"[{datetime.now()}] ✅ Database initialized")
        print()

        total = save_sam_data()

        # Search SAM.gov API and process results as they stream in
        print(f"[{datetime.now()}] Starting SAM.gov search for IT opportunities...")
        print(f"[{datetime.now()}] Query: keyword=IT, NAICS codes=541511,541512,541513,541519")
        print()



        if total == 0:
            print("No records were found.... ")
        print("\n")
        print(f"[{datetime.now()}] ✅ Search and save complete!")
        print(f"[{datetime.now()}] Total records processed: {total}")
        print(f"[{datetime.now()}] Files created:")
        print(f"[{datetime.now()}]   - Database: sam_opportunities.db")
        print(f"[{datetime.now()}]   - CSV: sam_results_extended.csv")
        
    except Exception as e:
        print(f"[{datetime.now()}] ❌ ERROR: {str(e)}")
        import traceback
        print(traceback.format_exc())
        exit(1)
