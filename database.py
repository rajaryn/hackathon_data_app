import gspread
import pandas as pd
import os
import traceback 
from dotenv import load_dotenv
import json

load_dotenv()

# --- Configuration ---
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE', 'service_account.json') 
SPREADSHEET_NAME = os.getenv('SPREADSHEET_NAME', 'Hackathon Data') # Matches your test_db output
WORKSHEET_NAME = os.getenv('WORKSHEET_NAME', 'Sheet1') 

UNIQUE_ID_COL = 'Unique ID'
HACKATHON_COL = 'Hackathon Name' 
TEAM_MEMBERS_COL = 'Team Members' 
TIMESTAMP_COL = 'Timestamp'

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet_client():
    try:

        if os.getenv('GOOGLE_CREDENTIALS'):
            # Convert the string back to a dictionary
            creds_dict = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
            client = gspread.service_account_from_dict(creds_dict, scopes=SCOPES)

        # 2. LOCAL METHOD: Fallback to file
        elif os.path.exists(SERVICE_ACCOUNT_FILE):
            client = gspread.service_account(filename=SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            
        else:
            print("🚨 Error: No credentials found (Env Var or File).")
            return None
        # Open the Spreadsheet and Tab
        spreadsheet = client.open(SPREADSHEET_NAME)
        sheet = spreadsheet.worksheet(WORKSHEET_NAME)
        return sheet

    except Exception:
        print("\n--- DATABASE CONNECTION ERROR ---")
        traceback.print_exc() 
        print("------------------------------------\n")
        return None

        

# -----------------------------------------------------
# Read Data Function
# -----------------------------------------------------

def get_all_data():
    sheet = get_sheet_client()
   
    if sheet is None:
        return pd.DataFrame()
    
    try:
        data = sheet.get_all_records() 
        return pd.DataFrame(data)
    except Exception:
        print("\nError reading data:")
        traceback.print_exc()
        return pd.DataFrame()

# -----------------------------------------------------
# Write Data Function
# -----------------------------------------------------

def append_new_entry(entry_id, hackathon_name, team_members, timestamp):
    sheet = get_sheet_client()
    if sheet is None:
        return False
    
    check_db_connection()
    new_row = [entry_id, hackathon_name, team_members, timestamp]
    
    try:
        sheet.append_row(new_row)
        print(f"Saved: {hackathon_name}")
        return True
    except Exception:
        print("\nError writing data:")
        traceback.print_exc()
        return False

# -----------------------------------------------------
# Delete Data Function
# -----------------------------------------------------

def delete_entry_by_id(id_to_delete):
    sheet = get_sheet_client()
   
    if sheet is None:
        return False
    
    try:
        # Find the header cell to get the correct column index
        header_cell = sheet.find(UNIQUE_ID_COL)
        unique_id_col_num = header_cell.col 
        
        # Find the row with the ID
        cell = sheet.find(id_to_delete, in_column=unique_id_col_num)
        
        if cell:
            sheet.delete_rows(cell.row)
            print(f"Deleted row {cell.row}")
            return True
        else:
            print(f"ID {id_to_delete} not found.")
            return False
            
    except Exception:
        print("\nError deleting data:")
        traceback.print_exc()
        return False
    

def check_db_connection():
    """Returns True if the sheet is accessible, False otherwise."""
    if get_sheet_client():
        print('Online')
        return True
    print('Offline')
    return False