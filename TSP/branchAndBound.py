import copy
import tree

class BranchAndBound:
  __boundStorage = dict()
  __graph = None
  path = None

  def __init__(self, graph, bestPath = None, minKnownValue = float('Inf')):
    self.__graph = graph

    cities = set(graph.cities)
    startCity = (cities.pop(),)

    # Generate Branches
    branches = {startCity:self.getLowerBound(startCity)}
    scores = list(branches.values())
    minScore = min(scores)
    while minScore < minKnownValue:
      # Get minimum valued branch
      minScoreIndex = scores.index(minScore)
      branchList = list(branches.keys())
      minBranch = branchList[minScoreIndex]

      # Try new branch
      newCities = cities - set(minBranch)
      while True:
        if len(minBranch) == len(cities) - 1:
          newCities = tuple(newCities)

          # Add first permutation
          newBranch = minBranch + newCities
          newBranchValue = graph.getScore(list(newBranch))
          if newBranchValue < minKnownValue:
            minKnownValue = newBranchValue
          branchSet = {newBranch:float('Inf')}
          branches.update(branchSet)

          ## Add second permutation
          newBranch = minBranch + newCities[::-1]
          newBranchValue = graph.getScore(list(newBranch))
          if newBranchValue < minKnownValue:
            minKnownValue = newBranchValue
          branchSet = {newBranch:float('Inf')}
          branches.update(branchSet)

          # Eliminate the parent branch from consideration.
          branches[minBranch] = float('Inf')
          break
        else:
          newBranch = minBranch + (newCities.pop(),)

        if newBranch not in branchList:
          branchSet = {newBranch:self.getLowerBound(newBranch)}
          branches.update(branchSet)
          break
        elif newCities == set():
          branches[minBranch] = float('Inf')
          break
      scores = list(branches.values())
      minScore = min(scores)
    self.path = list(bestPath)

  def getLowerBound(self, prefix):
    cities = self.__graph.cities

    # Calculate prefix path score. For the last city we can get the minimum distance against the
    # remaining cities.
    lastPrefixCity = prefix[-1]
    
    pathLength = 0
    for i in range(0, len(prefix) - 1):
      fromCity = prefix[i]
      toCity = prefix[i + 1]
      pathLength = pathLength + self.__graph.getDistance(fromCity, toCity)

    # Get the list of cities ex the prefix and add the last prefix city
    citiesExPrefix = tuple(c for c in cities if c not in prefix or c == lastPrefixCity)

    # Get bound for non-prefix path score
    exPrefixBound = self.__boundStorage.get(citiesExPrefix) 
    if exPrefixBound is None:
      exPrefixBound = 0
      for i in range(0, len(citiesExPrefix)):
         city = citiesExPrefix[i]
         (closestNeighbors, minimalDistance) = self.__graph.getClosestNeighbors(city, citiesExPrefix)
         partner = closestNeighbors[0]
         if city != partner:
           exPrefixBound = exPrefixBound + minimalDistance
      self.__boundStorage[citiesExPrefix] = exPrefixBound
    bound = pathLength + exPrefixBound
    return bound

if __name__ == '__main__':
  import sys
  import time
  import graph
  import tree
  start = time.clock()

  mapPath = str(sys.argv[1])
  rawMap = graph.getRawMap(mapPath)

  thisGraph = graph.Graph(rawMap);

  # Calculate path based on Christophides Algorithm.
  thisTree = tree.Tree(thisGraph)
  path = thisTree.getChristophidesPath()

  # Return score for path.
  score = thisGraph.getScore(path)
  print("Score: " + str(score))

  # Branch and Bound
  # There seems to be a bug here!
  branchAndBound = BranchAndBound(thisGraph, path, score)
  bestPath = branchAndBound.path
  score = thisGraph.getScore(bestPath)

  print("Score: " + str(score))
  print("Total Exectuion Time: " + str(time.clock() - start))
