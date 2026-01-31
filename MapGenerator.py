import numpy
import random
import time

def CheckTilesMain(Map, object):
    availableTiles = []
    for row in range(len(Map)):
        for column in range(len(Map[row])):
            nearWaterWithDiagonals = False
            nearWaterClose = False
            nearB = False
            nearH = False
            if Map[row][column] == ".":
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (row+i >= 0 and row+i < len(Map)) and (column+j >= 0 and column+j < len(Map[row])):
                            if Map[row+i][column+j] == "B":
                                    nearB = True
                            if Map[row+i][column+j] == "H":
                                    nearH = True
                            if Map[row+i][column+j] == "W":
                                if i == 0 or j == 0:
                                    nearWaterClose = True
                                nearWaterWithDiagonals = True
                if object not in ["X", "B"]:
                    if not nearWaterWithDiagonals and not nearB:
                        if object == "H" and not nearH: 
                            availableTiles.append([row, column])
                        elif object != "H":
                            availableTiles.append([row, column])
                else:
                    if object == "X":
                        if nearWaterClose and not nearB:
                            availableTiles.append([row, column])
                    else:
                        if nearWaterClose:
                            availableTiles.append([row, column])
    return availableTiles

def placeRandomlyMain(Map, object, amount):
    for n in range(amount):
        availableTiles = CheckTilesMain(Map, object)
        if object != "B":
            chosenTile = random.choice(availableTiles)
            Map[chosenTile[0]][chosenTile[1]] = object
        else:
            if n == 0:
                chosenTile = random.choice(availableTiles)
                Map[chosenTile[0]][chosenTile[1]] = object
            else:
                TilesToRemove = []
                for k in availableTiles:
                    foundB = False
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if (k[0]+i >= 0 and k[0]+i < len(Map)) and (k[1]+j >= 0 and k[1]+j < len(Map[0])):
                                if Map[k[0]+i][k[1]+j] == "B":
                                    foundB = True
                    if not foundB:
                        TilesToRemove.append(k)
                for d in TilesToRemove:
                    availableTiles.remove(d)
                chosenTile = random.choice(availableTiles)
                Map[chosenTile[0]][chosenTile[1]] = object
        print(f"\033[{len(Map)-chosenTile[0]}A", end="\r")
        print(f"{"".join(Map[chosenTile[0]])}")
        print(f"\033[{len(Map)-chosenTile[0]}B", end="\r")
        time.sleep(0.05)        

def placeObjects(Map, difficulty):
    match(difficulty):
        case "low":
            placeRandomlyMain(Map , "B", 20)
            placeRandomlyMain(Map , "X", 1)
            placeRandomlyMain(Map , "*", 8)
            placeRandomlyMain(Map , "H", 3)
            placeRandomlyMain(Map , "R", 2)
        case "mid":
            placeRandomlyMain(Map , "B", 20)
            placeRandomlyMain(Map , "X", 1)
            placeRandomlyMain(Map , "*", 15)
            placeRandomlyMain(Map , "H", 2)
            placeRandomlyMain(Map , "R", 5)
        case "high":
            placeRandomlyMain(Map , "B", 30)
            placeRandomlyMain(Map , "X", 1)
            placeRandomlyMain(Map , "*", 20)
            placeRandomlyMain(Map , "H", 1)
            placeRandomlyMain(Map , "R", 10)
    
def generateRoundMap(difficulty = "low", width = 42, height = 20):
    file = open("MapDataGenerated.txt", "w")
    Map = numpy.full((height, width), "W", dtype=str)
    for b in Map:
        print("".join(b))
    print(f"\033[{height}A", end="\r")
    centre_x, centre_y = (width // 2) - random.uniform(0,1), (height // 2) - random.uniform(0,1)
    max_radius_x, max_radius_y = (width // 2) - random.uniform(1,2), (height // 2) - random.uniform(1,2)
    for y in range(height):
        for x in range(width):
            distanceFromCentre = ((x-centre_x)**2/max_radius_x**2)+((y-centre_y)**2/max_radius_y**2)
            if distanceFromCentre < random.uniform(0.9,1.0):
                Map[y,x] = "."
                print(f"{"".join(Map[y])}", end="\r")
                time.sleep(0.001)
        print()
    for row in range(height):
        for column in range(width):
            NumOfSandsAround = 0
            if Map[row][column] == "W":
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (row+i >= 0 and row+i < height) and (column+j >= 0 and column+j < width):
                            if Map[row+i][column+j] == ".":
                                NumOfSandsAround += 1
            if NumOfSandsAround >= 5:
                Map[row][column] = "."
                print(f"\033[{len(Map)-row}A", end="\r")
                print(f"{"".join(Map[row])}")
                print(f"\033[{len(Map)-row}B", end="\r")
                time.sleep(0.05)
    placeObjects(Map, difficulty)
    print()
    file.write(f"{height}, {width}"+"\n")
    for n in range(len(Map)):
        if n == len(Map)-1:
            file.write("".join(Map[n]))
        else:
            file.write("".join(Map[n])+"\n")
    generateHiddenMapData(Map, width, height, difficulty)
    file.close()

def PlaceHidden(Map, HiddenMap, difficulty):
    match(difficulty):
        case "low":
            placeRandomlyHidden(Map, HiddenMap, "G", 12)
            placeRandomlyHidden(Map, HiddenMap, "T", 1)
            placeRandomlyHidden(Map, HiddenMap, "C", 15)
        case "mid":
            placeRandomlyHidden(Map, HiddenMap, "G", 10)
            placeRandomlyHidden(Map, HiddenMap, "T", 1)
            placeRandomlyHidden(Map, HiddenMap, "C", 12)
        case "high":
            placeRandomlyHidden(Map, HiddenMap, "G", 6)
            placeRandomlyHidden(Map, HiddenMap, "T", 1)
            placeRandomlyHidden(Map, HiddenMap, "C", 9)

def CheckTilesHidden(Map, HiddenMap, object, order):
    availableTiles = []
    for row in range(len(Map)):
        for column in range(len(Map[row])):
            nearG = False
            if Map[row][column] == ".":
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (row+i >= 0 and row+i < len(Map)) and (column+j >= 0 and column+j < len(Map[0])):
                            if HiddenMap[row+i][column+j] == "G":
                                    nearG = True
                if object == "C":
                    availableTiles.append([row, column])
                else:
                    if (nearG or order == 0) and object == "G":
                        availableTiles.append([row, column])
                    elif nearG and object == "T":
                        availableTiles.append([row, column])
    return availableTiles

def placeRandomlyHidden(Map, HiddenMap, object, amount):
    for n in range(amount):
        availableTiles = CheckTilesHidden(Map, HiddenMap, object, n)
        chosenTile = random.choice(availableTiles)
        HiddenMap[chosenTile[0]][chosenTile[1]] = object

def generateHiddenMapData(Map, width, height, difficulty):
    fileHidden = open("HiddenDataGenerated.txt", "w")
    fileHiddenMap = open("HiddenMapGenerated.txt", "w")
    HiddenMap = numpy.full((height, width), ".", dtype=str)
    PlaceHidden(Map, HiddenMap, difficulty)
    for n in range(len(HiddenMap)):
        if n == len(HiddenMap)-1:
            fileHiddenMap.write("".join(HiddenMap[n]))
        else:
            fileHiddenMap.write("".join(HiddenMap[n])+"\n")
        for k in range(len(HiddenMap[n])):
                if HiddenMap[n][k] != ".":
                    if n == len(HiddenMap)-1:
                        fileHidden.write(f"{HiddenMap[n][k]},{n},{k}")
                    else:
                        fileHidden.write(f"{HiddenMap[n][k]},{n},{k}\n")
    fileHidden.close()
    fileHiddenMap.close()