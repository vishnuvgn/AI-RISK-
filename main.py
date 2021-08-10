#################################################
# Term Project: RISK
#
# Your name: Vishnu Venugopal
# Your andrew id: vvenugop
#
#################################################

# import cs112_n21_week4_linter
import math, copy, random

import worldMap
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


# if fill color not given, that means it should be transparent b/c the circle is within a country
def drawCircle(app, canvas, row, col, fillColor=""): 
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    r = 15 # radius of circle is 15
    canvas.create_oval(x0-r, y0-r, x1+r, y1+r, fill=fillColor)

def drawAllCircles(app, canvas):
    color = "white"
    # NORTH AMERICA
    drawCircle(app, canvas, 3, 2,color) # Alaska
    drawCircle(app, canvas, 4, 10,color) # Northwest Territory
    drawCircle(app, canvas, 19, 4,color) # Alberta
    drawCircle(app, canvas, 26, 4,color) # Western United States
    drawCircle(app, canvas, 36, 6,color) # Central America
    drawCircle(app, canvas, 29, 17,color) # Eastern United States
    drawCircle(app, canvas, 3, 21,color) # Greenland
    drawCircle(app, canvas, 13, 14,color) # Ontario
    drawCircle(app, canvas, 17, 21,color) # Quebec

    drawCircle(app, canvas, 35, 16,color) # Venezuela
    drawCircle(app, canvas, 45, 8,color) # Peru
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska
    # drawCircle(app, canvas, 3, 2,"white") # Alaska



def mousePressed(app, event):
    print(getCell(app, event.x, event.y))


def main():
    runApp(width=1280, height=755)

if __name__ == '__main__':
    main()



