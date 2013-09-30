import copy
import random

class Board:
  BOARD_LENGTH = 30
  BOARD_WEIGHT = 3
  INITIAL_WEIGHTLOCATION = -4
  PIVOT_LEFT_LOCATION = -3
  PIVOT_RIGHT_LOCATION = -1
  __board = None
  __pivotLeftDistanceMap = None
  __pivotRightDistanceMap = None
  playerOneWeights = None
  playerTwoWeights = None
  playerOneMoves = None
  playerTwoMoves = None

  def __init__(self):
    # Initial weights available to both players
    self.playerOneWeights = set(range(1,12+1))
    self.playerTwoWeights = set(range(1,12+1))

    # Initialize player sub-boards
    self.playerOneMoves = (0,)*(self.BOARD_LENGTH+1)
    self.playerTwoMoves = (0,)*(self.BOARD_LENGTH+1)

    # Initialize board
    self.__board = (0,)*(self.BOARD_LENGTH+1)
    self.addWeight(self.INITIAL_WEIGHTLOCATION, self.BOARD_WEIGHT, 0)

    # Setup values for evaluating torque
    self.__pivotLeftDistanceMap = self.__getDistanceMapForLocation(self.PIVOT_LEFT_LOCATION)
    self.__pivotRightDistanceMap = self.__getDistanceMapForLocation(self.PIVOT_RIGHT_LOCATION)

    if self.checkIfTipped():
      raise Exception('Invalid Board Setup: Board Tips')

  def __clone__(self):
    clone = copy.deepcopy(self)
    return clone

  def printBoard(self):
    print(self.__board)

  def getRandomOccupiedLocation(self, player = None):
    locations = list(self.getOccupiedLocations(player))
    location = random.choice(locations)
    return location

  def getRandomUnoccupiedLocation(self):
    locations = list(self.getUnoccupiedLocations())
    location = random.choice(locations)
    return location

  def getRandomWeightToAdd(self, player):
    if player == 1:
      weights = list(self.playerOneWeights)
    elif player == 2:
      weights = list(self.playerOneWeights)
    else:
      raise Exception('Invalid player number')
    weight = random.choice(weights)
    return weight

  def getRandomWeightToRemove(self, player = None):
    weights = [self.getWeightAtLocation(i) for i in self.getOccupiedLocations(player)]
    weight = random.choice(weights)
    return weight

  def getPlayableAddMoves(self, player):
    if player == 1:
      weights = self.playerOneWeights
    elif player == 2:
      weights = self.playerTwoWeights
    else:
      raise Exception('Invalid playerNumber')

    locations = self.getUnoccupiedLocations()

    playableMoves = set()
    for weight in weights:
      for location in locations:
        testBoard = self.__clone__()
        testBoard.addWeight(location, weight, player)

        move = (location, weight)
        if not testBoard.checkIfTipped():
          playableMoves.add(move)
    return playableMoves

  def getPlayableRemoveMoves(self, player = None):
    locations = self.getOccupiedLocations(player)

    # Player one cannot remove the weights player two added unless those are the only weights left.
    playableMoves = set()
    for location in locations:
      weight = self.getWeightAtLocation(location)

      testBoard = self.__clone__()
      testBoard.removeWeight(location, weight)

      move = (location, weight)
      if not testBoard.checkIfTipped():
        playableMoves.add(move)
    return playableMoves

  def getWeightAtLocation(self, location):
    index = self.__getIndexFromBoardLocation(location)
    weight = self.__board[index]
    return weight

  def getUnoccupiedLocations(self):
    unoccupiedLocations = set(self.__getBoardLocationFromIndex(i)
                          for i, v in enumerate(self.__board)
                          if v == 0)
    return unoccupiedLocations

  def getOccupiedLocations(self, player = None):
    if player == None:
      testBoard = self.__board
    elif player == 1:
      testBoard = self.playerOneMoves
    elif player == 2:
      testBoard = self.__board
    occupiedLocations = set(self.__getBoardLocationFromIndex(i)
                          for i, v in enumerate(testBoard)
                          if v != 0)
    return occupiedLocations

  def checkIfTipped(self):
    (torqueLeftPivot, torqueRightPivot) = self.getTorque()
    return True if torqueLeftPivot < 0 or torqueRightPivot > 0 else False

  def getTorque(self):
    torqueLeftPivot = self.__getTorque(self.__pivotLeftDistanceMap)
    torqueRightPivot = self.__getTorque(self.__pivotRightDistanceMap)
    return (torqueLeftPivot, torqueRightPivot)

  def __getTorque(self, distanceMap):
    torque = tuple(distanceMap[i] * self.__board[i] for i in range(0, self.BOARD_LENGTH+1))

    centerOfDistanceForce = distanceMap[self.__getIndexFromBoardLocation(0)] * self.BOARD_WEIGHT 
    torque = sum(torque) + centerOfDistanceForce
    return torque

  def addWeight(self, location, weight, player):
    if weight < 0:
      raise Exception("Weight cannot be negative")
    elif abs(location) > self.BOARD_LENGTH/2:
      raise Exception("Location not on board")

    if player == 1:
      if weight not in self.playerOneWeights:
        raise Exception("Player 1 does not have weight: " + str(weight) + " available")
      else:
        self.playerOneWeights.remove(weight)
        self.playerOneMoves = self.__replaceBoardAtLocationWithValue(self.playerOneMoves, location, weight)
    elif player == 2:
      if weight not in self.playerTwoWeights:
        raise Exception("Player 2 does not have weight: " + str(weight) + " available")
      else:
        self.playerTwoWeights.remove(weight)
        self.playerTwoMoves = self.__replaceBoardAtLocationWithValue(self.playerTwoMoves, location, weight)
    elif player == 0 and not (weight == 0 or weight == self.BOARD_WEIGHT):
      raise Exception("Invalid weight for player 0")
    elif player not in {0,1,2}:
      raise Exception("Invalid player")

    index = self.__getIndexFromBoardLocation(location)
    if self.getWeightAtLocation(location) != 0:
      raise Exception("Location is already occupied")
    self.__board = self.__replaceBoardAtLocationWithValue(self.__board, location, weight)

  def removeWeight(self, location, weight):
    index = self.__getIndexFromBoardLocation(location)
    if self.getWeightAtLocation(location) == weight:
      self.__board = self.__replaceBoardAtLocationWithValue(self.__board, location, 0)
      self.playerOneMoves = self.__replaceBoardAtLocationWithValue(self.playerOneMoves, location, 0)
      self.playerTwoMoves = self.__replaceBoardAtLocationWithValue(self.playerTwoMoves, location, 0)
    else:
      raise Exception("Weight at location: " + str(weightAtIndex) +
          " Tried to remove weight: " + str(weight))

  def __getIndexFromBoardLocation(self, location):
    index = int(location + self.BOARD_LENGTH/2)
    return index

  def __getBoardLocationFromIndex(self, index):
    location = int(index - self.BOARD_LENGTH/2)
    return location

  def __getDistanceMapForLocation(self, location):
    index = self.__getIndexFromBoardLocation(location)
    distanceMap = tuple(range(0-index, (self.BOARD_LENGTH+1)-index))
    return distanceMap

  def __replaceBoardAtLocationWithValue(self, inputBoard, location, value):
    index = self.__getIndexFromBoardLocation(location)
    outputBoard = inputBoard[0:index] + (value,) + inputBoard[index + 1:]
    return outputBoard

def readMoves(fileName):
  thisBoard = Board()
  with open(fileName, 'r') as file_:
    data = file_.read()
  data = data.split('\n')

  if data[-1] == '':
    data = data[0:-1]

  for index in range(0, len(data)-1):
    values = data[index].split()

    mode = int(values[0])
    location = int(values[1])
    weight = int(values[2])
    player = int(values[3])
    if mode == 1:
      thisBoard.addWeight(location, weight, player)
    elif mode == 2:
      thisBoard.removeWeight(location, weight)
    else:
      raise Exception("Invalid mode")

    torque = thisBoard.getTorque()

    if mode == 1:
      if thisBoard.checkIfTipped():
        print('The board has tipped adding weight: ' + str(weight) + 
              ' at location: ' + str(location) + ' resulting in torque: ' + str(torque))
        print('Player ' + str(player) + ' lost!')
      else:
        print('Player: ' + str(player) + ' Added weight: ' + str(weight) +
              ' at location: ' + str(location) + 
              ' resulting in torque: ' + str(torque))
    else:
      if thisBoard.checkIfTipped():
       print('The board has tipped removing weight: ' + str(weight) + 
             ' at location: ' + str(location) + ' resulting in torque: ' + str(torque))
       print('Player ' + str(player) + ' lost!')
      else:
        print('Player: ' + str(player) + ' Removed weight: ' + str(weight) +
              ' at location: ' + str(location) + 
              ' resulting in torque: ' + str(torque))
  value = data[-1].split()
  playerOneTime = value[1]
  playerTwoTime = value[2]
  print('Player 1 Total Time: ' + str(playerOneTime) + ' Player 2 TotalTime: ' + str(playerTwoTime))
  return thisBoard

def readBoard(fileName):
  thisBoard = Board()
  with open(fileName, 'r') as file_:
    data = file_.read()
  data = data.split('\n')

  if data[-1] == '':
    data = data[0:-1]

  # Remove default value at initial weight location
  thisBoard.removeWeight(thisBoard.INITIAL_WEIGHTLOCATION, thisBoard.BOARD_WEIGHT)
  
  for values in data:
    values = values.split()
    location = int(values[0])
    weight = int(values[1])
    player = int(values[2])
    thisBoard.addWeight(location, weight, player)
  
  torque = thisBoard.getTorque()
  #print("Current Torque: " + str(torque))
  if thisBoard.checkIfTipped():
    print("The board has already tipped")
  return thisBoard

if __name__ == '__main__':
  thisBoard = readMoves('move.txt')
  thisBoard = readBoard('board.txt')
