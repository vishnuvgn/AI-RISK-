# This file contains what will happen if the mouse is pressed depending on 
# the step that the game is in (attacking vs placing troops)

from worldMap import *
from aiPlayingRandom import *

def mousePressed(app, event):
    # bottom right corner of map
    if(event.x <= app.mapRightX and event.y <= app.mapBottomY): 

        if(app.setup == True):
            setupMouseClicked(app, event)
        elif(app.step1Now == True):
            step1MouseClicked(app, event)
        elif(app.step2Now == True):
            step2MouseClicked(app, event)
        elif(app.step3Now == True):
            step3MouseClicked(app, event)

def calculateTroopPlaceCount(app, territoriesSet):
    if(len(territoriesSet) < 9):
        return 3
    else:
        return (len(app.currentPlayer.territories) // 3)

def setupMouseClicked(app, event):
    app.helpStringKey1 = 0
    for region in regionsSet:
        (cx, cy) = region.circleCoordinates
        # checks if the user clicked inside the circle that 
        # is linked to a region

        allRegionsOccupied = checkRegionsOccupied()
        if(not allRegionsOccupied):
            booleanExpression = 'region.occupied == False'
        else:
            booleanExpression = 'region.troopGeneral == app.currentPlayer'

        if (clickedInCircle(app, cx, cy, event.x, event.y) and 
            eval(booleanExpression)):
            region.occupied = True
        # print(f"{region.name} troop count:", region.troopCount)
            region.troopCount += 1 # adding one troop for now, will change later
        # print(f"{region.name} troop count:", region.troopCount)

            app.currentPlayer.territories.add(region)
            region.troopGeneral = app.currentPlayer

            region.color = app.currentPlayer.color

            app.currentPlayer.initialNumOfTroops -= 1
            app.currentIndex = ((app.currentIndex + 1) % app.numOfPlayers)
            app.currentPlayer = app.turns[app.currentIndex]

            # if ai's turn, call aiPlaySETUP for it to make a move
            if(app.currentPlayer.isAI):
                aiPlaySETUP(app)      
            
            if(app.turns[len(app.turns) - 1].initialNumOfTroops == 0):
                app.setup = False
                app.step1Now = True
                app.step2Now = False
                app.step3Now = False
                app.currentPlayer.troopPlaceCount = calculateTroopPlaceCount(app, app.currentPlayer.territories)



def step1MouseClicked(app, event): # reinforcement
    app.helpStringKey1 = 0
    for region in regionsSet:
        (cx, cy) = region.circleCoordinates
        # checks if the user clicked inside the circle that 
        # is linked to a region
        if (clickedInCircle(app, cx, cy, event.x, event.y) and
            region.troopGeneral == app.currentPlayer):
            
            if(app.currentPlayer.troopPlaceCount > 0):
                region.troopCount += 1
                app.currentPlayer.troopPlaceCount -= 1

            if(app.currentPlayer.troopPlaceCount == 0):
                app.setup = False
                app.step1Now = False
                app.step2Now = True
                app.step3Now = False
                app.finishedRequired = True # all required thing are done
                app.helpStringKey1 = 1
                app.helpStringKey2 = 2
                app.helpStringKey3 = 3


def step2MouseClicked(app, event): # attacking
    for region in regionsSet:
        (cx, cy) = region.circleCoordinates
        # checks if the user clicked inside the circle that 
        # is linked to a region

        if (clickedInCircle(app, cx, cy, event.x, event.y)):
            app.selectedRegionObject = region
            app.selectedRegionName = region.name 
            # print(f'selected region name = {app.selectedRegionName}')

            if(app.isFrom == True and app.isTo == False):
                app.fromRegionString = app.selectedRegionName
                app.fromRegionObject = app.selectedRegionObject
                verifyFromRegion(app, "attack")

            elif(app.isFrom == False and app.isTo == True and app.isFromLegal == True):
                app.toRegionString = app.selectedRegionName
                app.toRegionObject = app.selectedRegionObject
                verifyToRegion(app)

# verifys if the fromRegion is valid
# changes app.isFromLegal accordingly
def verifyFromRegion(app, action):
    # checks if the player controls from region
    if(app.fromRegionObject not in app.currentPlayer.territories): 
        app.errorString = f"You don't control {app.fromRegionString}"
        app.fromRegionString = ''
        app.fromRegionObject = None
        app.isFromLegal = False
    # checks if the player has the minimum number of troops 
    # to attack from the fromRegion
    elif(app.fromRegionObject.troopCount < 2):
        app.errorString = f"You don't have enough troops in {app.fromRegionString} to {action}"
        app.fromRegionString = ''
        app.fromRegionObject = None
        app.isFromLegal = False
    else:
        app.isFromLegal = True
        app.errorString = ''

# verifys if the toRegion is valid
# changes app.isToLegal accordingly
def verifyToRegion(app):
    # checks if the player already controls that region
    # if they do, then what's the point of attacking?
    # it will not allow it
    if(app.toRegionObject in app.currentPlayer.territories):
        app.errorString = f"You already control {app.toRegionString}"
        app.toRegionString = ''
        app.toRegionObject = None
        app.isToLegal = False

    elif(app.toRegionObject not in worldMap[app.fromRegionString]):
        # print(f'app.toRegionString = {app.toRegionString}')
        # print(f'')
        app.errorString = f"{app.toRegionString} is not a neighbor of {app.fromRegionString}"
        app.toRegionString = ''
        app.toRegionObject = None
        app.isToLegal = False
    else:
        app.isToLegal = True
        app.helpStringKey1 = 1
        app.helpStringKey2 = 4
        app.helpStringKey3 = 5
        app.errorString = ''


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


def step3MouseClicked(app, event):
    for region in regionsSet:
        (cx, cy) = region.circleCoordinates
        # checks if the user clicked inside the circle that 
        # is linked to a region

        if (clickedInCircle(app, cx, cy, event.x, event.y)):
            app.selectedRegionObject = region
            app.selectedRegionName = region.name 
            # print(f'selected region name = {app.selectedRegionName}')

            if(app.isFrom == True and app.isTo == False):                
                app.fromRegionString = app.selectedRegionName
                app.fromRegionObject = app.selectedRegionObject
                verifyFromRegion(app, "maneuver")

            elif(app.isFrom == False and app.isTo == True and app.isFromLegal == True):
                app.toRegionString = app.selectedRegionName
                app.toRegionObject = app.selectedRegionObject
                checkStep3To(app)

            

def checkStep3To(app):
    breadCrumbs = []
    if(app.toRegionObject not in app.currentPlayer.territories):
        app.errorString = f"You don't control {app.toRegionString}"
        app.toRegionString = ''
        app.toRegionObject = None
        app.isToLegal = False

    elif(isThereAPath(worldMap, app.fromRegionString, app.toRegionObject, breadCrumbs, app.currentPlayer) == False): # no path
        # print(f'app.toRegionString = {app.toRegionString}')
        # print(f'')
        app.errorString = f"There is not a path from {app.fromRegionString} to {app.toRegionString}"
        app.toRegionString = ''
        app.toRegionObject = None
        app.isToLegal = False
    else:
        app.isToLegal = True
        app.helpStringKey1 = 8
        app.helpStringKey2 = 11
        app.helpStringKey3 = 12
        app.errorString = ''


'''
How this fn works:
- check recursively depth (checking the children)
- check iteratively latterally (checking the siblings)
'''
def isThereAPath(worldMap, node, target, breadCrumbs, currentPlayer):
    # breadCrumbs.add(node)
    breadCrumbs.append(node)
    #   print(breadCrumbs)
    # print(f"target.name: {target.name}")
    # print(f"node: {node}")
    # print(f"breadCrumbs: {breadCrumbs}")
    # # check 1
    if(target in worldMap[node]):
        # breadCrumbs.append(target.name)
        return True
        
    # check 2
    for neighbor in worldMap[node]:
        if(neighbor in currentPlayer.territories and
            neighbor.name not in breadCrumbs):
            # go down this path recursively
            boolExp = isThereAPath(worldMap, neighbor.name, target, breadCrumbs, currentPlayer)
            if(boolExp == True):
                return True
            else:
                continue
    return False
