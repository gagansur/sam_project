#!/usr/bin/env python
"""
Test the RFI/RFQ/RFP checker with realistic mock data
"""

from storage import init_db, save_db
from rfi_rfq_rfp_checker import RFIRFQRFPChecker

# Mock data with various RFI/RFQ/RFP document types
MOCK_DATA = [
    {
        "title": "RFI: Cloud Computing Infrastructure Assessment",
        "solicitationNumber": "RFI-CLOUD-001",
        "noticeId": "001",
        "agency": "DEPT OF DEFENSE",
        "type": "Request for Information",
        "notice_type": "RFI",
        "postedDate": "12/20/2025",
        "naics": "541512",
        "description": "Request for Information on cloud computing capabilities and vendors",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "John Doe",
        "link": "https://api.sam.gov/..."
    },
    {
        "title": "RFQ: IT Software Development Services",
        "solicitationNumber": "RFQ-IT-002",
        "noticeId": "002",
        "agency": "DEPT OF HEALTH AND HUMAN SERVICES",
        "type": "Request for Quote",
        "notice_type": "RFQ",
        "postedDate": "12/21/2025",
        "naics": "541511",
        "description": "Request for Quotation on custom software development and integration",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "Jane Smith",
        "link": "https://api.sam.gov/..."
    },
    {
        "title": "RFP: Enterprise IT Infrastructure Modernization",
        "solicitationNumber": "RFP-INFRA-003",
        "noticeId": "003",
        "agency": "GENERAL SERVICES ADMINISTRATION",
        "type": "Request for Proposal",
        "notice_type": "RFP",
        "postedDate": "12/22/2025",
        "naics": "541513",
        "description": "Request for Proposal for comprehensive IT infrastructure modernization and cloud migration",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "Mike Johnson",
        "link": "https://api.sam.gov/..."
    },
    {
        "title": "RFP: Cybersecurity Solutions Implementation",
        "solicitationNumber": "RFP-SEC-004",
        "noticeId": "004",
        "agency": "DEPT OF DEFENSE",
        "type": "Request for Proposal",
        "notice_type": "RFP",
        "postedDate": "12/23/2025",
        "naics": "541519",
        "description": "Request for Proposal for enterprise cybersecurity solutions and implementation services",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "Sarah Wilson",
        "link": "https://api.sam.gov/..."
    },
    {
        "title": "Standard IT Services Solicitation",
        "solicitationNumber": "SOL-IT-005",
        "noticeId": "005",
        "agency": "DEPT OF COMMERCE",
        "type": "Solicitation",
        "notice_type": "Solicitation",
        "postedDate": "12/24/2025",
        "naics": "541512",
        "description": "General solicitation for IT services and support",
        "opportunityStatus": "Open",
        "classificationCode": "G",
        "pointOfContact": "Robert Brown",
        "link": "https://api.sam.gov/..."
    }
]

if __name__ == "__main__":
    print("=" * 80)
    print("RFI/RFQ/RFP CHECKER - TEST WITH MOCK DATA")
    print("=" * 80 + "\n")
    
    # Initialize and save mock data
    print("Initializing database with mock data...")
    init_db()
    save_db(MOCK_DATA)
    print(f"✓ Saved {len(MOCK_DATA)} mock records\n")
    
    # Create checker instance
    checker = RFIRFQRFPChecker()
    
    # Print summary
    checker.print_summary()
    
    # Print statistics
    stats = checker.get_statistics()
    print("\nSTATISTICS:")
    print(f"  Total: {stats['total']}")
    print(f"  RFI: {stats['rfi_count']} ({stats['rfi_percentage']:.1f}%)")
    print(f"  RFQ: {stats['rfq_count']} ({stats['rfq_percentage']:.1f}%)")
    print(f"  RFP: {stats['rfp_count']} ({stats['rfp_percentage']:.1f}%)")
    print(f"  Other: {stats['other_count']} ({stats['other_percentage']:.1f}%)")
    
    # Export to CSV
    checker.export_to_csv("test_rfi_rfq_rfp_report.csv")
    
    print("\n" + "=" * 80)
    print("✅ TEST COMPLETE - Run 'python rfi_rfq_rfp_checker.py' for interactive mode")
    print("=" * 80)
