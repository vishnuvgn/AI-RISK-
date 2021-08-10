# draws a rectangle for sidebar
def drawSideBar(app, canvas):
    canvas.create_rectangle(app.mapWidth + 10, 10, app.width - 10,
                            app.height-10, outline="black")
    drawStep1(app, canvas)

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
    step1Height = sideBarHeight / 5 # divides 
    # draws the box for step1
    canvas.create_rectangle(sideBarx0, sideBary0, sideBarx1, sideBary0 + step1Height)

    canvas.create_text((sideBarx1 + sideBarx0)/2, sideBary0+10,
                       text="Place Troops")

    troopsAtATime = 1
    troopsLeft = 5
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

# used to draw both how many troops left and how many troops placed at a time
# draws one rectangle at row, col with troop info in center (the number)
def drawTroopsBox(app, canvas, troopCount, step1x0,step1y0,
                            step1Height,step1Width,row,col, message):
    x0 = (col*step1Width/5) + step1x0
    y0 = (row*step1Height/5) + step1y0
    x1 = x0 + (step1Width/5)
    y1 = y0 + (step1Height/5)
    countBoxHeight = y1-y0
    # countBoxWidth = x1-x0

    canvas.create_rectangle(x0,y0,x1,y1)
    canvas.create_text((x1+x0)/2,(y1+y0)/2, text=troopCount)
    canvas.create_text((x1+x0)/2,(y1+y0)/2+countBoxHeight,
                        text=message)

####################################################