#################################################
# Term Project: RISK
#
# Your name: Vishnu Venugopal
# Your andrew id: vvenugop
#
#################################################

# import cs112_n21_week4_linter
import math, copy, random

from worldMap import *
from cmuHelperFns import *
from drawingFunctions import *

# whats the diff btw import and from...import

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
    def __init__(self):
        # self.name = ""
        self.cardCount = 0 # how many territory cards they have at a certain time
        self.cards = [] # what the cards are - list of Card objects
        self.territories = [] # list of territories under Player control
        self.troopPlaceCount = None # how many troops Player gets to place on the map at the start of their turn
        self.controlContinent = False
        self.color = None

    # methods for recieving (placing) troops, attacking, defending, manuevering
        
class Card(object):
    def __init__(self, territory, icon): # EX: c1 = Card(Alaska, Cavalry)
        self.territory = territory
        self.icon = icon

def appStarted(app):
    app.map = app.loadImage('riskmap.jpeg')
    app.map = app.scaleImage(app.map, 1)
    app.rows = 100
    app.cols = 100
    app.circleRadius = 15
    app.setup = False
    app.step1Now = False # if player on step1 or not
    app.step2Now = False # if player on step2 or not
    app.step3Now = False # if player on step3 or not
    
    app.selectedRegionName = None

    app.isFrom = False
    app.isTo = False
    app.fromRegion = ''
    app.toRegion = ''
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
    color = "white"
    # NORTH AMERICA
    Alaska.circleCoordinates = drawCircle(app, canvas, 3, 2, Alaska, color) # Alaska
    Northwest_Territory.circleCoordinates = drawCircle(app, canvas, 4, 10, Northwest_Territory, color) # Northwest Territory
    Alberta.circleCoordinates = drawCircle(app, canvas, 19, 4, Alberta, color) # Alberta
    Western_United_States.circleCoordinates = drawCircle(app, canvas, 26, 4, Western_United_States, color) # Western United States
    Central_America.circleCoordinates = drawCircle(app, canvas, 36, 6, Central_America, color) # Central America
    Eastern_United_States.circleCoordinates = drawCircle(app, canvas, 29, 17, Eastern_United_States, color) # Eastern United States
    Greenland.circleCoordinates = drawCircle(app, canvas, 3, 21, Greenland, color) # Greenland
    Ontario.circleCoordinates = drawCircle(app, canvas, 13, 14, Ontario, color) # Ontario
    Quebec.circleCoordinates = drawCircle(app, canvas, 17, 21, Quebec, color) # Quebec


    # drawCircle(app, canvas, 35, 16,color) # Venezuela
    # drawCircle(app, canvas, 45, 8,color) # Peru
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska



def mousePressed(app, event):
    print("(row,col):", getCell(app, event.x, event.y))
    print("event.x = ", event.x)
    print("event.y = ", event.y)
    # print("Alaska Coordinates", Alaska.circleCoordinates)


    for region in regionsSet:
        cx, cy = region.circleCoordinates
        # checks if the user clicked inside the circle that 
        # is linked to a region
        if (clickedInCircle(app, cx, cy, event.x, event.y)):
            print(f"{region.name} troop count:", region.troopCount)
            region.troopCount += 1 # adding one troop for now, will change later
            print(f"{region.name} troop count:", region.troopCount)
            
            # sets the last clicked region to selected region,
            # this is useful for drawFromTo function

            app.selectedRegionName = (region.name)
            # fix me, error handling 'Not in Neighbor'
            if (app.isFrom == True and app.isTo == False):
                app.fromRegion = app.selectedRegionName
                if(app.toRegion != ''):
                    ifNeighbors = checkIfNeighbors(app.fromRegion,app.toRegion)
                    if(not ifNeighbors):
                        app.fromRegion = 'Not a Neighbor'
            elif (app.isTo == True and app.isFrom == False):
                app.toRegion = app.selectedRegionName
                if(app.fromRegion != ''):
                        ifNeighbors = checkIfNeighbors(app.fromRegion,app.toRegion)
                        if(not ifNeighbors):
                            app.toRegion = 'Not a Neighbor'
            # region.occupied = True
            # region.troopGeneral = player1 (whatever)
        

# distance formula to ckeck if clicked in circle
def clickedInCircle(app, cx, cy, x, y):
    dist = ((x - cx)**2 + (y - cy)**2)**0.5
    if(dist <= app.circleRadius + 3): # give a little leeway 
        return True
    return False

def keyPressed(app, event):
    if (event.key == 'f'):
        app.isFrom = True
        app.isTo = False

    elif (event.key == 't'):
        app.isFrom = False
        app.isTo = True
    
    elif (event.key == 'r'):
        app.fromRegion = ''
        app.toRegion = ''




def main():
    runApp(width=1280, height=755)

if __name__ == '__main__':
    main()
