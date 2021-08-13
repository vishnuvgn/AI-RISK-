# This file includes functions that control the computer's moves

import random
from worldMap import *
from helpers import *
from diceRoll import *

def checkRegionsOccupied():
    for region in regionsSet:
        if(region.occupied == False):
            return False
    return True

def aiPlaySETUP(app):
    
    region = random.choice(list(regionsSet))
    while(region.occupied == True):
        region = random.choice(list(regionsSet))
        allRegionsOccupied = checkRegionsOccupied()
        if(allRegionsOccupied):
            region = random.choice(list(app.currentPlayer.territories))
            break

    region.occupied = True

    region.troopCount += 1 # adding one troop for now, will change later

    app.currentPlayer.territories.add(region)
    region.troopGeneral = app.currentPlayer

    region.color = app.currentPlayer.color

    app.currentPlayer.initialNumOfTroops -= 1
    app.currentIndex = ((app.currentIndex + 1) % app.numOfPlayers)
    app.currentPlayer = app.turns[app.currentIndex]

    # print("ai is playing")

def aiPlay(app):
    aiPlaySTEP1(app)
    aiPlaySTEP2(app)

def aiPlaySTEP1(app):
    while (app.currentPlayer.troopPlaceCount > 0):
        region = random.choice(list(app.currentPlayer.territories))
        region.troopCount += 1
        app.currentPlayer.troopPlaceCount -= 1

        # print(f"region: {region.name}, troops there: {region.troopCount}")

    if(app.currentPlayer.troopPlaceCount == 0):
        app.setup = False
        app.step1Now = False
        app.step2Now = True
        app.step3Now = False
        app.finishedRequired = True # all required thing are done

    # print("ai is playing")

def aiPlaySTEP2(app):
    a_or_n = attackOrNot()

    if (a_or_n == True):

        app.fromRegionObject = decideFromRegion(app)
        # print(f'app.fromRegionObject : {app.fromRegionObject}')
        if(app.fromRegionObject == False):
            return 
        # print(f'app.fromRegionObjectName : {app.fromRegionObject.name}')

        app.fromRegionString = app.fromRegionObject.name


        app.toRegionObject = decideToRegion(app, app.fromRegionObject)
        app.toRegionString = app.toRegionObject.name

        app.attackingTroopCount = decideTroopAttackCount(app.fromRegionObject)
        app.defendingTroopCount = app.toRegionObject.troopCount

        (app.attackingDice, app.defendingDice,
        app.diedAttacking, app.diedDefending) = rollDice(app.attackingTroopCount, 
                                                        app.defendingTroopCount)

    #     print(f'''{app.fromRegionString} with {app.fromRegionObject.troopCount} soldiers
    # to {app.toRegionString} with {app.toRegionObject.troopCount} soldiers''')

        app.fromRegionObject.troopCount -= app.diedAttacking
        app.toRegionObject.troopCount -= app.diedDefending

        if(app.toRegionObject.troopCount < 1):
            conquer(app, app.toRegionObject, app.fromRegionObject,
                    app.attackingTroopCount, app.diedAttacking)


    app.setup = False
    app.step1Now = False
    app.step2Now = False
    app.step3Now = True
    app.finishedRequired = True # all required thing are done

    # print("ai is playing")

# helper fn that decides whether the computer should attack or not
def attackOrNot():
    decision = random.choice([0, 1])
    # decision = random.choice(0,1)
    if(decision == 0):
        # print("ai not attacking")
        return False    
    else:
        # print("ai attacking")
        return True
        

# helper fn that decides where to attack from
def decideFromRegion(app):
    fromRegions = list(app.currentPlayer.territories)
    region = random.choice(fromRegions)

    while(len(fromRegions) > 0):
        if(region.troopCount > 1 and checkNeighbors(app, region)):
            return region
        else:
            fromRegions.remove(region)
            if(len(fromRegions) == 0):
                return False
            else:    
                region = random.choice(fromRegions)
    
    return False


def checkNeighbors(app, fromRegion):
    for neighbor in worldMap[fromRegion.name]:
        if (neighbor.troopGeneral.name != app.currentPlayer.name):
            return True
    
    return False

# helper fn that decides where to attack to
def decideToRegion(app, fromRegion):
    legalToAttackPlaces = []

    for place in worldMap[fromRegion.name]:
        if (place.troopGeneral.name != app.currentPlayer.name):
            legalToAttackPlaces.append(place)
    
    # print(legalToAttackPlaces)
    region = random.choice(legalToAttackPlaces)

    return region

# helper fn that decides how many troops to attack with
def decideTroopAttackCount(fromRegion):

    attackingMax = checkMaxTroopsToAttack_AI(fromRegion)

    numOfTroops = random.randint(1, attackingMax - 1)
    return numOfTroops


def checkMaxTroopsToAttack_AI(fromRegion):
    highestNum = fromRegion.troopCount - 1
    if(highestNum >= 3):
        return 3
    else:
        return 2


####################
# AI Defending
####################

def aiDefend(app):
    num = decideTroopDefendCount(app.toRegionObject)
    return num

def decideTroopDefendCount(toRegion):

    defendingMax = checkMaxTroopsToDefend_AI(toRegion)

    numOfTroops = random.randint(1, defendingMax)
    return numOfTroops

def checkMaxTroopsToDefend_AI(toRegion):
    highestNum = toRegion.troopCount
    if(highestNum >= 2):
        return 2
    else: # highestNum < 2
        return 1


