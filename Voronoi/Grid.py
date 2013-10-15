import cPickle
import math

class Grid:
  RED = 1
  BLUE = 2
  GRID_LENGTH = 25
  
  __grid = None
  __moves = None
  
  def __init__(self, gridLength, moves):
    self.GRID_LENGTH = gridLength
    self.__grid = []
    self.__moves = moves
    for i in range (0, self.GRID_LENGTH):
      self.__grid.append([])
      for j in range (0, self.GRID_LENGTH):
        self.__grid[i].append(0)

  def __distance(self, p1, p2):
    dist = math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
    return dist

  def __calcPull(self):
    for y in range(0, self.GRID_LENGTH):
      for x in range(0, self.GRID_LENGTH):
        self.__calcPullForPoint((x, y))

  def __calcPullForColor(self, color, point):
    pull = 0.0
    for move in self.__moves:
      if move[0] == color:
        dist = self.__distance((move[1], move[2]), point)
        #print 'distance is ' + str(dist)
        if dist != 0:
          pull = pull + 1.0 / (dist * dist)
          #print 'pulltmp = ' + str(pullTmp) + ' pull is ' + str(pull)
        else:
          pull = float('Inf')

    #print 'pull for color ' + str(color) + ' is ' + str(pull)
    return pull
        
  def __calcPullForPoint(self, point):
    redPull = self.__calcPullForColor(self.RED, point)
    #raw_input (str(redPull) + ' ' + str(point))
    bluePull = self.__calcPullForColor(self.BLUE, point)

    # TODO: what to do if pull is equal for both colors?
    if redPull > bluePull:
      self.__grid[point[0]][point[1]] = self.RED
    elif bluePull > redPull:
      self.__grid[point[0]][point[1]] = self.BLUE

  def calcGrid(self):
    self.__calcPull()

  def getGrid(self):
    return self.__grid

  def __getStoneAtLocation(self, x, y):
    for move in self.__moves:
      if move[1] == x and move[2] == y:
        if move[0] == self.RED:
          return 'R'
        elif move[0] == self.BLUE:
          return 'B'

    return ''
  
  def printGrid(self):
    self.calcGrid()
    strtmp = ''
    stone = ''
    for y in range(0, self.GRID_LENGTH):
      strtmp = ''
      for x in range(0, self.GRID_LENGTH):
        stone = self.__getStoneAtLocation(x, y)
        if stone == '':
          strtmp = strtmp + str(self.__grid[x][y])
        else:
          strtmp = strtmp + stone
      print strtmp

  def saveGridToFile(self):
    output = open('grid.p', 'wb')
    cPickle.dump(self.__grid, output, -1)
    output.close()
    
if __name__ == '__main__':
    g = Grid()
    g.addMove(Grid.RED, 0, 0)
    g.addMove(Grid.BLUE, Grid.GRID_LENGTH/2, Grid.GRID_LENGTH/2)
    g.addMove(Grid.RED, Grid.GRID_LENGTH-1, 0)
    #g.addMove(Grid.BLUE, 6, 7)
    g.calcGrid()
    g.printGrid()
    g.saveGridToFile()
