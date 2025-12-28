#!/usr/bin/env python3
"""
Test script for SAM.gov document download API endpoint
"""

import requests
import json
from config import API_KEY

# Sample opportunity data to test with
test_opportunity = {
    "solicitationNumber": "140G0222A0008",  # From the earlier CSV data
    "title": "SINGLE AWARD BPA FOR PROFESSIONAL IT SERVICES",
    "description": "This is a test download",
    "organization": "Test Org"
}

def test_download_endpoint():
    """Test the /api/download-docs endpoint"""
    
    url = "http://localhost:5000/api/download-docs"
    
    print("=" * 60)
    print("Testing SAM.gov Document Download API Endpoint")
    print("=" * 60)
    print(f"\nEndpoint: POST {url}")
    print(f"Payload: {json.dumps(test_opportunity, indent=2)}")
    print(f"\nAPI Key Status: {'✓ Set' if API_KEY else '✗ Not set'}")
    
    if not API_KEY:
        print("\n[ERROR] API_KEY not configured in config.py")
        return
    
    print("\nSending request...")
    try:
        response = requests.post(
            url,
            json=test_opportunity,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        response_data = response.json()
        print(f"Response Data:\n{json.dumps(response_data, indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ Request successful!")
            if response_data.get('success'):
                print(f"   - Solicitation: {response_data.get('solicitation')}")
                print(f"   - Description Saved: {response_data.get('description_saved')}")
                print(f"   - Attachments: {response_data.get('attachments_downloaded')}")
            else:
                print(f"❌ Download failed: {response_data.get('message')}")
        else:
            print(f"\n❌ Request failed with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to Flask server")
        print("Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {str(e)}")

if __name__ == '__main__':
    test_download_endpoint()
