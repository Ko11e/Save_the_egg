import gspread
from google.oauth2.service_account import Credentials as cd
from colorama import Fore, Style
from shutil import get_terminal_size
from random import randint
from time import sleep
import pyfiglet
from os import system
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
    """
    TEXT
    """
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
        self.names = np.insert(self.names, position, new_name)
        self.names = np.delete(self.names, -1)

        # Add the score on the right position and removes the last score that is now on the 6:th place
        self.scores = np.insert(self.scores, position, new_score)
        self.scores = np.delete(self.scores, -1)

    def uppdate_sheet(self):
        for i  in range(2,7):
            SHEET.worksheet(self.level).update([[self.names[i-2]]],f'A{i}')
            SHEET.worksheet(self.level).update([[self.scores[i-2]]],f'B{i}')

def clear_screen():
    """
    This function waits for 2 seconds and then
    clears the terminal and prints the title of the game
    ------------------
        Parameters
            No argumnets nedded
    """
    sleep(2)
    system('clear')
    print_acsii_centred('Save the egg', 'bulbhead')

def end_title():
    """
    This function Waits for 2 seconds and 
    then clears the terminal and prints a text 
    thanking you for playing the game
    -------------------
        Parameters
            No argumnets nedded
    """
    sleep(2)
    system('clear')
    print_acsii_centred('Thank you for playing', 'mini')
    print_acsii_centred('Save the egg', 'bulbhead')

def choose_height():
    """
    Get height from the user that the egg is going to be droped from.
    Run a while loop to collect a valid number that is a integer och a flaot.
    The loop will request input until the input is valid.
    -------------------------------------------
        Parameters
            No arguments is needed
        
        Retruns 
            float: Given number by the user is return as a float.

    """
    while True:
        selected_height = input('Choose the height from which you want to drop the egg [meters]:\n')
        if validation_number(selected_height):
            print(Fore.GREEN + f"\nYou have chosen to release the egg from {selected_height} metres." +Style.RESET_ALL)

            break
    
    return float(selected_height)

def validation_number(user_input, lst=None):
    """
    Inside the try, converts the string value to a flaot.
    Raises a ValueError if the string can't be converted into a flaot.
    ------------------------------------
        Parameters
            user_input : str 
                String to check if it's a number
            lst :list, optional 
                A list with numbers (int) to check if ´user_input´ is in the list. 
                If ´lst´ is None this function is not executed 
        
        Returns
            boolean : True if the sting  a number and False it it's not.
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
    ------------------------------------
        Parameters
            input : str 
                string to check if it's a int and if the value is in lst
            lst :list
                A list with numbers (int) to check if ´input´ is in the list. 
        
        Returns
            out : boolean 
                True if the sting  a number and False it it's not.
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
    """
    Checks if the 'input' is a sting that is a Y, y, Yes, YES, yes, N, n, No, NO or no.
    Raises a error with a string saying that the string provided is not a yes or a no.
    -------------------------------------------
        Parameters
            input : str

        Returns
            out : boolean
                True if the ´input´ is a Y, y, Yes, YES, yes, N, n, No, NO or no and False if not.           
    """

    if input in YES_NO:
        return True
    else:
        print(Fore.CYAN +f'You entered {input}, Please enter a \033[1mY for Yes and N for No.\033[0m'+ Style.RESET_ALL)
        return False

def yes_no_question(question):
    """
    
    """
    while True:
        try_again = input(question)
        if validation_yes_no(try_again):
            break
    
    return try_again

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
    print(df['material'].to_string() +"\n")

    #Asks the user to select a option
    while True:
        value = input('\nPlease enter the number for the material that you want to use:\n')
        if validation_number(value, df):
            break
    
    return df['material'][int(value)], int(df['impact'][int(value)])

def impact_calculation(height, radius_egg):
    """
    Calculates the force that the egg will be impacted by when they hit the ground.
    ---------------------------------------------
        Parameters
            height : int
                TEXT
            radius_egg : float
                TEXT
        
        Returns
            out : float
                Text
    """
    g = 9.82 # Average gravity in m/s^2
    mass = 0.05 # Mass of the egg in kg
    
    impact_force = (2*g*height*mass)/radius_egg

    return impact_force

def randomizing_land_of_egg():
    """
    Generates a 0 or a 1 which will indicate whether the egg lands horizontally or vertically.
    --------------------------------------
        Parameters
            No arguments nedded
        
        Returns:
            out : int
                Value return is int that is a 0 or 1

    """

    return randint(0,1)

def broken_egg():
    """
    Prints a broken egg
    -------------------
        Parameters
            No argumnets nedded
        Returns:
            No value but prints a ASCII art of a broken egg
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
    ------------------
        Parameters
            No argumnets nedded
        Returns:
            No value but prints a ASCII art of a egg
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
    """
    Text
    -------------------
        Parameters
            difficulty_level : str

        Returns
            out : class
                test
    """
    sheet_highscore = SHEET.worksheet(difficulty_level)
    data = np.array(sheet_highscore.get_all_values()).T[:,1:]

    highscore_data = Highscore(difficulty_level, data[0], data[1])

    return highscore_data

def reduce_force_limit(egg, landingposition, impact_force):
    """
    Tets
    -----------------
        Parameters
            egg : numpy.ndarray
                TEXT
            landingposition : int
                TEXT
            impact_force : float
                TEXT
        
        Returns
            out : numpy.ndarray
                TEXT
    """
    procent_impact = impact_force/egg['force_limit'][landingposition]
    reduce_force = np.array([20,30])*procent_impact

    return egg['force_limit']-reduce_force

def print_centre(text):
    print(text.center(get_terminal_size().columns))

def print_acsii_centred(text, fonts):
    f = pyfiglet.Figlet(font=fonts)
    print(Fore.YELLOW)
    print(*[x.center(get_terminal_size().columns) for x in f.renderText(text).split("\n")],sep="\n")
    print(Style.RESET_ALL)

def title_and_intro():
    print_acsii_centred('Save the egg', 'bulbhead')
    print(Fore.YELLOW)
    print_centre("The game is about getting as many points as possible by dropping an egg as high")
    print_centre("as you can without breaking the egg. To be able to drop the egg higher, there are")
    print_centre("different materials to protect the egg.\n")
    print_centre("You can play the game on three different levels, see below how these levels work.\n")
    print_centre("Press ENTER to Start the game\n")
    input("")
    print(Style.RESET_ALL)

def main():
    """
    The main function running the game save the egg.
    """
    title_and_intro()   
    egg = np.array([(0.04, 40),(0.06, 60)], dtype=[('height', float),('force_limit', float)])
    highscore_easy = get_highscore_data('easy')
    score = 0

    while True:

        while True: 
            height = choose_height()
            clear_screen()

            material, reduction_of_impact = select_protection()
            clear_screen()

            landingposition = randomizing_land_of_egg()
        
            impact_force = impact_calculation(height, egg['height'][landingposition])
            total_impact_force = impact_force - reduction_of_impact

            if (total_impact_force) < egg['force_limit'][landingposition]:
                intact_egg()
                score += int(impact_force *10)
                position_on_highscore = highscore_easy.made_highscore(score)

                if position_on_highscore != 10:
                    print(f'Woho!! You scored {score} and got on the {position_on_highscore+1}:th place\n')
                    print(highscore_easy)
                    try_again = yes_no_question('\nDo you want to try to increase your score? [Y/N]:')

                    if YES_NO.index(try_again) >= 5:
                        name = input('Enter your name to the highscore list:\n')
                        highscore_easy.add_to_board(position_on_highscore, name, score)
                        print(highscore_easy)
                        highscore_easy.uppdate_sheet()
                        break
                        
                    else:
                        egg['force_limit'] = reduce_force_limit(egg, landingposition, total_impact_force)
                        print(egg)


                else:
                    print(f'\nYou scored {score} points and your score did not make the top 5')
                    try_again = yes_no_question('\nDo you want to try to increase your score? [Y/N]:')

                    if YES_NO.index(try_again) < 5:
                        egg['force_limit'] = reduce_force_limit(egg, landingposition, impact_force)
                        print(egg)
                    else:
                        break    
            else:
                broken_egg()
                break
        
        play_again = yes_no_question('Do you want to play again? [Y/N]')
        
        if YES_NO.index(play_again) < 5:
            clear_screen()
            print_acsii_centred('New game', 'mini')
        else:
            end_title()
            break

class Protection:
    id_number = 0
    def __init__ (self, material, impact, pionts):
        self.material = material
        self.impact_red = impact
        self.pionts_red = pionts
        self.id = Protection.id_number
        Protection.id_number += 1

    def __str__(self):
        return f'{self.id}       {self.material}'

    @classmethod
    def get_all_materials(cls):
        protection = SHEET.worksheet('materials')
        data = protection.get_all_records()
        list_of_protection = []
        for chooses in data:
            material = cls(**chooses)
            list_of_protection.append(material)

        return list_of_protection

    #def delete_option(id, list_of_all):



main()