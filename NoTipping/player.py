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
      bestMove = self.playRandomAddStrategy()
    return bestMove

  def playRandomAddStrategy(self):
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
      playerNumber = None
    else:
      playerNumber = self.playerNumber
    moves = self.__board.getPlayableRemoveMoves(playerNumber)

    sortedMoves = sorted(moves, key = operator.itemgetter(1,0), reverse = True)
    if len(sortedMoves) > 0:
      bestMove = sortedMoves[0]
    else:
      bestMove = self.playRandomRemoveStrategy(playerNumber)
    return bestMove

  def playRandomRemoveStrategy(self, playerNumber):
    location = self.__board.getRandomOccupiedLocation(playerNumber)
    weight = self.__board.getWeightAtLocation(location)
    bestMove = (location, weight)
    return bestMove

  def play(self, mode):
    if mode == 1:
      (location, weight) = self.playAddStrategy()
    elif mode == 2:
      (location, weight) = self.playRemoveStrategy()
    else:
      raise Exception("Invalid Mode")
    return (location, weight)

if __name__ == '__main__':
  if len(sys.argv) < 4:
    remainingTime = float('Inf')
  else:
    remainingTime = float(sys.argv[3])

  mode = int(sys.argv[1])
  playerNumber = int(sys.argv[2])

  thisPlayer = Player(playerNumber, remainingTime)
  (location, weight) = thisPlayer.play(mode)
  print(str(location) + ' ' + str(weight))
