

#!/usr/bin/env python
"""
Interactive Dashboard for SAM.gov IT Projects
Browse and download documents for projects you're interested in
"""

import csv
import sys
from pathlib import Path
from typing import List, Dict
from document_downloader import DocumentDownloader


class ProjectDashboard:
    """Interactive dashboard for browsing and downloading IT projects"""
    
    def __init__(self, csv_dir: str = "data"):
        """
        Initialize the dashboard
        
        Args:
            csv_dir: Directory containing CSV files (default: "data")
        """
        self.csv_dir = Path(csv_dir)
        self.opportunities = []
        self.selected = []
        self.all_columns = []  # Track all available columns
        self.display_columns = []  # Columns to display (key fields)
        self.load_opportunities()
        self._determine_display_columns()
    
    def _determine_display_columns(self):
        """Determine which columns to display by default"""
        # Priority columns to display if available
        priority_cols = [
            'title', 'solicitationNumber', 'postedDate', 'responseDeadLine',
            'type', 'naicsCode', 'naicsCodes', 'typeOfSetAside',
            'description', 'placeOfPerformance', 'pointOfContact',
            'officeAddress', 'organizationType', 'active'
        ]
        
        self.display_columns = [col for col in priority_cols if col in self.all_columns]
        if not self.display_columns and self.all_columns:
            # Fallback to first 5 columns if priority columns not found
            self.display_columns = self.all_columns[:5]
    
    def load_opportunities(self):
        """Load opportunities from all CSV files in the data directory"""
        try:
            if not self.csv_dir.exists():
                print(f"❌ Directory not found: {self.csv_dir}")
                self.opportunities = []
                return
            
            csv_files = sorted(self.csv_dir.glob("*.csv"))
            
            if not csv_files:
                print(f"❌ No CSV files found in: {self.csv_dir}")
                self.opportunities = []
                return
            
            # Load all CSV files
            file_count = 0
            for csv_file in csv_files:
                try:
                    with open(csv_file, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        records = list(reader)
                        
                        # Track all unique columns across all files
                        if records:
                            self.all_columns = list(set(self.all_columns) | set(records[0].keys()))
                        
                        self.opportunities.extend(records)
                        file_count += 1
                        print(f"  ✓ {csv_file.name}: {len(records)} records")
                
                except Exception as e:
                    print(f"  ⚠ Error loading {csv_file.name}: {e}")
                    continue
            
            # Sort all columns alphabetically for consistent ordering
            self.all_columns.sort()
            
            print(f"\n✓ Loaded {len(self.opportunities)} total opportunities from {file_count} CSV files")
            print(f"✓ Total columns available: {len(self.all_columns)}\n")
        
        except Exception as e:
            print(f"❌ Error loading CSV files: {e}")
            self.opportunities = []
            self.all_columns = []
    

    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*80)
        print(f"SAM.gov OPPORTUNITIES - INTERACTIVE DASHBOARD")
        print(f"📊 Data Source: {self.csv_dir} ({len(self.opportunities)} records)")
        print(f"📋 Available Columns: {len(self.all_columns)}")
        print("="*80)
        print("\nOptions:")
        print("  1. View all opportunities (paginated)")
        print("  2. Search by NAICS code")
        print("  3. Search by agency/organization")
        print("  4. Search by keyword in title")
        print("  5. View selected projects")
        print("  6. Download documents for selected projects")
        print("  7. Clear selection")
        print("  8. Show available columns")
        print("  9. Exit")
        print("\n" + "="*80)
    
    def _format_opportunity(self, opp: Dict, number: int = None) -> str:
        """Format opportunity for display showing available fields"""
        lines = []
        
        if number:
            lines.append(f"{number}. {opp.get('title', 'Untitled')[:70]}")
        else:
            lines.append(f"   {opp.get('title', 'Untitled')[:70]}")
        
        # Show key fields if available
        key_fields = {
            'solicitationNumber': 'Solicitation',
            'postedDate': 'Posted',
            'responseDeadLine': 'Deadline',
            'naicsCode': 'NAICS',
            'type': 'Type',
            'active': 'Status',
            'organizationType': 'Org Type'
        }
        
        for field, label in key_fields.items():
            value = opp.get(field, '')
            if value:
                # Truncate long values
                value_str = str(value)[:50]
                if len(str(value)) > 50:
                    value_str += '...'
                lines.append(f"   {label}: {value_str}")
        
        return '\n'.join(lines)
    
    def view_all_opportunities(self, page=1, per_page=5):
        """Display opportunities with pagination"""
        if not self.opportunities:
            print("❌ No opportunities available")
            return
        
        total = len(self.opportunities)
        total_pages = (total + per_page - 1) // per_page
        
        start = (page - 1) * per_page
        end = min(start + per_page, total)
        
        print(f"\n{'='*80}")
        print(f"OPPORTUNITIES - Page {page} of {total_pages} (showing {end-start} of {total} records)")
        print(f"{'='*80}\n")
        
        for idx, opp in enumerate(self.opportunities[start:end], 1):
            real_idx = start + idx
            print(self._format_opportunity(opp, real_idx))
            print()
        
        if page < total_pages:
            print(f"Type 'next' to see more opportunities")
    
    def search_by_naics(self, naics_code: str) -> List[Dict]:
        """Search opportunities by NAICS code"""
        results = [o for o in self.opportunities 
                  if naics_code.lower() in str(o.get('naicsCode', '')).lower() or
                     naics_code.lower() in str(o.get('naicsCodes', '')).lower()]
        
        print(f"\n{'='*80}")
        print(f"SEARCH RESULTS - NAICS Code: {naics_code}")
        print(f"Found {len(results)} opportunities")
        print(f"{'='*80}\n")
        
        for idx, opp in enumerate(results, 1):
            print(self._format_opportunity(opp, idx))
            print()
        
        return results
    
    def search_by_agency(self, agency: str) -> List[Dict]:
        """Search opportunities by agency/organization"""
        # Check multiple fields for organization info
        org_fields = ['organizationType', 'fullParentPathName', 'officeAddress']
        
        results = []
        for opp in self.opportunities:
            for field in org_fields:
                if agency.lower() in str(opp.get(field, '')).lower():
                    if opp not in results:
                        results.append(opp)
                    break
        
        print(f"\n{'='*80}")
        print(f"SEARCH RESULTS - Organization: {agency}")
        print(f"Found {len(results)} opportunities")
        print(f"{'='*80}\n")
        
        for idx, opp in enumerate(results, 1):
            print(self._format_opportunity(opp, idx))
            print()
        
        return results
    
    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """Search opportunities by title keyword"""
        keyword_lower = keyword.lower()
        results = [o for o in self.opportunities 
                  if keyword_lower in o.get('title', '').lower()]
        
        print(f"\n{'='*80}")
        print(f"SEARCH RESULTS - Keyword: '{keyword}'")
        print(f"Found {len(results)} opportunities")
        print(f"{'='*80}\n")
        
        for idx, opp in enumerate(results, 1):
            print(self._format_opportunity(opp, idx))
            print()
        
        return results
    
    def select_opportunity(self, index: int):
        """Add opportunity to selection"""
        if 0 < index <= len(self.opportunities):
            opp = self.opportunities[index - 1]
            if opp not in self.selected:
                self.selected.append(opp)
                print(f"✓ Selected: {opp.get('title', 'Untitled')[:60]}")
            else:
                print(f"⚠ Already selected: {opp.get('title', 'Untitled')[:60]}")
        else:
            print(f"❌ Invalid selection: {index}")
    
    def view_selected(self):
        """Display selected opportunities"""
        if not self.selected:
            print("\n⚠️  No opportunities selected yet")
            return
        
        print(f"\n{'='*80}")
        print(f"SELECTED OPPORTUNITIES ({len(self.selected)})")
        print(f"{'='*80}\n")
        
        for idx, opp in enumerate(self.selected, 1):
            print(self._format_opportunity(opp, idx))
            print()
    
    def show_available_columns(self):
        """Display all available columns"""
        print(f"\n{'='*80}")
        print(f"AVAILABLE COLUMNS ({len(self.all_columns)} total)")
        print(f"{'='*80}\n")
        
        # Display in columns
        cols_per_row = 3
        for i in range(0, len(self.all_columns), cols_per_row):
            chunk = self.all_columns[i:i+cols_per_row]
            print("  " + " | ".join(f"{col:<25}" for col in chunk))
        
        print(f"\n{'='*80}\n")
    
    def download_selected(self):
        """Download documents for selected opportunities"""
        if not self.selected:
            print("\n❌ No opportunities selected")
            return
        
        print(f"\n{'='*80}")
        print(f"DOWNLOADING DOCUMENTS")
        print(f"{'='*80}\n")
        print(f"📥 Starting download for {len(self.selected)} projects...\n")
        
        downloader = DocumentDownloader(output_dir="downloaded_docs")
        log = downloader.download_documents(self.selected)
        downloader.save_download_log()
        downloader.print_summary()
        
        print("✅ Download complete!")
    
    def clear_selection(self):
        """Clear selected opportunities"""
        self.selected = []
        print("\n✓ Selection cleared")
    
    def run(self):
        """Run the interactive dashboard"""
        if not self.opportunities:
            print("❌ No opportunities available. Please check the data directory.")
            return
        
        page = 1
        
        while True:
            self.display_menu()
            
            choice = input("\nEnter your choice (1-9): ").strip()
            
            if choice == "1":
                self.view_all_opportunities(page=page)
                next_choice = input("\nEnter 'next' for next page, or opportunity number to select: ").strip()
                if next_choice.lower() == "next":
                    page += 1
                else:
                    try:
                        idx = int(next_choice)
                        self.select_opportunity(idx)
                    except ValueError:
                        pass
            
            elif choice == "2":
                naics = input("Enter NAICS code (e.g., 532120): ").strip()
                results = self.search_by_naics(naics)
                if results:
                    try:
                        idx = int(input("Select opportunity number (0 to skip): ").strip())
                        if idx > 0 and idx <= len(results):
                            self.selected.append(results[idx - 1])
                            print(f"✓ Selected: {results[idx - 1].get('title', 'Untitled')[:60]}")
                    except ValueError:
                        pass
            
            elif choice == "3":
                agency = input("Enter organization name (partial match OK): ").strip()
                results = self.search_by_agency(agency)
                if results:
                    try:
                        idx = int(input("Select opportunity number (0 to skip): ").strip())
                        if idx > 0 and idx <= len(results):
                            self.selected.append(results[idx - 1])
                            print(f"✓ Selected: {results[idx - 1].get('title', 'Untitled')[:60]}")
                    except ValueError:
                        pass
            
            elif choice == "4":
                keyword = input("Enter keyword to search in title: ").strip()
                results = self.search_by_keyword(keyword)
                if results:
                    try:
                        idx = int(input("Select opportunity number (0 to skip): ").strip())
                        if idx > 0 and idx <= len(results):
                            self.selected.append(results[idx - 1])
                            print(f"✓ Selected: {results[idx - 1].get('title', 'Untitled')[:60]}")
                    except ValueError:
                        pass
            
            elif choice == "5":
                self.view_selected()
            
            elif choice == "6":
                self.download_selected()
            
            elif choice == "7":
                self.clear_selection()
            
            elif choice == "8":
                self.show_available_columns()
            
            elif choice == "9":
                print("\nGoodbye! 👋\n")
                break
            
            else:
                print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    # Load from data folder
    dashboard = ProjectDashboard(csv_dir="data")
    dashboard.run()
