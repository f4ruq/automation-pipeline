import gspread
import os
from google.oauth2.service_account import Credentials
from logs.logger import log

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def write_gsheet(items, sheet_name, credentials_file="credentials.json"):
    if not items:
        log("No items to write to Google Sheets.")
        return

    # Check for credentials in common locations
    if not os.path.exists(credentials_file):
        if os.path.exists(f"credentials/{credentials_file}"):
            credentials_file = f"credentials/{credentials_file}"
        else:
             log(f"Credentials file not found: {credentials_file}", level="ERROR")
             return

    try:
        credentials = Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES
        )
        gc = gspread.authorize(credentials)
        
        # Open the spreadsheet
        try:
            sh = gc.open(sheet_name)
        except gspread.SpreadsheetNotFound:
            log(f"Spreadsheet '{sheet_name}' not found. Please create it and share with the service account email.")
            return

        # Select the first worksheet
        worksheet = sh.sheet1

        # Prepare data
        headers = list(items[0].keys())
        values = [list(item.values()) for item in items]
        
        # Clear existing content and write new data
        worksheet.clear()
        worksheet.append_row(headers)
        worksheet.append_rows(values)
        
        log(f"Successfully wrote {len(items)} records to Google Sheet: {sheet_name}")

    except FileNotFoundError:
        log(f"Credentials file not found: {credentials_file}", level="ERROR")
    except Exception as e:
        log(f"Error writing to Google Sheets: {e}", level="ERROR")
