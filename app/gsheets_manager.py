import gspread
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = "BeeMobilityCRM_Interactions"

def get_gsheets_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials/credentials.json", scope)
    return gspread.authorize(credentials)

def log_interaction_to_sheets(customer_name, contact_info, query, resolution, status):
    client = get_gsheets_client()
    sheet = client.open(SHEET_NAME).sheet1
    sheet.append_row([customer_name, contact_info, query, resolution, status])
