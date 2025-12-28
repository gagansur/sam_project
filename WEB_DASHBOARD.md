# Web Dashboard Setup

## Starting the Web Server

```bash
python api_server.py
```

The web dashboard will be available at: **http://localhost:5000**

## Features

### 🔍 Search
- **Keyword Search** - Find opportunities by title
- **NAICS Code Search** - Filter by industry classification
- **Organization Search** - Find by organization/agency name

### 📊 Browse
- **Paginated View** - 10 records per page
- **All Opportunities** - View complete dataset
- **Intelligent Formatting** - Shows available data for each record

### 📋 Data Info
- **View All Columns** - See 27 available data fields
- **Statistics** - Total records, columns, data files
- **Dynamic Display** - Shows relevant fields per record

## Data Source

The web dashboard loads the same CSV files as the CLI dashboard:
- **Location**: `data/` folder
- **Files**: 19 CSV files
- **Records**: 1,900+ opportunities
- **Columns**: 27 available fields

## API Endpoints

### `GET /` 
Serves the web dashboard HTML

### `GET /api/opportunities`
Get paginated opportunities
```
Parameters:
- page: Page number (default: 1)
- per_page: Records per page (default: 10)

Response:
{
  "data": [...],
  "page": 1,
  "per_page": 10,
  "total": 1900,
  "total_pages": 190
}
```

### `GET /api/search`
Search opportunities
```
Parameters:
- type: 'keyword', 'naics', or 'organization'
- query: Search term
- page: Page number (default: 1)
- per_page: Records per page (default: 10)

Response:
{
  "data": [...],
  "page": 1,
  "per_page": 10,
  "total": 50,
  "total_pages": 5,
  "query": "software",
  "search_type": "keyword"
}
```

### `GET /api/columns`
Get all available columns
```
Response:
{
  "columns": ["title", "solicitationNumber", ...],
  "total": 27
}
```

### `GET /api/stats`
Get dataset statistics
```
Response:
{
  "total_opportunities": 1900,
  "total_columns": 27,
  "data_files": 19
}
```

## Browser Compatibility

Works on all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## Performance

- **Load Time**: ~1-2 seconds for 1,900 records
- **Search**: Instant results
- **Responsive**: Mobile-friendly design

## Features Comparison

| Feature | CLI Dashboard | Web Dashboard |
|---------|--------------|---------------|
| View Opportunities | ✅ | ✅ |
| Pagination | ✅ | ✅ |
| Keyword Search | ✅ | ✅ |
| NAICS Search | ✅ | ✅ |
| Organization Search | ✅ | ✅ |
| View Columns | ✅ | ✅ |
| Multi-Select | ✅ | - |
| Download Docs | ✅ | - |
| Mobile Friendly | ❌ | ✅ |
| No Installation | ❌ | ✅ |

## Common Tasks

### View All Opportunities
1. Open http://localhost:5000
2. Click "View All" or wait for automatic load

### Search by Keyword
1. Select "Keyword" in search dropdown
2. Enter search term (e.g., "software")
3. Click "Search"

### Search by NAICS Code
1. Select "NAICS Code" in search dropdown
2. Enter NAICS code (e.g., "532120")
3. Click "Search"

### View Available Columns
1. Click "Columns" tab
2. Click "Show All Columns"
3. See list of 27 available fields

## Troubleshooting

### Server won't start
```bash
# Check if port 5000 is available
# Or change port in api_server.py
app.run(debug=True, port=5001)
```

### No data loading
```bash
# Ensure data folder exists with CSV files
ls data/
# Should show: sam_results_extended_1.csv, etc.
```

### Slow performance
```bash
# Check available memory
# Large dataset (1,900 records) loads on startup
# First load may take 2-3 seconds
```

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the Flask server.

