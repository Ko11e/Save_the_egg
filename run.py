import gspread
from google.oauth2.service_account import Credentials as cd
from colorama import Fore, Back, Style
from random import randint 
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

def choose_height():
    """
    Get height from the user that the egg is going to be droped from.
    Run a while loop to collect a valid number that is a integer och a flaot.
    The loop will request input until the input is valid.
    """
    while True:
        selected_height = input('Choose the height from which you want to drop the egg [meters]:\n')
        if validation_number(selected_height):
            print(f"\nYou have chosen to release the egg from {selected_height} metres.")
            break
    return selected_height

def validation_number(user_input, lst=None):
    """
    Inside the try, converts the string value to a flaot.
    Raises a ValueError if the string can't be converted into a flaot.
    """
    try:
        float(user_input)
        if lst is not None:
            return validation_int(user_input, lst)
        
    except ValueError:
        print(Fore.CYAN + f"You have entered a string, please enter a number.\n"+ Style.RESET_ALL)
        return False

    return True

def validation_int(input, lst):
    """
    Inside the try, converts a string or in to a integers.
    Raises ValueError if string can't be converted into int 
    and TypeError if the nummber is higher the number is 
    higher than the length of the list.
    """
    try:
        int(input)
        if int(input) > len(lst):  
            raise TypeError

    except ValueError:
        print(Fore.CYAN + f"Please enter a whole number, you have entered {input} which is a decimal number"+ Style.RESET_ALL)
        return False
    
    except TypeError:
        print(Fore.CYAN + f'Please enter a number between 0-{len(lst)-1}'+ Style.RESET_ALL)
        return False 
    
    return True

def select_protection():
    """
    Presents the protection materials that can be selected.
    Asks the user to indicate which protection they want.
    Run a while loop to collect a valid number that is a integer och a flaot.
    The loop will request input until the input is valid.
    """
    # Gets the data for the google sheet
    protection = SHEET.worksheet('materials')
    data = protection.get_all_values()
    df = pd.DataFrame(data[1:], columns = data[0])

    #Presents the user of the options
    print("Specify which material you want to use to protect your egg?")
    print(pyfiglet.figlet_format("Materials", font = "digital"))
    print(df['Material'].to_string() +"\n")

    #Asks the user to select a option
    while True:
        value = input('\nPlease enter the number for the material that you want to use:\n')
        if validation_number(value, df):
            break
    
    return df['Material'][int(value)], df['Impact reduction'][int(value)]

def impact_calculation(height, radius_egg):
    """
    Calculates the force that the egg will be impacted by when they hit the ground.
    """
    g = 9.82 # Average gravity in m/s^2
    mass = 0.05 # Mass of the egg in kg
    
    impact_force = (2*g*height*mass)/radius_egg

    return impact_force

def broken_egg():
    """
    Prints a broken egg
    """
    print("                          ⣠⣄⣀")
    print("    ⣼⣄                   ⣹⣿⣿⣿⣷⣤")
    print(" ⢀⣾⣿⣿⣯                   ⣿⣿⣿⣿⣿⣿⣿⣄")
    print(" ⣼⣿⣿⣿⣿⣀                  ⣰⣿⣿⣿⣿⣿⣿⣿⡇")
    print("⣾⣿⣿⣿⣿⣿⣿⣀     "+Fore.YELLOW+"⣠⣴⣾⣿⣿⣷⣦⣀"+Style.RESET_ALL+"   ⠸⣿⣿⣿⣿⣿⣿⣿⡿ ")
    print("⢹⣿⣿⣿⣿⣿⣿⣿⣿⣷ "+Fore.YELLOW+"⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄"+Style.RESET_ALL+"  ⠹⣿⣿⣿⣿⣿⣿⠟")
    print(" ⠙⢻⣿⣿⣿⣿⣿⡟⠋ "+Fore.YELLOW+"⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃"+Style.RESET_ALL+" ⣸⣿⣿⣿⡿⠟⠋")
    print("    ⠙⠛⠛⠛⠋   "+Fore.YELLOW+"⠉⠻⠿⠿⠿⠿⠟⠋"+Style.RESET_ALL+"   ⠉⠉⠉") 

def intact_egg():
    """
    Prints a intact egg
    """
    print("    ⣠⣾⣿⣿⣿⣿⣷⣄")
    print("   ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣧")
    print("  ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄")
    print(" ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧")
    print(" ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print(" ⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟")
    print("  ⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃")
    print("   ⠈⢿⣿⣿⣿⣿⣿⣿⡿⠋ ")
    print("      ⠉⠉⠉⠉ ")

def main():
    egg = [0.04, 0.06]
    egg_impact = [40, 60]

    print(pyfiglet.figlet_format("Save the Egg", font = "bulbhead" ))
    height = int(choose_height())
    material, reduction_of_impact = select_protection()
    v_or_h = randint(0,1)
    
    impact_force = impact_calculation(height, egg[v_or_h])
    
    if impact_force < egg_impact[v_or_h]:
        print('You managed to save the egg')
        intact_egg()
    else:
        print("Oooo no, the egg broke")
        broken_egg()


main()
#print(pyfiglet.figlet_format("Save the Egg", font = "bulbhead" ))

#impact_calculation(2, 0.04)

#choose_height()
