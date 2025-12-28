#!/usr/bin/env python
"""
Mock test to demonstrate IT project search functionality
"""
from storage import save_csv, save_csv_extended, init_db, save_db

# Mock data representing IT-related opportunities from SAM.gov
MOCK_IT_RESULTS = [
    {
        "title": "Information Technology System Integration Services",
        "solicitationNumber": "F33657-25-R-0001",
        "noticeId": "d6d33af67294460a8cdc3efd55353745",
        "agency": "DEPT OF THE AIR FORCE",
        "type": "Solicitation",
        "notice_type": "Solicitation",
        "postedDate": "12/20/2025",
        "naics": "541512",
        "description": "Seeking proposals for IT system integration and modernization services",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "John Smith",
        "link": "https://api.sam.gov/prod/opportunities/v1/noticedesc?noticeid=d6d33af67294460a8cdc3efd55353745"
    },
    {
        "title": "Custom IT Software Development for Federal Agency",
        "solicitationNumber": "HHS-2025-001234",
        "noticeId": "a69484e93c094bf9a52493509e17b3df",
        "agency": "DEPT OF HEALTH AND HUMAN SERVICES",
        "type": "Solicitation",
        "notice_type": "Solicitation",
        "postedDate": "12/22/2025",
        "naics": "541511",
        "description": "Custom development of enterprise software solutions",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "Jane Doe",
        "link": "https://api.sam.gov/prod/opportunities/v1/noticedesc?noticeid=a69484e93c094bf9a52493509e17b3df"
    },
    {
        "title": "IT Infrastructure Management and Operations",
        "solicitationNumber": "GSA-IT-25-0567",
        "noticeId": "fe263144420a4ac9a9e33bb16c715922",
        "agency": "GENERAL SERVICES ADMINISTRATION",
        "type": "Solicitation",
        "notice_type": "Solicitation",
        "postedDate": "12/23/2025",
        "naics": "541513",
        "description": "Comprehensive IT infrastructure management services",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "Mike Johnson",
        "link": "https://api.sam.gov/prod/opportunities/v1/noticedesc?noticeid=fe263144420a4ac9a9e33bb16c715922"
    },
    {
        "title": "Cybersecurity and IT Security Services",
        "solicitationNumber": "DOD-SEC-25-2891",
        "noticeId": "fa1c1351d6004072bd67e29f942e877f",
        "agency": "DEPT OF DEFENSE",
        "type": "Solicitation",
        "notice_type": "Solicitation",
        "postedDate": "12/24/2025",
        "naics": "541519",
        "description": "Enterprise cybersecurity and information security services",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "Sarah Wilson",
        "link": "https://api.sam.gov/prod/opportunities/v1/noticedesc?noticeid=fa1c1351d6004072bd67e29f942e877f"
    },
    {
        "title": "Cloud Computing and IT Consulting Services",
        "solicitationNumber": "NOAA-IT-25-0042",
        "noticeId": "f1ce0c9b482044a696ca3250a0fd9be4",
        "agency": "DEPT OF COMMERCE",
        "type": "Solicitation",
        "notice_type": "Solicitation",
        "postedDate": "12/25/2025",
        "naics": "541512",
        "description": "Cloud infrastructure setup and IT consulting",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "Robert Brown",
        "link": "https://api.sam.gov/prod/opportunities/v1/noticedesc?noticeid=f1ce0c9b482044a696ca3250a0fd9be4"
    }
]

if __name__ == "__main__":
    print("IT-Related Projects Search - Results Summary")
    print("=" * 80)
    
    init_db()
    print("✓ Database initialized")
    print()
    
    print(f"Found {len(MOCK_IT_RESULTS)} IT-related opportunities")
    print()
    print("Sample IT Projects:")
    print("-" * 80)
    
    for i, result in enumerate(MOCK_IT_RESULTS, 1):
        print(f"\n{i}. {result.get('title', 'N/A')}")
        print(f"   Solicitation #: {result.get('solicitationNumber', 'N/A')}")
        print(f"   Agency: {result.get('agency', 'N/A')}")
        print(f"   NAICS Code: {result.get('naics', 'N/A')}")
        print(f"   Status: {result.get('opportunityStatus', 'N/A')}")
        print(f"   Posted: {result.get('postedDate', 'N/A')}")

    save_csv(MOCK_IT_RESULTS)
    print(f"\n✓ Results saved to sam_results.csv")
    
    save_csv_extended(MOCK_IT_RESULTS)
    
    save_db(MOCK_IT_RESULTS)
    print(f"✓ Results saved to database (sam_opportunities.db)")

    print("\n" + "=" * 80)
    print(f"Total: {len(MOCK_IT_RESULTS)} IT projects processed successfully")
    print("=" * 80)
