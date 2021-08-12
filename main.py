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

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))


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
        Player.numberOfPlayers += 1
        # Player.colors.add(self.color)
        Player.players.append(self)

        
# class Card(object):
#     def __init__(self, territory, icon): # EX: c1 = Card(Alaska, Cavalry)
#         self.territory = territory
#         self.icon = icon

# instantionation of the two players
# make sure that no two players can have the same color
player1 = Player("Player 1", "lightblue")
player2 = Player("Player 2", "lightgreen")
# player3 = Player('salmon')
# player4 = Player('cyan')

def appStarted(app):

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
            troops = 22 # should be 35 -> for testing purposes, it's 15
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
    # STEP 3 -> Manuever
    app.troopsManuevered = 0
    app.troopsToMoveWidth = 1
    #############################

    # bottome right corner of map
    app.mapBottomY = 538
    app.mapRightX = 806



    # code to get size of image
    # https://newbedev.com/python-get-width-and-height-of-image-tkinter-code-example

    # img = Image.open('riskmap.jpeg')
    # mapPic = ImageTk.PhotoImage(img)
    # app.mapHeight = mapPic.height()
    # app.mapWidth = mapPic.width()
    
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
    app.troopsManuevered = 0
    app.troopsToMoveWidth = 1

def nextPlayer(app):
    resetStep1(app)
    resetStep2(app)
    resetStep3(app)

    app.currentIndex = (app.currentIndex + 1) % len(app.turns)
    app.currentPlayer = app.turns[app.currentIndex]
    app.currentPlayer.troopPlaceCount = calculateTroopPlaceCount(app, app.currentPlayer.territories)

def keyPressed(app, event):   
    ###################
    # QUIT
    ###################
    if(event.key == "q"):
        endGame(app)

    if(app.gameEnded):
        return

    if(event.key == "m" and app.finishedRequired):
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
            app.width_A = 1
            app.width_D = 3

            app.isFrom = False
            app.isTo = False

            app.setDefend = True

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
                app.defendingTroopCount < defendingMax):

                app.defendingTroopCount += 1

        elif(event.key == "Down"):
            if(app.substate_setting_A_Troops == True and 
               app.attackingTroopCount > 1):
                app.attackingTroopCount -= 1

            elif(app.substate_setting_D_Troops == True and
                 app.defendingTroopCount > 1):
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
                conquer(app.toRegionObject, app.fromRegionObject,
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

                if(app.troopsManuevered < movingMax):                
                    app.troopsManuevered += 1

            elif(event.key == "Down"):
                if(app.troopsManuevered > 1):
                    app.troopsManuevered -= 1

            elif(event.key == "c"): # confirm move
                app.fromRegionObject.troopCount -= app.troopsManuevered
                app.toRegionObject.troopCount += app.troopsManuevered
                nextPlayer(app)

def endGame(app):
    # drawBlankScreen and show who won or tie
    app.gameEnded = True
    app.mode = 'gameEndedMode'
    listOfNumOfRegions = []
    for player in app.turns:
        listOfNumOfRegions.append(len(player.territories))
    
    for i in range(len(listOfNumOfRegions) - 1):
        if(listOfNumOfRegions[i] != listOfNumOfRegions[i+1]):
            app.isTie = False
        else:
            app.isTie = True

    if(app.isTie == False):
        bestWinner = None
        bestWinnerTerritoryCount = -1
        for player in app.turns:
            if(len(player.territories) > bestWinnerTerritoryCount):
                bestWinner = player
                bestWinnerTerritoryCount = len(player.territories)
        app.winner = bestWinner

def checkGameEnd(currentPlayer):
    if(len(currentPlayer.territories) == len(regionsSet)):
        app.winner = currentPlayer
        return True
    else:
        return False

def conquer(toRegionObject, fromRegionObject, attackCount, diedAttacking):
    conquered = toRegionObject.troopGeneral
    conquerer = fromRegionObject.troopGeneral

    toRegionObject.troopGeneral = fromRegionObject.troopGeneral
    toRegionObject.occupied = True
    toRegionObject.color = fromRegionObject.color
    
    # removes the region from conqueredPlayer's set of territories
    conquered.territories.remove(toRegionObject) 
    # removes the region from conqueredPlayer's set of territories
    conquerer.territories.add(toRegionObject) 

    toRegionObject.troopCount = (attackCount - diedAttacking)
    fromRegionObject.troopCount -= toRegionObject.troopCount

    if(checkGameEnd(conquerer)):
        endGame()


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
