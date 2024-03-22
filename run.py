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
            None
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
            None
    """
    sleep(2)
    system('clear')
    print_acsii_centred('Thank you for playing', 'mini')
    print_acsii_centred('Save the egg', 'bulbhead')

def title_and_intro():
    """
    Prints the titel of the game (Save the egg) and a introdution to the game
    ----------------------------------
        Parameters
            None
    """
    print_acsii_centred('Save the egg', 'bulbhead')
    print(Fore.YELLOW)
    print_centre("The game is about getting as many points as possible by dropping an egg as high")
    print_centre("as you can without breaking the egg. To be able to drop the egg higher, there are")
    print_centre("different materials to protect the egg.\n")
    print_centre("You can play the game on three different levels, see below how these levels work.\n")
    print_centre("\033[1mPress ENTER to Start the game\033[0m\n")
    input("")
    print(Style.RESET_ALL)
    
def choose_height():
    """
    Get height from the user that the egg is going to be droped from.
    Run a while loop to collect a valid number that is a integer och a flaot.
    The loop will request input until the input is valid.
    -------------------------------------------
        Parameters
            None
        
        Retruns 
            out : float 
                Given number by the user is return as a float.

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
    Inside the try, converts a string in to a integers.
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

def validation_answer(input, lst, exp_answers):
    """
    Checks if the 'input' is in the list ´lst´.
    Raises a error with a string saying that the string provided is not the value the are expected (exp_answers).
    -------------------------------------------
        Parameters
            input : str
                The string the needs to be validated.
            lst : list
                A list of strings the are the expected values from the user
            exp_answers : str
                The values the user chould answer as a stinge the is entered after "Please enter"
        Returns
            out : boolean
                True if the ´input´ is in ´lst´ and False if not.           
    """

    if input in lst:
        return True
    else:
        print(Fore.CYAN +f'\nYou entered {input}, Please enter \033[1m{exp_answers}\033[0m'+ Style.RESET_ALL)
        return False

def question_with_valiadation(question, lst, exp_answers):
    """
    Ask the user a 'question' which is a string and checks if the value that is expected. 
    Run a while loop to collect a valid answer that is in the list 'lst', where 'lst' is a list with strings.
    Return the valid answer
    ----------------------------------------------------
        Parameters
            question : str
                The question the user should answer, the string need to end with a \n
                    exempel; "Do you what to play the game again?\n"
            lst : list
                A list of strings that are the expected values from the user
            exp_answers : str
                The values the user should answer as a stinge the is entered after "Please enter"
        Returns
            out : str
                One of the expected values as a string

    """
    while True:
        answer = input(question)
        if validation_answer(answer, lst, exp_answers):
            break
    
    return answer

def get_data(sheet_name):
    """
    Gets data from the google sheets and returns the data as the type pandas.DataFrame
    ----------------------------------
        Parameters
            sheet_name : str

        returns
            out : pandas.DataFrame
                The data in the sheet that have the name 'sheet_name' is returned as pd.DataFrame
    """
    sheet = SHEET.worksheet(sheet_name)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    return df

def select_protection(pandas_data):
    """
    Presents the protection materials that can be selected.
    Asks the user to indicate which protection they want.
    Run a while loop to collect a valid number that is a integer och a flaot.
    The loop will request input until the input is valid.
    ------------------------------------
        Parameters
            pandas_data : pandas.DataFrame

        Returns
            out1 : str
                A string with the chosen material for protection
            out2 : int
                The value as a int the the impact will be reduced by
            out3 : int
                The index number of the chosen material
    """
    #Presents the user of the options
    print("Specify which material you want to use to protect your egg?")
    print(pyfiglet.figlet_format("Materials", font = "digital"))
    print(pandas_data['material'].to_string() +"\n")

    #Asks the user to select a option
    while True:
        value = input('\nPlease enter the number for the material that you want to use:\n')
        if validation_number(value, pandas_data):
            break
    
    value = int(value)

    return pandas_data['material'][value], int(pandas_data['impact'][value]), value

def impact_calculation(height, radius_egg):
    """
    Calculates the force that the egg will be impacted by when it hit the ground.
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
    Generates a 0 or a 1
    --------------------------------------
        Parameters
            No arguments nedded
        
        Returns:
            out : int
                Value return is int that is a 0 or 1

    """

    return randint(0,1)

def get_highscore_data(difficulty_level):
    """
    Gets data from the googlesheet with the name 'difficulty_level' 
    and returns the data as a class Highscore
    -------------------
        Parameters
            difficulty_level : str
                The level of the game and the name of the Sheet in googlesheet 'Save the egg'
                (easy, meduim or hard are the values the can be entered)

        Returns
            out : class Highscore
    """
    sheet_highscore = SHEET.worksheet(difficulty_level)
    data = np.array(sheet_highscore.get_all_values()).T[:,1:]

    highscore_data = Highscore(difficulty_level, data[0], data[1])

    return highscore_data

def reduce_force_limit(egg, landingposition, impact_force):
    """
    Reduces the limit of force the egg dependent on how much force the egg 
    was subjected to during the first strike. One-third of the initial 
    force limit times the percentage force to which the egg was subjected 
    will be removed from limit. The reduce force limit will be returned.
    Exempel: 
    impact_force= 59 egg_limit=60 
    This means 98% of [13, 20] will be reduced from [40,60]
    which leads to the new egg_limit being [27, 40]
    -----------------
        Parameters
            egg : numpy.ndarray
                the np.array need to have the dimension 2,2 and have the keyvalue 'force_limit'
            landingposition : int
                the value of 0 or 1
            impact_force : float
        
        Returns
            out : numpy.ndarray
                a np.array with the dimension 1,2
    """
    procent_impact = impact_force/egg['force_limit'][landingposition]
    reduce_force = np.array([13,20])*procent_impact

    return egg['force_limit']-reduce_force

def reason(impact_total, material, egg_position):
    """
    Prints the reason if the egg is intact or breaks
    --------------------------------------
        Parameter
            impact_total : float
                The total force to which the egg was exposed to 
            material : str
                A string of the material that was used to protect the egg 
            egg_position : int
                The value 0 or 1
        Returns
            None
    """
    egg_limit = [40,60]

    if egg_limit[egg_position] == 40:
        if impact_total < 40:
            print(f'\nThe {material} managed to protect your egg sufficiently')
        elif impact_total > 40 and impact_total < 60:
            print(f'\nBecause the egg landed horizontally the {material} failed to protect your egg')
    else:
        if impact_total < 40:
            print(f'\nThe {material} managed to protect your egg sufficiently, even if it had landed horizontally')
        elif impact_total > 40 and impact_total < 60:
            print(f'\nThe {material} managed to protect your egg sufficiently, but only because it landed vertically')
        else:
            print(f'\nThe {material} failed to protect your egg')

# ACSII picture functions 
def broken_egg():
    """
    Prints a broken egg
    -------------------
        Parameters
            None
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
            None
        Returns:
            No value but prints a ASCII art of a egg
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
# Text style functions
def print_centre(text):
    """
    Prints the text in the center of the terminal
    ----------------------
        Parameters
            text : str
                The ´text´ you want to be centred in the terminal
        Retuns
            No returns 
    """
    print(text.center(get_terminal_size().columns))

def print_acsii_centred(text, fonts):
    """
    Print the text entered an ACSII and with the font given as fonts. 
    The text is also centered of the terminal.
    ---------------------------------
        Parameter
            text : str
            fonts :str
                The exempel fonts can be found on at https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/  

    """
    f = pyfiglet.Figlet(font=fonts)
    print(Fore.YELLOW)
    print(*[x.center(get_terminal_size().columns) for x in f.renderText(text).split("\n")],sep="\n")
    print(Style.RESET_ALL)

def main():
    """
    The main function running the game save the egg.
    """
    title_and_intro()   

    while True:
        #Values the change under the game and reset when the user starts a new game
        egg = np.array([(0.04, 40),(0.06, 60)], dtype=[('height', float),('force_limit', float)])
        data_protection = get_data('materials')
        score = 0

        # User selects difficulty of the game
        level = question_with_valiadation('What level do you want to play at? [easy/medium/hard]:\n', ['easy','medium', 'hard'], 'easy, medium or hard')
        highscore = get_highscore_data(level)
        print(Fore.GREEN + f'\nYou have chosen to play with difficulty level: {level}\n' + Style.RESET_ALL)

        while True: 
            height = choose_height()
            clear_screen()

            material, reduction_of_impact, value = select_protection(data_protection)
            data_protection = data_protection.drop([value])
            clear_screen()

            landingposition = randomizing_land_of_egg()

            #Calculates the force at the impact with the ground
            impact_force = impact_calculation(height, egg['height'][landingposition])
            total_impact_force = impact_force - reduction_of_impact

            if (total_impact_force) < egg['force_limit'][landingposition]:
                intact_egg()
                reason(total_impact_force, material, landingposition)
                score += int(impact_force *10)
                position_on_highscore = highscore.made_highscore(score)

                if position_on_highscore != 10:
                    print(f'Woho!! You scored {score} and got on the {position_on_highscore+1}:th place\n')
                    try_again = question_with_valiadation('\nDo you want to try to increase your score? [Y/N]:\n', YES_NO, 'Y for Yes or N for No')
                    clear_screen()

                    if YES_NO.index(try_again) >= 5:
                        name = input('Enter your name to the highscore list:\n')
                        highscore.add_to_board(position_on_highscore, name, score)
                        print(highscore)
                        highscore.uppdate_sheet()
                        clear_screen()
                        break
                        
                    else:
                        egg['force_limit'] = reduce_force_limit(egg, landingposition, total_impact_force)

                else:
                    print(f'\nYou scored {score} points and your score did not make the top 5')
                    try_again = question_with_valiadation('\nDo you want to try to increase your score? [Y/N]:\n', YES_NO, 'Y for Yes or N for No')
                    clear_screen()

                    if YES_NO.index(try_again) < 5:
                        egg['force_limit'] = reduce_force_limit(egg, landingposition, impact_force)
                    else:
                        break    
            else:
                broken_egg()
                reason(total_impact_force, material, landingposition)
                break
        
        play_again = question_with_valiadation('Do you want to play again? [Y/N]:\n', YES_NO, 'Y for Yes or N for No')

        if YES_NO.index(play_again) < 5:
            clear_screen()
            print_acsii_centred('New game', 'mini')
        else:
            end_title()
            break


main()
