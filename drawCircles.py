from worldMap import *
from cmuHelperFns import *
# draws a circle that shows the number of troops in the country
def drawCircle(app, canvas, row, col, territory, fillColor=""): 
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    cx = (x0+x1) / 2
    cy = (y0+y1) / 2
    canvas.create_oval(x0-app.circleRadius, y0-app.circleRadius,
                       x1+app.circleRadius, y1+app.circleRadius,
                       fill=fillColor)
    troopCount = territory.troopCount
    # ^ add font color and everything later
    canvas.create_text(cx,cy, text=troopCount)
    return (cx,cy) # returns the cooridinates of the center of the circle

def drawAllCircles(app, canvas):
    # NORTH AMERICA
    Alaska.circleCoordinates = drawCircle(app, canvas, 3, 2, Alaska, Alaska.color) # Alaska
    Northwest_Territory.circleCoordinates = drawCircle(app, canvas, 4, 10, Northwest_Territory, Northwest_Territory.color) # Northwest Territory
    Alberta.circleCoordinates = drawCircle(app, canvas, 19, 4, Alberta, Alberta.color) # Alberta
    Western_United_States.circleCoordinates = drawCircle(app, canvas, 26, 4, Western_United_States, Western_United_States.color) # Western United States
    Central_America.circleCoordinates = drawCircle(app, canvas, 36, 6, Central_America, Central_America.color) # Central America
    Eastern_United_States.circleCoordinates = drawCircle(app, canvas, 29, 17, Eastern_United_States, Eastern_United_States.color) # Eastern United States
    Greenland.circleCoordinates = drawCircle(app, canvas, 3, 21, Greenland, Greenland.color) # Greenland
    Ontario.circleCoordinates = drawCircle(app, canvas, 13, 14, Ontario, Ontario.color) # Ontario
    Quebec.circleCoordinates = drawCircle(app, canvas, 18, 20, Quebec, Quebec.color) # Quebec

    # SOUTH AMERICA
    Venezuela.circleCoordinates = drawCircle(app, canvas, 35, 16, Venezuela, Venezuela.color) # Venezuela
    Peru.circleCoordinates = drawCircle(app, canvas, 45, 8, Peru, Peru.color) # Peru
    Argentina.circleCoordinates = drawCircle(app, canvas, 57, 11, Argentina, Argentina.color) # Argentina
    Brazil.circleCoordinates = drawCircle(app, canvas, 50, 19, Brazil, Brazil.color) # Brazil
    
    # AFRICA
    North_Africa.circleCoordinates = drawCircle(app, canvas, 41, 27, North_Africa, North_Africa.color) # North_Africa
    Congo.circleCoordinates = drawCircle(app, canvas, 54, 28, Congo, Congo.color) # Congo
    South_Africa.circleCoordinates = drawCircle(app, canvas, 64, 29, South_Africa, South_Africa.color) # South_Africa
    Madagascar.circleCoordinates = drawCircle(app, canvas, 66, 41, Madagascar, Madagascar.color) # Madagascar
    East_Africa.circleCoordinates = drawCircle(app, canvas, 52, 40, East_Africa, East_Africa.color) # East_Africa
    Egypt.circleCoordinates = drawCircle(app, canvas, 38, 33, Egypt, Egypt.color) # Egypt

    # EUROPE
    Western_Europe.circleCoordinates = drawCircle(app, canvas, 35, 22, Western_Europe, Western_Europe.color) # Western_Europe
    Great_Britain.circleCoordinates = drawCircle(app, canvas, 26, 21, Great_Britain, Great_Britain.color) # Great_Britain
    Iceland.circleCoordinates = drawCircle(app, canvas, 9, 26, Iceland, Iceland.color) # Iceland
    Scandinavia.circleCoordinates = drawCircle(app, canvas, 5, 32, Scandinavia, Scandinavia.color) # Scandinavia
    Ukraine.circleCoordinates = drawCircle(app, canvas, 13, 38, Ukraine, Ukraine.color) # Ukraine
    Northern_Europe.circleCoordinates = drawCircle(app, canvas, 19, 31, Northern_Europe, Northern_Europe.color) # Northern_Europe
    Southern_Europe.circleCoordinates = drawCircle(app, canvas, 33, 30, Southern_Europe, Southern_Europe.color) # Southern_Europe

    # ASIA
    Middle_East.circleCoordinates = drawCircle(app, canvas, 41, 38, Middle_East, Middle_East.color) # Middle_East
    India.circleCoordinates = drawCircle(app, canvas, 43, 45, India, India.color) # India
    Siam.circleCoordinates = drawCircle(app, canvas, 41, 53, Siam, Siam.color) # Siam
    China.circleCoordinates = drawCircle(app, canvas, 33, 52, China, China.color) # China
    Afghanistan.circleCoordinates = drawCircle(app, canvas, 29, 41, Afghanistan, Afghanistan.color) # Afghanistan
    Ural.circleCoordinates = drawCircle(app, canvas, 12, 42, Ural, Ural.color) # Ural
    Siberia.circleCoordinates = drawCircle(app, canvas, 5, 45, Siberia, Siberia.color) # Siberia
    Irkutsk.circleCoordinates = drawCircle(app, canvas, 13, 50, Irkutsk, Irkutsk.color) # Irkutsk
    Yakutsk.circleCoordinates = drawCircle(app, canvas, 3, 51, Yakutsk, Yakutsk.color) # Yakutsk
    Mongolia.circleCoordinates = drawCircle(app, canvas, 20, 52, Mongolia, Mongolia.color) # Mongolia
    Kamchatka.circleCoordinates = drawCircle(app, canvas, 3, 58, Kamchatka, Kamchatka.color) # Kamchatka
    Japan.circleCoordinates = drawCircle(app, canvas, 22, 59, Japan, Japan.color) # Japan
    
    # AUSTRALIA
    Indonesia.circleCoordinates = drawCircle(app, canvas, 54, 47, Indonesia, Indonesia.color) # Indonesia
    New_Guinea.circleCoordinates = drawCircle(app, canvas, 46, 59, New_Guinea, New_Guinea.color) # New_Guinea
    Western_Australia.circleCoordinates = drawCircle(app, canvas, 67, 52, Western_Australia, Western_Australia.color) # Western_Australia
    Eastern_Australia.circleCoordinates = drawCircle(app, canvas, 64, 60, Eastern_Australia, Eastern_Australia.color) # Eastern_Australia


