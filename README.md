# **Save the Egg**
**PICTURE** 
<br>
"Save the Egg" is a Python command line interface (CLI) game. The main objective of the game is to earn as many points as possible by dropping the egg from as high as possible without breaking it. To protect the egg from breaking, the user can use different materials. The game features three levels, each increasing in difficulty to make it less predictable. 

View the live application here: [Save the Egg](https://savetheegg-09d1666a8257.herokuapp.com/)

Google Sheets Materials, Incident (Level: Hard), Leaderboard - easy, medium, hard (view only) [here](https://docs.google.com/spreadsheets/d/1SLiWQUgkEJjnfCm5Y_rsjwojI7-m6nipCWDagON4oKk/edit?usp=sharing).

## Content
* [**User Experience/User Interface (UX/UI)**](#user-experienceuser-interface-uxui)
  * [User Goals](#user-goals)
  * [User Stories](#user-stories)
* [**Creation process**](#creation-process)
  * [Project Planning](#project-planning)
  * [Flowchart](#flowchart)
  * [Google API SetUp](#google-api-setup)
  * [Logic](#logic)
  * [Google Sheets](#Google-sheets)
  * [Design Choices](#design-choices)
* [**Features**](#features)
  * [How to play Save the egg](#how-play-use-Save-the-egg)
  * [Future Features](#future-features)
* [**Technologies Used**](#technologies-used)
* [**Packages and Libraries**](#packages-and-libraries)
* [**Testing**](#testing)
* [**Deployment**](#creation--deployment)
* [**Credits**](#credits) 
<br>

# User Experience/User Interface (UX/UI)

## User Goals
"Save the Egg" is designed as a fun game for the user to test the force limit of an egg. The game is displayed in a command line interface and the 5 highest scores is stored in a secure Google Sheet. These are some of the points I focused on when creating this project

  - It must be easy to navigate and to understand the rules the first time the user read them
  - An engaging UI to capture the user's interest.
  - Clear instructions for entering data correctly are provided.
  - No dead ends to trap the user at the end of a function.

## User Stories
1. As a User, i would like to understand the game after reading the instuctions ones
2. As a User, i want some pysichs to be behind the game
3. As a User, i want to be able to enter low numbers then 1 m for droping the egg
4. As a User, i want to be enganged in the game
5. As a User, i want the game to be harder and less pedictibel at higher levels

# Creation process
## Project Planning
When planning this project, I wanted to create a game based on my knowledge of physics. To begin with, the whole game was supposed to be as physically correct as possible. Unfortunately, the calculations of the material force reduction became too complex, so the force reduction was estimated with the help of Wikipedia. The same goes for the events in the hardest level, but some of the events are designed in such a way that the user will fail no matter what height the user chooses to drop the egg from.

To structure the coding I made a flowchart using Lucischart. The flowchart is also used to see which inputs need to be validated to keep the game from crashing.

To make the game more interesting, there is also a highscore list for the three different levels. As a user, you can only enter a name if you have enough points. 

I decided to use Google Sheets to store the leaderboards for the different levels and also to store the materials to protect the egg and the different incidents that can happen when playing the game on the most difficult level. 

## Flowchart
To help structre the project, Lucidchart was use to create a flowchat over the game and the main functions needed.
![Flowchart of Save the egg](images/flowchart.webp)
## Google API SetUp

## Logic
For this game, I wanted it to follow some of the physics rules. To find a formula to calculate the force the egg is exposed to, some assumptions are made.  To start with, we need to know the speed of the egg before it hits the ground. To find this velocity the assumption is made that there is no wind resistance no matter what the shape of the egg or the shape after the egg is protected. This means that the energy is conserved and will be the same just before the egg hits the ground as it is when the egg is released, leading to 
$$mgh = {mv^2\over2} \Rightarrow v_i = \sqrt{2gh} \quad.$$

The force to which the egg is subjected depends on the sum of all the forces over time. This is also an impulse, which can be seen as the momentum the egg has before the collision ( $\vec{p_i}$ ) and after the collision ( $\vec{p_f}$ ).
$$\vec{I} = \vec{\Delta{p}}=\vec{p_f}-\vec{p_i}=m(\vec{v_f}-\vec{v_i}) .$$

Here we assume that the collision is elastic, meaning that no energy is lost through heat. We also assume that the egg does not bounce off the ground, which means that $v_f=0$. This leads to
$$F= {I \over \Delta{t}}={mv_i\over \Delta{t}}.$$

For simplicity, I also assume that the collision time is equal to <br> 
$$\Delta{t}={distance \over velocity} = {h_{egg} \over v_i} \ . $$

This results in the collision force being 
$$F = {2mgh \over h_{egg}} \ . $$

As you can see, there are a lot of assumptions involved, which leads to further complexity if the force reduction is to be calculated correctly. 

The force that can be applied to the egg before it breaks is taken from a YouTube video, see [Cedits](#credits).  

## Google Sheets
I created a Google Sheets document to storage the materials that can be used to protect an egg and their consequences on harder levels of a game. The document also contains the events that can occur on the hardest level. In addition, there's a leaderboard for the three difficulty levels where users can enter their names if they achieve a high score. The document is only editable by me, but you can view it using the link I provided. **[here](https://docs.google.com/spreadsheets/d/1SLiWQUgkEJjnfCm5Y_rsjwojI7-m6nipCWDagON4oKk/edit?usp=sharing)**

### Materials
On this sheet contains the materials the user can chose from and the diffrenc of the impact is does on the egg. 
![Google Sheets, worksheet materials](images/sheet-materials.png)
### Incidents
Shown below are the incidents that can occure. The incidents depent on the meterials the user have chosen to use. To see all the incidents click in the lick to the view over the whole google sheet.
![Google Sheets, worksheet incidents](images/sheet-incidents.png)
### Highscores
|Easy|Medium|Hard|
|:----:|:-----:|:---:|
|![Leaderboard Easy](images/highscore_easy.png)|![Leaderboard Medium](images/highscore_medium.png)|![Leaderboard Hard](images/highscore_hard.png)|

## Design Choices

### Egg ASCII art
To make the game more appealing, I wanted to show a whole egg or a broken egg depending on the result, unfortunately I had a hard time finding ASCII art, so I decided to make my own, which can be seen below.


# Feature

## Future Features
- The user can see the leaderboard for the diffrent levels before starting the game.
- The game can be played a diffrent planet

# Technologies Used
- **HTML, CSS, Javascript** <br>
Was provided by the temple made by the Cod Institute for this project focusing on Python code.
- **Python**<br>
The program was writen in python code inperation and code not writen by my self is cretieded in the section Credits.
- **Gitpod** <br>
Used as a workspace to create the program.
- **GitHub** <br>
The source code is hosted on GitHub and deployed using Git Pages.
- **Git** <br>
During the development of the website, Git was utilized to commit and push code.
- **Lucidchart**<br>
Used to create the flowchart of the project.
- **Google Sheets worhsheets**<br>
Used to save the highscores on the leaderboard and the materiales usable to protect the egg. As well as the incidints that can occure on the hardest level.
- **Google cloud console**<br>
It is used to provide an API connection between the Python code and the worksheet in Google Sheets.
- **Heroku**<br>
Was used to deploy the project.
- **Tinyjpg** <br>
Used https://tinyjpg.com/ to compress the size of the images.

# Packages and Libraries
Some of the imports have only one function imported, this is to make the programme more efficient, seen I only use one function in the libraries. 
- **google.oauth.service_account** <br> 
<span style="color:red;">This libary is used to acess the </span>
- **gspread** <br>
This was imported and used its functionality to smoothly add, remove and manipulate data in the linked Google Sheets spreadsheets.
- **Pandas**<br>
Pandas has been used to make it easy to handle the data from the worksheet and to present it in the user interface.
- **Numpy** <br>
This libary was used to esaly substact and add values to avode using for-loops.
Since numpy is used to handle vectors and matrices, reorganising some of the data is accomplished with more efficient code. 
- **radint, from random** <br> 
This function was used to generate an integer corresponding to the event or position of the egg when it lands. This makes the player less predictable, even at a lower level.
- **system, from os** <br>
This is used to clear the terminal of text, making it easier for the user to follow the game.
- **sleep, from time** <br>
Used to allow the user time to read the text on the screen before it is cleared.
- **Design**<br>
The libarys/functions was used to make the design of the game more appyling and intresting.
  - **_pyfiglet_** <br>
  Used for ASCII art text in the Start and the end of the game
  - **_Fore and Style, from colorama_** <br>
  Used to give the user a visual feedback of the input and results in the game. Makes the text in the terminal brighter and the UI more appealing.
  - **_get_terminal_size, from shutil_** <br>
  To make the text in the termial in the ceter of the interface. 

# Testing
I have created an additional file for manual testing and validation. You can find it here: **[TESTING](/TESTING.md)**

# Deployment
 
# Credits


[Back to the top](#save-the-egg)