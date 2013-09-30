import board
import time

class Strategies:
  __boardStorage = None
  initialPlayer = None

  def __init__(self, playerNumber):
    self.initialPlayer = playerNumber
    self.__boardStorage = None

  def minimax(self, playerNumber, thisBoard, depth):
    score = 0
    if thisBoard.playerTwoWeights == set():
      playableMoves = thisBoard.getPlayableRemoveMoves()
    else:
      playableMoves = thisBoard.getPlayableAddMoves(playerNumber)

    if playerNumber == 1:
      opponentNumber = 2
    else:
      opponentNumber = 1

    if playerNumber == self.initialPlayer and len(playableMoves) == 0:
      score = -1
    elif len(playableMoves) == 0:
      score = 1
    elif depth == 1:
      score = 0

    for move in playableMoves:
      location = move[0]
      weight = move[1]
      #print('Location: ' + str(location) + ' Weight: ' + str(weight) + ' Player: ' + str(playerNumber))

      if thisBoard.playerTwoWeights == set():
        thisBoard.removeWeight(location, weight)
      else:
        thisBoard.addWeight(location, weight, playerNumber)
      #thisBoard.printBoard()

      #if depth == 1:
      #  score = 0
      #elif playerNumber == self.initialPlayer and len(playableMoves) == 0:
      #  score = -1
      #elif len(playableMoves) == 0:
      #  score = 1
      #else:
      score = score + self.minimax(opponentNumber, thisBoard, depth - 1)

      if thisBoard.playerTwoWeights == set():
        thisBoard.undoRemove(location, weight, playerNumber)
      else:
        thisBoard.undoAdd(location, weight, playerNumber)
    print(score)
    return score

if __name__ == '__main__':
  startTime = time.clock()
  thisBoard = board.readBoard('testBoard')

  testStrategies = Strategies(1)
  score = testStrategies.minimax(1, thisBoard, 4)
  print(time.clock() - startTime)
