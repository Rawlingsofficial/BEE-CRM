import sqlite3
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SERVICE_ACCOUNT_FILE = "path/to/service_account.json"

def upload_to_google_sheets(database_path, sheet_name="customer_interactions_data", worksheet_name="Sheet1"):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(database_path)
        query = "SELECT * FROM interactions"  # Replace with your table name
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Authenticate and open the Google Sheet
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open(sheet_name).worksheet(worksheet_name)

        # Get existing data from Google Sheets
        existing_data = sheet.get_all_records()
        existing_df = pd.DataFrame(existing_data)

        # Find rows not already in Google Sheets
        if not existing_df.empty:
            new_rows = df[~df.isin(existing_df).all(1)]
        else:
            new_rows = df

        if new_rows.empty:
            return "No new data to upload."

        # Append new rows to Google Sheets
        sheet.append_rows(new_rows.values.tolist(), value_input_option="RAW")
        return "New data successfully uploaded to Google Sheets."

    except Exception as e:
        return f"Error uploading data: {e}"
