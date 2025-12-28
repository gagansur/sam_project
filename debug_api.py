#!/usr/bin/env python
"""Debug script to inspect API response structure"""

from sam_api import search_sam
import json

# Get a small sample
results = search_sam(limit=5)

if results:
    print("Sample API Response Structure:")
    print("=" * 80)
    print(json.dumps(results[0], indent=2)[:1000])
    print("\n... (truncated)")
    print("\n" + "=" * 80)
    print("\nAvailable Keys in Response:")
    print(list(results[0].keys()))
else:
    print("No results returned")
