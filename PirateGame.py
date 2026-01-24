# Entire Code:
# Skeleton Program for the AQA AS Summer 2025 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in a Python 3 environment
# Use pip install colorama
import random
from colorama import init

init()

SAND = '.'
WATER = 'W'
GOLD_COIN = 'G'
COCONUT = 'C'
TREASURE = 'T'
PIRATES = 'P'
ROCK = 'R'
HUT = 'H'
TREE = '*'
BOULDER = 'B'
DUG_HOLE = 'O'

BLANK = " "
PRESSED_ENTER = ""
MAX_ROWS = 20
MAX_COLUMNS = 50

class MapSizeRecord:
  def __init__(self):
    self.Rows = MAX_ROWS
    self.Columns = MAX_COLUMNS

class PirateRecord:
  def __init__(self):
    self.Row = 0
    self.Column = 0
    self.Score = 100
    self.DigTime = 0.0
    self.TreasureFound = False
    self.NumberOfCoinsFound = 0
    self.NumOfDigs = 0
    self.UsedDynamite = False
    self.NumOfActions = 0

def ResetMapSize(MapSize):
  MapSize.Rows = MAX_ROWS
  MapSize.Columns = MAX_COLUMNS
  return MapSize

def ResetMaps(Map, HiddenMap):
  for Row in range (MAX_ROWS):
    for Column in range (MAX_COLUMNS):
      Map[Row][Column] = SAND
      HiddenMap[Row][Column] = SAND

def ResetPirateRecord(Pirate):
  Pirate.Row = 0
  Pirate.Column = 0
  Pirate.Score = 100
  Pirate.DigTime = 0.0
  Pirate.TreasureFound = False
  Pirate.NumberOfCoinsFound = 0
  Pirate.NumofDigs = 0

def GenerateMap(Map, MapSize):
  FileIn = open("MapData.txt", 'r')
  DataString = FileIn.readline()
  Data = DataString.split(',')
  MapSize.Rows = int(Data[0])
  MapSize.Columns = int(Data[1])
  for Row in range(MapSize.Rows):
    DataString = FileIn.readline()
    for Column in range(MapSize.Columns):
      Map[Row][Column] = DataString[Column]
  FileIn.close()
  return MapSize

def ProcessDataInputString(Map, DataString):
  Data = DataString.split(',')
  Item = Data[0]
  Row = int(Data[1])
  Column = int(Data[2])
  Map[Row][Column] = Item

def GenerateHiddenMap(HiddenMap):
  FileIn = open("HiddenData.txt", 'r')
  DataString = FileIn.readline()
  while DataString != "":
    ProcessDataInputString(HiddenMap, DataString)
    DataString = FileIn.readline()
  FileIn.close()

def DisplayCompass(Row):
  if Row == 1:
    print()
  elif Row == 2:
    print("          N         ")
  elif Row == 3:
    print("     NW   |   NE    ")
  elif Row == 4:
    print("        \ | /       ")
  elif Row == 5:
    print("   W -----|----- E  ")
  elif Row == 6:
    print("        / | \       ")
  elif Row == 7:
    print("     SW   |   SE    ")
  elif Row == 8:
    print("          S         ")
  else:
    print()

def DisplayMap(Map, MapSize):
  print()
  print("  ", end='')
  for i in range(MapSize.Columns):
    print(i % 10, end='')
  print()
  for Row in range(MapSize.Rows):
    print(f"{Row % 10} ", end='')
    for Column in range(MapSize.Columns):
      print(Map[Row][Column], end='')
    DisplayCompass(Row)
  print()

def FoundPirate(Map, MapSize, Steps):
  DisplayMap(Map, MapSize)
  print("X marks the spot where the pirate comes ashore")
  print(f"Number of steps to find the pirate: {Steps}")
  print()

def CheckPirate(Map, Pirate, Row, Column):
  if Map[Row][Column] == 'X':
    Pirate.Row = Row
    Pirate.Column = Column
    return True
  return False

def FindLandingPlace(Map, MapSize, Pirate):
  Found = False
  Steps = 0
  top = 0
  bottom = MapSize.Rows
  left = 0
  right = MapSize.Columns
  while top <= bottom and left <= right and (not Found):
    for i in range(left, right):
      if CheckPirate(Map, Pirate, top, i):
        Found = True
        break
      Steps += 1
    top += 1
    if Found:
        break
    for i in range(top, bottom):
      if CheckPirate(Map, Pirate, i, right-1):
        Found = True
        break
      Steps += 1
    right -= 1
    if Found:
        break
    for i in range(right, left-1, -1):
      if CheckPirate(Map, Pirate, bottom-1, i):
        Found = True
        break
      Steps += 1
    bottom -= 1
    if Found:
        break
    for i in range(bottom-1, top-1, -1):
      if CheckPirate(Map, Pirate, i, left):
        Found = True
        break
      Steps += 1
    left += 1
    if Found:
        break
  FoundPirate(Map, MapSize, Steps)



def CheckDistance(Distance):
  ValidDistance = True
  NumberOfSquares = -1
  try:
    NumberOfSquares = int(Distance)
    if NumberOfSquares < 1 or NumberOfSquares > 9:
      print("Distance must be between 1 and 9")
      ValidDistance = False
  except:
    print("Not a valid integer between 1 and 9")
    ValidDistance = False
  return ValidDistance, NumberOfSquares

def CheckDirection(Direction, Row, Column, NumberOfSquares):
  ValidDirection = True
  if Direction == "N":
    Row -= NumberOfSquares
  elif Direction == "NE":
    Row -= NumberOfSquares
    Column += NumberOfSquares
  elif Direction == "E":
    Column += NumberOfSquares
  elif Direction == "SE":
    Row += NumberOfSquares
    Column += NumberOfSquares
  elif Direction == "S":
    Row += NumberOfSquares
  elif Direction == "SW":
    Row += NumberOfSquares
    Column -= NumberOfSquares
  elif Direction == "W":
    Column -= NumberOfSquares
  elif Direction == "NW":
    Row -= NumberOfSquares
    Column -= NumberOfSquares
  else:
    print("Not a valid direction")
    ValidDirection = False
  return ValidDirection, Row, Column

def CheckPath(Map, StartRow, StartColumn, EndRow, EndColumn, Direction, O_not_obstacle):
  ObstacleFound = False
  if Direction == "N":
    for Row in range(EndRow, StartRow):
      if Map[Row][StartColumn] != SAND and (Map[Row][StartColumn] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "NE":
    for i in range(1, StartRow - EndRow + 1):
      if Map[StartRow - i][StartColumn + i] != SAND and (Map[StartRow - i][StartColumn + i] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "E":
    for Column in range(StartColumn + 1, EndColumn + 1):
      if Map[StartRow][Column] != SAND and (Map[StartRow][Column] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "SE":
    for i in range(1, EndRow - StartRow + 1):
      if Map[StartRow + i][StartColumn + i] != SAND and (Map[StartRow + i][StartColumn + i] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "S":
    for Row in range(StartRow + 1, EndRow + 1):
      if Map[Row][StartColumn] != SAND and (Map[Row][StartColumn] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "SW":
    for i in range(1, EndRow - StartRow + 1):
      if Map[StartRow + i][StartColumn - i] != SAND and (Map[StartRow + i][StartColumn - i] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "W":
    for Column in range(EndColumn, StartColumn):
      if Map[StartRow][Column] != SAND and (Map[StartRow][Column] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "NW":
    for i in range(1, StartRow - EndRow + 1):
      if Map[StartRow - i][StartColumn - i] != SAND and (Map[StartRow - i][StartColumn - i] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  return ObstacleFound

def Move(Map, MapSize, Pirate, Row, Column):
  if Map[Pirate.Row][Pirate.Column] == PIRATES:
    Map[Pirate.Row][Pirate.Column] = SAND
  Pirate.Row = Row
  Pirate.Column = Column
  Pirate.Score -= 5
  Map[Pirate.Row][Pirate.Column] = PIRATES
  DisplayMap(Map, MapSize)

def PirateWalks(Map, MapSize, HiddenMap, Pirate):
  ObstacleInPath = True
  ValidDistance = False
  ValidDirection = False
  SurroundedByObstacles = True
  O_not_obstacle = False
  while ObstacleInPath or not ValidDistance or not ValidDirection:
    WalkData = input("Enter length (1 to 9) and direction (N, NE, E, SE, S, SW, W, NW): ")
    Row = Pirate.Row
    Column = Pirate.Column
    for i in [-1, 0, 1]:
      for j in [-1, 0, 1]:
        if Map[Pirate.Row+i][Pirate.Column+j] == SAND:
          SurroundedByObstacles = False
    ValidDistance, NumberOfSquares = CheckDistance(WalkData[0])
    if SurroundedByObstacles:
      O_not_obstacle = True
      if WalkData[0] == "1":
        ValidDistance = False
        print("Need to get out of the entire dynamite hole!")
    Direction = WalkData[1:]
    ValidDirection, Row, Column = CheckDirection(Direction, Row, Column, NumberOfSquares)
    if Row >= MapSize.Rows or Column >= MapSize.Columns or Row < 0 or Column < 0:
      ValidDirection = False
      print("Error")
    if ValidDirection:
      ObstacleInPath = CheckPath(Map, Pirate.Row, Pirate.Column, Row, Column, Direction, O_not_obstacle)
      if ObstacleInPath:
        print("Pirate can't walk this way as there is an obstacle in the way")
  Move(Map, MapSize, Pirate, Row, Column)

def DisplayFind(Map, Pirate, ItemFound):
  if ItemFound == COCONUT:
    Item = "Coconut"
    Pirate.Score += 10
    Map[Pirate.Row][Pirate.Column] = COCONUT
  elif ItemFound == TREASURE:
    Item = "\033[32mTreasure chest\033[0m"
    Pirate.TreasureFound = True
    Pirate.Score += 200
    Map[Pirate.Row][Pirate.Column] = TREASURE
  elif ItemFound == GOLD_COIN:
    Item = "Gold coin"
    Pirate.NumberOfCoinsFound += 1
    print("The treasure must be nearby")
    Map[Pirate.Row][Pirate.Column] = GOLD_COIN
  elif ItemFound == DUG_HOLE:
    return
  else:
    Item = "Unidentified item"
  print(f"Found {Item}")

def PirateDigs(Map, HiddenMap, Pirate):
  if HiddenMap[Pirate.Row][Pirate.Column] not in [SAND, DUG_HOLE]:
    DisplayFind(Map, Pirate, HiddenMap[Pirate.Row][Pirate.Column])
  else:
    if HiddenMap[Pirate.Row][Pirate.Column] == DUG_HOLE:
      print("You've already dug here!")
    else:
      print("Nothing found")
  if Pirate.NumOfDigs >= 3:
    Pirate.Score -= (10+(Pirate.NumOfDigs-2)*2)
  else:
    Pirate.Score -= 10
  HiddenMap[Pirate.Row][Pirate.Column] = DUG_HOLE
  Map[Pirate.Row][Pirate.Column] = DUG_HOLE
  Pirate.DigTime += 1.75
  Pirate.NumOfDigs += 1
  DisplayResults(Pirate)

def PirateUsesDynamite(Map, MapSize, HiddenMap, Pirate):
  TreasureDestroyed = False
  for i in [-1, 0, 1]:
    for j in [-1, 0, 1]:
      if Map[Pirate.Row+i][Pirate.Column+j] in [SAND, PIRATES, DUG_HOLE, GOLD_COIN]:
        if HiddenMap[Pirate.Row+i][Pirate.Column+j] not in [SAND, DUG_HOLE]:
          if HiddenMap[Pirate.Row+i][Pirate.Column+j] == TREASURE:
            print(f"\033[31mTreasure was destroyed at {Pirate.Row+i+1},{Pirate.Column+j+1}\033[0m")
            TreasureDestroyed = True
            break
          DisplayFind(Map, Pirate, HiddenMap[Pirate.Row+i][Pirate.Column+j])
          HiddenMap[Pirate.Row+i][Pirate.Column+j] = SAND
        else:
          print(f"Noting found at {Pirate.Row+i},{Pirate.Column+j}")
      if not (i == 0 and j == 0):
        HiddenMap[Pirate.Row+i][Pirate.Column+j] = DUG_HOLE
        Map[Pirate.Row+i][Pirate.Column+j] = DUG_HOLE
    if TreasureDestroyed:
      break
  Pirate.Score -= 30
  Pirate.UsedDynamite = True
  DisplayMap(Map, MapSize)
  HiddenMap[Pirate.Row][Pirate.Column] = DUG_HOLE
  Map[Pirate.Row][Pirate.Column] = DUG_HOLE
  DisplayResults(Pirate)
  return TreasureDestroyed

def MoveTreasure(Map, MapSize, HiddenMap):
  AvailableTiles = []
  for Row in range(MapSize.Rows):
    for Column in range(MapSize.Columns):
      if Map[Row][Column] == SAND:
        AvailableTiles.append([Row, Column])
      if HiddenMap[Row][Column] == TREASURE:
        TreasureRow = Row
        TreasureColumn = Column
  NewTile = random.choice(AvailableTiles)
  # Setting previous tile to sand
  Map[TreasureRow][TreasureColumn] = SAND
  HiddenMap[TreasureRow][TreasureColumn] = SAND
  # Putting tresure into new place
  HiddenMap[NewTile[0]][NewTile[1]] = TREASURE


def GetPirateAction(Map, MapSize, HiddenMap, Pirate, Answer):
    TreasureDestroyed = False
    if Pirate.NumOfActions % 8 == 0 and Pirate.NumOfActions > 0:
      MoveTreasure(Map, MapSize, HiddenMap)
      print("The tresure has moved!")
    Answer = input("Pirate to walk (W), dig (D) or use dynamite (B), to finish game press Enter: ")
    while not (Answer in ["W", "D", "B", PRESSED_ENTER]):
      Answer = input("Pirate to walk (W), dig (D) or use dynamite (B), to finish game press Enter: ")
    if Answer == "W":
      PirateWalks(Map, MapSize, HiddenMap, Pirate)
    elif Answer == "D":
      PirateDigs(Map, HiddenMap, Pirate)
    elif Answer == "B":
      if Pirate.UsedDynamite == False:
        TreasureDestroyed = PirateUsesDynamite(Map, MapSize, HiddenMap, Pirate)
      else:
        print(f"The pirate has already used dynamite!")
        return Answer
    Pirate.NumOfActions += 1
    if TreasureDestroyed:
      return PRESSED_ENTER
    return Answer

def DisplayResults(Pirate):
  if Pirate.NumberOfCoinsFound > 0:
    print(f"{Pirate.NumberOfCoinsFound} gold coins found")
  print(f"{Pirate.DigTime} hours spent digging")
  print(f"The score is {Pirate.Score}")

def TreasureIsland():
  MapSize = MapSizeRecord()
  Pirate = PirateRecord()
  MapSize = ResetMapSize(MapSize)
  ResetMaps(Map, HiddenMap)
  MapSize = GenerateMap(Map, MapSize)
  GenerateHiddenMap(HiddenMap)
  ResetPirateRecord(Pirate)
  FindLandingPlace(Map, MapSize, Pirate)
  Answer = BLANK
  while Answer != PRESSED_ENTER and Pirate.Score >= 0 and not Pirate.TreasureFound:
    Answer = GetPirateAction(Map, MapSize, HiddenMap, Pirate, Answer)
  print(f"\nFinal results:")
  DisplayResults(Pirate)

if __name__ == "__main__":
  Map = [[SAND for i in range(MAX_COLUMNS)] for j in range(MAX_ROWS)]
  HiddenMap = [[SAND for i in range(MAX_COLUMNS)] for j in range(MAX_ROWS)]
  TreasureIsland()
  ResetMaps(Map, HiddenMap)
  input("Press Enter to finish")