# SAM.gov Opportunities Project

A comprehensive system for searching, browsing, and analyzing federal opportunities from SAM.gov with intelligent filtering and document management.

## 🚀 Quick Start

### Prerequisites
- Python 3.14+
- Virtual environment (`.venv`)

### Installation
```bash
# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Project

#### 1. Fetch Data
```bash
python main.py
```
This fetches IT opportunities from SAM.gov API and saves to CSV files in the `data/` folder.

#### 2. Browse Opportunities (CLI)
```bash
python dashboard.py
```
Interactive dashboard to search, filter, and select opportunities.

#### 3. Web Dashboard (Recommended)
```bash
python api_server.py
```
Modern web interface with search, filtering, and **Bidding Strategy Generator**.
Open browser to: http://localhost:5000

#### 4. Analyze RFI/RFQ/RFP
```bash
python rfi_rfq_rfp_checker.py
```
Analyze and filter opportunities by document type (RFI, RFQ, RFP).

## 📊 Features

### Data Source: CSV Files
- **Location**: `data/` folder
- **Files**: 19 CSV files (sam_results_extended_1.csv through sam_results_extended_19.csv)
- **Records**: 1,900+ opportunities
- **Columns**: 27 dynamic fields

### Dashboard Features

**Web Dashboard (Recommended):**
1. 🔍 **Search** - By keyword, NAICS code, or organization
2. 📋 **Browse** - Paginated view of 1,900+ opportunities
3. 📊 **View Columns** - See all 27 available data fields
4. 🔗 **Direct Links** - Open opportunities on SAM.gov
5. 📈 **Statistics** - Total records, columns, and files
6. 🎯 **Bidding Strategy** - Auto-generate proposal strategies
   - Document type detection (RFI/RFQ/RFP)
   - Deadline tracking
   - Special requirements analysis
   - Multi-section strategy document
   - Download as text file

**CLI Dashboard:**
1. **View Opportunities** - Paginated browsing with smart formatting
2. **Search by NAICS** - Find by North American Industry Classification
3. **Search by Organization** - Filter by agency/organization name
4. **Search by Keyword** - Find opportunities in title
5. **Select Projects** - Multi-select for batch operations
6. **Download Documents** - Download opportunity descriptions
7. **View Columns** - See all available data fields

### RFI/RFQ/RFP Analysis
- Identifies document type from title/description
- Categorizes opportunities by type
- Generates statistics and reports
- Exports to CSV for analysis

## 📁 Project Structure

```
sam_project/
├── main.py                          # Fetch data from SAM.gov API
├── dashboard.py                     # Interactive browsing dashboard
├── rfi_rfq_rfp_checker.py          # Document type analyzer
├── sam_api.py                       # SAM.gov API wrapper (generator)
├── storage.py                       # CSV file operations
├── document_downloader.py           # Download opportunity docs
├── config.py                        # Configuration (API key, settings)
├── data/                            # CSV data files (1,900 records)
├── downloaded_docs/                 # Downloaded documents
│   ├── descriptions/                # Opportunity descriptions
│   ├── attachments/                 # Attachments
│   └── download_log.json            # Download tracking
├── README.md                        # This file
├── DASHBOARD_CSV_ONLY.md            # Dashboard documentation
├── DASHBOARD_MULTI_FILE.md          # Multi-file loading info
└── GENERATOR_IMPLEMENTATION.md      # API streaming implementation
```

## 🔧 Configuration

Edit `config.py`:
```python
API_KEY = "your-api-key"           # SAM.gov API key
DEFAULT_DAYS = 30                   # Search range (days)
DEFAULT_LIMIT = 100                 # Records per API page
```

## 💾 Data Files

### Input: CSV Files
- Location: `data/` folder
- Format: Standard CSV with headers
- Columns: title, solicitationNumber, postedDate, responseDeadLine, naicsCode, type, etc.

### Output: Downloaded Documents
- Location: `downloaded_docs/`
- Structure:
  ```
  downloaded_docs/
  ├── descriptions/       # Opportunity descriptions as text files
  ├── attachments/        # Downloadable attachments
  └── download_log.json   # Metadata and tracking
  ```

## 🔍 Search Examples

### By NAICS Code
```
Enter NAICS code: 532120
Found 50 opportunities
```

### By Organization
```
Enter organization name: DEFENSE
Found 45 opportunities related to Department of Defense
```

### By Keyword
```
Enter keyword: software
Found 120 opportunities with "software" in title
```

## 📋 Available Data Fields

The dashboard supports 27 columns across all CSV files:

**Core Fields:**
- title - Opportunity title
- solicitationNumber - SAM.gov solicitation number
- postedDate - Date posted
- responseDeadLine - Response deadline
- naicsCode, naicsCodes - Industry classification

**Document Info:**
- type - Opportunity type
- typeOfSetAside - Set-aside classification
- typeOfSetAsideDescription - Detailed set-aside info

**Organization:**
- organizationType - Organization type
- fullParentPathName - Full organizational path
- officeAddress - Office address

**Additional:**
- active - Active status
- description - Full opportunity description
- pointOfContact - Contact information
- resourceLinks - Related resources
- And 12+ more fields...

## 🎯 Common Tasks

### Task 1: Generate Bidding Strategy (Web Dashboard)
```bash
python api_server.py
# Open: http://localhost:5000
# 1. Search for opportunity
# 2. Click "Generate Bidding Strategy"
# 3. Review automated proposal roadmap
# 4. Download as text document
```

This generates:
- ✅ Document type analysis (RFI/RFQ/RFP)
- ✅ Deadline tracking and timeline
- ✅ Special requirements identification
- ✅ 8-section proposal strategy
- ✅ Action plan with milestones
- ✅ Resource requirements
- ✅ Success criteria checklist

### Task 2: Find All Defense Opportunities
```bash
python dashboard.py
# Option 3: Search by agency/organization
# Enter: DEFENSE
```

### Task 3: Identify RFI/RFQ/RFP
```bash
python rfi_rfq_rfp_checker.py
# Shows statistics and breakdown by document type
```

### Task 4: Download Selected Documents
```bash
python dashboard.py
# Option 1: View opportunities
# Select items (multiple)
# Option 6: Download documents
```

## ⚙️ Technical Details

### API Integration (main.py)
- Uses generator pattern for memory efficiency
- Streams data in 100-record batches
- Saves incrementally to avoid data loss
- Handles timeouts and errors gracefully

### CSV Processing
- Multi-file aggregation in `dashboard.py`
- Dynamic column discovery
- Intelligent field selection for display
- Efficient in-memory searching

### Document Analysis (rfi_rfq_rfp_checker.py)
- Keyword-based classification
- Case-insensitive matching
- Multi-field analysis (title + description)
- Statistical reporting

## 📊 Statistics

- **Total Opportunities**: 1,900+
- **Data Files**: 19 CSV files
- **Columns Available**: 27 fields
- **Load Time**: 1-2 seconds
- **Memory Usage**: ~50-100 MB

## 🚨 Troubleshooting

### No data in dashboard
```bash
# Ensure data folder has CSV files
ls data/
# Should show: sam_results_extended_1.csv, etc.
```

### API timeout when fetching
```bash
# Check internet connection
# Verify API key in config.py
# Try running again (can resume from where it stopped)
```

### Can't find a column
```bash
# Option 8 in dashboard shows all available columns
# Not all columns exist in all records
```

## 📝 Files Documentation

- **main.py** - Fetch opportunities from SAM.gov, save to CSV
- **dashboard.py** - Interactive dashboard for browsing (CSV files only)
- **rfi_rfq_rfp_checker.py** - Analyze by document type
- **sam_api.py** - SAM.gov API wrapper with streaming
- **storage.py** - CSV file operations and formatting
- **document_downloader.py** - Download and organize documents
- **config.py** - Configuration and settings

## 🔐 Security

- API key in `config.py` (not committed to repo)
- No sensitive data in CSV exports
- Document downloads are local only
- Standard HTTPS for API calls

## 📈 Performance

- Loads 1,900 records in ~1-2 seconds
- Searches complete instantly
- Minimal memory footprint (~50-100 MB)
- Efficient CSV parsing with built-in csv module

## ✅ Version History

**Current**: CSV-only dashboard with multi-file support
- Removed database dependency
- Streamlined for file-based operations
- Generator-based API streaming
- Dynamic column detection

## 🤝 Contributing

To add new features:
1. Edit relevant module (main.py, dashboard.py, etc.)
2. Test with existing data
3. Update README if needed

## 📞 Support

For issues with:
- **SAM.gov API**: Check config.py API key
- **Dashboard**: Ensure CSV files in data/ folder
- **Downloads**: Check downloaded_docs/ folder permissions

