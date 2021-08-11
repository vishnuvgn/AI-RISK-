# draws a rectangle for sidebar
def drawSideBar(app, canvas):
    canvas.create_rectangle(app.mapWidth + 10, 10, app.width - 10,
                            app.height-10, outline="black")
    drawStep1(app, canvas)
    drawStep2(app, canvas)

def drawBottomBar(app, canvas):
    canvas.create_rectangle(10, app.mapHeight+10, app.mapWidth-10,
                            app.height-10, outline="black")

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
                            sideBary0 + step1Height, width=2)
    canvas.create_text((sideBarx1 + sideBarx0)/2, sideBary0+10,
                        text="Place Troops")

    troopsAtATime = 1 # static for now, remember to change
    troopsLeft = 5 # static for now, remember to change

    # app, canvas, troopNumber,
    # top left of sidebar, height of step1box, width of step1box (same as sidebar),
    # row, col (row, col of rectangle),
    # message ("troops placed at a time" or "troops left")
    placedTroopsMessage = "Troops Placed at a Time"
    drawTroopsBox(app, canvas, troopsAtATime,
                  sideBarx0,sideBary0, step1Height,
                  sideBarWidth,2,1,placedTroopsMessage)

    troopsLeftMessage = "Troops Left"                                            
    drawTroopsBox(app, canvas, troopsLeft,
                  sideBarx0,sideBary0,step1Height,
                  sideBarWidth,2,3, troopsLeftMessage)
    drawNextButton(app, canvas)

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

def drawNextButton(app, canvas):
    sideBarx0, sideBary0, sideBarx1, sideBary1 = (app.mapWidth + 10, 10,
                                                  app.width - 10, app.height-10)
    sideBarHeight = sideBary1 - sideBary0
    sideBarWidth = sideBarx1 - sideBarx0

    nextButtonHeigth = 20

    x0 = (4*sideBarWidth/5) + sideBarx0
    y0 = sideBary0
    x1 = x0 + (sideBarWidth/5)
    y1 = y0 + nextButtonHeigth

    canvas.create_rectangle(x0,y0,x1,y1)
    canvas.create_text((x1+x0)/2, (y1+y0)/2, text="NEXT")





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
                         text="Attack")
    drawSkipButton(app, canvas)
    drawFromTo(app, canvas, step2x0, step2y0, step2x1, step2y1)
    drawChooseTroopCount(app, canvas, step2x0, step2y0, step2x1, step2y1)
    drawRollButton(app,canvas)
    
# if skipbutton is clicked, then remember to change boolean app.step2Now
def drawSkipButton(app, canvas):
    sideBarx0, sideBary0, sideBarx1, sideBary1 = (app.mapWidth + 10, 10,
                                                  app.width - 10, app.height-10)
    sideBarHeight = sideBary1 - sideBary0
    sideBarWidth = sideBarx1 - sideBarx0

    skipButtonHeigth = 20

    x0 = (4*sideBarWidth/5) + sideBarx0
    y0 = (1*sideBarHeight/5) + sideBary0
    x1 = x0 + (sideBarWidth/5)
    y1 = y0 + skipButtonHeigth

    canvas.create_rectangle(x0,y0,x1,y1)
    canvas.create_text((x1+x0)/2, (y1+y0)/2, text="SKIP")


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
    
    fromText = f'FROM: {app.fromRegion} '
    toText = f'TO: {app.toRegion}' 


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

    canvas.create_rectangle(x0Attacking, y0Attacking, x1Attacking, y1Attacking)
    
    attackingTroopMessage = "Attacking Troops:" 
    # text for attacking troops
    canvas.create_text((x1Attacking+x0Attacking)/2, (y1Attacking+y0Attacking)/2,
                        text=attackingTroopMessage)


    x0Defending = step2x1 - (step2BoxWidth/2)
    y0Defending = (2*step2BoxHeight/10) + step2y0 + 5
    x1Defending = step2x1
    y1Defending = y0Defending + (step2BoxHeight/10)

    canvas.create_rectangle(x0Defending, y0Defending, x1Defending, y1Defending)

    defendingTroopMessage = "Defending Troops:" 
    # text for defending troops
    canvas.create_text((x1Defending+x0Defending)/2, (y1Defending+y0Defending)/2,
                        text=defendingTroopMessage)

    attackingTroopNum = 1 # static for now, will change
    drawTroopCountSquare(app, canvas, x0Attacking, y0Attacking,
                         x1Attacking, y1Attacking,attackingTroopNum)

    defendingTroopNum = 5 # static for now, will change
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

    x0 = step2x0 + (sideBarWidth / 3)
    y0 = 3*step2Height/5
    x1 = x0 + (sideBarWidth / 3)
    y1 = y0 + 15

    canvas.create_rectangle(x0,y0,x1,y1)