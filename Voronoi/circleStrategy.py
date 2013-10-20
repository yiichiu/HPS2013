import random
import math

def playMove(state):
  points = getPointsOnCircle((500, 500), 260, state.boardSize)
  index = random.randint(0, len(points))

  return points[index]

def getPointsOnCircle(center, radius, boardSize):
  return [(x, y)
          for x in range(0, boardSize)
          for y in range(0, boardSize)
          if abs(getDistance(center, (x, y)) - radius) < 10]

def getDistance((x1, y1), (x2, y2)):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

if __name__ == '__main__':
  points = getPointsOnCircle((500, 500), 100, 1000)
  print(points)
