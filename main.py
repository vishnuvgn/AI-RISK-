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

    # methods for recieving (placing) troops, attacking, defending, manuevering
        
class Card(object):
    def __init__(self, territory, icon): # EX: c1 = Card(Alaska, Cavalry)
        self.territory = territory
        self.icon = icon

def appStarted(app):
    app.map = app.loadImage('riskmap.jpeg')

    # code to get size of image
    # https://newbedev.com/python-get-width-and-height-of-image-tkinter-code-example
    img = Image.open('riskmap.jpeg')
    mapPic = ImageTk.PhotoImage(img)
    app.mapHeight = mapPic.height()
    app.mapWidth = mapPic.width()
    
def gameDimensions():
    pass

def redrawAll(app, canvas):
    drawMap(app, canvas)
    drawSideBar(app, canvas)

def drawMap(app, canvas):
    canvas.create_image(app.mapWidth/2, app.mapHeight/2, image=ImageTk.PhotoImage(app.map))

def drawSideBar(app, canvas):
    canvas.create_rectangle(app.mapWidth + 10, 10, app.width - 10, app.mapHeight, outline="black", fill="black")
    canvas.create_text((app.width - 10 + (app.mapWidth + 10) )/2,
                        (app.mapHeight - 10)/2, text="hello", fill="white")

def main():
    runApp(width=1280, height=755)

if __name__ == '__main__':
    main()



