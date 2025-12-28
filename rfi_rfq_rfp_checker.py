#!/usr/bin/env python
"""
RFI/RFQ/RFP Checker and Analyzer
Searches SAM.gov for Request for Information, Request for Quote, and Request for Proposal documents
"""

import sqlite3
from typing import List, Dict, Tuple
from datetime import datetime


class RFIRFQRFPChecker:
    """Check for RFI, RFQ, and RFP documents in opportunities"""
    
    # Keywords to identify document types
    RFI_KEYWORDS = ["rfi", "request for information", "information request"]
    RFQ_KEYWORDS = ["rfq", "request for quote", "request for quotation", "quotation"]
    RFP_KEYWORDS = ["rfp", "request for proposal", "proposal request"]
    
    def __init__(self, db_file="sam_opportunities.db"):
        """Initialize the checker"""
        self.db_file = db_file
        self.opportunities = []
        self.load_opportunities()
    
    def load_opportunities(self):
        """Load opportunities from database"""
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            
            c.execute("""
                SELECT id, title, solicitationNumber, agency, type, description, 
                       postedDate, naics, opportunityStatus, link
                FROM opportunities 
                ORDER BY postedDate DESC
            """)
            
            for row in c.fetchall():
                self.opportunities.append(dict(row))
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error loading database: {e}")
            self.opportunities = []
    
    def check_document_type(self, text: str) -> Tuple[str, str]:
        """
        Check if text contains RFI, RFQ, or RFP keywords
        Returns tuple of (document_type, keyword_found)
        """
        if not text:
            return ("Unknown", "")
        
        text_lower = text.lower()
        
        # Check in order of specificity (RFP first as it's most common)
        for keyword in self.RFP_KEYWORDS:
            if keyword in text_lower:
                return ("RFP", keyword.upper())
        
        for keyword in self.RFQ_KEYWORDS:
            if keyword in text_lower:
                return ("RFQ", keyword.upper())
        
        for keyword in self.RFI_KEYWORDS:
            if keyword in text_lower:
                return ("RFI", keyword.upper())
        
        return ("Solicitation", "")
    
    def filter_by_document_type(self, doc_type: str) -> List[Dict]:
        """Filter opportunities by document type (RFI, RFQ, RFP, or Solicitation)"""
        results = []
        
        for opp in self.opportunities:
            # Check title and description
            combined_text = f"{opp.get('title', '')} {opp.get('description', '')}"
            found_type, keyword = self.check_document_type(combined_text)
            
            if found_type.upper() == doc_type.upper():
                results.append({
                    **opp,
                    "document_type": found_type,
                    "keyword_match": keyword
                })
        
        return results
    
    def get_all_document_types(self) -> Dict[str, List[Dict]]:
        """Get all opportunities grouped by document type"""
        rfi_docs = self.filter_by_document_type("RFI")
        rfq_docs = self.filter_by_document_type("RFQ")
        rfp_docs = self.filter_by_document_type("RFP")
        others = self.filter_by_document_type("Solicitation")
        
        return {
            "RFI": rfi_docs,
            "RFQ": rfq_docs,
            "RFP": rfp_docs,
            "Other Solicitations": others
        }
    
    def print_summary(self):
        """Print summary of document types found"""
        doc_types = self.get_all_document_types()
        
        print("\n" + "=" * 80)
        print("RFI/RFQ/RFP ANALYSIS SUMMARY")
        print("=" * 80 + "\n")
        
        print(f"Total Opportunities: {len(self.opportunities)}\n")
        
        for doc_type, docs in doc_types.items():
            print(f"{doc_type}: {len(docs)} opportunities")
            
            if docs:
                print(f"  Examples:")
                for doc in docs[:3]:
                    print(f"    - {doc['title'][:60]}")
                    print(f"      Solicitation: {doc['solicitationNumber']}")
                    print(f"      Agency: {doc['agency']}")
                    if doc.get('keyword_match'):
                        print(f"      Match: {doc['keyword_match']}")
                    print()
        
        print("=" * 80 + "\n")
    
    def print_detailed_report(self, doc_type: str = None):
        """Print detailed report for specific document type"""
        if doc_type:
            docs = self.filter_by_document_type(doc_type)
            title = f"{doc_type} OPPORTUNITIES"
        else:
            docs = self.opportunities
            title = "ALL OPPORTUNITIES"
        
        print("\n" + "=" * 80)
        print(f"{title} - DETAILED REPORT")
        print("=" * 80 + "\n")
        
        print(f"Total: {len(docs)} opportunities\n")
        
        for idx, doc in enumerate(docs, 1):
            document_type, keyword = self.check_document_type(
                f"{doc['title']} {doc.get('description', '')}"
            )
            
            print(f"{idx}. {doc['title']}")
            print(f"   Solicitation #: {doc['solicitationNumber']}")
            print(f"   Agency: {doc['agency']}")
            print(f"   Type: {document_type}")
            if keyword:
                print(f"   Keyword Match: {keyword}")
            print(f"   Status: {doc.get('opportunityStatus', 'Unknown')}")
            print(f"   Posted: {doc['postedDate']}")
            print(f"   NAICS: {doc.get('naics', 'N/A')}")
            print()
    
    def export_to_csv(self, filename: str = "rfi_rfq_rfp_report.csv"):
        """Export document type analysis to CSV"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'solicitationNumber', 'title', 'agency', 'document_type',
                'postedDate', 'opportunityStatus', 'naics', 'keyword_match'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for opp in self.opportunities:
                combined_text = f"{opp.get('title', '')} {opp.get('description', '')}"
                doc_type, keyword = self.check_document_type(combined_text)
                
                writer.writerow({
                    'solicitationNumber': opp.get('solicitationNumber', ''),
                    'title': opp.get('title', '')[:100],
                    'agency': opp.get('agency', ''),
                    'document_type': doc_type,
                    'postedDate': opp.get('postedDate', ''),
                    'opportunityStatus': opp.get('opportunityStatus', ''),
                    'naics': opp.get('naics', ''),
                    'keyword_match': keyword
                })
        
        print(f"\n✓ Report exported to {filename}")
    
    def get_statistics(self) -> Dict:
        """Get statistics about document types"""
        doc_types = self.get_all_document_types()
        
        total = len(self.opportunities)
        
        return {
            "total": total,
            "rfi_count": len(doc_types["RFI"]),
            "rfq_count": len(doc_types["RFQ"]),
            "rfp_count": len(doc_types["RFP"]),
            "other_count": len(doc_types["Other Solicitations"]),
            "rfi_percentage": (len(doc_types["RFI"]) / total * 100) if total > 0 else 0,
            "rfq_percentage": (len(doc_types["RFQ"]) / total * 100) if total > 0 else 0,
            "rfp_percentage": (len(doc_types["RFP"]) / total * 100) if total > 0 else 0,
            "other_percentage": (len(doc_types["Other Solicitations"]) / total * 100) if total > 0 else 0,
        }


def interactive_rfi_rfq_rfp_checker():
    """Interactive CLI for RFI/RFQ/RFP checking"""
    checker = RFIRFQRFPChecker()
    
    if not checker.opportunities:
        print("❌ No opportunities found in database")
        print("Please run main.py first to fetch data")
        return
    
    while True:
        print("\n" + "=" * 80)
        print("RFI/RFQ/RFP CHECKER - INTERACTIVE MENU")
        print("=" * 80)
        print("\nOptions:")
        print("  1. View summary of document types")
        print("  2. View all RFI (Request for Information)")
        print("  3. View all RFQ (Request for Quote)")
        print("  4. View all RFP (Request for Proposal)")
        print("  5. View other solicitations")
        print("  6. View statistics")
        print("  7. Export to CSV")
        print("  8. Exit")
        print("\n" + "=" * 80)
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            checker.print_summary()
        
        elif choice == "2":
            checker.print_detailed_report("RFI")
        
        elif choice == "3":
            checker.print_detailed_report("RFQ")
        
        elif choice == "4":
            checker.print_detailed_report("RFP")
        
        elif choice == "5":
            checker.print_detailed_report("Solicitation")
        
        elif choice == "6":
            stats = checker.get_statistics()
            print("\n" + "=" * 80)
            print("DOCUMENT TYPE STATISTICS")
            print("=" * 80 + "\n")
            print(f"Total Opportunities: {stats['total']}")
            print(f"\nRFI: {stats['rfi_count']} ({stats['rfi_percentage']:.1f}%)")
            print(f"RFQ: {stats['rfq_count']} ({stats['rfq_percentage']:.1f}%)")
            print(f"RFP: {stats['rfp_count']} ({stats['rfp_percentage']:.1f}%)")
            print(f"Other: {stats['other_count']} ({stats['other_percentage']:.1f}%)")
            print("\n" + "=" * 80)
        
        elif choice == "7":
            filename = input("Enter filename (default: rfi_rfq_rfp_report.csv): ").strip()
            if not filename:
                filename = "rfi_rfq_rfp_report.csv"
            checker.export_to_csv(filename)
        
        elif choice == "8":
            print("\nGoodbye! 👋\n")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    interactive_rfi_rfq_rfp_checker()
