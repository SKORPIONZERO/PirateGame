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
    self.Score = 300
    self.DigTime = 0.0
    self.TreasureFound = False
    self.NumberOfCoinsFound = 0
    self.NumOfDigs = 0
    self.UsedDynamite = False
    self.NumOfActions = 0
    self.Drown = False
    self.NumOfCoconuts = 0

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
  Pirate.Score = 300
  Pirate.DigTime = 0.0
  Pirate.TreasureFound = False
  Pirate.NumberOfCoinsFound = 0
  Pirate.NumofDigs = 0
  Pirate.UsedDynamite = False
  Pirate.NumOfActions = 0
  Pirate.Drown = False
  Pirate.NumOfCoconuts = 0

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
    if NumberOfSquares < 1 or NumberOfSquares > 20:
      print("Distance must be between 1 and 20")
      ValidDistance = False
  except:
    print("Not a valid integer between 1 and 20")
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
      if Map[Row][StartColumn] not in [SAND,DUG_HOLE] or (Map[Row][StartColumn] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "NE":
    for i in range(1, StartRow - EndRow + 1):
      if Map[StartRow - i][StartColumn + i] not in [SAND,DUG_HOLE] or (Map[StartRow - i][StartColumn + i] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "E":
    for Column in range(StartColumn + 1, EndColumn + 1):
      if Map[StartRow][Column] not in [SAND,DUG_HOLE] or (Map[StartRow][Column] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "SE":
    for i in range(1, EndRow - StartRow + 1):
      if Map[StartRow + i][StartColumn + i] not in [SAND,DUG_HOLE] or (Map[StartRow + i][StartColumn + i] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "S":
    for Row in range(StartRow + 1, EndRow + 1):
      if Map[Row][StartColumn] not in [SAND,DUG_HOLE] or (Map[Row][StartColumn] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "SW":
    for i in range(1, EndRow - StartRow + 1):
      if Map[StartRow + i][StartColumn - i] not in [SAND,DUG_HOLE] or (Map[StartRow + i][StartColumn - i] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "W":
    for Column in range(EndColumn, StartColumn):
      if Map[StartRow][Column] not in [SAND,DUG_HOLE] or (Map[StartRow][Column] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  elif Direction == "NW":
    for i in range(1, StartRow - EndRow + 1):
      if Map[StartRow - i][StartColumn - i] not in [SAND,DUG_HOLE] or (Map[StartRow - i][StartColumn - i] == DUG_HOLE and not O_not_obstacle):
        ObstacleFound = True
  return ObstacleFound

def Move(Map, MapSize, Pirate, Row, Column, Distance):
  if Map[Pirate.Row][Pirate.Column] == PIRATES:
    Map[Pirate.Row][Pirate.Column] = SAND
  Pirate.Row = Row
  Pirate.Column = Column
  Pirate.Score -= int(Distance)
  Map[Pirate.Row][Pirate.Column] = PIRATES
  DisplayMap(Map, MapSize)

def PirateWalks(Map, MapSize, HiddenMap, Pirate):
  ObstacleInPath = True
  ValidDistance = False
  ValidDirection = False
  SurroundedByObstacles = True
  O_not_obstacle = False
  while ObstacleInPath or not ValidDistance or not ValidDirection:
    WalkData = input("Enter length (1 to 20) and direction (N, NE, E, SE, S, SW, W, NW): ")
    Distance = 0
    Direction = BLANK
    for k in range(len(WalkData)):
      if WalkData[0:k+1].isdigit():
        Distance = WalkData[0:k+1]
    for n in range(len(WalkData)):
      if WalkData[-1:-n-2:-1].isalpha():
        Direction = WalkData[-n-1:]
    Row = Pirate.Row
    Column = Pirate.Column
    for i in [-1, 0, 1]:
      for j in [-1, 0, 1]:
        if Map[Pirate.Row+i][Pirate.Column+j] == SAND:
          SurroundedByObstacles = False
    ValidDistance, NumberOfSquares = CheckDistance(Distance)
    if SurroundedByObstacles:
      O_not_obstacle = True
      if Distance == "1":
        ValidDistance = False
        print("Need to get out of the entire hole!")
    ValidDirection, Row, Column = CheckDirection(Direction, Row, Column, NumberOfSquares)
    if Row >= MapSize.Rows or Column >= MapSize.Columns or Row < 0 or Column < 0:
      ValidDirection = False
      print("Error")
    if ValidDirection:
      ObstacleInPath = CheckPath(Map, Pirate.Row, Pirate.Column, Row, Column, Direction, O_not_obstacle)
      if ObstacleInPath:
        print("Pirate can't walk this way as there is an obstacle in the way")
  Move(Map, MapSize, Pirate, Row, Column, WalkData[0])

def DisplayFind(Pirate, ItemFound):
  if ItemFound == COCONUT:
    Item = "Coconut"
    Pirate.NumOfCoconuts += 1
  elif ItemFound == TREASURE:
    Item = "\033[32mTreasure chest\033[0m"
    Pirate.TreasureFound = True
    Pirate.Score += 200
  elif ItemFound == GOLD_COIN:
    Item = "Gold coin"
    Pirate.NumberOfCoinsFound += 1
    print("The treasure must be nearby")
  elif ItemFound == DUG_HOLE:
    return
  else:
    Item = "Unidentified item"
  print(f"Found {Item}")

def OpenMapPart():
  return

def PirateDigs(Map, HiddenMap, Pirate):
  RandomValue = random.randint(0,9)
  if RandomValue == 0:
    OpenMapPart()
  if HiddenMap[Pirate.Row][Pirate.Column] not in [SAND, DUG_HOLE]:
    DisplayFind(Pirate, HiddenMap[Pirate.Row][Pirate.Column])
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
          DisplayFind(Pirate, HiddenMap[Pirate.Row+i][Pirate.Column+j])
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
  return [NewTile[0],NewTile[1]]

def MoveWater(Map, MapSize, Pirate):
  TilesTurnToWater = []
  Row = 0
  while Row < MapSize.Rows:
    Column = 0
    while Column < MapSize.Columns:
      if Map[Row][Column] == WATER:
        for i in [-1, 0, 1]:
          for j in [-1, 0, 1]:
            if not (Row+i < 0 or Row+i>=MapSize.Rows) and not (Column+j < 0 or Column+j>=MapSize.Columns):
              if Row+i == Pirate.Row and Column+j == Pirate.Column:
                Pirate.Drown = True
              TilesTurnToWater.append([Row+i,Column+j])
      Column += 1
    Row += 1
    print(Row)
  for n in TilesTurnToWater:
    Map[n[0]][n[1]] = WATER
  DisplayMap(Map, MapSize)

def OpenInventory(Pirate):
  print(f"Inventory: Number of coconuts: {Pirate.NumOfCoconuts}")
  Answer = BLANK
  while not (Answer in ["C", "Q"]): 
    Answer = input("Press to eat a coconut (C), to drop a coconut(D), to close inventory (Q): ")
    match(Answer):
      case "C":
        if Pirate.NumOfCoconuts != 0:
          Pirate.NumOfCoconuts -= 1
          Pirate.Score += 20
          print(f"You ate a coconut and restored 20 score points")
          print(f"New pirate score is: {Pirate.Score}")
          Answer = BLANK
          continue
        else:
          print("You haven't found any coconuts!")
          Answer = BLANK
          continue
      case "Q":
        return
      case "D":
        CoconutDroppedSuccessfuly = False
        if Pirate.NumOfCoconuts != 0:
          Pirate.NumOfCoconuts -= 1
          for row in [-1,1]:
            for column in [-1, 1]:
              if Map[Pirate.Row + row][Pirate.Column + column] == HUT:
                print("\nYou successfully saved a coconut next to the corner of the hut to relax after working!")
                CoconutDroppedSuccessfuly = True
          if CoconutDroppedSuccessfuly == False:
            print("\nYou dropped a coconut in the incorrect spot")
            Map[Pirate.Row][Pirate.Column] = COCONUT
        else:
          print("You haven't found any coconuts!")
          Answer = BLANK
          continue
      case _:
        continue
  
def GetPirateAction(Map, MapSize, HiddenMap, Pirate, Answer):
    TreasureDestroyed = False
    Answer = input("Pirate to walk (W), dig (D), use dynamite (B) or open inventory (I), to finish game press Enter: ")
    while not (Answer in ["W", "D", "B","I", PRESSED_ENTER]):
      Answer = input("Pirate to walk (W), dig (D), use dynamite (B) or open inventory (I), to finish game press Enter: ")
    match(Answer):
      case "W":
        PirateWalks(Map, MapSize, HiddenMap, Pirate)
      case "D":
        PirateDigs(Map, HiddenMap, Pirate)
      case "B":
        if Pirate.UsedDynamite == False:
          TreasureDestroyed = PirateUsesDynamite(Map, MapSize, HiddenMap, Pirate)
        else:
          print(f"The pirate has already used dynamite!")
          return Answer
      case "I":
        OpenInventory(Pirate)
      case _:
        pass
    Pirate.NumOfActions += 1
    if TreasureDestroyed:
      return PRESSED_ENTER
    if Pirate.NumOfActions % 8 == 0 and Pirate.NumOfActions > 0:
      TreasreTile = MoveTreasure(Map, MapSize, HiddenMap)
      print("The tresure has moved!")
      print(f"New treasure location is {TreasreTile}")
    if Pirate.NumOfActions % 10 == 0 and Pirate.NumOfActions > 0:
      MoveWater(Map, MapSize, Pirate)
      print("The water level is rising!")
      if Pirate.Drown:
        print(f"\033[31mThe pirate has drown!\033[0m")
        return PRESSED_ENTER
    return Answer

def DisplayResults(Pirate):
  if Pirate.NumberOfCoinsFound > 0:
    print(f"{Pirate.NumberOfCoinsFound} gold coins found")
  print(f"{Pirate.DigTime} hours spent digging")
  print(f"The score is {Pirate.Score}")

def DisplayMissing(MapSize, HiddenMap):
  Row = 0
  MissingCoconuts = 0
  MissingCoins = 0
  MissingTreasure = False
  FinalStatement = ""
  while Row < MapSize.Rows:
    Column = 0
    while Column < MapSize.Columns:
      if HiddenMap[Row][Column] != SAND:
        if HiddenMap[Row][Column] == COCONUT:
          MissingCoconuts += 1
        if HiddenMap[Row][Column] == GOLD_COIN:
          MissingCoins += 1
        if HiddenMap[Row][Column] == TREASURE:
          MissingTreasure = True
      Column += 1
    Row += 1
  if MissingCoconuts != 0:
    FinalStatement += f"{MissingCoconuts} coconuts"
  if len(FinalStatement) != 0:
    FinalStatement += ", "
  if MissingCoins != 0:
    FinalStatement += f"{MissingCoins} coins"
  if MissingTreasure == True:
    if len(FinalStatement) != 0:
      FinalStatement += " and the treasure chest were left behind."
    else:
      FinalStatement += "treasure chest was left behind."
  else:
    if len(FinalStatement) != 0:
      if (MissingCoconuts == 0 and MissingCoins == 1) or (MissingCoconuts == 1 and MissingCoins == 0):
        FinalStatement += " was left behind."
      else:
        FinalStatement += " were left behind."
    else:
      FinalStatement += "Nothing was left behind)"
  print(FinalStatement)

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
  DisplayMissing(MapSize, HiddenMap)

if __name__ == "__main__":
  Map = [[SAND for i in range(MAX_COLUMNS)] for j in range(MAX_ROWS)]
  HiddenMap = [[SAND for i in range(MAX_COLUMNS)] for j in range(MAX_ROWS)]
  TreasureIsland()
  ResetMaps(Map, HiddenMap)
  input("\nPress Enter to finish")