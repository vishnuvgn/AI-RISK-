Project Description:
- Name: AI RISK
- My term project will be the digital version of the board game RISK where 
  a user can compete with another player or the computer. It will
  have an interactive user interface where the user can decide where to deploy
  their troops, whether to attack (and if so, from where, to where, and with 
  how many troops), and whether to maneuver troops (with the same three options 
  as attacking). When playing against the computer, it will randomly make its 
  decisions. For instance, it will randomly decide where to place its troops,
  whether to attack, etc. 

Running the Project:
- Run main.py from the editor and have all other files in the same folder. This 
  includes the jpegs, the pngs, and the actual python files.

Libraries/Modules
- In order to use all the feature of the cmu_112_graphics file, I had to install
  pillow and requests

- from cmu_112_graphics import *
- import math, copy, random


Shortcut Commands:

    When in Step 2 (Attacking):
    - Press 'm' to maneuver. Press 'y' to yield your turn
    - Press 'f' and click on a region that you want to attack from
    - Press 't' and click on the region that you want to attack
    - Press 'a' and press the 'Up' and 'Down' arrow keys to change the attacking troop count
    - Press 'd' and press the 'Up' and 'Down' arrow keys to change the defending troop count
    - Press 'Space' to roll the dice
    - Press 'r' to restart your attack

    When in Step 3 (Maneuvering):
    - Press 'y' to yield your turn
    - Press 'f' and click on a region that you want to maneuver troops from
    - Press 't' and click on a region that you want to maneuver troops to
    - Press 'Enter' then use the 'Up' and 'Down' arrow keys to change troops maneuvered
    - Press 'c' to confirm your choice and give the turn to the other player

    At any time, press 'q' to quit the game