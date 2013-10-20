import random
import math
import copy
from FastMoves import FastMoves

def playMove(state):
  points = getPointsOnCircle((500, 500), 260, state.boardSize)

  #moves = populateMoves(state)
  #bestMove = -1
  #bestScore = -1
  #print('Points to process: ' + str(len(points)))
  #for point in points:
  #  print('Processing: ' + str(point))
  #  tempMoves = copy.deepcopy(moves)
  #  tempMoves.addMove(state.playerId, point[0], point[1])
  #  score = moves.score
  #  if score > bestScore:
  #    bestScore = score
  #    bestMove = point
  index = random.randint(0,len(points)-1)
  bestMove = points[index]
  return bestMove

def populateMoves(state):
  opponentId = 1 if state.playerId == 2 else 2
  playerMoves = state.moves[state.playerId]
  opponentMoves = state.moves[opponentId]

  moves = FastMoves(state.boardSize, state.numberOfStones)
  addMoves(moves, playerMoves, state.playerId)
  addMoves(moves, opponentMoves, opponentId)
  return moves

def addMoves(moves, playerMoves, playerId):
  for move in playerMoves:
    moves.addMove(playerId, move[0], move[1])

def getPointsOnCircle(center, radius, boardSize):
  return [(x, y)
          for x in range(0, boardSize)
          for y in range(0, boardSize)
          if abs(getDistance(center, (x, y)) - radius) == 0]

def getDistance((x1, y1), (x2, y2)):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def calibrateRadis():
  pass

if __name__ == '__main__':
  points = getPointsOnCircle((500, 500), 100, 1000)
  print(points)
