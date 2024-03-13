import gspread
from google.oauth2.service_account import Credentials as cd
from colorama import Fore, Back, Style
import pyfiglet
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

def choose_height():
    while True:
        selected_height = input('Choose the height from which you want to drop the egg [meters]:\n')
        if validation_int(selected_height):
            print(f"You have chosen to release the egg from {selected_height} metres.")
            break
    return selected_height

def validation_int(user_input):
    try:
        float(user_input)
        return True
    except ValueError:
        print(f"You have enters a string, please select a number.\n")
        return False

def impact_calculation(height, radius_egg):
    g = 9.82 # Average gravity in m/s^2
    mass = 0.05 # Mass of the egg in kg
    
    impact_force = (2*g*height*mass)/radius_egg

    return impact_force

def broken_egg():
    print("                          ⣠⣄⣀")
    print("    ⣼⣄                   ⣹⣿⣿⣿⣷⣤")
    print(" ⢀⣾⣿⣿⣯                   ⣿⣿⣿⣿⣿⣿⣿⣄")
    print(" ⣼⣿⣿⣿⣿⣀                  ⣰⣿⣿⣿⣿⣿⣿⣿⡇")
    print("⣾⣿⣿⣿⣿⣿⣿⣀     "+Fore.YELLOW+"⣠⣴⣾⣿⣿⣷⣦⣀"+Style.RESET_ALL+"   ⠸⣿⣿⣿⣿⣿⣿⣿⡿ ")
    print("⢹⣿⣿⣿⣿⣿⣿⣿⣿⣷ "+Fore.YELLOW+"⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄"+Style.RESET_ALL+"  ⠹⣿⣿⣿⣿⣿⣿⠟")
    print(" ⠙⢻⣿⣿⣿⣿⣿⡟⠋ "+Fore.YELLOW+"⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃"+Style.RESET_ALL+" ⣸⣿⣿⣿⡿⠟⠋")
    print("    ⠙⠛⠛⠛⠋   "+Fore.YELLOW+"⠉⠻⠿⠿⠿⠿⠟⠋"+Style.RESET_ALL+"   ⠉⠉⠉") 

def intact_egg():
    print("    ⣠⣾⣿⣿⣿⣿⣷⣄")
    print("   ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣧")
    print("  ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄")
    print(" ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧")
    print(" ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print(" ⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟")
    print("  ⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃")
    print("   ⠈⢿⣿⣿⣿⣿⣿⣿⡿⠋ ")
    print("      ⠉⠉⠉⠉ ")



#print(pyfiglet.figlet_format("Save the Egg", font = "bulbhead" ))


intact_egg()
"""
from colorama import Fore, Back, Style
print(Fore.YELLOW + 'some red text' + Style.RESET_ALL)
#print(Back.GREEN + 'and with a green background')
#print(Style.DIM + 'and in dim text')
#print(Style.RESET_ALL)
print('back to normal now')
print(Style.RESET_ALL)
"""