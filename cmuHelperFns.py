def drawGrid(app,canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1)

def getCellBounds(app, row, col):
    gridWidth  = app.width 
    gridHeight = app.height
    cellWidth = gridWidth / app.cols
    # print("cellWidth =" f'{cellWidth}')
    cellHeight = gridHeight / app.rows
    # print("cellHeight =" f'{cellHeight}')
    x0 = col * cellWidth
    x1 = (col+1) * cellWidth
    y0 = row * cellHeight
    y1 = (row+1) * cellHeight
    return (x0, y0, x1, y1)

def getCell(app, x, y):
    gridWidth  = app.width 
    gridHeight = app.height
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y) / cellHeight)
    col = int((x) / cellWidth)

    return (row, col)
