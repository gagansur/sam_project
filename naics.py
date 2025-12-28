import requests
import json

# Common IT-related NAICS codes and a comprehensive list
NAICS_CODES_DB = {
    # Computer & IT Services
    "541511": "Custom Computer Programming Services",
    "541512": "Computer Systems Design Services",
    "541513": "Computer Facilities Management Services",
    "541519": "Other Computer Related Services",
    "541690": "Other Professional, Scientific, and Technical Services",
    
    # Construction
    "236220": "Commercial and Institutional Building Construction",
    "236210": "Industrial Building and Warehouse Construction",
    "237990": "Other Heavy and Civil Engineering Construction",
    
    # Engineering Services
    "541330": "Engineering Services",
    "541340": "Drafting Services",
    "541360": "Geophysical Surveying and Mapping Services",
    
    # Management Services
    "541611": "Administrative Management and General Management Consulting Services",
    "541612": "Human Resources Consulting Services",
    "541618": "Other Management Consulting Services",
    
    # Professional Services
    "541810": "Advertising Agencies",
    "541820": "Public Relations Agencies",
    "541870": "Advertising Material Distribution Services",
}

def get_naics_from_sam(api_key=None):
    """
    Fetches all NAICS codes. First tries to get from SAM.gov API,
    falls back to local database if API fails.
    
    Returns a list of dictionaries:
    [
        {"code": "541511", "description": "Custom Computer Programming Services"},
        ...
    ]
    """
    if api_key is None:
        try:
            from config import API_KEY
            api_key = API_KEY
        except ImportError:
            api_key = None
    
    naics_list = []
    
    # Try to fetch from SAM.gov API first
    if api_key:
        print("Attempting to fetch NAICS codes from SAM.gov API...")
        naics_list = _fetch_from_sam_api(api_key)
    
    # If API fails or no API key, use local database
    if not naics_list:
        print("Using local NAICS code database...")
        naics_list = _get_local_naics()
    
    return naics_list


def _fetch_from_sam_api(api_key):
    """
    Attempts to fetch NAICS codes from SAM.gov opportunities data.
    """
    all_naics = {}
    offset = 0
    limit = 100
    max_pages = 50  # Limit to prevent infinite loops
    page = 0
    
    try:
        while page < max_pages:
            params = {
                "api_key": api_key,
                "limit": limit,
                "offset": offset,
            }
            
            response = requests.get(
                "https://api.sam.gov/opportunities/v2/search",
                params=params,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"API Error (Status {response.status_code}): Falling back to local database")
                return []
            
            data = response.json()
            batch = data.get("opportunitiesData", [])
            
            if not batch:
                print(f"✓ Fetched {len(all_naics)} unique NAICS codes from SAM.gov")
                break
            
            # Extract unique NAICS codes from opportunities
            for opp in batch:
                naics_code = opp.get("naics")
                if naics_code and naics_code not in all_naics:
                    all_naics[naics_code] = {
                        "code": naics_code,
                        "description": f"NAICS {naics_code}"
                    }
            
            print(f"  Page {page + 1}: Processed {len(batch)} opportunities, {len(all_naics)} unique NAICS codes")
            
            if len(batch) < limit:
                break
            
            offset += limit
            page += 1
            
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return []
    
    return list(all_naics.values())


def _get_local_naics():
    """
    Returns the local NAICS codes database.
    """
    return [
        {"code": code, "description": desc}
        for code, desc in NAICS_CODES_DB.items()
    ]


if __name__ == "__main__":
    naics = get_naics_from_sam()
    print(f"Loaded {len(naics)} NAICS codes from SAM.gov")
    for item in naics[:10]:
        print(item)
