import copy
import disjointSet
import operator

class Tree:
  __edgeList = dict()
  mstLength = 0
  __graph = None

  def __init__(self, graph):
    self.__graph = graph
    thisSet = disjointSet.DisjointSet()

    # Kurskal's MST
    for city in graph.cities:
      thisSet.makeSet(city)

    sortedWeights = sorted(graph.edges.items(), key = operator.itemgetter(1))
    for ((thisEdge, thatEdge), weight) in sortedWeights:
      if thisSet.find(thisEdge) != thisSet.find(thatEdge):
        # Add to EdgeList
        self.__addEdge(thisEdge, thatEdge)
        thisSet.union(thisEdge, thatEdge)
        self.mstLength = self.mstLength + weight

  def __addEdge(self, thisEdge, thatEdge):
    self.__addArc(thisEdge, thatEdge)
    self.__addArc(thatEdge, thisEdge)

  def __addArc(self, thisEdge, thatEdge):
    thisEdgeList = copy.deepcopy(self.__edgeList.get(thisEdge))
    if thisEdgeList is None:
      edgeList = {thatEdge}
    else:
      edgeList = thisEdgeList.union({thatEdge})
    self.__edgeList.update({thisEdge:edgeList})

  def getGreedyMatching(self, oddNodes):
    edgeList = copy.deepcopy(self.__edgeList)
    
    for city in oddNodes:
      cities = [c for c in oddNodes if c not in edgeList[city]]
      (closestNeighbors, _) = self.__graph.getClosestNeighbors(city, cities)
      partnerCity = closestNeighbors[0]

      oddNodes.remove(city)
      oddNodes.remove(partnerCity)

      edgeList[city] = edgeList[city].union({partnerCity})
      edgeList[partnerCity] = edgeList[partnerCity].union({city})
    return edgeList

  def getChristophidesPath(self):
    # Get greedy matching of odd nodes. Perfect was too hard. Greedy seems not to work/ Gives worse
    # path.
    #oddNodes = [i for i in self.__edgeList if len(self.__edgeList[i]) % 2 == 1]
    #edgeList = self.getGreedyMatching(oddNodes)

    # Walk the path with shortcutting.
    edgeList = self.__edgeList
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

    # Add start and remove longest edge
    longestEdge = self.__graph.getLongestEdge(path)
    path = reorderPath(path, longestEdge[0])
    return path

def reorderPath(path, edge):
  index1 = path.index(edge[0])
  index2 = path.index(edge[1])
  path = tuple(path)
  part1 = path[0:index1 + 1]
  part2 = path[index2:]
  path = list(part2 + part1)
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

  print("MST Length: " + str(thisTree.mstLength))
  print("Score: " + str(score))
  print("Total Exectuion Time: " + str(time.clock() - start))
