# draws a rectangle for sidebar
def drawSideBar(app, canvas):
    canvas.create_rectangle(app.mapWidth + 10, 10, app.width - 10,
                            app.height-10, outline="black")
    if(app.setup == True):
        drawSetup(app, canvas)
    elif(app.step1Now == True):
        drawStep1(app, canvas)
    elif(app.step2Now == True):
        drawStep1(app, canvas)
        drawStep2(app, canvas)
    else:
        drawStep1(app, canvas)
        # drawStep2(app, canvas)
        drawStep3(app, canvas)

def drawBottomBar(app, canvas):
    canvas.create_rectangle(10, app.mapHeight+10, app.mapWidth,
                            app.height-10, outline="black")
    drawHelp(app, canvas)
    drawError(app, canvas)

def drawHelp(app, canvas):
    x0 = 10
    y0 = app.mapHeight+10
    x1 = app.mapWidth
    y1 = ((app.mapHeight+10) + ((app.height-10) - (app.mapHeight+10))/2) + 20
    canvas.create_rectangle(x0, y0, x1, y1)


    help1 = app.helpStringsDict[app.helpStringKey1]
    font="Papyrus 16"
    canvas.create_text((x0+x1)/2, ((y0+y1)/2)-30,
                    text=help1, font=font)


    help2 = ''
    if(app.helpStringKey2 > -1):
        help2 = app.helpStringsDict[app.helpStringKey2]

    canvas.create_text((x0+x1)/2, (y0+y1)/2,
                    text=help2, font=font)
    
    help3 = ''
    if(app.helpStringKey3 > -1):
        help3 = app.helpStringsDict[app.helpStringKey3]

    canvas.create_text((x0+x1)/2, ((y0+y1)/2)+30,
                    text=help3, font=font)


def drawError(app, canvas):
    x0 = 10
    y0 = ((app.mapHeight+10) + ((app.height-10) - (app.mapHeight+10))/2) + 20
    x1 = app.mapWidth                        
    y1 = app.height-10

    canvas.create_rectangle(x0, y0, x1, y1)
    font="Papyrus 16"

    error = app.errorString

    canvas.create_text((x0+x1)/2, (y0+y1)/2,
                    text=error, fill="red", font=font)
    



























# PRE GAME STAGE => SETUP
####################################################
def drawSetup(app, canvas):
    sideBarx0 = app.mapWidth + 10
    sideBary0 = 10
    sideBarx1 = app.width - 10
    sideBary1 = app.height - 10

    sideBarHeight = sideBary1 - sideBary0
    sideBarWidth = sideBarx1 - sideBarx0
    setupHeight = sideBarHeight / app.numOfPlayers

    setup_x0 = sideBarx0
    setup_y0 = sideBary0
    setup_x1 = sideBarx1
    setup_y1 = setup_y0 + setupHeight
    # draws the box for setup

    for i in range(app.numOfPlayers):
        if(i == app.currentIndex):
            width=4
            # troopsLeft = app.currentPlayer.initialNumOfTroops

        else:
            # troopsLeft = app.turns[i].initialNumOfTroops
            width=2

        canvas.create_rectangle(setup_x0, setup_y0, setup_x1,
                            setup_y1, width=width, fill=app.turns[i].color)

        canvas.create_text((setup_x1 + setup_x0)/2, setup_y0+10,
                        text=f"{app.turns[i].name} Place Troops", 
                        fill="black")
        
        troopsLeft = app.turns[i].initialNumOfTroops
        # (at least until all countries are covered) --^

        # app, canvas, troopNumber,
        # top left of sidebar, height of step1box, width of step1box (same as sidebar),
        # row, col (row, col of rectangle),
        # message ("troops placed at a time" or "troops left")

        troopsLeftMessage = "Troops Left"                                            
        drawTroopsBox(app, canvas, troopsLeft,
                    setup_x0,setup_y0,setupHeight,
                    sideBarWidth,2,2, troopsLeftMessage)
        setup_y0 += setupHeight
        setup_y1 = setup_y0 + setupHeight



####################################################


# FIRST STEP DRAWING STUFF
####################################################

# draws all of step 1 (recieving and placing troops)
def drawStep1(app,canvas):
    sideBarx0, sideBary0, sideBarx1, sideBary1 = app.mapWidth + 10, 10, app.width - 10, app.height-10
    sideBarHeight = sideBary1 - sideBary0
    sideBarWidth = sideBarx1 - sideBarx0
    step1Height = sideBarHeight / 5 # divides into 5 rows
    # draws the box for step1
    canvas.create_rectangle(sideBarx0, sideBary0, sideBarx1,
                            sideBary0 + step1Height, width=2, fill=app.currentPlayer.color)
    canvas.create_text((sideBarx1 + sideBarx0)/2, sideBary0+10,
                        text="Place Troops", fill="black")

    troopsLeft = app.currentPlayer.troopPlaceCount # static for now, remember to change

    # app, canvas, troopNumber,
    # top left of sidebar, height of step1box, width of step1box (same as sidebar),
    # row, col (row, col of rectangle),
    # message ("troops placed at a time" or "troops left")

    troopsLeftMessage = "Troops Left"                                            
    drawTroopsBox(app, canvas, troopsLeft,
                  sideBarx0,sideBary0,step1Height,
                  sideBarWidth,2,2, troopsLeftMessage)
    # drawCoverStep2(app, canvas)

# def drawCoverStep2(app, canvas):
#     sideBarx0, sideBary0, sideBarx1, sideBary1 = (app.mapWidth + 10, 10,
#                                                   app.width - 10, app.height-10)
#     sideBarHeight = sideBary1 - sideBary0
#     sideBarWidth = sideBarx1 - sideBarx0
#     topOfStep2Box = sideBarHeight / 5 

#     # step2x0, step2y0, step2x1, step2y1 top left and bottom right points 
#     # of the step2 box
#     step2x0 = sideBarx0
#     step2y0 = topOfStep2Box + 10
#     step2x1 = sideBarx1
#     step2y1 = sideBary1

#     canvas.create_rectangle(step2x0,step2y0,step2x1,step2y1, 
#                             width=2,fill='lightgray')


# used to draw both how many troops left and how many troops placed at a time
# draws one rectangle at row, col with troop info in center (the number)
def drawTroopsBox(app, canvas, troopCount, sideBarx0,sideBary0,
                            step1Height,step1Width,row,col, message):
    x0 = (col*step1Width/5) + sideBarx0
    y0 = (row*step1Height/5) + sideBary0
    x1 = x0 + (step1Width/5)
    y1 = y0 + (step1Height/5)
    countBoxHeight = y1-y0
    # countBoxWidth = x1-x0

    canvas.create_rectangle(x0,y0,x1,y1)
    canvas.create_text((x1+x0)/2,(y1+y0)/2, text=troopCount)
    canvas.create_text((x1+x0)/2,(y1+y0)/2+countBoxHeight,
                        text=message)



####################################################

# SECOND STEP DRAWING STUFF
####################################################
# draws the box for step 2
def drawStep2(app, canvas):
    sideBarx0, sideBary0, sideBarx1, sideBary1 = (app.mapWidth + 10, 10,
                                                  app.width - 10, app.height-10)
    sideBarHeight = sideBary1 - sideBary0
    sideBarWidth = sideBarx1 - sideBarx0
    topOfStep2Box = sideBarHeight / 5 

    # step2x0, step2y0, step2x1, step2y1 top left and bottom right points 
    # of the step2 box
    step2x0 = sideBarx0
    step2y0 = topOfStep2Box + 10
    step2x1 = sideBarx1
    step2y1 = sideBary1

    canvas.create_rectangle(step2x0,step2y0,step2x1,step2y1, width=2)
    canvas.create_text((step2x0 + step2x1)/2, step2y0+10,
                         text="ATTACK")
    # drawSkipButton(app, canvas)
    drawFromTo(app, canvas, step2x0, step2y0, step2x1, step2y1)
    drawChooseTroopCount(app, canvas, step2x0, step2y0, step2x1, step2y1)
    drawRollButton(app,canvas)
    drawDice(app,canvas)
    drawBattleResults(app, canvas)

# # if skipbutton is clicked, then remember to change boolean app.step2Now
# def drawSkipButton(app, canvas):
#     sideBarx0, sideBary0, sideBarx1, sideBary1 = (app.mapWidth + 10, 10,
#                                                   app.width - 10, app.height-10)
#     sideBarHeight = sideBary1 - sideBary0
#     sideBarWidth = sideBarx1 - sideBarx0

#     skipButtonHeigth = 20

#     x0 = (4*sideBarWidth/5) + sideBarx0
#     y0 = (1*sideBarHeight/5) + sideBary0
#     x1 = x0 + (sideBarWidth/5)
#     y1 = y0 + skipButtonHeigth

#     canvas.create_rectangle(x0,y0,x1,y1)
#     canvas.create_text((x1+x0)/2, (y1+y0)/2, text="SKIP")


# step2x0, step2y0, step2x1, step2y1 top left and bottom right points 
# of the step2 box
def drawFromTo(app, canvas, step2x0, step2y0, step2x1, step2y1):
    
    step2BoxHeight = step2y1 - step2y0 # height of step2 box
    step2BoxWidth = step2x1 - step2x0 # width of step2 box / same sidebar width

    x0From = step2x0
    y0From = (step2BoxHeight/10) + step2y0
    x1From = x0From + (step2BoxWidth/2)
    y1From = y0From + (step2BoxHeight/10)
    

    if(app.isFrom == True and app.isTo == False): # if 'f' key has been pressed
        fromWidth = 3
        toWidth = 1
    elif(app.isTo == True and app.isFrom == False): # if 't' key has been pressed
        toWidth = 3
        fromWidth = 1
    else:                   # if neither key has been pressed
        fromWidth = 1
        toWidth = 1
    
    fromText = f'FROM: {app.fromRegionString} '
    toText = f'TO: {app.toRegionString}' 


    canvas.create_rectangle(x0From, y0From, x1From, y1From, width=fromWidth)
    canvas.create_text((x1From+x0From)/2,(y1From+y0From)/2,
                        text=fromText)

    x0To = step2x1 - (step2BoxWidth/2)
    y0To = (step2BoxHeight/10) + step2y0
    x1To = step2x1
    y1To = y0From + (step2BoxHeight/10)

    
    canvas.create_rectangle(x0To, y0To, x1To, y1To, width=toWidth)
    canvas.create_text((x1To+x0To)/2,(y1To+y0To)/2,
                        text=toText)


def drawChooseTroopCount(app, canvas, step2x0, step2y0, step2x1, step2y1):
    # Number of Attacking Troops: 
    # Number of Defending Troops: 
        
    step2BoxHeight = step2y1 - step2y0 # height of step2 box
    step2BoxWidth = step2x1 - step2x0 # width of step2 box / same sidebar width

    x0Attacking = step2x0
    y0Attacking = (2*step2BoxHeight/10) + step2y0 + 5
    x1Attacking = x0Attacking + (step2BoxWidth/2)
    y1Attacking = y0Attacking + (step2BoxHeight/10)

    canvas.create_rectangle(x0Attacking, y0Attacking, x1Attacking, y1Attacking,
                            width=app.width_A)
    
    attackingTroopMessage = "Attacking Troops:" 
    # text for attacking troops
    canvas.create_text((x1Attacking+x0Attacking)/2, (y1Attacking+y0Attacking)/2,
                        text=attackingTroopMessage)


    x0Defending = step2x1 - (step2BoxWidth/2)
    y0Defending = (2*step2BoxHeight/10) + step2y0 + 5
    x1Defending = step2x1
    y1Defending = y0Defending + (step2BoxHeight/10)

    canvas.create_rectangle(x0Defending, y0Defending, x1Defending, y1Defending,
                            width=app.width_D)

    defendingTroopMessage = "Defending Troops:" 
    # text for defending troops
    canvas.create_text((x1Defending+x0Defending)/2, (y1Defending+y0Defending)/2,
                        text=defendingTroopMessage)


    attackingTroopNum = app.attackingTroopCount
    drawTroopCountSquare(app, canvas, x0Attacking, y0Attacking,
                         x1Attacking, y1Attacking,attackingTroopNum)

    defendingTroopNum = app.defendingTroopCount
    drawTroopCountSquare(app, canvas, x0Defending, y0Defending,
                         x1Defending, y1Defending,defendingTroopNum)

    


# A_D => attacking or defending rectangle
def drawTroopCountSquare(app, canvas, A_D_x0, A_D_y0, A_D_x1, A_D_y1,A_D_troopNum): 
    A_D_BoxHeight = A_D_y1 - A_D_y0 # height of A_D_ box
    A_D_BoxWidth = A_D_x1 - A_D_x0 # width of A_D_ box 

    x0CountSquare = A_D_x1 - (A_D_BoxWidth/6) - 10
    y0CountSquare = A_D_y0 + 10
    x1CountSquare = x0CountSquare + (A_D_BoxWidth/6) 
    y1CountSquare = y0CountSquare + (A_D_BoxWidth/6)

    canvas.create_rectangle(x0CountSquare, y0CountSquare,
                            x1CountSquare, y1CountSquare)

    canvas.create_text((x1CountSquare+x0CountSquare)/2,
                        (y1CountSquare + y0CountSquare)/2,
                        text=A_D_troopNum)


def drawRollButton(app, canvas):
    sideBarx0, sideBary0, sideBarx1, sideBary1 = (app.mapWidth + 10, 10,
                                                  app.width - 10, app.height-10)
    sideBarHeight = sideBary1 - sideBary0
    sideBarWidth = sideBarx1 - sideBarx0
    topOfStep2Box = sideBarHeight / 5 
    
    step2x0 = sideBarx0
    step2y0 = topOfStep2Box + 10
    step2x1 = sideBarx1
    step2y1 = sideBary1

    step2Height = step2y1 - step2y0

    x0 = sideBarx0 + (2*sideBarWidth / 5)
    y0 = (3*step2Height/5)
    x1 = x0 + (sideBarWidth / 5) 
    y1 = y0 + 30

    canvas.create_rectangle(x0,y0,x1,y1)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text="ROLL")
    
# fn that draws the dice and takes in the 
# attackingDice list and the defendingDice list    
def drawDice(app, canvas):
    sideBarx0, sideBary0, sideBarx1, sideBary1 = (app.mapWidth + 10, 10,
                                                  app.width - 10, app.height-10)
    sideBarHeight = sideBary1 - sideBary0
    sideBarWidth = sideBarx1 - sideBarx0
    topOfStep2Box = sideBarHeight / 5 
    
    step2x0 = sideBarx0
    step2y0 = topOfStep2Box + 10
    step2x1 = sideBarx1
    step2y1 = sideBary1

    step2Height = step2y1 - step2y0

    A_x0 = sideBarx0 + (sideBarWidth / 7)
    A_y0 = (3*step2Height/5) + 30
    A_x1 = A_x0 + (sideBarWidth / 7) 
    A_y1 = A_y0 + 30

    canvas.create_text((A_x1+A_x0)/2, (A_y0+A_y1)/2, text="ATTACKER")

    D_x0 = sideBarx0 + (5*sideBarWidth / 7)
    D_y0 = (3*step2Height/5) + 30
    D_x1 = D_x0 + (sideBarWidth / 7) 
    D_y1 = D_y0 + 30

    canvas.create_text((D_x1+D_x0)/2, (D_y0+D_y1)/2, text="DEFENDER")

    diceLength = 50 # dice height and width is 25

    attackDice_x0 = sideBarx0 + (sideBarWidth / 7) + 7.5
    attackDice_y0 = (3*step2Height/5) + 30
    attackDice_x1 = attackDice_x0 + diceLength 
    attackDice_y1 = attackDice_y0 + diceLength

    defenceDice_x0 = sideBarx0 + (5*sideBarWidth / 7) + 7.5
    defenceDice_y0 = (3*step2Height/5) + 30
    defenceDice_x1 = defenceDice_x0 + diceLength 
    defenceDice_y1 = defenceDice_y0 + diceLength


    for i in range(app.attackingTroopCount):
        attackDice_y0 += diceLength
        attackDice_y1 = attackDice_y0 + diceLength
        canvas.create_rectangle(attackDice_x0, attackDice_y0,
                                attackDice_x1, attackDice_y1)
        canvas.create_text((attackDice_x0+attackDice_x1)/2,
                           (attackDice_y1+attackDice_y0)/2,
                           text=f'{app.attackingDice[i]}')

    for i in range(app.defendingTroopCount):
        defenceDice_y0 += diceLength
        defenceDice_y1 = defenceDice_y0 + diceLength        
        canvas.create_rectangle(defenceDice_x0, defenceDice_y0,
                                defenceDice_x1, defenceDice_y1)                                
        canvas.create_text((defenceDice_x0+defenceDice_x1)/2,
                           (defenceDice_y0+defenceDice_y1)/2,
                           text=f'{app.defendingDice[i]}')


def drawBattleResults(app, canvas):
    sideBarx0, sideBary0, sideBarx1, sideBary1 = (app.mapWidth + 10, 10,
                                                  app.width - 10, app.height-10)
    sideBarHeight = sideBary1 - sideBary0
    sideBarWidth = sideBarx1 - sideBarx0
    topOfStep2Box = sideBarHeight / 5 
    
    step2x0 = sideBarx0
    step2y0 = topOfStep2Box + 10
    step2x1 = sideBarx1
    step2y1 = sideBary1

    step2Height = step2y1 - step2y0
    
    x0 = step2x0 + 20
    y0 = step2y1 - 140
    x1 = step2x1 - 20
    y1 = step2y1 - 20

    canvas.create_rectangle(x0,y0,x1,y1)


    attackerMessage = f'{app.diedAttacking} troops died while attacking'
    defenderMessage = f'{app.diedDefending} troops died while defending'
    
    font = "Papyrus 24 bold"
    canvas.create_text((x0+x1)/2, (y0+y1)/2,
                        text=attackerMessage, anchor="s", font=font)
    canvas.create_text((x0+x1)/2, (y0+y1)/2,
                        text=defenderMessage, anchor="n", font=font)


####################################################

# THIRD STEP DRAWING STUFF
####################################################


def drawStep3(app, canvas):
    sideBarx0, sideBary0, sideBarx1, sideBary1 = (app.mapWidth + 10, 10,
                                                  app.width - 10, app.height-10)
    sideBarHeight = sideBary1 - sideBary0
    sideBarWidth = sideBarx1 - sideBarx0
    topOfStep3Box = sideBarHeight / 5 

    # step2x0, step2y0, step2x1, step2y1 top left and bottom right points 
    # of the step2 box
    step3x0 = sideBarx0
    step3y0 = topOfStep3Box + 10
    step3x1 = sideBarx1
    step3y1 = sideBary1

    canvas.create_rectangle(step3x0,step3y0,step3x1,step3y1, width=2)
    canvas.create_text((step3x0 + step3x1)/2, step3y0+10,
                         text="MANEUVER")

    drawFromTo(app, canvas, step3x0, step3y0, step3x1, step3y1)
    drawChooseTroopsToMove(app, canvas, step3x0, step3y0, step3x1, step3y1)

def drawChooseTroopsToMove(app, canvas, step3x0, step3y0, step3x1, step3y1):
        
    step3BoxHeight = step3y1 - step3y0 # height of step2 box
    step3BoxWidth = step3x1 - step3x0 # width of step2 box / same sidebar width

    x0Moving = step3x0
    y0Moving = (2*step3BoxHeight/10) + step3y0 + 5
    x1Moving = step3BoxWidth + x0Moving
    y1Moving = y0Moving + (step3BoxHeight/10)

    canvas.create_rectangle(x0Moving, y0Moving, x1Moving, y1Moving, width=app.troopsToMoveWidth)

    canvas.create_text((x1Moving + x0Moving)/2, (y1Moving + y0Moving)/2, 
                        text="Troops to Move:")

    movedTroopsBoxLen = 45

    troopsManeuvered = app.troopsManeuvered

    movedTroops_x0 = (x0Moving + 5*step3BoxWidth / 7) - 25
    movedTroops_y0 = (y1Moving+y0Moving)/2 - movedTroopsBoxLen/2
    movedTroops_x1 = (movedTroops_x0 + movedTroopsBoxLen)
    movedTroops_y1 = (y1Moving+y0Moving)/2 + movedTroopsBoxLen/2

    canvas.create_rectangle(movedTroops_x0, movedTroops_y0,
                            movedTroops_x1, movedTroops_y1)

    canvas.create_text((movedTroops_x0+movedTroops_x1)/2,
                       (movedTroops_y0+movedTroops_y1)/2,
                        text=troopsManeuvered)

####################################################

# GAME ENDED DRAWING STUFF
####################################################

def gameEndedMode_redrawAll(app, canvas):
    if(app.isTie):
        gameEndMessage = "It's a Tie!"
    else:
        gameEndMessage = f"{app.winner.name} WON!"
    
    font="Papyrus 100 bold"
    canvas.create_rectangle(0,0,app.width,app.height,fill="CadetBlue1")
    canvas.create_text(app.width/2,app.height/2,
                       text=gameEndMessage, font=font, fill="purple")

    drawGoodbyeMessage(app, canvas)

def drawGoodbyeMessage(app, canvas):

    canvas.create_text(((2*app.width/5)+50+(3*app.width/5)-50)/2,
                      ((((3*app.height/5)+30)+((4*app.height/5)-30))/2),
                         text="Good Game! Press Ctrl Q to quit", font="Papyrus 40 bold")




