import copy
import random

class Player:
  playerNumber = None
  board = None
  playerOneBoard = None
  playerOneWeights = None
  playerTwoWeights = None
  
  def __init__(self, playerNumber, board, playerOneBoard, playerOneWeights, playerTwoWeights):
    self.playerNumber = playerNumber
    self.board = board
    self.playerOneBoard = playerOneBoard
    self.playerOneWeights = playerOneWeights
    self.playerTwoWeights = playerTwoWeights

  def play(self, mode):
    if mode == 1:
      return self.playAddMove()
    else:
      return self.playRemoveMove()

  def playAddMove(self):
    moves = self.getPlayableAddMoves()
    if len(moves) == 0:
      move = self.playRandomAddMove()
    else:
      move = self.playBalancePlayerOneMove(moves)
    return move

  def playRemoveMove(self):
    moves = self.getPlayableRemoveMoves()
    if len(moves) == 0:
      move = self.playRandomRemoveMove()
    else:
      move = self.playBalancePlayerOneMove(moves)
    return move

  def playBalancePlayerOneMove(self, moves):
    # The moves are sorted by the left torque
    sortedMoves = sorted(moves, key = operator.itemgetter(2), reverse = True)
    (playerOneTorqueLeft, playerOneTorqueRight) = self.playerOneBoard.getTorque()
    if self.playerNumber == 1:
      # We want to balance the weights that player one placed as much as possible.
      if abs(playerOneToqureLeft) > abs(playerOneToqureRight):
        bestMove = sortedMoves[-1]
      else:
        bestMove = sortedMoves[0]
    else:
      # Otherwise we want to unbalance the weights that player one placed as much as possible.
      bestMove = sortedMoves[0]
    return bestMove

  def getPlayableAddMoves(self):
    if self.playerNumber == 1:
      weights = self.playerOneWeights
    elif self.playerNumber == 2:
      weights = self.playerTwoWeights

    locations = self.board.getUnoccupiedLocations()

    playableMoves = set()
    for weight in weights:
      for location in locations:
        testBoard = self.board.__clone__()
        testBoard.addWeight(location, weight)

        move = (location, weight)
        if not testBoard.checkIfTipped():
          # Playable moves are (location, weight, torque1, torque2)
          torque = testBoard.getTorque()
          thisMove = move + torque
          playableMoves.add(thisMove)
    return playableMoves

  def getPlayableRemoveMoves(self):
    # Player one cannot remove the weights player two added unless those are the only weights left.
    locations = set()
    if self.playerNumber == 1:
      locations = self.playerOneBoard.getOccupiedLocations()
      board = self.playerOneBoard
    if locations == set():
      locations = self.board.getOccupiedLocations()
      board = self.board

    playableMoves = set()
    for location in locations:
      weight = board.getWeightAtLocation(location)

      testBoard = board.__clone__()
      testBoard.removeWeight(location, weight)

      move = (location, weight)
      if not testBoard.checkIfTipped():
        # Playable moves are (location, weight, torque1, torque2)
        torque = testBoard.getTorque()
        thisMove = move + torque
        playableMoves.add(thisMove)
    return playableMoves

  def playRandomAddMove(self):
    # We only reach this place if we know we will lose, so implement to choose anything.
    if self.playerNumber == 1:
      weights = self.playerOneWeights
    elif self.playerNumber == 2:
      weights = self.playerTwoWeights

    locations = self.board.getUnoccupiedLocations()
    location = random.choice(tuple(locations))
    weight = random.choice(tuple(weights))

    testBoard = board.__clone__()
    testBoard.addWeight(location, weight)
    torque = testBoard.getTorque()
    move = (location, weight) + torque
    return move

  def playRandomRemoveMove(self):
    # We only reach this place if we know we will lose, so implement to choose anything.
    # Player one cannot remove the weights player two added unless those are the only weights left.
    locations = set()
    if self.playerNumber == 1:
      locations = self.playerOneBoard.getOccupiedLocations()
      board = self.playerOneBoard
    if locations == set():
      locations = self.board.getOccupiedLocations()
      board = self.board

    location = random.choice(tuple(locations))
    weight = board.getWeightAtLocation(location)

    testBoard = board.__clone__()
    testBoard.removeWeight(location, weight)
    torque = testBoard.getTorque()
    move = (location, weight) + torque
    return move

class Board:
  BOARD_LENGTH = 30
  BOARD_WEIGHT = 3
  PIVOT_LEFT_LOCATION = -3
  PIVOT_RIGHT_LOCATION = -1
  __board = None
  __pivotLeftDistanceMap = None
  __pivotRightDistanceMap = None

  def __init__(self):
    # Initialize board and setup values for evaluating torque
    self.__board = (0,)*(self.BOARD_LENGTH+1)
    self.__pivotLeftDistanceMap = self.__getDistanceMapForLocation(self.PIVOT_LEFT_LOCATION)
    self.__pivotRightDistanceMap = self.__getDistanceMapForLocation(self.PIVOT_RIGHT_LOCATION)

  def __clone__(self):
    clone = copy.deepcopy(self)
    return clone

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

  def addWeight(self, location, weight):
    if weight < 0:
      raise Exception("Weight cannot be negative")
    elif abs(location) > self.BOARD_LENGTH/2:
      raise Exception("Location not on board")
    elif self.getWeightAtLocation(location) != 0:
      raise Exception('Location: ' + str(location) + ' is already occupied with Weight: ' + str(weight))
    self.__board = self.__replaceBoardAtLocationWithValue(self.__board, location, weight)

  def removeWeight(self, location, weight):
    index = self.__getIndexFromBoardLocation(location)
    weightAtLocation = self.getWeightAtLocation(location) 
    if weightAtLocation == weight:
      self.__board = self.__replaceBoardAtLocationWithValue(self.__board, location, 0)
    else:
      raise Exception("Location: " + str( location) + " Weight at location: " + str(weightAtLocation) +
          " Tried to remove weight: " + str(weight))

  def getWeightAtLocation(self, location):
    index = self.__getIndexFromBoardLocation(location)
    weight = self.__board[index]
    return weight

  def getUnoccupiedLocations(self):
    unoccupiedLocations = set(self.__getBoardLocationFromIndex(i)
                          for i, v in enumerate(self.__board)
                          if v == 0)
    return unoccupiedLocations

  def getOccupiedLocations(self):
    occupiedLocations = set(self.__getBoardLocationFromIndex(i)
                          for i, v in enumerate(self.__board)
                          if v != 0)
    return occupiedLocations

  def __getDistanceMapForLocation(self, location):
    index = self.__getIndexFromBoardLocation(location)
    distanceMap = tuple(range(0-index, (self.BOARD_LENGTH+1)-index))
    return distanceMap

  def __replaceBoardAtLocationWithValue(self, inputBoard, location, value):
    index = self.__getIndexFromBoardLocation(location)
    outputBoard = inputBoard[0:index] + (value,) + inputBoard[index + 1:]
    return outputBoard

  def __getIndexFromBoardLocation(self, location):
    index = int(location + self.BOARD_LENGTH/2)
    return index

  def __getBoardLocationFromIndex(self, index):
    location = int(index - self.BOARD_LENGTH/2)
    return location

def readBoard(fileName, maxWeight = 12):
  board = Board()
  playerOneBoard = Board()
  playerOneWeights = set(range(1,maxWeight+1))
  playerTwoWeights = set(range(1,maxWeight+1))
  with open(fileName, 'r') as file_:
    data = file_.read()
  data = data.split('\n')

  if data[-1] == '':
    data = data[0:-1]

  for values in data:
    values = values.split()
    location = int(values[0])
    weight = int(values[1])
    playerNumber = int(values[2])
    if playerNumber in {0, 1}:
      playerOneBoard.addWeight(location,weight)
    board.addWeight(location, weight)
      
    if playerNumber == 1 and weight != 0:
      playerOneWeights.remove(weight)
    elif playerNumber == 2 and weight != 0:
      playerTwoWeights.remove(weight)
  
  if board.checkIfTipped():
    print("The board has already tipped")
  return (board, playerOneBoard, playerOneWeights, playerTwoWeights)

def execute(mode, playerNumber):
  (board, playerOneBoard, playerOneWeights, playerTwoWeights) = readBoard('board.txt')
  player = Player(playerNumber, board, playerOneBoard, playerOneWeights, playerTwoWeights)
  return player.play(mode)

if __name__ == '__main__':
  import sys

  if len(sys.argv) < 4:
    remainingTime = float('Inf')
  else:
    remainingTime = float(sys.argv[3])

  mode = int(sys.argv[1])
  playerNumber = int(sys.argv[2])
  move = execute(mode, playerNumber)
  print(str(move[0]) + ' ' + str(move[1]))
