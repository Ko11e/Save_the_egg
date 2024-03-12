import gspread
from google.oauth2.service_account import Credentials as cd
import pandas as pd

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Code to access the excel file in google dive
CREDS = cd.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Save_the_egg')

#Global varibel for validation
YES_NO = ['Y', 'y', 'Yes', 'YES', 'yes', 'N', 'n', 'No', 'NO', 'no']

#protection = SHEET.worksheet('materials')
#data = protection.get_all_values()


def validation_int(user_input):
    try:
        int(user_input)
        return user_input
    except ValueError:
        print(f"You have enters a string, please select a number.\n")
        return 0

   