# SAM.gov Document Download Feature

## Overview

The SAM.gov Document Download feature allows you to download opportunity documents directly from SAM.gov through the web dashboard and save them to your local `downloaded_docs/` folder.

## How to Use

### Step 1: Open the Dashboard
Navigate to `http://localhost:5000` in your web browser.

### Step 2: Find an Opportunity
- Browse the opportunity list
- Use the search functionality to find specific opportunities
- Filter by NAICS code, status, or other criteria

### Step 3: Download Documents
For any opportunity, click the **"⬇️ Download from SAM.gov"** button:

```
[⬇️ Download from SAM.gov] [📋 Bidding Strategy] [📥 Documents]
```

### Step 4: Monitor Download Progress
A modal will appear showing:
- Loading message: "Downloading documents from SAM.gov..."
- Progress indicator while the system fetches and saves files

### Step 5: View Results
Once complete, the modal shows:

**Success Result:**
```
✅ Download Complete!
   Solicitation: [Number]
   Description: ✓ Saved
   Attachments: [Count]
   
   📁 Documents saved to: downloaded_docs/
```

**Error Result:**
```
❌ Download Failed
   Error: [Error message]
   
   Troubleshooting:
   - Verify your SAM.gov API key in config.py
   - Check your internet connection
   - Ensure the opportunity number is correct
   - Verify the downloaded_docs folder exists and is writable
```

## File Structure

Documents are saved in the following structure:

```
downloaded_docs/
├── descriptions/
│   ├── {solicitation_number}_description.txt
│   ├── {solicitation_number}_description.txt
│   └── ...
├── attachments/
│   ├── {filename}.pdf
│   ├── {filename}.docx
│   └── ...
└── download_log.json
```

### Description Files
Text files containing the opportunity description downloaded from SAM.gov.

### Attachments
Original files (PDF, DOCX, etc.) attached to the opportunity on SAM.gov.

### Download Log
JSON file tracking all downloaded documents with timestamps.

## View Downloaded Documents

After downloading, you can view the saved documents by clicking **"📥 Documents"** button on the same opportunity card. This will show all downloaded attachments and allow you to download them to your computer.

## Requirements

1. **SAM.gov API Key**: Set `API_KEY` in `config.py`
   ```python
   API_KEY = "your_sam_gov_api_key_here"
   ```

2. **Folder Permissions**: Ensure the `downloaded_docs/` folder exists and is writable

3. **Internet Connection**: Required to fetch documents from SAM.gov

## Configuration

Edit `config.py` to configure the download behavior:

```python
# SAM.gov API Configuration
API_KEY = "your_api_key"
API_BASE_URL = "https://api.sam.gov/prod/v2"

# Document Download Settings
DOWNLOAD_DIRECTORY = "downloaded_docs"
DOWNLOAD_TIMEOUT = 30  # seconds
```

## Troubleshooting

### "Download Failed" with API key error
- Verify `API_KEY` is set correctly in `config.py`
- Check that the key has proper SAM.gov API permissions
- Ensure the key hasn't expired

### "Download Failed" with network error
- Check your internet connection
- Verify SAM.gov API is accessible (https://api.sam.gov)
- Try again after a few moments

### Documents not saving to folder
- Verify `downloaded_docs/` folder exists in the project root
- Check folder permissions (must be writable)
- Ensure no disk space issues
- Check the application logs for detailed errors

### Specific documents failing to download
- Some opportunities may not have attachments
- Files may be temporarily unavailable on SAM.gov
- Try downloading again later

## Features

✅ **One-Click Download** - Single button to download all documents  
✅ **Progress Feedback** - Modal shows loading state  
✅ **Success Summary** - Shows count of documents downloaded  
✅ **Error Details** - Detailed error messages and troubleshooting  
✅ **Automatic Organization** - Documents saved in organized folders  
✅ **Download Tracking** - Log file tracks all downloads  
✅ **Integration** - Works with existing "📥 Documents" viewer  

## API Endpoint

The feature uses the backend `/api/download-docs` endpoint:

```http
POST /api/download-docs
Content-Type: application/json

{
  "solicitation_number": "...",
  "organization": "...",
  ...
}

Response:
{
  "success": true,
  "message": "Documents downloaded successfully",
  "solicitation": "...",
  "description_saved": true,
  "attachments_downloaded": 5
}
```

## Security Notes

- API keys should never be committed to version control
- Keep `config.py` secure and don't share it publicly
- Downloaded documents may contain sensitive information
- Consider the storage location for downloaded files

## Tips & Tricks

1. **Batch Operations** - Download documents for multiple opportunities by clicking each one
2. **Search Then Download** - Use search filters to find relevant opportunities, then download all their documents
3. **Organize by Solicitation** - The folder structure automatically organizes by opportunity number
4. **Review Before Bidding** - Review downloaded documents using "📥 Documents" before using "📋 Bidding Strategy"

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review application logs in the console
3. Verify SAM.gov API status
4. Ensure proper configuration in `config.py`
