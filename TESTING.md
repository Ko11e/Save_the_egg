# Testing of Save the Egg

## Content
**[Validation](#validation)** <br>
**[Manual Testing](#manual-testing)**<br>
**[Bugs](#bugs)**

## Validation
### PEP8
The code has been validated using Code Institute's PEP8 Linter. No errors were found in the last validation test, see the result below:
![Result PEP8 validation](images/PEP8-validation.png) 

## Manual Testing
### User Stories 

 1. As a User, I want the explanation and the rules of the game to be clear and easy to understand.

    - At the start of the game there are clear instructions for the game.
    - By pressing 1 or 2 in the start menu the user can read more about the difficulties and the high scores of the levels
 
 2. As a user, I want to be provided with clear instructions throughout the main menu and game.

    - All sections requiring user input are signposted with clear instructions on how to proceed
    - User is prompted and instructed when invalid information is entered

 3. As a User, I want to be able to navigate back to the Main Menu.

    - By pressing ENTER the user will return to the main menu

 4. As a User, I want to be engaged in the game

    - Colorama library is used to produce text with engaging colors and meaning and make ASCII art more appealing.
    - GREEN for valid input and good incident for hard-level
    - RED for invalid input and bad incident for hard-level
    - CYAN for the user's attention to be drawn to important information
    - YELLOW for the main menu and when a user gets first place
    - Having a Scoreboard to engage the user to want a higher score

 5. As a User, I want the game to be harder and less predictable at higher levels

    -From easy to medium points will be reduced depending on the material
        - The user has the choice to protect the egg or not, but receive 200 points if the egg survives
    - From medium to hard 
        - An incident can occur which can be good or bad

### Function Testing
#### Validation
![Validation list](images/Validations.png) <br>
The remaining questions have the same validation function, which means that their test is not documented.

#### Calculations
I have tested functions by printing their output and verifying the results manually. Additionally, all the randomly generated events were printed and cross-checked manually in the Google Sheets worksheet. Below is the list of all the tested functions.<br>
![Table of all the tested functions](images/test_functions.png)
## Bugs
### Fixed Bugs

|Bug     |Solution      |
|:----|:-----|
|The function validation_number does not run validation_int if a list is provided | The wrong if statement was used. Where `lst != None` was used first and found through Stackoverflow that it should be `lst is not None`|
|Getting the wrong value from the data.<br> Exempel Sleepingbag was chosen and Woodenbox was selected. | The wrong function was used `.iloc` was replaced with `.loc`|
|If the impact value becomes negative due to a low height drop and good protection. The egg force limit will increase rather than decrease. |By having an if statement, check if the value of the total impact is negative. If the value is negative no calculations are made and the force limit remains the same.   |
|If the incident, on a hard level, was bad the value retrieved from the Google sheet was a string instead of an integer.|By checking the retrieved value if it is a string and then remaking it into an integer. This bug/solution to the bug made it easier to print the occurrence of the text in green or red.|
|When entering a name to add to the high score it only adds five characters without there being any restriction in the code|When "self.names" and "self.scores" were changed from a `numpy.array` to a `list`, the bug disappeared. However, there is now a 10-character restriction for user input. When entering their name, users will be notified of a 10-character limit for input.|



### Unfixed Bugs
No known bugs found

--------------------

[Return to main README](/README.md)