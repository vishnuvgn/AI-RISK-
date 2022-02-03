# This file includes functions that control the computer's moves
# this file is the ai who thinks about placement and attacking

import random
from worldMap import *
from helpers import *
from diceRoll import *


def checkRegionsOccupied():
    for region in regionsSet:
        if(region.occupied == False):
            return False
    return True

# setup is kept at random for
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
# def aiPlaySTEP1(app):
#     while (app.currentPlayer.troopPlaceCount > 0):
#         region = random.choice(list(app.currentPlayer.territories))
#         region.troopCount += 1
#         app.currentPlayer.troopPlaceCount -= 1

#         print(f"placing --> region: {region.name}, troops there: {region.troopCount}")

#     if(app.currentPlayer.troopPlaceCount == 0):
#         app.setup = False
#         app.step1Now = False
#         app.step2Now = True
#         app.step3Now = False
#         app.finishedRequired = True # all required thing are done

#     # print("ai is playing")

# makes sure a country is on the border
def checkNeighbors(app, fromRegion):
    for neighbor in worldMap[fromRegion.name]:
        if (neighbor.troopGeneral.name != app.currentPlayer.name):
            return True
    
    return False


# for step1
def findBorderCountries(app):
    borderCountries = []
    currentTerritories = list(app.currentPlayer.territories)
    for terr in currentTerritories:
        if checkNeighbors(app, terr):
            borderCountries.append(terr)

    return borderCountries.copy()

# for step1, gets the deficit sum for 1 territory
def enemiesAround(app, country, borderCountries):
    # print(f"from={country.name}")
    dSum = 0
    for neighbor in worldMap[country.name]:
        if (neighbor.troopGeneral.name != app.currentPlayer.name):
            if(neighbor.troopCount > 1): # weeds out enemies who cannot attack
                deficit = abs(neighbor.troopCount - country.troopCount)
                dSum += deficit
    return dSum

# finds the weakest country of the oppoenent
def findWeakest(app, borderCountries):
    weakestCount = None # none b/c it can't be a number as you are not finding the strongest. Negative #'s are all smaller so default -1 can't be used
    weakestCountry = None

    for country in borderCountries:
        # print(f"from={country.name}")
        for neighbor in worldMap[country.name]:
            if (neighbor.troopGeneral.name != app.currentPlayer.name):
                # the second parameter just allows for the loop to start
                if(weakestCount == None or neighbor.troopCount < weakestCount):
                    weakestCount = neighbor.troopCount
                    weakestCountry = neighbor
    
    return(weakestCount, weakestCountry)


def aiPlaySTEP1(app):
    borderCountries = findBorderCountries(app)

    ################################ 
    # placement for defense
    countryAndDeficit = []
    # looping through border countries and finding the deficits
    for country in borderCountries:
        dSum = enemiesAround(app, country, borderCountries)
        countryAndDeficit.append((dSum, country.name, country))
    
    countryAndDeficit.sort(reverse=True) # sorts the country and respective deficits in decesnding order    
    print(f'countryDeficit = {countryAndDeficit}')
    countryNum = 0
    length = len(borderCountries)
    for (dSum, countryName, country) in countryAndDeficit:
        if(dSum == 0 or dSum - country.troopCount <= 0):
            break
        countryNum += 1
        # checks if it is worth trying to defend
        if(country.troopCount + app.currentPlayer.troopPlaceCount >= dSum):
            # adding just enough troops so that the troopCount in that territory 
            # is equal to the deficit
            app.currentPlayer.troopPlaceCount -= (dSum - country.troopCount)
            print(f"placed {(dSum - country.troopCount)} troops in {country.name}")
            country.troopCount += (dSum - country.troopCount)
            
            if(app.currentPlayer.troopPlaceCount == 0):
                break
        # last index of array
        elif(countryNum == length-1):
            print(f"end of array: placed {(app.currentPlayer.troopPlaceCount)} troops in {country.name}")
            country.troopCount += app.currentPlayer.troopPlaceCount
            app.currentPlayer.troopPlaceCount = 0
    ################################ 
    # placing any remaining troops getting ready for attack
    if(app.currentPlayer.troopPlaceCount != 0)  :  
        weakestCount, weakestCountry = findWeakest(app, borderCountries)
        # fromPossibles is a set of the attacker's countries that border the 
        # weakest country of the opponent
        fromPossibles = worldMap[weakestCountry.name]
        possibles = []
        for state in fromPossibles:
            if (state.troopGeneral.name == app.currentPlayer.name):
                possibles.append(state)
        
        for place in possibles:
            print(f'possible = {place.name}', end="")

        placeHere = random.choice(possibles)
        print(f"placed {(app.currentPlayer.troopPlaceCount)} troops in {placeHere.name} to plan an attack {weakestCountry.name}")
        placeHere.troopCount += app.currentPlayer.troopPlaceCount
        app.currentPlayer.troopPlaceCount = 0


    app.setup = False
    app.step1Now = False
    app.step2Now = True
    app.step3Now = False
    app.finishedRequired = True # all required thing are done

    print("ai is playing")
    

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
        


# finds the greatest difference in troops
def decideFromToRegion(app):
    # borderCountries is a list of the attacking player's countries that are on the border
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


