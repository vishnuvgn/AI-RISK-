# This file includes functions that control the computer's moves
# this file is the ai who only thinks about attacking

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

# places troops downs
def aiPlaySTEP1(app):
    while (app.currentPlayer.troopPlaceCount > 0):
        region = random.choice(list(app.currentPlayer.territories))
        region.troopCount += 1
        app.currentPlayer.troopPlaceCount -= 1

        print(f"placing --> region: {region.name}, troops there: {region.troopCount}")

    if(app.currentPlayer.troopPlaceCount == 0):
        app.setup = False
        app.step1Now = False
        app.step2Now = True
        app.step3Now = False
        app.finishedRequired = True # all required thing are done

    # print("ai is playing")

def aiPlaySTEP2(app):
    (fromR, toR) = decideFromToRegion(app)

    while (fromR != False):

        app.fromRegionObject = fromR
        # print(f'app.fromRegionObject : {app.fromRegionObject}')
        # print(f'app.fromRegionObjectName : {app.fromRegionObject.name}')

        app.fromRegionString = app.fromRegionObject.name


        app.toRegionObject = toR
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
        (fromR, toR) = decideFromToRegion(app)


    app.setup = False
    app.step1Now = False
    app.step2Now = False
    app.step3Now = True
    app.finishedRequired = True # all required thing are done

    # print("ai is playing")



# differences between aiPlaying and aiBrain so far:
# - the decision to attack is not random anymore
# - where to attack and from where is also not random anymore
#   - finds the largest difference between neighbor




# # helper fn that decides whether the computer should attack or not
# def attackOrNot():
#     decision = random.choice([0, 1])
#     # decision = random.choice(0,1)
#     if(decision == 0):
#         print("ai not attacking")
#         return False    
#     else:
#         print("ai attacking")
#         return True
        

# makes sure a country is on the border
def checkNeighbors(app, fromRegion):
    for neighbor in worldMap[fromRegion.name]:
        if (neighbor.troopGeneral.name != app.currentPlayer.name):
            return True
    
    return False

# finds the greatest difference in troops
def decideFromToRegion(app):
    # borderCountries is a list of the attacking player's countries that are on the border
    # helper fn written in aiBrainPlace for finding border territories
    borderCountries = []
    currentTerritories = list(app.currentPlayer.territories)
    for terr in currentTerritories:
        if checkNeighbors(app, terr):
            borderCountries.append(terr)
    
    # checks if the border countries have enough troops to attack
    hasEnoughTroops = False
    for country in borderCountries:
        if country.troopCount > 1:
            hasEnoughTroops = True
        else:
            # if the country doesn't have enough troops, this removes them 
            # from the list
            borderCountries.remove(country) 
    # print(borderCountries)
    # if no country has enough troops, then it will return false and not attack
    if(hasEnoughTroops == False):
        return (False, False) # must return a tuple, but really the second value doesn't mean anything
    
    bestFrom = None
    bestTo = None
    bestDiff = -1
    for country in borderCountries:
        # print(f"from={country.name}")
        for neighbor in worldMap[country.name]:
            if (neighbor.troopGeneral.name != app.currentPlayer.name):
                diff = country.troopCount-neighbor.troopCount
                # print(f"neighbor={neighbor.name}, diff={diff}")
                if(diff > bestDiff):
                    bestDiff = diff
                    bestFrom = country
                    bestTo = neighbor
    # is the diff is less than 2, there is really no point attacking 
    # print(f"bestDiff = {bestDiff}") 
    if(bestDiff < 2):
        return (False, False) # must return a tuple, but really the second value doesn't mean anything
    print(f"attacking --> from = {bestFrom.name}, to = {bestTo.name}")
    return (bestFrom, bestTo)


# # helper fn that decides where to attack from
# # now a wrapper fn
# def decideFromRegion(app):
    

# # helper fn that decides where to attack to
# def decideToRegion(app, fromRegion):
#     legalToAttackPlaces = []

#     for place in worldMap[fromRegion.name]:
#         if (place.troopGeneral.name != app.currentPlayer.name):
#             legalToAttackPlaces.append(place)
    
#     # print(legalToAttackPlaces)
#     # region = random.choice(legalToAttackPlaces)

#     # return region
#     return legalToAttackPlaces



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


