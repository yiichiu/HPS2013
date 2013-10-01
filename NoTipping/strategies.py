import board
import time
import operator

class Strategies:
  __boardStorage = None
  MAX_DEPTH = 2
  initialPlayer = None
  currentPlayer = None
  undoRemove = None
  depth = None

  def __init__(self, playerNumber):
    self.initialPlayer = playerNumber
    self.currentPlayer = playerNumber
    self.__boardStorage = None

  def alphaBeta(self, thisBoard, A, B):
    if self.depth == None:
      self.depth = 0
    else:
      self.depth = self.depth + 1

    if self.isLeaf(thisBoard) or self.depth == self.MAX_DEPTH:
      return self.estimateScore(thisBoard)

    alpha = A
    beta = B

    playableMoves = self.getPlayableMoves(thisBoard)

    if self.isMaxNode():
      for playableMove in playableMoves:
        # Configure thisBoard so that it looks like the successor
        self.playMove(thisBoard, playableMove)
        
        # Alpha Beta Pruning
        alpha = self.getMaxPlayableMove(alpha, self.alphaBeta(thisBoard, alpha, beta))

        # Undo Move
        self.undoMove(thisBoard, playableMove)
        self.depth = self.depth - 1

        return self.getMaxPlayableMove(alpha, beta)
        #if alpha >= beta:
        #  return beta
        #return alpha

    else:
      for playableMove in playableMoves:
        # Configure thisBoard so that it looks like the successor
        self.playMove(thisBoard, playableMove)

        # Alpha Beta Pruning
        beta = self.getMaxPlayableMove(beta, self.alphaBeta(thisBoard, alpha, beta))

        # Undo Move
        self.undoMove(thisBoard, playableMove)
        self.depth = self.depth - 1

        return self.getMaxPlayableMove(alpha, beta)

  def getMaxPlayableMove(self, set1, set2):
    inf = float('Inf')
    infSet = (inf, inf, inf, inf)
    if set1 == set() and set2 == set():
      return infSet
    if set1 == infSet:
      return set2
    elif set2 == infSet:
      return set1
    elif set1[2] > set2[2]:
      return set1
    else:
      return set2

  def playMove(self, thisBoard, playableMove):
    location = playableMove[0] 
    weight = playableMove[1] 

    # Advance the board
    if thisBoard.playerTwoWeights == set():
      # We should be removing
      thisBoard.removeWeight(location, weight)
      self.undoRemove = True
    else:
      thisBoard.addWeight(location, weight, self.currentPlayer)
      self.undoRemove = False

    # Shift the player to the opponent
    self.currentPlayer = self.getOpponent()

  def undoMove(self, thisBoard, playableMove):
    location = playableMove[0] 
    weight = playableMove[1] 

    # Shift the player back
    self.currentPlayer = self.getOpponent()
    if len([i for i in thisBoard.playerOneMoves if i != 0]) == thisBoard.MAX_WEIGHT:
      self.undoRemove = False

    # undo the board
    if self.undoRemove:
      # We should be undoing a remove
      thisBoard.undoRemove(location, weight, self.currentPlayer)
    else:
      thisBoard.undoAdd(location, weight, self.currentPlayer)

  def getOpponent(self):
    if self.currentPlayer == 1:
      return 2
    else:
      return 1

  def isMaxNode(self):
    if self.currentPlayer == self.initialPlayer:
      return True
    else:
      return False

  def isLeaf(self, thisBoard):
    if len(self.getPlayableMoves(thisBoard)) == 0:
      return True
    else:
      return False

  def getPlayableMoves(self, thisBoard):
    if thisBoard.playerTwoWeights == set():
      return thisBoard.getPlayableRemoveMoves()
    else:
      return thisBoard.getPlayableAddMoves(self.currentPlayer)

  def estimateScore(self, thisBoard):
    playableMoves = thisBoard.getPlayableRemoveMoves()

    # Sort the torques so that (torque1, torque2) torque1 goes from highest to lowest. This means of
    # course that torque2 will go fomr lowest to highest.
    sortedMoves = sorted(playableMoves, key = operator.itemgetter(2), reverse = True)

    if len(sortedMoves) == 0:
      return worst

    (playerOneTorque1, playerOneTorque2) = thisBoard.getTorque(thisBoard.playerOneMoves)
    if self.currentPlayer == 1:
      # We want to balance the weights that player one placed as much as possible.
      if abs(playerOneTorque1) > abs(playerOneTorque2):
        bestMove = sortedMoves[-1]
      else:
        bestMove = sortedMoves[0]
    else:
      # Otherwise we want to unbalance the weights that player one placed as much as possible.
      bestMove = sortedMoves[0]
    return bestMove

def runAlphaBeta(thisBoard, playerNumber):
  inf = float('Inf')
  infSet1 = (inf, inf, inf, inf)
  infSet2 = (inf, inf, inf, inf)
  testStrategies = Strategies(playerNumber)
  score =  testStrategies.alphaBeta(thisBoard, infSet1, infSet2)
  output = (score[0], score[1])
  return output

if __name__ == '__main__':
  thisBoard = board.readBoard('board.txt')

  output = runAlphaBeta(thisBoard, 1)
  print(output)
