from worldMap import *


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

def checkGameEnd(app, currentPlayer):
    if(len(currentPlayer.territories) == len(regionsSet)):
        app.winner = currentPlayer
        return True
    else:
        return False

def conquer(app, toRegionObject, fromRegionObject, attackCount, diedAttacking):
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

    if(checkGameEnd(app, conquerer)):
        endGame(app)

