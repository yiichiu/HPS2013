class Tree:
  __edgeList = None
  __graph = None

  def __init__(self, graph):
    # Create Edge list
    edgeList = {}

    # Store the edge information of the minimum spanning tree in the edge list.
    for city in graph.cities:
      citiesInEdgeList = list(edgeList.keys())
      if citiesInEdgeList == []:
        cityList = {city:[]}
      else:
        # Get the closest neighbor of those cities already in the edge list. We will just get the
        # first index if there are ties.
        closestNeighbors = graph.getClosestNeighbors(city, citiesInEdgeList)
        cityList = {city:[closestNeighbors[0]]}

        # Update that closestNeighbors edge list
        edgeList[closestNeighbors[0]].append(city)

      edgeList.update(cityList)
    self.__edgeList = edgeList
    self.__graph = graph

  def getGreedyMatching(self, oddNodes):
    edgeList = dict(self.__edgeList)
    
    for city in oddNodes:
      cities = [c for c in oddNodes if c not in edgeList[city]]
      closestNeighbors = self.__graph.getClosestNeighbors(city, cities)
      partnerCity = closestNeighbors[0]

      oddNodes.remove(city)
      oddNodes.remove(partnerCity)

      edgeList[city] = edgeList[city] + [partnerCity]
      edgeList[partnerCity] = edgeList[partnerCity] + [city]
    return edgeList

  def getChristophidesPath(self):
    # Get greedy matching of odd nodes. Perfect was too hard. Greedy seems not to work.
    oddNodes = [i for i in self.__edgeList if len(self.__edgeList[i]) % 2 == 1]
    edgeList = self.getGreedyMatching(oddNodes)

    # Walk the path with shortcutting.
    #edgeList = self.__edgeList
    citiesToVisit = set(edgeList.keys())
    path = [];
    cityStack = [];

    while len(citiesToVisit) != 0:
      if len(path) == 0:
        city = citiesToVisit.pop()
        path.append(city)
        cityStack.append(city)

      # Get the list of neighbors for the last city on the stack.
      neighbors = edgeList[cityStack[-1]]
      neighborsNotInPath = [n for n in neighbors if n not in path]
      while len(neighborsNotInPath) == 0:
        cityStack.pop()
        neighbors = edgeList[cityStack[-1]]
        neighborsNotInPath = [n for n in neighbors if n not in path]

      # Add the next unvisited city to the path.
      nextCity = neighborsNotInPath[0]
      path.append(nextCity)
      cityStack.append(nextCity)
      citiesToVisit.remove(nextCity)
    return path
  
if __name__ == '__main__':
  import sys
  import time
  import graph
  start = time.clock()

  mapPath = str(sys.argv[1])
  rawMap = graph.getRawMap(mapPath)
  thisGraph = graph.Graph(rawMap)

  # Calculate path based on Christophides Algorithm.
  thisTree = Tree(thisGraph)
  path = thisTree.getChristophidesPath()

  # Return score for path.
  score = thisGraph.getScore(path)

  print("Score: " + str(score))
  print("Total Exectuion Time: " + str(time.clock() - start))
