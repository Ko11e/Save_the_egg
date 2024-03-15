import gspread
from google.oauth2.service_account import Credentials as cd
from colorama import Fore, Back, Style
from random import randint 
import pyfiglet
import pandas as pd
import numpy as np

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

class Highscore:
    def __init__(self, level, names, scores):
        self.level = level
        self.names = names
        self.scores = scores

    def __str__(self):
        board = pd.DataFrame({'Name': self.names, 'Score': self.scores}, index=[1,2,3,4,5])
        print(pyfiglet.figlet_format("Highescore", font = "threepoint" ))
        return board.to_string()

    def made_highscore(self, new_score):
        position = 10
        for i in range(1,5):
            if new_score > int(self.scores[0]):
                position = 0
            elif new_score < int(self.scores[i-1]) and new_score > int(self.scores[i]):
                position = i
                
        return position

    def add_to_board(self, position, new_name, new_score):
        # Add the name on the right position and removes the last name that is now on the 6:th place
        self.names.insert(position, new_name)
        self.names.pop(-1)

        # Add the score on the right position and removes the last score that is now on the 6:th place
        self.scores.insert(position, new_score)
        self.scores.pop(-1)

    def uppdate_sheet(self):
        for i  in range(2,7):
            SHEET.worksheet(self.level).update([[self.names[i-2]]],f'A{i}')
            SHEET.worksheet(self.level).update([[self.scores[i-2]]],f'B{i}')

def choose_height():
    """
    Get height from the user that the egg is going to be droped from.
    Run a while loop to collect a valid number that is a integer och a flaot.
    The loop will request input until the input is valid.
    """
    while True:
        selected_height = input('Choose the height from which you want to drop the egg [meters]:\n')
        if validation_number(selected_height):
            print(Fore.GREEN + f"\nYou have chosen to release the egg from {selected_height} metres." +Style.RESET_ALL)
            print('--------------------------------------------\n')
            break
    
    return float(selected_height)

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
        if int(input) > len(lst)-1:  
            raise TypeError

    except ValueError:
        print(Fore.CYAN + f"Please enter a whole number, you have entered {input} which is a decimal number"+ Style.RESET_ALL)
        return False
    
    except TypeError:
        print(Fore.CYAN + f'Please enter a number between 0-{len(lst)-1}'+ Style.RESET_ALL)
        return False 
    
    return True

def validation_yes_no(input):
    if input in YES_NO:
        return True
    else:
        print(Fore.CYAN +f'You entered {input}, Please enter a \033[1mY for Yes and N for No.\033[0m'+ Style.RESET_ALL)
        return False

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
    
    return df['Material'][int(value)], int(df['Impact reduction'][int(value)])

def impact_calculation(height, radius_egg):
    """
    Calculates the force that the egg will be impacted by when they hit the ground.
    """
    g = 9.82 # Average gravity in m/s^2
    mass = 0.05 # Mass of the egg in kg
    
    impact_force = (2*g*height*mass)/radius_egg

    return impact_force

def randomizing_land_of_egg():
    """
    Generates a 1 or a 2 which will indicate whether the egg lands horizontally or vertically.
    """
    return randint(0,1)

def broken_egg():
    """
    Prints a broken egg
    """
    print("Oooo no, the egg broke\n")
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
    print('You managed to save the egg\n')
    print("    ⣠⣾⣿⣿⣿⣿⣷⣄")
    print("   ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣧")
    print("  ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄")
    print(" ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧")
    print(" ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print(" ⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟")
    print("  ⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃")
    print("   ⠈⢿⣿⣿⣿⣿⣿⣿⡿⠋ ")
    print("      ⠉⠉⠉⠉ ")

def get_highscore_data(difficulty_level):
    sheet_highscore = SHEET.worksheet(difficulty_level)
    data = np.array(sheet_highscore.get_all_values()).T[:,1:]

    highscore_data = Highscore(difficulty_level, data[0], data[1])

    return highscore_data

def reduce_force_limit(egg, landingposition, impact_force):
    procent_impact = impact_force/egg['force_limit'][landingposition]
    reduce_force = np.array([20,30])*procent_impact

    return egg['force_limit']-reduce_force


def main():
    egg = np.array([(0.04, 40),(0.06, 60)], dtype=[('height', float),('force_limit', float)])
    highscore_easy = get_highscore_data('easy')
    
    print(pyfiglet.figlet_format("Save the Egg", font = "bulbhead" ))
    while True: 
        height = choose_height()
        material, reduction_of_impact = select_protection()
        landingposition = randomizing_land_of_egg()
    
        impact_force = impact_calculation(height, egg['height'][landingposition])
    
        if (impact_force - reduction_of_impact) < egg['force_limit'][landingposition]:
            intact_egg()
            score = int(impact_force *10)
            position_on_highscore = highscore_easy.made_highscore(score)

            if position_on_highscore != 10:
                print(f'Woho!! You scored {score} and got on the {position_on_highscore+1}:th place\n')
                print(highscore_easy)
                while True:
                    try_again = input('\nDo you have to try to increase your score? [Y/N]:')
                    if validation_yes_no(try_again):
                        break
                if YES_NO.index(try_again) >= 5:
                    name = input('Enter your name to the highscore list:\n')
                    highscore_easy.add_to_board(position_on_highscore, name, score)
                    print(highscore_easy)
                    break
                else:
                    egg['force_limit'] = reduce_force_limit(egg, landingposition, impact_force)


            else:
                print(f'\nYour score is {score} and your score did not make the top 5')
                while True:
                    try_again = input('Do you want to try to increase your score? [Y/N]:')
                    if validation_yes_no(try_again):
                        break
                if YES_NO.index(try_again) >= 5:
                    break
                else:
                    egg['force_limit'] = reduce_force_limit(egg, landingposition, impact_force)


        else:
            broken_egg()
            break



#main()
# print(pyfiglet.figlet_format("Save the Egg", font = "bulbhead" ))

# highscore(50)
#sheet_highscore = SHEET.worksheet('easy')
#data_easy = np.array(sheet_highscore.get_all_values()).T[:,1:]

#print(data_easy[0], data_easy[1])
egg = np.array([(0.04, 40),(0.06, 60)], dtype=[('height', float),('force_limit', float)])
print(egg)
egg['force_limit'] = reduce_force_limit(egg, 1, 50)
print(egg)