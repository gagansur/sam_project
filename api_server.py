from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import csv
import json
import re
from datetime import datetime

app = Flask(__name__, template_folder='.', static_folder='.')

# Global data cache
OPPORTUNITIES = []
ALL_COLUMNS = []

def load_csv_data():
    """Load all CSV files from data folder"""
    global OPPORTUNITIES, ALL_COLUMNS
    
    data_dir = Path("data")
    if not data_dir.exists():
        return False
    
    OPPORTUNITIES = []
    ALL_COLUMNS = []
    
    csv_files = sorted(data_dir.glob("*.csv"))
    
    for csv_file in csv_files:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            records = list(reader)
            if records:
                ALL_COLUMNS = list(set(ALL_COLUMNS) | set(records[0].keys()))
                OPPORTUNITIES.extend(records)
    
    ALL_COLUMNS.sort()
    return len(OPPORTUNITIES) > 0

# Load data on startup
load_csv_data()

@app.route('/')
def index():
    """Serve the web dashboard"""
    return render_template('dashboard.html', 
                         total_records=len(OPPORTUNITIES),
                         total_columns=len(ALL_COLUMNS))

@app.route('/api/opportunities', methods=['GET'])
def get_opportunities():
    """Get opportunities with pagination"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    start = (page - 1) * per_page
    end = start + per_page
    
    total = len(OPPORTUNITIES)
    total_pages = (total + per_page - 1) // per_page
    
    return jsonify({
        'data': OPPORTUNITIES[start:end],
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages
    })

@app.route('/api/search', methods=['GET'])
def search():
    """Search opportunities"""
    search_type = request.args.get('type', 'keyword')
    query = request.args.get('query', '').lower()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    results = []
    
    if search_type == 'keyword':
        results = [o for o in OPPORTUNITIES 
                  if query in o.get('title', '').lower()]
    
    elif search_type == 'naics':
        results = [o for o in OPPORTUNITIES 
                  if query in str(o.get('naicsCode', '')).lower() or
                     query in str(o.get('naicsCodes', '')).lower()]
    
    elif search_type == 'organization':
        org_fields = ['organizationType', 'fullParentPathName', 'officeAddress']
        results = []
        for o in OPPORTUNITIES:
            for field in org_fields:
                if query in str(o.get(field, '')).lower():
                    if o not in results:
                        results.append(o)
                    break
    
    total = len(results)
    total_pages = (total + per_page - 1) // per_page
    
    start = (page - 1) * per_page
    end = start + per_page
    
    return jsonify({
        'data': results[start:end],
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'query': query,
        'search_type': search_type
    })

@app.route('/api/columns', methods=['GET'])
def get_columns():
    """Get all available columns"""
    return jsonify({
        'columns': ALL_COLUMNS,
        'total': len(ALL_COLUMNS)
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get data statistics"""
    return jsonify({
        'total_opportunities': len(OPPORTUNITIES),
        'total_columns': len(ALL_COLUMNS),
        'data_files': len(list(Path('data').glob('*.csv'))) if Path('data').exists() else 0
    })

@app.route('/api/documents/<solicitation_number>', methods=['GET'])
def get_documents(solicitation_number):
    """Get available documents for an opportunity"""
    docs_dir = Path('downloaded_docs')
    documents = []
    
    if not docs_dir.exists():
        return jsonify({'documents': [], 'total': 0})
    
    # Look for description file
    descriptions_dir = docs_dir / 'descriptions'
    if descriptions_dir.exists():
        for file in descriptions_dir.glob('*.txt'):
            # Check if this file matches the solicitation number
            if solicitation_number in file.name:
                documents.append({
                    'name': file.name,
                    'type': 'text',
                    'size': file.stat().st_size,
                    'path': f'/download/document/{file.name}'
                })
    
    # Look for attachment files
    attachments_dir = docs_dir / 'attachments'
    if attachments_dir.exists():
        for file in attachments_dir.glob('*'):
            if file.is_file() and solicitation_number in file.name:
                ext = file.suffix.lower()
                doc_type = 'pdf' if ext == '.pdf' else 'document' if ext in ['.docx', '.doc'] else 'file'
                documents.append({
                    'name': file.name,
                    'type': doc_type,
                    'size': file.stat().st_size,
                    'path': f'/download/document/{file.name}'
                })
    
    return jsonify({
        'documents': documents,
        'total': len(documents),
        'solicitation': solicitation_number
    })

@app.route('/api/documents', methods=['GET'])
def list_all_documents():
    """List all available documents"""
    docs_dir = Path('downloaded_docs')
    documents = []
    
    if not docs_dir.exists():
        return jsonify({'documents': [], 'total': 0})
    
    # Get all description files
    descriptions_dir = docs_dir / 'descriptions'
    if descriptions_dir.exists():
        for file in descriptions_dir.glob('*.txt'):
            documents.append({
                'name': file.name,
                'type': 'description',
                'size': file.stat().st_size,
                'path': f'/download/document/{file.name}'
            })
    
    # Get all attachment files
    attachments_dir = docs_dir / 'attachments'
    if attachments_dir.exists():
        for file in attachments_dir.glob('*'):
            if file.is_file():
                ext = file.suffix.lower()
                doc_type = 'pdf' if ext == '.pdf' else 'docx' if ext == '.docx' else 'doc' if ext == '.doc' else 'attachment'
                documents.append({
                    'name': file.name,
                    'type': doc_type,
                    'size': file.stat().st_size,
                    'path': f'/download/document/{file.name}'
                })
    
    return jsonify({
        'documents': documents,
        'total': len(documents)
    })

@app.route('/download/document/<filename>', methods=['GET'])
def download_document(filename):
    """Download a document file"""
    docs_dir = Path('downloaded_docs')
    
    # Security: prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        return jsonify({'error': 'Invalid filename'}), 400
    
    # Try to find file in descriptions or attachments
    descriptions_file = docs_dir / 'descriptions' / filename
    attachments_file = docs_dir / 'attachments' / filename
    
    file_path = None
    if descriptions_file.exists():
        file_path = descriptions_file
    elif attachments_file.exists():
        file_path = attachments_file
    
    if file_path and file_path.is_file():
        return send_from_directory(file_path.parent, file_path.name, as_attachment=True)
    
    return jsonify({'error': 'Document not found'}), 404

@app.route('/api/download-docs', methods=['POST'])
def download_docs():
    """Download documents from SAM.gov for an opportunity"""
    try:
        data = request.get_json()
        # Handle both direct opportunity object and wrapped format
        opportunity = data if isinstance(data, dict) and 'solicitationNumber' in data else data.get('opportunity', {})
        
        if not opportunity:
            return jsonify({
                'success': False,
                'error': 'No opportunity provided',
                'message': 'Missing opportunity data in request'
            }), 400
        
        # Import and use DocumentDownloader
        from document_downloader import DocumentDownloader
        from config import API_KEY
        
        solicitation_number = opportunity.get('solicitationNumber', '')
        if not solicitation_number:
            return jsonify({
                'success': False,
                'error': 'No solicitation number',
                'message': 'The opportunity must have a solicitationNumber'
            }), 400
        
        # Initialize downloader
        downloader = DocumentDownloader(output_dir='downloaded_docs', api_key=API_KEY)
        
        # Fetch detailed opportunity info from SAM.gov
        try:
            print(f"[DEBUG] Fetching opportunity details for: {solicitation_number}")
            opp_details = downloader.get_opportunity_details(solicitation_number)
            
            if not opp_details:
                return jsonify({
                    'success': False,
                    'message': 'Could not fetch opportunity details from SAM.gov. The solicitation number may be invalid or the opportunity may no longer be available.',
                    'solicitation': solicitation_number,
                    'debug': 'get_opportunity_details returned None'
                }), 400
            
            print(f"[DEBUG] Successfully fetched details for {solicitation_number}")
            
            # Save description
            desc_saved = downloader.save_description(opp_details)
            print(f"[DEBUG] Description saved: {desc_saved}")
            
            # Try to download attachments if they exist
            attachments_downloaded = 0
            if 'attachments' in opp_details and opp_details['attachments']:
                print(f"[DEBUG] Found {len(opp_details['attachments'])} attachments")
                for attachment in opp_details.get('attachments', []):
                    if 'url' in attachment:
                        filename = attachment.get('filename', f"attachment_{attachments_downloaded}")
                        if downloader.download_attachment(attachment['url'], solicitation_number, filename):
                            attachments_downloaded += 1
                            print(f"[DEBUG] Downloaded attachment: {filename}")
            
            # Save download log
            downloader.save_download_log()
            
            print(f"[DEBUG] Download complete for {solicitation_number}: {attachments_downloaded} attachments")
            
            return jsonify({
                'success': True,
                'message': f'Successfully downloaded documents for {solicitation_number}',
                'solicitation': solicitation_number,
                'description_saved': desc_saved,
                'attachments_downloaded': attachments_downloaded,
                'log_location': 'downloaded_docs/download_log.json'
            })
            
        except Exception as e:
            import traceback
            print(f"[ERROR] Exception in download_docs: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': str(e),
                'message': f'Error downloading from SAM.gov: {str(e)}',
                'solicitation': solicitation_number,
                'debug': traceback.format_exc()
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to process download request'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_opportunity():
    """Analyze opportunity for bidding and generate guidance document"""
    try:
        data = request.get_json()
        opportunity = data.get('opportunity', {})
        
        if not opportunity:
            return jsonify({'error': 'No opportunity provided'}), 400
        
        # Analyze the opportunity
        analysis = analyze_for_bidding(opportunity)
        
        # Generate bidding document
        bidding_doc = generate_bidding_document(opportunity, analysis)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'bidding_document': bidding_doc
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def analyze_for_bidding(opportunity):
    """Analyze opportunity for RFI/RFQ/RFP type and bidding requirements"""
    title = opportunity.get('title', '').lower()
    description = opportunity.get('description', '').lower()
    combined_text = f"{title} {description}"
    
    # Detect document type
    doc_type = "Solicitation"
    if any(kw in combined_text for kw in ['rfi', 'request for information']):
        doc_type = "RFI (Request for Information)"
    elif any(kw in combined_text for kw in ['rfq', 'request for quote', 'quotation']):
        doc_type = "RFQ (Request for Quote)"
    elif any(kw in combined_text for kw in ['rfp', 'request for proposal']):
        doc_type = "RFP (Request for Proposal)"
    
    # Extract key information
    solicitation_number = opportunity.get('solicitationNumber', 'N/A')
    posted_date = opportunity.get('postedDate', 'N/A')
    deadline = opportunity.get('responseDeadLine', 'N/A')
    org_type = opportunity.get('organizationType', 'N/A')
    naics = opportunity.get('naicsCode', 'N/A')
    
    # Calculate days until deadline
    days_until_deadline = "N/A"
    if deadline and deadline != 'N/A':
        try:
            from datetime import datetime, timedelta
            deadline_date = datetime.strptime(deadline, '%m/%d/%Y')
            days_until = (deadline_date - datetime.now()).days
            days_until_deadline = f"{days_until} days" if days_until > 0 else "EXPIRED"
        except:
            pass
    
    # Detect set-asides and special requirements
    set_aside = opportunity.get('typeOfSetAside', 'Open to All')
    set_aside_desc = opportunity.get('typeOfSetAsideDescription', '')
    
    # Identify potential competitors and concerns
    concerns = []
    if 'women' in combined_text:
        concerns.append("Women-owned business considerations")
    if 'small' in combined_text and 'business' in combined_text:
        concerns.append("Small business certifications required")
    if 'minority' in combined_text or 'mbe' in combined_text:
        concerns.append("Minority business enterprise certifications")
    if 'security clearance' in combined_text:
        concerns.append("Security clearance requirements")
    if 'secret' in combined_text or 'top secret' in combined_text:
        concerns.append("Classified work - high security requirements")
    
    return {
        'document_type': doc_type,
        'solicitation_number': solicitation_number,
        'posted_date': posted_date,
        'deadline': deadline,
        'days_until_deadline': days_until_deadline,
        'organization_type': org_type,
        'naics_code': naics,
        'set_aside_type': set_aside,
        'set_aside_description': set_aside_desc,
        'special_considerations': concerns if concerns else ['Standard competition']
    }

def generate_bidding_document(opportunity, analysis):
    """Generate a starting bidding document/proposal template"""
    
    title = opportunity.get('title', 'Untitled Opportunity')
    description = opportunity.get('description', '')
    
    doc = {
        'title': f"Bidding Strategy Document - {title}",
        'timestamp': datetime.now().strftime('%B %d, %Y'),
        'sections': {}
    }
    
    # 1. Executive Summary
    doc['sections']['Executive Summary'] = f"""
This bidding strategy document outlines our approach to respond to the {analysis['document_type']}.

Opportunity: {title}
Solicitation Number: {analysis['solicitation_number']}
Organization Type: {analysis['organization_type']}
Posted: {analysis['posted_date']}
Deadline: {analysis['deadline']} ({analysis['days_until_deadline']})
"""
    
    # 2. Opportunity Analysis
    doc['sections']['Opportunity Analysis'] = f"""
Document Type: {analysis['document_type']}
NAICS Code: {analysis['naics_code']}
Set-Aside Type: {analysis['set_aside_type']}

Opportunity Description:
{description[:500]}{'...' if len(description) > 500 else ''}

Key Considerations:
{chr(10).join([f"• {concern}" for concern in analysis['special_considerations']])}
"""
    
    # 3. Competitive Assessment
    doc['sections']['Competitive Assessment'] = """
1. Company Fit Analysis
   - Assess alignment with NAICS code requirements
   - Review technical capabilities match
   - Evaluate relevant past performance
   - Identify key wins and losses factors

2. Team Assembly
   - Identify key personnel needs
   - Assess availability of specialized skills
   - Plan subcontractor partnerships if needed

3. Risk Analysis
   - Bid/no-bid decision criteria
   - Identify technical risks
   - Evaluate resource constraints
   - Assess Win probability
"""
    
    # 4. Proposal Strategy
    doc['sections']['Proposal Strategy'] = """
Response Strategy:
1. Understand the customer's problem and how we solve it
2. Highlight differentiation and past performance
3. Show resource availability and commitment
4. Demonstrate compliance with all requirements
5. Address evaluation criteria directly

Key Proposal Elements:
• Executive Summary (2-3 pages)
• Company Background and Qualifications
• Relevant Experience and Past Performance
• Team Structure and Key Personnel
• Technical Approach and Methodology
• Project Timeline and Milestones
• Cost Estimate and Budget Justification
• Compliance Statement
"""
    
    # 5. Action Plan
    doc['sections']['Action Plan'] = f"""
Timeline to Response Deadline: {analysis['days_until_deadline']}

Key Milestones:
□ Day 1-2: Assemble bid team and conduct kickoff
□ Day 2-3: Detailed opportunity analysis and requirements mapping
□ Day 3-4: Draft proposal sections concurrently
□ Day 4-5: Internal review and quality checks
□ Day 5-6: Address review comments and finalize
□ Day 6-7: Final proofreading and submission preparation

Critical Review Points:
- Compliance checklist against RFP requirements
- Relevance of examples to customer needs
- Cost reasonableness and accuracy
- Proposal graphics and formatting
- Executive summary effectiveness
"""
    
    # 6. Resource Requirements
    doc['sections']['Resource Requirements'] = """
Personnel:
- Proposal Manager: Oversee response preparation
- Technical Writer(s): Draft proposal sections
- Subject Matter Experts: Provide technical content
- Graphics Designer: Create visuals and charts
- Editor/Proofreader: Quality assurance
- Finance Lead: Cost estimate development

Tools:
- Word processing for proposal document
- Graphics tools for charts and diagrams
- Project management tool for coordination
- Document collaboration platform (if team-based)
"""
    
    # 7. Success Criteria
    doc['sections']['Success Criteria'] = """
Proposal Should:
✓ Directly address all evaluation criteria
✓ Demonstrate clear understanding of requirements
✓ Show specific, relevant past performance
✓ Highlight competitive advantages
✓ Present realistic and well-justified costs
✓ Be compliant with all formatting requirements
✓ Be submitted before deadline
✓ Include all required attachments

Win Factors:
1. Technical approach superior to competitors
2. Stronger relevant past performance
3. Better team qualifications
4. Cost advantage with quality maintained
5. Better understanding of customer needs
"""
    
    # 8. Next Steps
    doc['sections']['Next Steps'] = f"""
Immediate Actions:
1. ✓ Schedule bid team kickoff meeting
2. ✓ Assign proposal roles and responsibilities
3. ✓ Create detailed outline/storyboard
4. ✓ Establish review schedule and checkpoints
5. ✓ Determine resource needs and constraints
6. ✓ Set up document sharing and collaboration

Preparation:
- Gather relevant past performance examples
- Prepare team resumes and qualifications
- Develop cost estimate parameters
- Review similar past proposals
- Identify subcontractor partners if needed

Timeline: {analysis['days_until_deadline']} to complete response
"""
    
    return doc

if __name__ == "__main__":
    print(f"✓ Loaded {len(OPPORTUNITIES)} opportunities from CSV files")
    print(f"✓ {len(ALL_COLUMNS)} columns available")
    print(f"\n🌐 Starting web server on http://localhost:5000")
    print(f"📊 Open your browser and go to http://localhost:5000")
    app.run(debug=True, port=5000)
