#!/usr/bin/env python
"""
Test script to verify IT project search functionality
"""
from sam_api import search_sam
from storage import save_csv, init_db, save_db

if __name__ == "__main__":
    print("Starting IT-related projects search...")
    print("=" * 60)
    
    init_db()
    print("✓ Database initialized")

    print("Searching for IT-related opportunities...")
    print("  - Keyword: 'IT'")
    print("  - NAICS codes: 541511, 541512, 541513, 541519")
    print("  - Time range: Last 30 days")
    print()
    
    results = search_sam(
        keyword="IT",
        naics=["541511", "541512", "541513", "541519"],
        agencies=None
    )

    print(f"\nFound {len(results)} IT-related opportunities")
    print("=" * 60)
    
    if results:
        print("\nSample results:")
        for i, result in enumerate(results[:3], 1):
            print(f"\n{i}. {result.get('title', 'N/A')}")
            print(f"   Solicitation: {result.get('solicitationNumber', 'N/A')}")
            print(f"   Agency: {result.get('agency', 'N/A')}")
            print(f"   Posted: {result.get('postedDate', 'N/A')}")

    save_csv(results)
    print(f"\n✓ Results saved to sam_results.csv")
    
    save_db(results)
    print(f"✓ Results saved to database (sam_opportunities.db)")

    print(f"\nTotal: {len(results)} results processed")
    print("=" * 60)
