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

# Global varibel for validation
YES_NO = ['Y', 'y', 'Yes', 'YES', 'yes', 'N', 'n', 'No', 'NO', 'no']


class Highscore:
    """
    A class for the highscore/leaderboard of top 5
    ......
        Attributes
        level : srt
            The level of the leaderboard ex. easy, meduim, hard
        names : numpy.ndarray
            The namnes on the leaderboard starting with
            the player with the highest score.
        score : numpy.ndarray
            The score if the players starting with the highest score

    Methods
    -------
    made_highscore(new_score)
        This methos checks if the 'new_score' is
        high enough to make the highscore/leaderboard
    add_to_board(position, new_name, new_score)
        This method and a new player and its score on the highscore/leaderboard
    uppdate_sheet()
        This updates the data in the google sheet.

    """
    def __init__(self, level, names, scores):
        """
        The constructor for Highscore class.
        ----------------------------------
            Parameter:
                level : srt
                    The level of the leaderboard ex. easy, meduim, hard
                names : numpy.ndarray
                    The namnes on the leaderboard starting with
                    the player with the highest score.
                score : numpy.ndarray
                    The score if the players starting with the highest score
        """
        self.level = level
        self.names = names.tolist()
        self.scores = scores.tolist()

    def __str__(self):
        """
        Convert the data in to a padas Dataframe and
        returns the data as a string. printing the leaderboard
        with the headline High Score.
        """
        board = pd.DataFrame(
            {'Name': self.names, 'Score': self.scores}, index=[1, 2, 3, 4, 5])
        print(Fore.LIGHTWHITE_EX)
        print(pyfiglet.figlet_format("High Score", font="threepoint"))
        return board.to_string()

    def made_highscore(self, new_score):
        """
        This method check if the new_score is high enough
        to make the top 5. If the score is not high enough
        the method returns the position of the placement
        and if it does not the number 10 is returned.
        -------------------------------------------------
        Parameter
            new_score : int

        Returns
            out : int
                The position the new_score have on the leaderboard or
                the number 10 if the score does not place on the leaderboard
        """
        position = 10
        for i in range(1, 5):
            if new_score > int(self.scores[0]):
                position = 0
            elif new_score < int(self.scores[i-1]) and \
                    new_score > int(self.scores[i]):
                position = i

        return position

    def add_to_board(self, position, new_name, new_score):
        """
        This method inserts the new_name and the new_score
        on the position given. After that it removes the
        last name in the list.
        ---------------------------
        Parameters
            position : int
                The position the user is placed on the top list.
                The number can not be higher then 4 (the 5:th placment)
            new_name : str
                The name of the player the have made the top 5
            new_score : int
                The score the player have scored
        Returns
            out : None
        """
        # Add the name on the right position and removes
        # the last name that is now on the 6:th place
        self.names.insert(position, new_name)
        self.names.pop(-1)

        # Add the score on the right position and removes
        # the last score that is now on the 6:th place
        self.scores.insert(position, new_score)
        self.scores.pop(-1)

    def uppdate_sheet(self):
        """
        This method updates the data in the google sheet.
        ----------------------------------------
        Parameters
            None
        """
        self.names = np.array(self.names)
        self.scores = np.array(self.scores)
        for i in range(2, 7):
            SHEET.worksheet(self.level).update([[self.names[i-2]]], f'A{i}')
            SHEET.worksheet(self.level).update([[self.scores[i-2]]], f'B{i}')


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
    print(Fore.LIGHTYELLOW_EX)
    print_acsii_centred('Save the egg', 'bulbhead')
    print(Style.RESET_ALL)


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
    print(Fore.LIGHTYELLOW_EX)
    print_acsii_centred('Thank you for playing', 'mini')
    print_acsii_centred('Save the egg', 'bulbhead')
    print(Style.BRIGHT)
    print_centre('Press RUN PROGRAM')
    print_centre('to restart the game')
    print(Style.RESET_ALL)


def start_menu():
    """
    Prints the titel of the game (Save the egg) and a introdution to the game
    ----------------------------------
        Parameters
            None
    """
    print(Fore.LIGHTYELLOW_EX)
    print_acsii_centred('Save the egg', 'bulbhead')
    print(' ')
    print_centre("The game is about getting as many points as possible")
    print_centre(
        "by dropping an egg as high as you can without breaking the egg.")
    print_centre(
        "To be able to drop the egg higher, there are different materials")
    print_centre(
        "to protect the egg. You can play the game on three different levels.")
    print("")
    print("""
 ------------------------------------------------------------------------------
    1. Rules for the levels   2. Highscores    3. Start the Game    4.Exit
 ------------------------------------------------------------------------------
 """)

    print(Style.RESET_ALL)
    while True:
        number = input('')
        if validation_number(number, (1, 2, 3, 4)):
            number = int(number)
            if number == 1:
                show_rules()
                break
            elif number == 2:
                show_highscores()
                break
            elif number == 3:
                main()
                break
            else:
                end_title()
                break


def show_rules():
    """
    Show the rules of the differens levels
    ---------------------------
        Parameters
            None
    """
    clear_screen()
    print(Fore.LIGHTYELLOW_EX)
    print("""
    EASY:   The way the egg lands, either horizontally or vertically,
            will determine how well it copes with the impact.
            If you successfully save the egg, you can attempt to earn
            more points by dropping it again. However, keep in mind that
            the egg has been damaged from the previous drop, and therefore
            it won't be able to withstand as big of a hit as before.
            If the egg breaks, you will lose your points.

    MEDUIM: For this level, the same rules as the previous level apply.
            However, your choice of protection will affect the final score
            and can also decreas your score if you dropp it more then once.
            Here you can chose NOT to protect the egg and get 200 points
            plus the other points.

    HARD:   For this level, the same rules as the previous levels apply.
            However, an event will occur after you have released the egg.
            This event can be good or bad. So take it carefully\n\n""")
    print_centre("\033[1mPress ENTER to go back to the main meun\033[0m")
    input('')
    system('clear')
    start_menu()


def get_n_insert_spaces(level):
    """
    Gets the data from the Google Sheets and insert
    1 column [1,2,3,4,5] and then 3 empty column.
    This is to make it more appealing when printed
    --------------------------------
        Parameter
            level : srt
                The level of the highscoreboard
    """
    data = get_data(level)
    data.insert(0, " ", [1, 2, 3, 4, 5], True)
    for i in range(2):
        data.insert(0, " ", [" ", " ", " ", " ", " "], True)

    return data


def show_highscores():
    """
    Show the leaderboard - easy medium and hard
    """
    clear_screen()
    print(Fore.LIGHTYELLOW_EX)
    print_acsii_centred('High Score', 'threepoint')
    print_acsii_centred('  Easy             Medium          Hard', 'mini')

    # Gets data from the Google sheet
    easy = get_data('easy')
    medium = get_n_insert_spaces('medium')
    hard = get_n_insert_spaces('hard')
    # merges the diffrent dataframes
    new_nd = pd.concat([easy, medium, hard], axis=1)
    new_fd = new_nd.set_axis([1, 2, 3, 4, 5], axis='index')

    # Convert DataFrame to string
    df_string = new_fd.to_string()
    df_split = df_string.split('\n')

    # Prints the lists in the center of the terminal
    for i in range(len(new_fd)+1):
        print_centre(df_split[i])
    print('')

    print_centre("Press ENTER to go back to the main meun")
    input('')
    system('clear')
    start_menu()
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
        selected_height = input(
            ' How high do you want the egg to drop from [meters]?\n\
 You can use decimals:')
        if validation_number(selected_height):
            print(Fore.GREEN + Style.BRIGHT + "You have chosen ",
                  f"to release the egg from {selected_height} meters.\n")
            print(Style.RESET_ALL)
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
                A list with numbers (int) to check if ´user_input´
                is in the list. If ´lst´ is None this function is not executed

        Returns
            boolean : True if the sting  a number and False it it's not.
    """
    try:
        float(user_input)
        if lst is not None:
            return validation_int(user_input, lst)

    except ValueError:
        print(Fore.LIGHTRED_EX + f"Invalid input. You entered '{user_input}',",
              " please enter a number." + Style.RESET_ALL)
        if ',' in user_input:
            print(Fore.LIGHTRED_EX + "Please use . as a decimal point" +
                  Style.RESET_ALL)
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
        if int(input) not in lst:
            raise TypeError

    except ValueError:
        print(Fore.LIGHTRED_EX + "Invalid input. Please enter a whole number,",
              f" you entered {input} which is a decimal number" +
              Style.RESET_ALL)
        return False

    except TypeError:
        # Converts the values in to a string with a ','
        # between evey value.
        string_lst = ', '.join(map(str, lst))

        print(Fore.LIGHTRED_EX + f'Invalid input. Please enter {string_lst}.' +
              Style.RESET_ALL)
        return False

    return True


def validation_answer(input, lst, exp_answers):
    """
    Checks if the 'input' is in the list ´lst´.
    Raises a error with a string saying that the string
    provided is not the value the are expected (exp_answers).
    -------------------------------------------
        Parameters
            input : str
                The string the needs to be validated.
            lst : list
                A list of strings the are the expected values from the user
            exp_answers : str
                The values the user could answer as a stinge
                the is entered after "Please enter"
        Returns
            out : boolean
                True if the ´input´ is in ´lst´ and False if not.
    """

    if input in lst:
        return True
    else:
        print(Fore.RED +
              f'Invalid input. You entered {input},',
              f'please enter \033[1m{exp_answers}\033[0m' +
              Style.RESET_ALL)
        return False


def question_with_valiadation(question, lst, exp_answers):
    """
    Ask the user a 'question' which is a string and checks if
    the value that is expected. Run a while loop to collect a valid
    answer that is in the list 'lst', where 'lst' is a list with strings.
    Return the valid answer
    ----------------------------------------------------
        Parameters
            question : str
                The question the user should answer,
                the string need to end with a \n
                    exempel; "Do you what to play the game again?\n"
            lst : list
                A list of strings that are the expected values from the user
            exp_answers : str
                The values the user should answer as a stinge
                and is entered after "Please enter"
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
    Gets data from the google sheets and returns
    the data as the type pandas.DataFrame
    ----------------------------------
        Parameters
            sheet_name : str
                the name of the sheet in the google sheet -´Save_the_egg´
        returns
            out : pandas.DataFrame
                The data in the sheet that have the name 'sheet_name'
                is returned as pd.DataFrame
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
    # Enter the keyvaule to a list that is needed when a element is removed
    keys_data = [x for x in pandas_data.index]

    if len(keys_data) == 0:
        print(Fore.LIGHTRED_EX + 'WARNING!\n'
              'You have run out of materials to protect your egg with.\n' +
              Style.RESET_ALL)
        return {'material': 'None', 'impact': 0, 'points': 0}, 100

    # Presents the user of the options
    print("Specify which material you want to use to protect your egg?")
    print(pyfiglet.figlet_format("Materials", font="digital"))
    print(pandas_data['material'].to_string() + "\n")

    # Asks the user to select a option
    while True:
        value = input('Please enter the number for\
 the material that you want to use:')
        if validation_number(value, keys_data):
            break

    value = int(value)
    print(Fore.GREEN + Style.BRIGHT + "You've chosen to protect your egg ",
          f"with a {pandas_data['material'][value]}.\n" + Style.RESET_ALL)

    return pandas_data.loc[value], value


def score_adjustment(score, protection, points):
    """
    Subtract or Add the points to the score depending
    if the egg is proterctet or not.
    -----------------------------------
        Parameters
            score : int
                The score that the player has scored
            protection : boolean
                if the player has chosen to protect
                the egg (TRUE)or not(FALSE)
            pionts : int
                The pionts that should added or substracted from the score.
        Returns
            out : int
                The adjusted score as a int
    """
    if protection is True:
        return score - points
    else:
        return score + points


def impact_calculation(height):
    """
    Calculates the force that the egg will
    be impacted by when it hit the ground.
    --------------------------------------
        Parameters
            height : int
                Height the egg is drops from
            radius_egg : float
                The raduis of the egg.
                (this determines the momentum of the collection
                i.e. impactfocre)

        Returns
            out : float
                The force that the egg will be exposed to in the impact
    """
    print('Dropping the egg.....')
    sleep(2)

    g = 9.82  # Average gravity in m/s^2
    mass = 0.05  # Mass of the egg in kg
    radius_egg_avg = 0.06  # meters

    impact_force = (2*g*height*mass)/radius_egg_avg

    return impact_force


def generatet_incident(material_value):
    """
    Generatets a incident depanting on the material the user have chosen.
    The function prints a text explaning if the incident was good or bad.
    Returns the value (int) the incident will affect the impact of the egg
    ---------------------------------
        Parameters
            material_value : str
                The chosen material of the user, this determents
                the incindents that are generareted.

        Returns
            out : int
                The value of the incident will affect the impact.
                If the incident is good a positiv value is return and
                negativ if bad.
    """
    data = get_data('incidents')
    # Extract data with the chosen protection material
    chosen_material = data[data['material'] == material_value]
    # Creates new index to the extracted data
    chosen_material.index = [1, 2, 3, 4, 5, 6, 7, 8]

    # Generates a number between 1 to 8
    incident = randint(1, 8)
    if incident <= 4:
        print(Fore.GREEN + "\033[1m" +
              chosen_material['text'][incident] + "\033[0m" + Style.RESET_ALL)
        print("")
    else:
        print(Fore.RED + "\033[1m" +
              chosen_material['text'][incident] + "\033[0m" + Style.RESET_ALL)
        print("")

    impact_effect = chosen_material['impact'][incident]
    # Convert the negative value in google sheet from a str to a int
    if type(impact_effect) == str:
        int_impact_effect = int(impact_effect.strip(impact_effect[0]))
        impact_effect = -int_impact_effect

    sleep(2)

    return impact_effect


def get_highscore_data(difficulty_level):
    """
    Gets data from the googlesheet with the name 'difficulty_level'
    and returns the data as a class Highscore
    -------------------
        Parameters
            difficulty_level : str
                The level of the game and the name of the Sheet
                in googlesheet 'Save the egg'.
                (easy, meduim or hard are the values that can be entered)

        Returns
            out : class Highscore
    """
    sheet_highscore = SHEET.worksheet(difficulty_level)
    data = np.array(sheet_highscore.get_all_values()).T[:, 1:]

    highscore_data = Highscore(difficulty_level, data[0], data[1])

    return highscore_data


def reduce_force_limit(egg, landingposition, impact_force):
    """
    Reduces the limit of force the egg dependent on how much force the egg
    was subjected to during the first strike. The percentage force to which
    the egg was subjected to will be removed from limit.
    The reduce force limit will be returned.
    Exempel:
    impact_force= 59 egg_limit=60
    This means 98% of the force limit will be reduce from [40, 60]
    which leads to the new egg_limit being [0.8, 1.2]
    -----------------
        Parameters
            egg : numpy.ndarray
                the np.array need to have the dimension 2,2 and
                have the keyvalue 'force_limit'
            landingposition : int
                the value of 0 or 1
            impact_force : float

        Returns
            out : numpy.ndarray
                a np.array with the dimension 1,2
    """
    # if the impact is negativ of zero the reduced force is zero
    # otherwise will the force_limit increase instead of decreasing
    if impact_force <= 0:
        reduce_force = 0
    else:
        procent_impact = impact_force/egg[landingposition]
        reduce_force = egg*procent_impact
    return egg-reduce_force


def reason(impact_total, material, egg_position, dropps):
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
    print(Fore.LIGHTCYAN_EX)
    if dropps == 7:
        print('You have droped the egg to many times so this time it broke')

    elif material == 'None':
        if impact_total < 40:
            print('The egg survived without any protection')

        elif impact_total > 40 and impact_total < 60 and egg_position == 1:
            print('The egg survived but only because it landed vertically.')

        elif impact_total > 40 and impact_total < 60 and egg_position == 0:
            print('The egg did not survive because is landed horizontally')
            print('Maybe you should have protected it...')

        else:
            print('The egg did not survive the drop')
            print('Maybe you should have protected it...')

    else:
        if impact_total < 40:
            print(f'The {material} managed to protect your egg sufficiently')

        elif impact_total > 40 and impact_total < 60 and egg_position == 0:
            print('Because the egg landed horizontally,\n',
                  f'the {material} failed to protect your egg')

        elif impact_total > 40 and impact_total < 60 and egg_position == 1:
            print(f'The {material} managed to protect your egg',
                  'sufficiently, \nbut only because it landed vertically')

        else:
            print(f'The {material} failed to protect your egg')
    print(Style.RESET_ALL)


def print_placement(placement, score):
    """
    Print a text that infroms where the user is
    placed on the lederboard.
    ------------------------------------
        Parameters
            placment : int
                this is the placment om the leadorbaord
                The function takes negativ numbers but
                for the right value enter positivt numbers
            score : int
                The score the user has
        Return
            None
    """
    if placement == 0:
        print(Style.BRIGHT + Fore.YELLOW)
        print(". ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁ . ⟡ ݁ .  ݁₊ ⊹ . ݁ ⟡ ݁ . ⊹ ₊ ݁.")
        print(f'Woho!! You scored {score} and got on FIRST place\n' +
              Style.RESET_ALL)
    elif placement == 1:
        print(Fore.LIGHTCYAN_EX + 'Woho!! You have a score of'
              f' {score} points and are in {placement+1}nd place.' +
              Style.RESET_ALL)
    elif placement == 2:
        print(Fore.LIGHTCYAN_EX + 'Woho!! You have a score of'
              f' {score} points and are in {placement+1}rd place.' +
              Style.RESET_ALL)
    else:
        print(Fore.LIGHTCYAN_EX + 'Woho!! You have a score of'
              f' {score} points and are in {placement+1}th place.' +
              Style.RESET_ALL)


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
    print(Style.BRIGHT)
    print("Oooo no, the egg broke\n")
    print("                          ⣠⣄⣀")
    print("    ⣼⣄                   ⣹⣿⣿⣿⣷⣤")
    print(" ⢀⣾⣿⣿⣯                   ⣿⣿⣿⣿⣿⣿⣿⣄")
    print(" ⣼⣿⣿⣿⣿⣀                  ⣰⣿⣿⣿⣿⣿⣿⣿⡇")
    print("⣾⣿⣿⣿⣿⣿⣿⣀     " + Fore.YELLOW +
          "⣠⣴⣾⣿⣿⣷⣦⣀" + Style.RESET_ALL + Style.BRIGHT +
          "   ⠸⣿⣿⣿⣿⣿⣿⣿⡿ ")
    print("⢹⣿⣿⣿⣿⣿⣿⣿⣿⣷ " + Fore.YELLOW +
          "⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄" + Style.RESET_ALL + Style.BRIGHT +
          "  ⠹⣿⣿⣿⣿⣿⣿⠟")
    print(" ⠙⢻⣿⣿⣿⣿⣿⡟⠋ " + Fore.YELLOW +
          "⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃" + Style.RESET_ALL + Style.BRIGHT +
          " ⣸⣿⣿⣿⡿⠟⠋")
    print("    ⠙⠛⠛⠛⠋   " + Fore.YELLOW +
          "⠉⠻⠿⠿⠿⠿⠟⠋" + Style.RESET_ALL + Style.BRIGHT +
          "   ⠉⠉⠉")
    print(Style.RESET_ALL)


def intact_egg():
    """
    Prints a intact egg
    ------------------
        Parameters
            None
        Returns:
            No value but prints a ASCII art of a egg
    """
    print(Style.BRIGHT)
    print("    ⣠⣾⣿⣿⣿⣿⣷⣄")
    print("   ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣧")
    print("  ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄")
    print(" ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧")
    print(" ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    print(" ⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟")
    print("  ⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃")
    print("   ⠈⢿⣿⣿⣿⣿⣿⣿⡿⠋ ")
    print("      ⠉⠉⠉⠉ ")
    print(Style.RESET_ALL)


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
                The text that will be printet
            fonts :str
                The font the text should be in
                The exempel fonts can be found on at
    https://www.geeksforgeeks.org/python-ascii-art-using-pyfiglet-module/
    """
    f = pyfiglet.Figlet(font=fonts)
    print(*[x.center(get_terminal_size().columns) for x in
          f.renderText(text).split("\n")], sep="\n")


def main():
    """
    The main function running the game save the egg.
    """
    while True:
        # Values the change under the game and
        # resets when the user starts a new game
        egg = np.array([40, 60])
        data_protection = get_data('materials')
        score = 0
        # Dropps counter to provent the user to drop the egg
        # more then 7 times
        dropps = 0

        clear_screen()
        # User selects difficulty of the game
        level = question_with_valiadation(
            'What level do you want to play at? [easy/medium/hard]:',
            ['easy', 'medium', 'hard'], 'easy, medium or hard.'
        )
        highscore = get_highscore_data(level)
        print(Fore.GREEN + Style.BRIGHT +
              f'You have chosen to play with difficulty level: {level}\n' +
              Style.RESET_ALL)

        while True:
            protection = True
            # If the level medium and hard is play
            # the user can chose to not protect the egg
            if level == 'medium' or level == 'hard':
                protecting_egg = question_with_valiadation(
                    '\nDo you like to protect the egg? [Y/N]',
                    YES_NO, 'Y for Yes or N for No'
                )

                # The user enterd No to protect the egg
                if YES_NO.index(protecting_egg) >= 5:
                    protection = False
                    material_values = {'material': 'None',
                                       'impact': 0,
                                       'points': 200}
                    print(Fore.GREEN + Style.BRIGHT + "You've chosen to ",
                          "not protect your egg\n" + Style.RESET_ALL)

            if protection is True:
                material_values, value = select_protection(data_protection)
                # Remove the chosen protection for the list
                # if the value is 100 this means the list is empty
                if value != 100:
                    data_protection = data_protection.drop([value])

            height = choose_height()
            clear_screen()

            # Generates the position of the egg, vertical or horizontal
            landingposition = randint(0, 1)

            # Calculates the force at the impact with the ground
            impact_force = impact_calculation(height)

            # Incident that happen at the hard level
            incident = generatet_incident(
                material_values['material']) if level == 'hard' else 0

            total_impact_force = impact_force - \
                material_values['impact'] - incident

            dropps += 1

            # Checks if the egg breaks
            if (total_impact_force) < egg[landingposition] and dropps != 7:
                intact_egg()
                reason(total_impact_force, material_values['material'],
                       landingposition, dropps)
                score += int(impact_force * 10)

                # Adjust the score depending on the material that was used to
                # protect the egg.
                if (level == 'medium' or level == 'hard'):
                    score = score_adjustment(score, protection,
                                             material_values['points'])

                # See if the score was high enough to make the Top 5
                position_on_highscore = highscore.made_highscore(score)

                if position_on_highscore != 10:
                    # Prints statmant for the placement for
                    # the user, gets stars i placed first
                    print_placement(position_on_highscore, score)

                    try_again = question_with_valiadation(
                        ('\nDo you want to risk\
 your points to increase your score \nand get to the top\
 of the leaderboard? [Y/N]:'),
                        YES_NO, 'Y for Yes or N for No'
                    )
                    clear_screen()

                    # Users answered NO to try to increase the score
                    if YES_NO.index(try_again) >= 5:
                        print('Enter your name to the leaderboard,')
                        name = input('Maximum of 10 characters:')
                        # Makes the name max 10 characters
                        name = name[:10] if len(name) > 11 else name
                        highscore.add_to_board(position_on_highscore,
                                               name, score)
                        # Prints the new leaderboard with the new name
                        print(highscore)
                        print(Style.RESET_ALL)
                        # Updates the sheet at google sheets
                        highscore.uppdate_sheet()
                        break

                    # User answered YES to try to increas the score
                    else:
                        # Reduces the forcelimit of the egg
                        egg = \
                            reduce_force_limit(egg,
                                               landingposition,
                                               total_impact_force)

                else:
                    print(Fore.LIGHTCYAN_EX +
                          f'You scored {score} points and ',
                          'your score did not make the top 5' +
                          Style.RESET_ALL)
                    try_again = question_with_valiadation(
                     '\nWould you like to risk your points to boost\
 your score \nand try to reach the leaderboard [Y/N]?',
                     YES_NO, 'Y for Yes or N for No'
                    )
                    clear_screen()

                    if YES_NO.index(try_again) < 5:
                        # Reduces the forcelimit of the egg
                        egg = \
                            reduce_force_limit(egg,
                                               landingposition,
                                               total_impact_force)

                    else:
                        break
            else:
                broken_egg()
                reason(total_impact_force,
                       material_values['material'], landingposition, dropps)
                break

        play_again = question_with_valiadation(
            '\nDo you want to play again? [Y/N]:\n',
            YES_NO, 'Y for Yes or N for No'
        )

        if YES_NO.index(play_again) < 5:
            clear_screen()
            print(Fore.YELLOW)
            print_acsii_centred('New game', 'mini')
            print(Style.RESET_ALL)
        else:
            end_title()
            break


start_menu()
