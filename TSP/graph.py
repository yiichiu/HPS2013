import math
import copy
import threading

class Graph:
  edges = dict()
  cities = None

  def __init__(self, rawMap):
    # Initialize a coordinate map. Assume that each city's data is seperated by a carriage return,
    # that the first value is the city name, and that the following numbers represent the city's
    # coordinates. We will make the assumption that there are three coordinate values.
    numberOfCities = rawMap.count('\n') + 1
    self.cities = [None for _ in range(numberOfCities)]
    coordinates = [[float('Inf') for _ in range(3)] for _ in range(numberOfCities)]

    # Populate the distance matrix.
    # Clean out ';' from the last line
    (rawMap, _, _) = rawMap.partition(';')

    for i in range(0, numberOfCities):
      # Each new line is a city's worth of data.
      (cityData, _, rawMap) = rawMap.partition('\n')

      # Each line contains (cityName, x, y, z).
      (cityName, _, cityData) = cityData.partition(' ')
      (x, _, cityData) = cityData.partition(' ')
      (y, _, cityData) = cityData.partition(' ')
      (z, _, cityData) = cityData.partition(' ')

      if self.cities.count(cityName) != 0:
        raise Exception("Data for this city already exits: Duplicate City!")

      self.cities[i] = int(cityName)

      coordinates[i][0] = int(x)
      coordinates[i][1] = int(y)
      coordinates[i][2] = int(z)

    # Populate Edges
    for i in range(0, numberOfCities):
      for j in range(i + 1, numberOfCities):
        a = self.cities[i]
        b = self.cities[j]
        self.edges.update({(a,b):self.__getDistance(i, j, coordinates)})

  def __getDistance(self, a, b, coordinates):
    a_x = coordinates[a][0]
    a_y = coordinates[a][1]
    a_z = coordinates[a][2]

    b_x = coordinates[b][0]
    b_y = coordinates[b][1]
    b_z = coordinates[b][2]

    distance = math.sqrt(pow(a_x - b_x, 2) + pow(a_y - b_y, 2) + pow(a_z - b_z, 2))
    return distance

  def getDistance(self, a, b):
    # To save time we only calculate the upper triangle of the distance matrix. However since the
    # distance matrix is symetric, we can just get the distance by reversing the inputs.
    if a < b: 
      distance = self.edges[(a,b)]
    elif a > b:
      distance = self.edges[(b,a)]
    else:
      distance = float('Inf')
    return distance

  def getLongestEdge(self, path):
    path = path + [path[0]]

    longestEdge = None
    maxDistance = 0
    for i in range(0, len(path) - 1):
      a = path[i]
      b = path[i + 1]
      distance = self.getDistance(a, b)
      if distance > maxDistance:
        maxDistance = distance
        longestEdge = [a, b]
    return (longestEdge, maxDistance)

  def getClosestNeighbors(self, a, neighborSet = None):
    if neighborSet is None:
      neighborSet = self.cities

    neighborDistances = [self.getDistance(a, b) for b in neighborSet]
    minimalDistance = min(neighborDistances)

    closestNeighbors = [neighborSet[i] for i, d in enumerate(neighborDistances) if d == minimalDistance]
    return (closestNeighbors, minimalDistance)

  def getScore(self, solution):
    score = 0
    for i in range(0, len(solution) - 1):
      fromCity = solution[i]
      toCity = solution[i + 1]
      score = score + self.getDistance(fromCity, toCity)
    return score

  def randomSwap(self, path):
    score = self.getScore(path)
    while True:
      stayInLoop = False
      for i in range(0, len(path) - 1):
        for j in range(i + 1, len(path)):
          tempPath = copy.deepcopy(path)
          tempPath[i], tempPath[j] = tempPath[j], tempPath[i]
          newScore = self.getScore(tempPath)
          if score > newScore:
            score = newScore
            path = tempPath
            stayInLoop = True
    return path

  def getBestNeighborWalkThreading(self):
    q = Queue.Queue()
    for i in range(0, len(self.cities), 100):
      j = i + 1
      if j > len(self.cities):
        j = len(self.cities)
      t = threading.Thread(target = self.getBestNeighborWalk, args = (i, j, q))
      t.daemon = True
      t.start()
    bestPath = None
    bestScore = float('Inf')
    for i in range(0, 10):
      (path, score) = q.get(True)
      if score < bestScore:
        bestPath = path
    return bestPath

  def getBestNeighborWalk(self, i = 0, j = None, q = None):
    if j == None:
      len(self.cities)
    bestScore = float('Inf')
    bestPath = None
    for i in range(i, j):
      startingPoint = self.cities[i]
      (path, score) = self.nearestNeighborWalk(startingPoint, bestScore)
      if score < bestScore:
        bestScore = score
        bestPath = path
    result = (bestPath, bestScore)
    if q == None:
      return result
    else:
      q.put(result)


  def nearestNeighborWalk(self, startingPoint, scoreToBeat = float('Inf')):
    path = [startingPoint]
    score = 0
    while len(path) < len(self.cities):
      city = path[-1]
      universe = [i for i in self.cities if i not in path]
      (nearestNeighbors, distance) = self.getClosestNeighbors(city, universe)
      path.append(nearestNeighbors[0])
      score = score + distance
      if score > scoreToBeat:
        return (path, float('Inf'))
    return (path, score)

def generateStringPath(path):
  # Convert path to string format.
   path = str(path)
   path = path[1:-1].replace(',', '') + ';'
   return path

def getRawMap(mapPath):
  with open(mapPath, 'r') as mapFile:
    rawMap = mapFile.read()

  # If last character is a carriage line, remove it.
  if rawMap[-1] == '\n':
    rawMap = rawMap[0:-1]

  return rawMap

if __name__ == '__main__':
  import sys
  import time
  import tree
  start = time.clock()
  mapPath = str(sys.argv[1])
  rawMap = getRawMap(mapPath)

  thisGraph = Graph(rawMap)

  # Calculate path based on Christophides Algorithm.
  thisTree = tree.Tree(thisGraph)
  path = thisTree.getChristophidesPath()
  #path = thisGraph.randomSwap(path)
  (nearestWalk, nearestWalkScore) = thisGraph.getBestNeighborWalk(1, 4)

  # Return score for path.
  score = thisGraph.getScore(path)

  print("Neares walk score: " + str(nearestWalkScore))
  print("Score: " + str(score))
  print("Total Exectuion Time: " + str(time.clock() - start))
