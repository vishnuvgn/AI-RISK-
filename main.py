# This is the main file and the one that should be run to run the application

#################################################
# Term Project: RISK
#
# Your name: Vishnu Venugopal
# Your andrew id: vvenugop
#
#################################################

import math, copy, random

from worldMap import *
from cmuHelperFns import *
from drawingFunctions import *
from diceRoll import *
from mousePressed import *
from drawCircles import *
from aiPlaying import *
from helpers import *
from drawIntroScreen import *

from cmu_112_graphics import *

# CITAION - the image below is the one I use for the risk map
# riskmap => https://www.ultraboardgames.com/risk/continents.php

class Player(object):
    # colors = set() 
    players = [] # set of all players
    numberOfPlayers = 0
    def __init__(self, name, color):
        self.name = name
        self.cardCount = 0 # how many territory cards they have at a certain time
        # self.cards = [] # what the cards are - list of Card objects
        self.territories = set() # set of territories under Player control
        self.troopPlaceCount = 0 # how many troops Player gets to place on the map at the start of their turn
        self.initialNumOfTroops = 0 # how many troops player gets at start of setup
        # self.controlContinent = False
        self.color = color

        self.isAI = False

        Player.numberOfPlayers += 1
        # Player.colors.add(self.color)
        Player.players.append(self)

    def setPlayerToAI(self):
        self.isAI = True


# instantionation of the two players
# make sure that no two players can have the same color
player1 = Player("Player 1", "lightblue")
player2 = Player("Player 2", "lightgreen")

# player3 = Player('salmon')
# player4 = Player('cyan')

##########################################
# Intro Screen Mode
##########################################


def clickedInsideBox(x, y, x0, y0, x1, y1):
    if(x0<=x<=x1 and y0<=y<=y1):
        return True
    return False

def introScreenMode_mousePressed(app, event):
    smallBoxWidth = app.width / 5
    smallBoxHeight = app.height / 5

    ## PVP BOX Calc
    (smallBox_x0_pvp, smallBox_y0_pvp,
    smallBox_x1_pvp, smallBox_y1_pvp) = calcSmallBoxDimensions(smallBoxWidth,
                                                            smallBoxHeight, 1)

    ## AI BOX Calc
    (smallBox_x0_AI, smallBox_y0_AI,
    smallBox_x1_AI, smallBox_y1_AI) = calcSmallBoxDimensions(smallBoxWidth,
                                                            smallBoxHeight, 3)

    if(clickedInsideBox(event.x, event.y, smallBox_x0_AI,
                        smallBox_y0_AI, smallBox_x1_AI, smallBox_y1_AI)):
        app.aiPlaying = True  
        player2.setPlayerToAI()    
        # print(f"app.aiPlaying = {app.aiPlaying}")
        app.mode = ''

    elif(clickedInsideBox(event.x, event.y, smallBox_x0_pvp,
                        smallBox_y0_pvp, smallBox_x1_pvp, smallBox_y1_pvp)):
        app.aiPlaying = False        
        app.mode = ''


def calcSmallBoxDimensions(smallBoxWidth, smallBoxHeight, i):
    smallBox_x0 = smallBoxWidth*2
    smallBox_y0 = smallBoxHeight * i
    smallBox_x1 = smallBox_x0 + smallBoxWidth
    smallBox_y1 = smallBox_y0 + smallBoxHeight
    return (smallBox_x0, smallBox_y0, smallBox_x1, smallBox_y1)

def introScreenMode_timerFired(app):
    app.timeStart += 1
    if(app.timeStart % 15 == 0):
        app.i = (app.i + 1) % len(app.colors)

def introScreenMode_redrawAll(app, canvas):
    color = app.colors[app.i]
    
    canvas.create_rectangle(0,0,app.width,app.height, fill=color)
    
    smallBoxWidth = app.width / 5
    smallBoxHeight = app.height / 5

    (smallBox_x0_pvp, smallBox_y0_pvp,
    smallBox_x1_pvp, smallBox_y1_pvp) = calcSmallBoxDimensions(smallBoxWidth,
                                                            smallBoxHeight, 1)

    # FONT
    font = 'Papyrus 70 bold'
    # PVP
    ######
    canvas.create_rectangle(smallBox_x0_pvp, smallBox_y0_pvp,
                            smallBox_x1_pvp, smallBox_y1_pvp, fill="maroon")

    canvas.create_text((smallBox_x0_pvp+smallBox_x1_pvp)/2, 
                        (smallBox_y0_pvp+smallBox_y1_pvp)/2,
                        text="P vs. P", font=font)


    (smallBox_x0_AI, smallBox_y0_AI,
    smallBox_x1_AI, smallBox_y1_AI) = calcSmallBoxDimensions(smallBoxWidth,
                                                            smallBoxHeight, 3)

    ######
    # COMPUTER
    canvas.create_rectangle(smallBox_x0_AI, smallBox_y0_AI,
                            smallBox_x1_AI, smallBox_y1_AI, fill="gold")

    canvas.create_text((smallBox_x0_AI+smallBox_x1_AI)/2, 
                        (smallBox_y0_AI+smallBox_y1_AI)/2, text="P vs. C", font=font)


    drawRiskPieces(app, canvas)
    drawTitle(app, canvas)


def appStarted(app):
    app.colors = ["snow", "lavender", "spring green", "tomato"]
    app.i = 0
    app.timeStart = 0
    loadRiskPieces(app)

    #################
    # Help Strings

    app.helpStringsDict = {
        
        # Setup and Step 1
        0 : "Click on circles on map to deploy troops",

        # Step 2
        1 : "Press 'm' to maneuver. Press 'y' to yield your turn",
        2 : "1) Press 'f' and click on a region that you want to attack from",
        3 : "2) Press 't' and click on the region that you want to attack",
        4 : "3) Press 'a' and press the 'Up' and 'Down' arrow keys to change the attacking troop count",
        5 : "4) Press 'd' and press the 'Up' and 'Down' arrow keys to change the defending troop count",
        6 : "5) Press 'Space' to roll the dice",
        7 : "6) Press 'r' to restart your attack",

        # Step 3
        8 : "Press 'y' to yield your turn",
        9 : "7) Press 'f' and click on a region that you want to maneuver troops from",
        10 : "8) Press 't' and click on a region that you want to maneuver troops to",
        11 : "9) Press 'Enter' then use the 'Up' and 'Down' arrow keys to change troops maneuvered",
        12 : "10) Press 'c' to confirm your choice and give the turn to the other player"
    }
    app.helpStringKey1 = 0
    app.helpStringKey2 = -1
    app.helpStringKey3 = -1
    #################

    #################
    # Error Strings
    app.errorString = ''
    #################

    app.mode = 'introScreenMode'
    app.gameEnded = False
    app.winner = None
    app.isTie = False

    app.map = app.loadImage('riskmap.jpeg')
    app.map = app.scaleImage(app.map, 1)
    app.rows = 100
    app.cols = 100
    app.circleRadius = 15

    app.numOfPlayers = Player.numberOfPlayers
    app.turns = []

    for player in Player.players:
        if (app.numOfPlayers <= 3):
            troops = 35
        elif (app.numOfPlayers == 4):
            troops = 30
        else:
            troops = 25

        player.initialNumOfTroops = troops
        app.turns.append(player)

    app.currentIndex = 0
    app.currentPlayer = app.turns[app.currentIndex]

    app.setup = True # should be True, if game hasn't officially began (setup stage)
    app.step1Now = False # if player on step1 or not
    app.step2Now = False # if player on step2 or not
    app.step3Now = False # if player on step3 or not

    #############################
    # STEP 2 - attacking
    app.selectedRegionName = ''
    app.selectedRegionObject = None

    app.isFrom = False # used to toggle between FROM and TO
    app.isTo = False # used to toggle between FROM and TO
    
    app.fromRegionString = '' # used for searching the dictionary as keys are strings
    app.toRegionString = '' # --^

    app.fromRegionObject = None # used to access the troopCount in each territory
    app.toRegionObject = None # --^

    app.isFromLegal = False
    app.isToLegal = False

    app.substate_settingRegions = True
    app.substate_setting_D_Troops = False # setting defending troops
    app.substate_setting_A_Troops = False # setting attacking troops
    app.substate_rolling = False

    app.setRegions = False
    app.setAttack = False
    app.setDefend = False

    app.width_A = 1 # width of attacking box (the count box)
    app.width_D = 1 # width of defending box (the count box)

    app.rolledCount = 0

    app.finishedRequired = False

    app.attackingTroopCount = 1 # static for now, will change later
    app.defendingTroopCount = 1 # static for now, will change later

    app.attackingDice = [None, None, None]
    app.defendingDice = [None, None]

    app.diedAttacking = 0 # change into player later?
    app.diedDefending = 0 # change into player later?


    #############################
    # STEP 3 -> Maneuver
    app.troopsManeuvered = 0
    app.troopsToMoveWidth = 1
    #############################

    # bottome right corner of map
    app.mapBottomY = 538
    app.mapRightX = 806

    # Citation : the lines 280-282 were used to get the size of the image using 
    # the code from the the link below
    # code to get size of image
    # https://newbedev.com/python-get-width-and-height-of-image-tkinter-code-example
    
    mapPic = ImageTk.PhotoImage(app.map)
    app.mapHeight = mapPic.height()
    app.mapWidth = mapPic.width()

def redrawAll(app, canvas):

    drawMap(app, canvas)
    drawStepsAndStats(app, canvas)
    # drawGrid(app, canvas)

def drawMap(app, canvas):
    canvas.create_image(app.mapWidth/2, app.mapHeight/2, image=ImageTk.PhotoImage(app.map))
    drawAllCircles(app, canvas)

####################################################

# the sidebar and the bottom bar
def drawStepsAndStats(app, canvas):
    drawSideBar(app, canvas)
    drawBottomBar(app, canvas)

####################################################

def resetStep1(app):
    app.setup = False 
    app.step1Now = True
    app.step2Now = False
    app.step3Now = False

def resetStep2(app):
    app.selectedRegionName = ''
    app.selectedRegionObject = None

    app.isFrom = False # used to toggle between FROM and TO
    app.isTo = False # used to toggle between FROM and TO
    
    app.fromRegionString = '' # used for searching the dictionary as keys are strings
    app.toRegionString = '' # --^

    app.fromRegionObject = None # used to access the troopCount in each territory
    app.toRegionObject = None # --^

    app.isFromLegal = False
    app.isToLegal = False

    app.substate_settingRegions = True
    app.substate_setting_D_Troops = False # setting defending troops
    app.substate_setting_A_Troops = False # setting attacking troops
    app.substate_rolling = False

    app.setRegions = False
    app.setAttack = False
    app.setDefend = False

    app.width_A = 1 # width of attacking box (the count box)
    app.width_D = 1 # width of defending box (the count box)

    app.rolledCount = 0

    app.finishedRequired = False

    app.attackingTroopCount = 1 # static for now, will change later
    app.defendingTroopCount = 1 # static for now, will change later

    app.attackingDice = [None, None, None]
    app.defendingDice = [None, None]

    app.diedAttacking = 0 # change into player later?
    app.diedDefending = 0 # change into player later?


def resetStep3(app):
    app.troopsManevered = 0
    app.troopsToMoveWidth = 1

def nextPlayer(app):
    resetStep1(app)
    resetStep2(app)
    resetStep3(app)

    app.helpStringKey1 = 0
    app.helpStringKey2 = -1
    app.helpStringKey3 = -1


    app.currentIndex = (app.currentIndex + 1) % len(app.turns)
    app.currentPlayer = app.turns[app.currentIndex]

    app.currentPlayer.troopPlaceCount = calculateTroopPlaceCount(app, app.currentPlayer.territories)
    # app.currentPlayer.troopPlaceCount = 0

    if(app.currentPlayer.isAI):
        # aiPlay
        aiPlay(app)
        if (not app.gameEnded):
            nextPlayer(app)

def keyPressed(app, event):   
    ###################
    # QUIT
    ###################
    if(event.key == "q"):
        endGame(app)

    if(app.gameEnded):
        return

    if(event.key == "m" and app.finishedRequired):
        
        app.helpStringKey1 = 8
        app.helpStringKey2 = 9
        app.helpStringKey3 = 10

        
        app.setup = False 
        app.step1Now = False
        app.step2Now = False
        app.step3Now = True 

        app.fromRegionString = ''
        app.toRegionString = ''
        app.toRegionObject = None
        app.fromRegionObject = None
        app.isFromLegal = False
        app.isToLegal = False
    
        app.isFrom = False # used for toggling 
        app.isTo = False # used for toggling

    elif(event.key == "y" and app.finishedRequired): # yield, move to next player
        nextPlayer(app)

    #step 2 stuff
    if(app.step2Now == True):
        if (event.key == 'f' and app.substate_settingRegions == True):
            app.isFrom = True
            app.isTo = False

        elif (event.key == 't' and app.isFromLegal == True 
                and app.substate_settingRegions == True):
            app.isFrom = False
            app.isTo = True
        
        elif (event.key == 'r'): # refresh
            app.substate_settingRegions = True
            app.substate_setting_A_Troops = False
            app.substate_setting_D_Troops = False
            app.substate_rolling = False
            
            app.setRegions = False 
            app.setAttack = False
            app.setDefend = False
            # app.rolled ?


            app.fromRegionString = ''
            app.toRegionString = ''
            app.toRegionObject = None
            app.fromRegionObject = None
            app.isFromLegal = False
            app.isToLegal = False

            app.width_A = 1
            app.width_D = 1
        
            app.attackingTroopCount = 1
            app.defendingTroopCount = 1

            app.attackingDice = [None, None, None]
            app.defendingDice = [None, None]

            app.rolledCount = 0

            app.helpStringKey1 = 1
            app.helpStringKey2 = 2
            app.helpStringKey3 = 3

        ###########################
        # makes sure that from and to regions are legal
        elif(event.key == 'a' and 
             app.isFromLegal == True and 
             app.isToLegal == True):
            app.width_A = 3
            app.width_D = 1

            app.setRegions = True # when a pressed, regions are set 
            app.setAttack = True
            

            app.isFrom = False
            app.isTo = False
            #both are false b/c you are no longer setting the regions

            # print(f"app.substate_setting_A_Troops = {app.substate_setting_A_Troops}")
            
            # setting substates to setting troop count

            app.substate_settingRegions = False
            app.substate_setting_A_Troops = True
            app.substate_setting_D_Troops = False
            app.substate_rolling = False


                # makes sure that from and to regions are legal
        elif(event.key == 'd' and 
             app.isFromLegal == True and 
             app.isToLegal == True and 
             app.substate_setting_A_Troops == True):

            if(app.aiPlaying):
                app.defendingTroopCount = aiDefend(app)


            app.width_A = 1
            app.width_D = 3

            app.isFrom = False
            app.isTo = False

            app.setDefend = True

            app.helpStringKey1 = 1
            app.helpStringKey2 = 6
            app.helpStringKey3 = 7



            #both are false b/c you are no longer setting the regions

            # print(f"app.substate_setting_A_Troops = {app.substate_setting_A_Troops}")
            
            # setting substates to setting troop count
            app.substate_settingRegions = False
            app.substate_setting_A_Troops = False
            app.substate_setting_D_Troops = True
            app.substate_rolling = True


        elif(event.key == "Up"):
            attackingMax = checkMaxTroopsToAttack(app)
            defendingMax = checkMaxTroopsToDefend(app)
            if(app.substate_setting_A_Troops == True and 
                app.attackingTroopCount < attackingMax):

                app.attackingTroopCount += 1

            elif(app.substate_setting_D_Troops == True and 
                app.defendingTroopCount < defendingMax and not app.aiPlaying):

                app.defendingTroopCount += 1

        elif(event.key == "Down"):
            if(app.substate_setting_A_Troops == True and 
               app.attackingTroopCount > 1):
                app.attackingTroopCount -= 1

            elif(app.substate_setting_D_Troops == True and
                 app.defendingTroopCount > 1 and not app.aiPlaying):
                  app.defendingTroopCount -= 1
        ###########################
        elif(event.key == 'Space' and (app.setRegions) and
            (app.setAttack) and (app.setDefend) and app.rolledCount == 0):
            
            app.rolledCount = 1
            (app.attackingDice, app.defendingDice,
            app.diedAttacking, app.diedDefending) = rollDice(app.attackingTroopCount, app.defendingTroopCount)
            

            app.fromRegionObject.troopCount -= app.diedAttacking
            app.toRegionObject.troopCount -= app.diedDefending

            if(app.toRegionObject.troopCount < 1):
                conquer(app, app.toRegionObject, app.fromRegionObject,
                        app.attackingTroopCount, app.diedAttacking)

    # STEP 3 stuff
    ###################
    elif(app.step3Now == True):
        if(event.key == "f"):
            app.isFrom = True
            app.isTo = False

        # makes sure that from region is legal
        elif(event.key == "t" and app.isFromLegal == True):
            app.isFrom = False
            app.isTo = True


        if(app.isToLegal and app.isFromLegal and
            app.isFromLegal == True and app.isToLegal == True):
            if(event.key == "Enter"):
                app.isFrom = False # toggles the width
                app.isTo = False # toggles the width
                app.troopsToMoveWidth = 3

            if(event.key == "Up"):
                movingMax = app.fromRegionObject.troopCount - 1

                if(app.troopsManeuvered < movingMax):                
                    app.troopsManeuvered += 1

            elif(event.key == "Down"):
                if(app.troopsManeuvered > 1):
                    app.troopsManeuvered -= 1

            elif(event.key == "c"): # confirm move
                app.fromRegionObject.troopCount -= app.troopsManeuvered
                app.toRegionObject.troopCount += app.troopsManeuvered
                nextPlayer(app)

# calculates the max num of troops player can attack with 
def checkMaxTroopsToAttack(app):
    if(app.fromRegionObject == None):
        return
    highestNum = app.fromRegionObject.troopCount - 1
    if(highestNum >= 3):
        return 3
    elif(highestNum == 2):
        return 2
    else: # <-- will never occur b/c already checking if fromRegion is legal
        return False

# calculates the max num of troops player can defend with 
def checkMaxTroopsToDefend(app):
    if(app.toRegionObject == None):
        return
    highestNum = app.toRegionObject.troopCount
    if(highestNum >= 2):
        return 2
    else: # highestNum < 2
        return 1

def main():
    runApp(width=1280, height=755)

if __name__ == '__main__':
    main()
