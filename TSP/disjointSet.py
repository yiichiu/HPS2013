class DisjointSet:
  __rank = dict()
  __parent = dict()

  def __init__(self):
    pass
  
  def makeSet(self, x):
    self.__rank.update({x:0})
    self.__parent.update({x:x})

  def union(self, x, y):
    xRoot = self.find(x)
    yRoot = self.find(y)
    if xRoot == yRoot:
      return

    xRootRank = self.__rank[xRoot]
    yRootRank = self.__rank[yRoot]

    if xRootRank < yRootRank:
      self.__parent.update({xRoot:yRoot})
    elif xRootRank > yRootRank:
      self.__parent.update({yRoot:xRoot})
    else:
      self.__parent.update({yRoot:xRoot})
      self.__rank.update({xRoot:xRootRank + 1})

  def find(self, x):
    parent = self.__parent[x]
    if x != parent:
      parent = self.find(parent)
    return parent

if __name__ == '__main__':
  thisSet = DisjointSet()
  thisSet.makeSet(1)
  thisSet.makeSet(2)
  thisSet.union(1, 2)
  parent1 = thisSet.find(1)
  parent2 = thisSet.find(2)
  print(parent1)
  print(parent2)
