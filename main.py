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


def calculateTroopPlaceCount(territoriesSet):
    if(len(territoriesSet) < 9):
        return 3
    else:
        return (len(territories) // 3)

class Player(object):
    # colors = set() 
    players = [] # set of all players
    numberOfPlayers = 0
    def __init__(self, color):
        # self.name = ""
        self.cardCount = 0 # how many territory cards they have at a certain time
        self.cards = [] # what the cards are - list of Card objects
        self.territories = set() # set of territories under Player control
        self.troopPlaceCount = calculateTroopPlaceCount(self.territories) # how many troops Player gets to place on the map at the start of their turn
        self.initialNumOfTroops = 0 # how many troops player gets at start of setup
        self.controlContinent = False
        self.color = color
        Player.numberOfPlayers += 1
        # Player.colors.add(self.color)
        Player.players.append(self)



    # methods for recieving (placing) troops, attacking, defending, manuevering
        
class Card(object):
    def __init__(self, territory, icon): # EX: c1 = Card(Alaska, Cavalry)
        self.territory = territory
        self.icon = icon

# instantionation of the two players
# make sure that no two players can have the same color
player1 = Player("lightblue")
player2 = Player("lightgreen")
# player3 = Player('salmon')
# player4 = Player('cyan')

def appStarted(app):
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

    app.setup = True    # if game hasn't officially began (setup stage)
    app.step1Now = False # if player on step1 or not
    app.step2Now = False # if player on step2 or not
    app.step3Now = False # if player on step3 or not
    
    app.selectedRegionName = None

    app.isFrom = False # used to toggle between FROM and TO
    app.isTo = False # used to toggle between FROM and TO
    
    app.fromRegionString = '' # used for searching the dictionary as keys are strings
    app.toRegionString = '' # --^

    app.fromRegionObject = None # used to access the troopCount in each territory
    app.toRegionObject = None # --^

    app.attackingTroopCount = 1 # static for now, will change later
    app.defendingTroopCount = 1 # static for now, will change later

    app.attackingDice = [None, None, None]
    app.defendingDice = [None, None]

    app.diedAttacking = 0 # change into player later?
    app.diedDefending = 0 # change into player later?

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


# draws a circle that shows the number of troops in the country
def drawCircle(app, canvas, row, col, territory, fillColor=""): 
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    cx = (x0+x1) / 2
    cy = (y0+y1) / 2
    canvas.create_oval(x0-app.circleRadius, y0-app.circleRadius,
                       x1+app.circleRadius, y1+app.circleRadius,
                       fill=fillColor)
    troopCount = territory.troopCount
    # ^ add font color and everything later
    canvas.create_text(cx,cy, text=troopCount)
    return (cx,cy) # returns the cooridinates of the center of the circle

def drawAllCircles(app, canvas):
    # NORTH AMERICA
    Alaska.circleCoordinates = drawCircle(app, canvas, 3, 2, Alaska, Alaska.color) # Alaska
    Northwest_Territory.circleCoordinates = drawCircle(app, canvas, 4, 10, Northwest_Territory, Northwest_Territory.color) # Northwest Territory
    Alberta.circleCoordinates = drawCircle(app, canvas, 19, 4, Alberta, Alberta.color) # Alberta
    Western_United_States.circleCoordinates = drawCircle(app, canvas, 26, 4, Western_United_States, Western_United_States.color) # Western United States
    Central_America.circleCoordinates = drawCircle(app, canvas, 36, 6, Central_America, Central_America.color) # Central America
    Eastern_United_States.circleCoordinates = drawCircle(app, canvas, 29, 17, Eastern_United_States, Eastern_United_States.color) # Eastern United States
    Greenland.circleCoordinates = drawCircle(app, canvas, 3, 21, Greenland, Greenland.color) # Greenland
    Ontario.circleCoordinates = drawCircle(app, canvas, 13, 14, Ontario, Ontario.color) # Ontario
    Quebec.circleCoordinates = drawCircle(app, canvas, 18, 20, Quebec, Quebec.color) # Quebec

    # SOUTH AMERICA
    Venezuela.circleCoordinates = drawCircle(app, canvas, 35, 16, Venezuela, Venezuela.color) # Venezuela
    Peru.circleCoordinates = drawCircle(app, canvas, 45, 8, Peru, Peru.color) # Peru
    Argentina.circleCoordinates = drawCircle(app, canvas, 57, 11, Argentina, Argentina.color) # Argentina
    Brazil.circleCoordinates = drawCircle(app, canvas, 50, 19, Brazil, Brazil.color) # Brazil
    
    # AFRICA
    North_Africa.circleCoordinates = drawCircle(app, canvas, 41, 27, North_Africa, North_Africa.color) # North_Africa
    Congo.circleCoordinates = drawCircle(app, canvas, 54, 28, Congo, Congo.color) # Congo
    South_Africa.circleCoordinates = drawCircle(app, canvas, 64, 29, South_Africa, South_Africa.color) # South_Africa
    Madagascar.circleCoordinates = drawCircle(app, canvas, 66, 41, Madagascar, Madagascar.color) # Madagascar
    East_Africa.circleCoordinates = drawCircle(app, canvas, 52, 40, East_Africa, East_Africa.color) # East_Africa
    Egypt.circleCoordinates = drawCircle(app, canvas, 38, 33, Egypt, Egypt.color) # Egypt

    # EUROPE
    Western_Europe.circleCoordinates = drawCircle(app, canvas, 35, 22, Western_Europe, Western_Europe.color) # Western_Europe
    Great_Britain.circleCoordinates = drawCircle(app, canvas, 26, 21, Great_Britain, Great_Britain.color) # Great_Britain
    Iceland.circleCoordinates = drawCircle(app, canvas, 9, 26, Iceland, Iceland.color) # Iceland
    Scandanavia.circleCoordinates = drawCircle(app, canvas, 5, 32, Scandanavia, Scandanavia.color) # Scandanavia
    Ukraine.circleCoordinates = drawCircle(app, canvas, 13, 38, Ukraine, Ukraine.color) # Ukraine
    Northern_Europe.circleCoordinates = drawCircle(app, canvas, 19, 31, Northern_Europe, Northern_Europe.color) # Northern_Europe
    Southern_Europe.circleCoordinates = drawCircle(app, canvas, 33, 30, Southern_Europe, Southern_Europe.color) # Southern_Europe

    # ASIA
    Middle_East.circleCoordinates = drawCircle(app, canvas, 41, 38, Middle_East, Middle_East.color) # Middle_East
    India.circleCoordinates = drawCircle(app, canvas, 43, 45, India, India.color) # India
    Siam.circleCoordinates = drawCircle(app, canvas, 41, 53, Siam, Siam.color) # Siam
    China.circleCoordinates = drawCircle(app, canvas, 33, 52, China, China.color) # China
    Afghanistan.circleCoordinates = drawCircle(app, canvas, 29, 41, Afghanistan, Afghanistan.color) # Afghanistan
    Ural.circleCoordinates = drawCircle(app, canvas, 12, 42, Ural, Ural.color) # Ural
    Siberia.circleCoordinates = drawCircle(app, canvas, 5, 45, Siberia, Siberia.color) # Siberia
    Irkutsk.circleCoordinates = drawCircle(app, canvas, 13, 50, Irkutsk, Irkutsk.color) # Irkutsk
    Yakutsk.circleCoordinates = drawCircle(app, canvas, 3, 51, Yakutsk, Yakutsk.color) # Yakutsk
    Mongolia.circleCoordinates = drawCircle(app, canvas, 20, 52, Mongolia, Mongolia.color) # Mongolia
    Kamchatka.circleCoordinates = drawCircle(app, canvas, 3, 58, Kamchatka, Kamchatka.color) # Kamchatka
    Japan.circleCoordinates = drawCircle(app, canvas, 22, 59, Japan, Japan.color) # Japan
    
    # AUSTRALIA
    Indonesia.circleCoordinates = drawCircle(app, canvas, 54, 47, Indonesia, Indonesia.color) # Indonesia
    New_Guinea.circleCoordinates = drawCircle(app, canvas, 46, 59, New_Guinea, New_Guinea.color) # New_Guinea
    Western_Australia.circleCoordinates = drawCircle(app, canvas, 67, 52, Western_Australia, Western_Australia.color) # Western_Australia
    Eastern_Australia.circleCoordinates = drawCircle(app, canvas, 64, 60, Eastern_Australia, Eastern_Australia.color) # Eastern_Australia



def mousePressed(app, event):
    # print("(row,col):", getCell(app, event.x, event.y))
    # print("event.x = ", event.x)
    # print("event.y = ", event.y)
    # print("Alaska Coordinates", Alaska.circleCoordinates)


    for region in regionsSet:
        cx, cy = region.circleCoordinates
        # checks if the user clicked inside the circle that 
        # is linked to a region

        allRegionsOccupied = checkRegionsOccupied()
        if(not allRegionsOccupied):
            booleanExpression = 'region.occupied == False'
        else:
            booleanExpression = 'region.troopGeneral == app.currentPlayer'



        # if (clickedInCircle(app, cx, cy, event.x, event.y) and 
        # (region.occupied == False or region.troopGeneral == app.currentPlayer)):
        if (clickedInCircle(app, cx, cy, event.x, event.y) and eval(booleanExpression)):
            region.occupied = True
            # print(f"{region.name} troop count:", region.troopCount)
            region.troopCount += 1 # adding one troop for now, will change later
            # print(f"{region.name} troop count:", region.troopCount)
            
            if(app.setup == True): # setup stage
                app.currentPlayer.territories.add(region)
                region.troopGeneral = app.currentPlayer

                region.color = app.currentPlayer.color

                app.currentPlayer.initialNumOfTroops -= 1
                # print(f'current index = {app.currentIndex}')
                app.currentIndex = ((app.currentIndex + 1) % app.numOfPlayers)
                # print(f'current index = {app.currentIndex}')
                app.currentPlayer = app.turns[app.currentIndex]
                
                if(app.turns[len(app.turns) - 1].initialNumOfTroops == 0):
                    app.setup = False
                    app.step1Now = True

            elif(app.step1Now == True):
                if(app.currentPlayer.troopPlaceCount > 0):
                    app.currentPlayer.troopPlaceCount -= 1    

                region.troopCount -= 1
                if(app.currentPlayer.troopPlaceCount == 0):
                    app.step1Now = False
                    app.step2Now = True



            # sets the last clicked region to selected region,
            # this is useful for drawFromTo function

            app.selectedRegionName = (region.name)
            # fix me, error handling 'Not in Neighbor'
            if (app.isFrom == True and app.isTo == False):
                app.fromRegionObject = region # used for calculating troop counts
                app.fromRegionString = app.selectedRegionName # used for dictionary searching
                if(app.toRegionString != ''):
                    ifNeighbors = checkIfNeighbors(app.fromRegionString, app.toRegionString)
                    if(not ifNeighbors):
                        app.fromRegionString = 'Not a Neighbor'
            elif (app.isTo == True and app.isFrom == False):
                app.toRegionObject = region # used for calculating troop counts
                app.toRegionString = app.selectedRegionName # used for dictionary searching
                if(app.fromRegionString != ''):
                        ifNeighbors = checkIfNeighbors(app.fromRegionString, app.toRegionString)
                        if(not ifNeighbors):
                            app.toRegionString = 'Not a Neighbor'

            #remember to add two conditons to the fromRegion toRegion code above
            # 1) toRegion cannot be a region that the current player occupies
            # 2) fromRegion must have AT LEAST two troops

            # region.occupied = True
            # region.troopGeneral = player1 (whatever)
        


    # if ROLL clicked (and on step2 of game), then call rollDice fn

def checkRegionsOccupied():
    for region in regionsSet:
        if(region.occupied == False):
            return False
    return True

# distance formula to ckeck if clicked in circle
def clickedInCircle(app, cx, cy, x, y):
    dist = ((x - cx)**2 + (y - cy)**2)**0.5
    if(dist <= app.circleRadius + 3): # give a little leeway 
        return True
    return False

def keyPressed(app, event):
    if(app.step2Now == True):
        if (event.key == 'f'):
            app.isFrom = True
            app.isTo = False

        elif (event.key == 't'):
            app.isFrom = False
            app.isTo = True
        
        elif (event.key == 'r'):
            app.fromRegionString = ''
            app.toRegionString = ''

        elif(event.key == 'a'):
        #  and 
        #     app.fromRegionString != '' and # <-- fix this
        #     app.toRegionString != ''): # <----^
            
            # app.A_width = 3

            attackingMax = checkMaxTroopsToAttack(app)

            if(event.key == "Up" and app.attackingTroopCount < attackingMax):
                app.attackingTroopCount += 1
            elif(event.key == "Down" and app.attackingTroopCount > 1):
                app.attackingTroopCount -= 1

        elif(event.key == 'd'):
        # and 
        #     app.fromRegionString != '' and # <-- fix this
        #     app.toRegionString != ''): # <-----^
            
#            app.B_width = 3

            defendingMax = checkMaxTroopsToDefend(app)

            if(event.key == "Up" and app.defendingTroopCount < defendingMax):
                app.attackingTroopCount += 1
            elif(event.key == "Down" and app.defendingTroopCount > 1):
                app.attackingTroopCount -= 1

        elif(event.key == 'Space'):
            (app.attackingDice, app.defendingDice,
            app.diedAttacking, app.diedDefending) = rollDice(app.attackingTroopCount, app.defendingTroopCount)

# calculates the max num of troops player can attack with 
def checkMaxTroopsToAttack(app):
    highestNum = app.fromRegionObject.troopCount - 1
    if(highestNum >= 3):
        return 3
    elif(highestNum == 2):
        return 2
    else:
        return False

# calculates the max num of troops player can defend with 
def checkMaxTroopsToDefend(app):
    highestNum = app.toRegionObject.troopCount
    if(highestNum >= 2):
        return 2
    else: # highestNum < 2
        return 1

def main():
    runApp(width=1280, height=755)

if __name__ == '__main__':
    main()
