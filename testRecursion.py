controlledRegions = {"Alaska", "Northwest_Territory","Ontario","Alberta","Western_United_States","Central_America"}

worldMap = {
    # NORTH AMERICA
    "Alaska" : {"Northwest_Territory", "Alberta", "Kamchatka"},
    "Northwest_Territory" : {"Alaska", "Alberta", "Ontario", "Greenland"},
    "Alberta" : {"Alaska", "Northwest_Territory", "Ontario", "Western_United_States"},
    "Ontario" : {"Alberta", "Northwest_Territory", "Greenland", "Quebec", "Eastern_United_States", "Western_United_States"},
    "Quebec" : {"Ontario", "Greenland", "Eastern_United_States"},
    "Greenland" : {"Northwest_Territory", "Ontario", "Quebec", "Iceland"},
    "Western_United_States" : {"Alberta", "Ontario", "Eastern_United_States", "Central_America"},
    "Eastern_United_States" : {"Western_United_States", "Ontario", "Quebec", "Central_America"},
    "Central_America" : {"Western_United_States", "Eastern_United_States", "Venezuela"}
}

breadCrumbs = []
'''
How this fn works:
- check recursively depth (checking the children)
- check iteratively latterally (checking the siblings)

'''
def isThereAPath(worldMap, node, target, breadCrumbs):
    # breadCrumbs.add(node)
    breadCrumbs.append(node)
    #   print(breadCrumbs)
    # check 1
    if(target in worldMap[node]):
        return True

    # check 2
    for neighbor in worldMap[node]:
        if(neighbor in controlledRegions and
            neighbor not in breadCrumbs):
            # go down this path recursively
            boolExp = isThereAPath(worldMap, neighbor, target, breadCrumbs)
            if(boolExp == True):
                return True
            else:
                continue
    return False

# print(isThereAPath(worldMap, "Kamchatka", "Brazil", breadCrumbs))
