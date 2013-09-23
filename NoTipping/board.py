class Board:
  BOARD_LENGTH = 30
  BOARD_WEIGHT = 3
  INITIAL_WEIGHTLOCATION = -4
  PIVOT_LEFT_LOCATION = -3
  PIVOT_RIGHT_LOCATION = -1
  __board = None
  __pivotLocations = None
  __remainingWeights = None
  __pivotLocations = None
  __pivotLeftDistanceMap = None
  __pivotRightDistanceMap = None

  def __init__(self):
    # Initialize board
    self.__board = (0,)*(self.BOARD_LENGTH+1)
    self.__pivotLocations = (self.PIVOT_LEFT_LOCATION, self.PIVOT_LEFT_LOCATION)
    self.addWeight(self.INITIAL_WEIGHTLOCATION, self.BOARD_WEIGHT)

    # Setup values for evaluating torque
    self.__pivotLeftDistanceMap = self.__getDistanceMapForLocation(self.PIVOT_LEFT_LOCATION)
    self.__pivotRightDistanceMap = self.__getDistanceMapForLocation(self.PIVOT_RIGHT_LOCATION)

    if self.checkIfTipped():
      raise Exception("Invalid Board Setup: Board Tips")

  def checkIfTipped(self):
    (torqueLeftPivot, torqueRightPivot) = self.getTorque()
    return True if torqueLeftPivot > 0 or torqueRightPivot < 0 else False

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

    index = self.__getIndexFromBoardLocation(location)
    if self.__board[index] != 0:
      raise Exeception("Location is already occupied")
    self.__board = self.__board[0:index] + (weight,) + self.__board[index + 1:]

  def removeWeight(self):
    pass

  def __getIndexFromBoardLocation(self, location):
    index = int(location + self.BOARD_LENGTH/2)
    return index

  def __getDistanceMapForLocation(self, location):
    index = self.__getIndexFromBoardLocation(location)
    distanceMap = tuple(range(index, index-(self.BOARD_LENGTH+1), -1))
    return distanceMap

def setupBoardFromFile(fileName):
  thisBoard = Board()
  with open(fileName, 'r') as file_:
    data = file_.read()
  data = data.split('\n')
  data.remove('')

  for values in data:
    values = values.split()
    location = int(values[0])
    weight = int(values[1])
    color = values[2:]
    thisBoard.addWeight(location, weight)

    if thisBoard.checkIfTipped():
      # Maybe this should be an exception
      print('The board has tipped adding weight: ' + str(weight) + ' at location: ' + str(location))
  return thisBoard

if __name__ == '__main__':
  thisBoard = setupBoardFromFile('input')
  torque = thisBoard.getTorque()
  print('Final Torque: ' + str(torque))
