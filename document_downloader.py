#!/usr/bin/env python
"""
Document Downloader for SAM.gov IT Projects
Downloads opportunity descriptions and related documents
"""

import os
import sys
import requests
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class DocumentDownloader:
    """Downloads documents and descriptions from SAM.gov opportunities"""
    
    def __init__(self, output_dir="downloaded_docs", api_key=None):
        """Initialize the downloader"""
        if api_key is None:
            from config import API_KEY
            api_key = API_KEY
        
        self.api_key = api_key
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.descriptions_dir = self.output_dir / "descriptions"
        self.attachments_dir = self.output_dir / "attachments"
        self.descriptions_dir.mkdir(exist_ok=True)
        self.attachments_dir.mkdir(exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SAM-Document-Downloader/1.0'
        })
        
        self.download_log = {
            'timestamp': datetime.now().isoformat(),
            'total_opportunities': 0,
            'documents_downloaded': 0,
            'descriptions_saved': 0,
            'errors': [],
            'details': []
        }
    
    def get_opportunity_details(self, solicitation_number: str) -> Optional[Dict]:
        """
        Fetch detailed information about a specific opportunity
        """
        try:
            # Using the detail endpoint
            url = f"https://api.sam.gov/opportunities/v2/search"
            params = {
                "api_key": self.api_key,
                "solicitationNumber": solicitation_number
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                opportunities = data.get("opportunitiesData", [])
                if opportunities:
                    return opportunities[0]
            else:
                self.download_log['errors'].append({
                    'solicitation': solicitation_number,
                    'error': f'HTTP {response.status_code}',
                    'action': 'get_opportunity_details'
                })
        
        except Exception as e:
            self.download_log['errors'].append({
                'solicitation': solicitation_number,
                'error': str(e),
                'action': 'get_opportunity_details'
            })
        
        return None
    
    def save_description(self, opportunity: Dict) -> bool:
        """
        Save opportunity description to a text file
        """
        try:
            solicitation_num = opportunity.get('solicitationNumber', 'UNKNOWN')
            title = opportunity.get('title', 'Untitled').replace('/', '_').replace('\\', '_')
            agency = opportunity.get('agency', 'Unknown').replace('/', '_')
            
            # Create filename
            filename = f"{solicitation_num}_{title[:50]}.txt"
            filepath = self.descriptions_dir / filename
            
            # Prepare content
            content = f"""================================================================================
OPPORTUNITY DETAILS
================================================================================

Title: {opportunity.get('title', 'N/A')}
Solicitation Number: {solicitation_num}
Agency: {agency}
Notice ID: {opportunity.get('noticeId', 'N/A')}
Type: {opportunity.get('type', 'N/A')}
Status: {opportunity.get('opportunityStatus', 'N/A')}
Posted Date: {opportunity.get('postedDate', 'N/A')}
NAICS Code: {opportunity.get('naics', 'N/A')}
Classification Code: {opportunity.get('classificationCode', 'N/A')}

================================================================================
DESCRIPTION
================================================================================

{opportunity.get('description', 'No description available')}

================================================================================
ADDITIONAL INFORMATION
================================================================================

Point of Contact: {opportunity.get('pointOfContact', 'N/A')}
Organization: {opportunity.get('organization', 'N/A')}

Link: {opportunity.get('link', 'N/A')}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.download_log['descriptions_saved'] += 1
            return True
        
        except Exception as e:
            self.download_log['errors'].append({
                'opportunity': opportunity.get('title', 'Unknown'),
                'error': str(e),
                'action': 'save_description'
            })
            return False
    
    def download_attachment(self, url: str, solicitation_num: str, filename: str) -> bool:
        """
        Download a single attachment
        """
        try:
            response = self.session.get(url, timeout=30, stream=True)
            
            if response.status_code == 200:
                # Create subdirectory for each opportunity
                opp_dir = self.attachments_dir / solicitation_num
                opp_dir.mkdir(exist_ok=True)
                
                filepath = opp_dir / filename
                
                # Download in chunks
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                self.download_log['documents_downloaded'] += 1
                return True
            else:
                self.download_log['errors'].append({
                    'solicitation': solicitation_num,
                    'file': filename,
                    'error': f'HTTP {response.status_code}',
                    'action': 'download_attachment'
                })
        
        except Exception as e:
            self.download_log['errors'].append({
                'solicitation': solicitation_num,
                'file': filename,
                'error': str(e),
                'action': 'download_attachment'
            })
        
        return False
    
    def download_documents(self, opportunities: List[Dict], max_per_opp: int = 5) -> Dict:
        """
        Download documents and descriptions for a list of opportunities
        """
        self.download_log['total_opportunities'] = len(opportunities)
        
        print(f"\n{'='*80}")
        print(f"DOCUMENT DOWNLOADER - SAM.gov IT Opportunities")
        print(f"{'='*80}\n")
        print(f"📥 Downloading documents for {len(opportunities)} opportunities...")
        print(f"📁 Output directory: {self.output_dir.absolute()}\n")
        
        for idx, opp in enumerate(opportunities, 1):
            solicitation_num = opp.get('solicitationNumber', f'OPP_{idx}')
            title = opp.get('title', 'Untitled')[:60]
            
            print(f"\n[{idx}/{len(opportunities)}] Processing: {title}")
            print(f"    Solicitation: {solicitation_num}")
            
            # Save description
            if self.save_description(opp):
                print(f"    ✓ Description saved")
            else:
                print(f"    ✗ Failed to save description")
            
            # Try to get additional details and documents
            details = self.get_opportunity_details(solicitation_num)
            
            if details:
                # Check for attachments/documents in the opportunity
                attachments = details.get('attachments', [])
                if attachments:
                    print(f"    📎 Found {len(attachments)} attachments")
                    for attach_idx, attachment in enumerate(attachments[:max_per_opp], 1):
                        # Attachment could be a dict or string
                        if isinstance(attachment, dict):
                            attach_url = attachment.get('url')
                            attach_name = attachment.get('filename', f'attachment_{attach_idx}')
                        else:
                            attach_url = str(attachment)
                            attach_name = f'attachment_{attach_idx}'
                        
                        if attach_url:
                            print(f"      Downloading: {attach_name}")
                            if self.download_attachment(attach_url, solicitation_num, attach_name):
                                print(f"      ✓ Downloaded")
                            else:
                                print(f"      ✗ Failed to download")
                else:
                    print(f"    ℹ No attachments found in opportunity data")
            
            # Log the opportunity
            self.download_log['details'].append({
                'solicitation_number': solicitation_num,
                'title': title,
                'agency': opp.get('agency'),
                'naics': opp.get('naics'),
                'description_saved': True,
                'attachments_count': len(details.get('attachments', [])) if details else 0
            })
        
        return self.download_log
    
    def save_download_log(self) -> str:
        """
        Save download log as JSON
        """
        log_file = self.output_dir / "download_log.json"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.download_log, f, indent=2)
        
        return str(log_file)
    
    def print_summary(self):
        """
        Print summary of downloads
        """
        log = self.download_log
        
        print(f"\n{'='*80}")
        print(f"DOWNLOAD SUMMARY")
        print(f"{'='*80}\n")
        print(f"📊 Statistics:")
        print(f"   Total Opportunities Processed: {log['total_opportunities']}")
        print(f"   Descriptions Saved: {log['descriptions_saved']}")
        print(f"   Documents Downloaded: {log['documents_downloaded']}")
        print(f"   Errors: {len(log['errors'])}")
        
        if log['errors']:
            print(f"\n⚠️  Errors encountered:")
            for err in log['errors'][:5]:  # Show first 5 errors
                print(f"   - {err.get('solicitation', err.get('file', 'Unknown'))}: {err.get('error')}")
            if len(log['errors']) > 5:
                print(f"   ... and {len(log['errors']) - 5} more errors")
        
        print(f"\n📁 Output Locations:")
        print(f"   Descriptions: {self.descriptions_dir.absolute()}")
        print(f"   Attachments: {self.attachments_dir.absolute()}")
        print(f"   Log File: {self.output_dir / 'download_log.json'}")
        print(f"\n{'='*80}\n")


if __name__ == "__main__":
    # Example usage
    print("Starting document download...")
    
    # Example: Download documents for specific opportunities
    example_opportunities = [
        {
            "solicitationNumber": "140G0222A0008",
            "title": "SINGLE AWARD BPA FOR PROFESSIONAL IT SERVICES",
            "agency": "General Services Administration",
            "naics": "541512",
            "description": "IT Services opportunity",
            "type": "BPA"
        }
    ]
    
    downloader = DocumentDownloader(output_dir="downloaded_docs", api_key=None)
    log = downloader.download_documents(example_opportunities)
    
    if log:
        print("✅ Download complete!")
    else:
        print("❌ Download failed or no data found")
