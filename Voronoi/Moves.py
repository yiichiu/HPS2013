import cPickle
import math

class Moves:
  PLAYER_ONE = 1
  PLAYER_TWO = 2
  GRID_LENGTH = 0
  TOTAL_MOVES = 0

  __moves = None
  
  def __init__(self, grLength, totMoves):
    self.GRID_LENGTH = grLength
    self.TOTAL_MOVES = totMoves

    self.__moves = []

  def getMoves(self):
    return self.__moves
  
  def movesLeft(self):
    return self.TOTAL_MOVES - len(self.__moves) / 2
  
  def addMove(self, player, x, y):
      if player != self.PLAYER_ONE and player != self.PLAYER_TWO:
        raise Exception('Invalid player ' + str(player))
      if (x < 0 or x >= self.GRID_LENGTH or y < 0 or y >= self.GRID_LENGTH):
          raise Exception('Invalid coordinates ' + str(x) + ',' + str(y))
        
      self.__moves.append((player, x, y))

  def unplayMove(self):
    self.__moves.pop()
    
  def __distance(self, p1, p2):
    dist = math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
    return dist

  def __calcPull(self):
    oneScore = 0
    twoScore = 0
    onePull = 0.0
    twoPull = 0.0
    for x in range(0, self.GRID_LENGTH):
      for y in range(0, self.GRID_LENGTH):
        (onePull, twoPull) = self.__calcPullForPoint((x, y))

        # TODO: what to do if pull is equal for both colors?
        if onePull > twoPull:
          oneScore += 1
        elif onePull < twoPull:
          twoScore += 1

    return (oneScore, twoScore)

  def __calcPullForPoint(self, point):
    onePull = 0.0
    twoPull = 0.0
    for move in self.__moves:
      dist = self.__distance((move[1], move[2]), point)
      if dist != 0:
        pull = 1.0 / (dist * dist)
      else:
        pull = float('Inf')

      if move[0] == self.PLAYER_ONE:
        if pull == float('Inf'):
          onePull = pull
        else:
          onePull += pull
      else:
        if pull == float('Inf'):
          twoPull = pull
        else:
          twoPull += pull
            
    return (onePull, twoPull)
        
  def calcScore(self):
    return self.__calcPull()
  
  def isValidMove(self, x, y):
    for move in self.__moves:
      if (move[0] == x and move[1] == y):
        return False
    return True
  
if __name__ == '__main__':
  m = Moves(25, 5)
  m.addMove(1, 12, 12)
  m.addMove(2, 24, 24)
  print str(m.calcScore())
