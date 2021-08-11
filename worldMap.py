# global set that holds all the territories
regionsSet = set()


class Territory(object):
    def __init__(self, name):
        self.name = name # region name
        self.occupied = False # if the region is occupied
        self.troopGeneral = None # who occupies the region 
        self.color = 'white'
        self.troopCount = 0 # how many troops occupy the region
        self.circleCoordinates = (-1,-1)
        regionsSet.add(self) # adds the object itself

# NORTH AMERICA
Alaska = Territory("Alaska")
Northwest_Territory = Territory("Northwest_Territory")
Alberta = Territory("Alberta")
Ontario = Territory("Ontario")
Quebec = Territory("Quebec")
Greenland = Territory("Greenland")
Western_United_States = Territory("Western_United_States")
Eastern_United_States = Territory("Eastern_United_States")
Central_America = Territory("Central_America")

# SOUTH AMERICA
Venezuela = Territory("Venezuela")
Peru = Territory("Peru")
Brazil = Territory("Brazil")
Argentina = Territory("Argentina")

# AFRICA
North_Africa = Territory("North_Africa")
Egypt = Territory("Egypt")
Congo = Territory("Congo")
East_Africa = Territory("East_Africa")
South_Africa = Territory("South_Africa")
Madagascar = Territory("Madagascar")

# EUROPE
Western_Europe = Territory("Western_Europe")
Great_Britain = Territory("Great_Britain")
Iceland = Territory("Iceland")
Scandanavia = Territory("Scandanavia")
Ukraine = Territory("Ukraine")
Northern_Europe = Territory("Northern_Europe")
Southern_Europe = Territory("Southern_Europe")

# ASIA
Middle_East = Territory("Middle_East")
India = Territory("India")
Siam = Territory("Siam")
China = Territory("China")
Afghanistan = Territory("Afghanistan")
Ural = Territory("Ural")
Siberia = Territory("Siberia")
Mongolia = Territory("Mongolia")
Japan = Territory("Japan")
Irkutsk = Territory("Irkutsk")
Yakutsk = Territory("Yakutsk")
Kamchatka = Territory("Kamchatka")

# AUSTRALIA
Indonesia = Territory("Indonesia")
New_Guinea = Territory("New_Guinea")
Western_Australia = Territory("Western_Australia")
Eastern_Australia = Territory("Eastern_Australia")



# neighbors
worldMap = {
    # NORTH AMERICA
    "Alaska" : {Northwest_Territory, Alberta, Kamchatka},
    "Northwest_Territory" : {Alaska, Alberta, Ontario, Greenland},
    "Alberta" : {Alaska, Northwest_Territory, Ontario, Western_United_States},
    "Ontario" : {Alberta, Northwest_Territory, Greenland, Quebec, Eastern_United_States, Western_United_States},
    "Quebec" : {Ontario, Greenland, Eastern_United_States},
    "Greenland" : {Northwest_Territory, Ontario, Quebec, Iceland},
    "Western_United_States" : {Alberta, Ontario, Eastern_United_States, Central_America},
    "Eastern_United_States" : {Western_United_States, Ontario, Quebec, Central_America},
    "Central_America" : {Western_United_States, Eastern_United_States, Venezuela},

    # SOUTH AMERICA
    "Venezuela" : {Central_America, Brazil, Peru},
    "Peru" : {Venezuela, Brazil, Argentina},
    "Brazil" : {Venezuela, Peru, Argentina, North_Africa},
    "Argentina" : {Peru, Brazil},

    # AFRICA
    "North_Africa" : {Brazil, Western_Europe, Southern_Europe, Egypt, East_Africa, Congo},
    "Egypt" : {North_Africa, East_Africa, Southern_Europe, Middle_East},
    "Congo" : {North_Africa, East_Africa, South_Africa},
    "East_Africa" : {Egypt, North_Africa, Congo, South_Africa, Madagascar}, 
    "South_Africa" : {Congo, East_Africa, Madagascar},
    "Madagascar" : {East_Africa, South_Africa},

    # EUROPE
    "Western_Europe" : {Great_Britain, Northern_Europe, Southern_Europe, North_Africa},
    "Great_Britain" : {Western_Europe, Iceland, Scandanavia, Northern_Europe},
    "Iceland" : {Greenland, Great_Britain, Scandanavia},
    "Scandanavia" : {Iceland, Great_Britain, Northern_Europe, Ukraine},
    "Ukraine" : {Scandanavia, Ural, Afghanistan, Middle_East, Northern_Europe, Southern_Europe},
    "Northern_Europe" : {Great_Britain, Scandanavia, Ukraine, Southern_Europe, Western_Europe},
    "Southern_Europe" : {Western_Europe, Northern_Europe, Ukraine, Middle_East, Egypt, North_Africa},

    # ASIA
    "Middle_East" : {East_Africa, Egypt, Southern_Europe, Ukraine, Afghanistan, India},
    "India" : {Middle_East, Afghanistan, China, Siam},
    "Siam" : {Indonesia, India, China},
    "China" : {Siam, India, Afghanistan, Ural, Siberia, Mongolia},
    "Afghanistan" : {Middle_East, Ukraine, Ural, China, India},
    "Ural" : {Afghanistan, Ukraine, Siberia, China},
    "Siberia" : {Ural, China, Mongolia, Irkutsk, Yakutsk},
    "Mongolia" : {China, Siberia, Irkutsk, Kamchatka, Japan},
    "Japan" : {Mongolia, Kamchatka},
    "Irkutsk" : {Siberia, Yakutsk, Kamchatka, Mongolia},
    "Yakutsk" : {Siberia, Irkutsk, Kamchatka},
    "Kamchatka" : {Yakutsk, Irkutsk, Japan, Alaska},

    # AUSTRALIA
    "Indonesia" : {Siam, New_Guinea, Western_Australia},
    "New_Guinea" : {Indonesia, Western_Australia, Eastern_Australia},
    "Western_Australia" : {Indonesia, New_Guinea, Eastern_Australia},
    "Eastern_Australia" : {New_Guinea, Western_Australia}
}

# checks if the two inputed regions are neighbors
def checkIfNeighbors(fromRegion, toRegion):
    neighborsNames = set()
    for region in worldMap[fromRegion]:
        print(region.name)
        neighborsNames.add(region.name)

    if(toRegion in neighborsNames):
        return True
    else:
        return False