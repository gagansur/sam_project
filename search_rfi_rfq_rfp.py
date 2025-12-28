#!/usr/bin/env python
"""
Enhanced main.py with RFI/RFQ/RFP filtering
Searches for IT-related projects with option to filter by document type
"""

from sam_api import search_sam
from storage import save_csv, save_csv_extended, init_db, save_db
from rfi_rfq_rfp_checker import RFIRFQRFPChecker


def main_with_filtering():
    """Main script with RFI/RFQ/RFP filtering"""
    
    init_db()
    print("Database initialized\n")
    
    print("Searching for IT-related opportunities...")
    results = search_sam(
        keyword="IT",
        naics=["541511", "541512", "541513", "541519"],
        agencies=None
    )
    
    print(f"Found {len(results)} total IT opportunities\n")
    
    # Save all results
    save_csv_extended(results)
    save_db(results)
    print(f"✓ Saved {len(results)} results to database\n")
    
    # Now analyze document types
    print("Analyzing document types (RFI/RFQ/RFP)...\n")
    
    checker = RFIRFQRFPChecker()
    
    # Get statistics
    stats = checker.get_statistics()
    
    print("=" * 80)
    print("DOCUMENT TYPE BREAKDOWN")
    print("=" * 80)
    print(f"Total: {stats['total']}")
    print(f"  RFI (Request for Information): {stats['rfi_count']} ({stats['rfi_percentage']:.1f}%)")
    print(f"  RFQ (Request for Quote): {stats['rfq_count']} ({stats['rfq_percentage']:.1f}%)")
    print(f"  RFP (Request for Proposal): {stats['rfp_count']} ({stats['rfp_percentage']:.1f}%)")
    print(f"  Other Solicitations: {stats['other_count']} ({stats['other_percentage']:.1f}%)")
    print("=" * 80)
    
    # Export analysis
    checker.export_to_csv("rfi_rfq_rfp_analysis.csv")
    
    print("\n✅ Complete! Run 'python rfi_rfq_rfp_checker.py' for interactive analysis")


if __name__ == "__main__":
    main_with_filtering()
