#!/usr/bin/env python
"""Test the updated naics.py to show all fetched NAICS codes"""

from naics import get_naics_from_sam

codes = get_naics_from_sam()
print(f"\nTotal NAICS Codes Available: {len(codes)}\n")
print("All NAICS Codes:")
print("=" * 70)

for c in codes:
    print(f"  {c['code']:<10} {c['description']}")

print("=" * 70)
print(f"Total: {len(codes)} NAICS codes")
