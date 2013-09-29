import sys
import board
import operator

class Player:
  BOARD_NAME = 'board.txt'
  __board = None
  playerNumber = None

  def __init__(self, playerNumber, remainingTime):
    self.__board = board.readBoard(self.BOARD_NAME)
    self.playerNumber = playerNumber

  def playAddStrategy(self):
    moves = self.__board.getPlayableAddMoves(self.playerNumber)
    sortedMoves = sorted(moves, key = operator.itemgetter(1,0), reverse = True)
    if len(sortedMoves) > 0:
      bestMove = sortedMoves[0]
    else:
      weight = self.__board.getRandomWeightToAdd()
      location = self.__board.getRandomUnoccupiedLocation()
      bestMove = (location, weight)
    return bestMove

  def playRemoveStrategy(self):
    remainingPlayerOneMoves = set(self.__board.playerOneMoves)
    # This tells us to not remove player two's weights if we are player one, unless we are forced
    # to do so.
    if remainingPlayerOneMoves == {0}:
      # This tells us to not remove player two's weights if we are player one, unless we are forced
      # to do so.
      print(moves)
      moves = self.__board.getPlayableRemoveMoves()
    else:
      moves = self.__board.getPlayableRemoveMoves(self.playerNumber)

    sortedMoves = sorted(moves, key = operator.itemgetter(1,0), reverse = True)
    if len(sortedMoves) > 0:
      bestMove = sortedMoves[0]
    else:
      location = self.__board.getRandomOccupiedLocation()
      weight = self.__board.getWeightAtLocation(location)
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
