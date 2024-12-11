import requests

def check_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            print("Internet connection is active.")
        else:
            print("Unable to connect to the internet.")
    except Exception as e:
        print(f"Internet check failed: {e}")

check_internet_connection()




from oauth2client.service_account import ServiceAccountCredentials
import gspread
import sqlite3
import pandas as pd

SERVICE_ACCOUNT_FILE = "service_account.json"  # Ensure this file is valid
SHEET_NAME = "customer_interactions_data"  # Replace with your Google Sheet name

def upload_to_google_sheets(database_path, sheet_name, worksheet_name="Sheet1"):
    try:
        # Step 1: Verify credentials file
        with open(SERVICE_ACCOUNT_FILE, "r") as f:
            print("Credentials file loaded successfully.")
        
        # Step 2: Connect to SQLite database
        conn = sqlite3.connect("data/database.db")
        df = pd.read_sql_query("SELECT * FROM interactions", conn)
        conn.close()

        # Step 3: Authenticate with Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        gc = gspread.authorize(credentials)

        # Step 4: Open the Google Sheet
        sheet = gc.open(sheet_name).worksheet(worksheet_name)

        # Step 5: Clear the existing worksheet data
        sheet.clear()

        # Step 6: Update the sheet with new data
        sheet.update([df.columns.values.tolist()] + df.values.tolist())

        print("Data successfully uploaded to Google Sheets.")
        return "Data successfully uploaded to Google Sheets."

    except FileNotFoundError:
        return "Error: service_account.json file not found."
    except gspread.exceptions.SpreadsheetNotFound:
        return f"Error: Google Sheet '{sheet_name}' not found."
    except Exception as e:
        return f"Error: {e}"

# Test function
result = upload_to_google_sheets("data.db", SHEET_NAME)
print(result)