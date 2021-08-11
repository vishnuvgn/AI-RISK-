from worldMap import *

def mousePressed(app, event):
    # bottom right corner of map
    if(event.x <= app.mapRightX and event.y <= app.mapBottomY): 

        if(app.setup == True):
            setupMouseClicked(app, event)
        elif(app.step1Now == True):
            step1MouseClicked(app, event)
        elif(app.step2Now == True):
            step2MouseClicked(app, event)
        elif(app.step2Now == True):
            pass

def setupMouseClicked(app, event):
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
            # print(f'current index = {app.currentIndex}')
            app.currentIndex = ((app.currentIndex + 1) % app.numOfPlayers)
            # print(f'current index = {app.currentIndex}')
            app.currentPlayer = app.turns[app.currentIndex]
            
            if(app.turns[len(app.turns) - 1].initialNumOfTroops == 0):
                app.setup = False
                app.step1Now = True
                app.step2Now = False
                app.step3Now = False

def step1MouseClicked(app, event): # reinforcement
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
                verifyFromRegion(app)

            elif(app.isFrom == False and app.isTo == True and app.isFromLegal == True):
                app.toRegionString = app.selectedRegionName
                app.toRegionObject = app.selectedRegionObject
                verifyToRegion(app)
# verifys if the fromRegion is valid
# changes app.isFromLegal accordingly
def verifyFromRegion(app):
    # checks if the player controls from region
    if(app.fromRegionObject not in app.currentPlayer.territories): 
        app.fromRegionString = f"You don't control {app.fromRegionString}"
        app.fromRegionObject = None
        app.isFromLegal = False
    # checks if the player has the minimum number of troops 
    # to attack from the fromRegion
    elif(app.fromRegionObject.troopCount < 2):
        app.fromRegionString = f"You don't have enough troops in {app.fromRegionString} to attack"
        app.fromRegionObject = None
        app.isFromLegal = False
    else:
        app.isFromLegal = True

# verifys if the toRegion is valid
# changes app.isToLegal accordingly
def verifyToRegion(app):
    # checks if the player already controls that region
    # if they do, then what's the point of attacking?
    # it will not allow it
    if(app.toRegionObject in app.currentPlayer.territories):
        app.toRegionString = f"You already control {app.toRegionString}"
        app.toRegionObject = None
        app.isToLegal = False

    elif(app.toRegionObject not in worldMap[app.fromRegionString]):
        # print(f'app.toRegionString = {app.toRegionString}')
        # print(f'')
        app.toRegionString = f"{app.toRegionString} is not a neighbor of {app.fromRegionString}"
        app.toRegionObject = None
        app.isToLegal = False
    else:
        app.isToLegal = True
 



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
