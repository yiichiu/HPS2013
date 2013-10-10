
class Grid:
  RED = 1
  BLUE = 2

  __grid = None
  __moves = None
  
  def __init__(self):
    self.__grid = []
    self.__moves = []
    for i in range (0, 1000):
      self.__grid.append([])
      for j in range (0, 1000):
        self.__grid[i].append(0)

  def addMove(self, color, x, y):
      if color != self.RED and color != self.BLUE:
        raise Exception('Invalid color ' + str(color))
      if (x < 1 or x > 1000 or y < 1 or y > 1000):
          raise Exception('Invalid coordinates ' + str(x) + ',' + str(y))
        
      self.__moves.append((color, x, y))


  def __distance(self, p1, p2):
    dist = pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2)
    return dist

  def __calcPull(self):
    for y in range(0, 1000):
      for x in range(0, 1000):
        self.__calcPullForPoint((x+1, y+1))

  def __calcPullForColor(self, color, point):
    pull = 0.0
    for move in self.__moves:
      if move[0] == color:
        dist = self.__distance((move[1], move[2]), point)
        if dist != 0:
          pull = pull + (1 / (dist * dist))
        
    return pull
        
  def __calcPullForPoint(self, point):
    redPull = self.__calcPullForColor(self.RED, point)
    bluePull = self.__calcPullForColor(self.BLUE, point)

    # TODO: what to do if pull is equal for both colors?
    if redPull > bluePull:
      self.__grid[point[0]][point[1]] = self.RED
    elif bluePull > redPull:
      self.__grid[point[0]][point[1]] = self.BLUE

  def calcGrid(self):
    self.__calcPull()
    
if __name__ == '__main__':
    g = Grid()
    g.addMove(Grid.RED, 5, 10)
    g.calcGrid()
