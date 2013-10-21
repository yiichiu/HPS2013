import cPickle
import math
from parakeet import jit

class FastMoves:
  PLAYER_ONE = 1
  PLAYER_TWO = 2
  GRID_LENGTH = 0
  TOTAL_MOVES = 0

  moves = None
  
  def __init__(self, grLength, totMoves):
    self.GRID_LENGTH = grLength
    self.TOTAL_MOVES = totMoves

    self.moves = []
    self.grid = [[(0, 0) for x in range(0, 1000)] for x in range(0, 1000)]
    self.score = (0, 0)

  @jit
  def addMove(self, player, x, y):
    if player != self.PLAYER_ONE and player != self.PLAYER_TWO:
      raise Exception('Invalid player ' + str(player))
    if (x < 0 or x >= self.GRID_LENGTH or y < 0 or y >= self.GRID_LENGTH):
      raise Exception('Invalid coordinates ' + str(x) + ',' + str(y))
      
    self.moves.append((player, x, y))

    # Append to grid
    oneScore = 0
    twoScore = 0
    onePull = 0.0
    twoPull = 0.0
    for x in range(0, self.GRID_LENGTH):
      for y in range(0, self.GRID_LENGTH):
        (onePull, twoPull) = self.__calcPullForPoint((x, y))
        (oldOnePull, oldTwoPull) = self.grid[x][y]
        (onePull, twoPull) = (oldOnePull+onePull, oldTwoPull+twoPull)
        self.grid[x][y] = (onePull, twoPull)

        if onePull > twoPull:
          oneScore += 1
        elif onePull < twoPull:
          twoScore += 1
    self.score = (oneScore, twoScore)

  @jit
  def __distance(self, p1, p2):
    dist = math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
    return dist

  @jit
  def __calcPullForPoint(self, point):
    onePull = 0.0
    twoPull = 0.0
    move = self.moves[-1]

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
        
if __name__ == '__main__':
  move = FastMoves(25, 5)
  move.addMove(1, 12, 12)
  move.addMove(2, 24, 24)
  print(move.score)
