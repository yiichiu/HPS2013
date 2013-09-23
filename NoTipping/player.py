import sys
import board
import operator

class Player:
  BOARD_NAME = 'board.txt'
  __board = None

  def __init__(self, playerNumber, remainingTime):
    self.__board = board.readBoard(self.BOARD_NAME)

  def playAddStrategy(self):
    moves = self.__board.getPlayableAddMoves(playerNumber)
    sortedMoves = sorted(moves, key = operator.itemgetter(1,0), reverse = True)
    if len(sortedMoves) > 0:
      bestMove = sortedMoves[0]
    else:
      weight = self.__board.getRandomWeight()
      location = self.__board.getRandomLocation()
      bestMove = (location, weight)
    return bestMove

  def playRemoveStrategy(self):
    moves = self.__board.getPlayableRemoveMoves()
    sortedMoves = sorted(moves, key = operator.itemgetter(1,0), reverse = True)
    if len(sortedMoves) > 0:
      bestMove = sortedMoves[0]
    else:
      weight = self.__board.getRandomWeight()
      location = self.__board.getRandomLocation()
      bestMove = (location, weight)
    return bestMove

if __name__ == '__main__':
  if len(sys.argv) < 4:
    remainingTime = float('Inf')
  else:
    remainingTime = float(sys.argv[3])

  mode = int(sys.argv[1])
  playerNumber = int(sys.argv[2])
  if mode == 1:
    (location, weight) = Player(playerNumber, remainingTime).playAddStrategy()
  elif mode == 2:
    (location, weight) = Player(playerNumber, remainingTime).playRemoveStrategy()
  else:
    raise Exception("Invalid Mode")
  print(str(location) + ' ' + str(weight))
