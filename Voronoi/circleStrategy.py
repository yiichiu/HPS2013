import random
import math
import copy
import itertools

def playMove(state):
  alreadyPlayedMoves = list(itertools.chain.from_iterable(state.moves))
  points = getPointsOnCircle((500, 500), 400, state.boardSize, alreadyPlayedMoves)
  innerPoints = getPointsOnCircle((500, 500), 150, state.boardSize, alreadyPlayedMoves)
  points = innerPoints + points
  (x, y) = getBestMove(state.moves, points)
  return (x, y)

def getBestMove(previousMoves, points):
  
  tmp='400,500,404,472,404,528,420,440\n1,1,0,0,2,500,500'
  p = subprocess.Popen([".\Voronoi.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  output = p.communicate(tmp)[0]
  return output

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

def getPointsOnCircle(center, radius, boardSize, excludeMoves = []):
  return [(x, y)
          for x in range(0, boardSize)
          for y in range(0, boardSize)
          if abs(getDistance(center, (x, y)) - radius) <= 0
          if (x,y) not in excludeMoves]

def getDistance((x1, y1), (x2, y2)):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def calibrateRadis():
  pass

if __name__ == '__main__':
  points = getPointsOnCircle((500, 500), 100, 1000)
  print(points)
