import random
'''

attacker chooses number of troops to attack with
defender chooses number of troops to defend with

roll attacking dice and roll defending dice

match up the largest die from both attacking and defending 
match up the 2nd largest die from both attacking and defending 

decide how many die from attacking and how many die from defending

subtract deadAttacking from the troopCount on the FROM region
subtract deadDefending from the troopCount on the TO region

display what happened and ask to roll again


'''

def rollDice(attackingTroopCount, defendingTroopCount):
    attackingDice = []
    defendingDice = []

    for i in range(attackingTroopCount):
        die = random.randint(1,6)
        attackingDice.append(die)

    for i in range(defendingTroopCount):
        die = random.randint(1,6)
        defendingDice.append(die)

    # will sort lists in decending order

    decendingOrder(attackingDice)
    decendingOrder(defendingDice)

    # print(f'attack: {attackingDice}')
    # print(f'defend: {defendingDice}')

    lengthOfShortestList = min(attackingTroopCount, defendingTroopCount)    
    shortened_A_dice = attackingDice[:lengthOfShortestList]
    shortened_D_dice = defendingDice[:lengthOfShortestList]
    
    # print()
    # print(f'attack: {shortened_A_dice}')
    # print(f'defend: {shortened_D_dice}')

    diedAttacking = 0
    diedDefending = 0
    for i in range(lengthOfShortestList):
        if(shortened_A_dice[i] > shortened_D_dice[i]):
            diedDefending += 1 
        else: # attackingDice[i] <= defendingDice[i]
            diedAttacking += 1

    # print()
    # print(f'diedAttacking = {diedAttacking}')
    # print(f'diedDefending = {diedDefending}')

    return (attackingDice, defendingDice, diedAttacking, diedDefending)

# destructive fn that sorts a list of nums in decending order
def decendingOrder(L):
    L.sort()
    L.reverse()

rollDice(3,2)