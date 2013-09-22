import math

class Graph:
  __distanceMatrix = None
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

    # Initialize a distance Matrix [from][to].
    self.__distanceMatrix = [[float('Inf') for _ in range(numberOfCities)] for _ in
        range(numberOfCities)]

    # Populate distance matrix.
    for i in range(0, numberOfCities):
      for j in range(i + 1, numberOfCities):
        self.__distanceMatrix[i][j] = self.__getDistance(i, j, coordinates)

  def __getDistance(self, a, b, coordinates):
    a_x = coordinates[a][0]
    a_y = coordinates[a][1]
    a_z = coordinates[a][2]

    b_x = coordinates[b][0]
    b_y = coordinates[b][1]
    b_z = coordinates[b][2]

    distance = math.sqrt(pow(a_x - b_x, 2) + pow(a_y - b_y, 2) + pow(a_z - b_z, 2))
    return distance

  def __getDistanceMatrixCoordinates(self, a):
    # Align city name to index in internal city list.
    # a = self.cities.index(a)
    a = a - 1
    return a

  def getDistance(self, a, b):
    a = self.__getDistanceMatrixCoordinates(a)
    b = self.__getDistanceMatrixCoordinates(b)

    # To save time we only calculate the upper triangle of the distance matrix. However since the
    # distance matrix is symetric, we can just get the distance by reversing the inputs.
    distance = self.__distanceMatrix[a][b]
    if a != b and distance == float('Inf'):
      distance = self.__distanceMatrix[b][a]
    if a != b and distance == float('Inf'):
      raise Exception("Distance is Inf between two distinct cities")
    return distance

  def getClosestNeighbors(self, a, neighborSet = None):
    if neighborSet is None:
      neighborSet = self.cities

    neighborDistances = [self.getDistance(a, b) for b in neighborSet]
    minimalDistance = min(neighborDistances)

    closestNeighbors = [neighborSet[i] for i, d in enumerate(neighborDistances) if d == minimalDistance]
    return closestNeighbors

  def getScore(self, solution):
    score = 0
    for i in range(0, len(solution) - 1):
      fromCity = solution[i]
      toCity = solution[i + 1]
      score = score + self.getDistance(fromCity, toCity)
    return score

def generateStringPath(path):
  # Convert path to string format.
   path = str(path)
   path = path[1:-1].replace(',', '') + ';'
   return path

def getRawMap(mapPath):
  with open(mapPath, 'r') as mapFile:
    rawMap = mapFile.read()
  return rawMap

if __name__ == '__main__':
  import sys
  import time
  import tree
  start = time.clock()

  mapPath = str(sys.argv[1])
  rawMap = getRawMap(mapPath)

  thisGraph = Graph(rawMap);

  # Calculate path based on Christophides Algorithm.
  thisTree = tree.Tree(thisGraph)
  path = thisTree.getChristophidesPath()

  # Return score for path.
  score = thisGraph.getScore(path)

  print("Score: " + str(score))
  print("Total Exectuion Time: " + str(time.clock() - start))
