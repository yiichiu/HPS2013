import random
import math
import copy
import itertools
import subprocess
from operator import itemgetter

def playMove(state):
  alreadyPlayedMoves = list(itertools.chain.from_iterable(state.moves))
  if state.playerId == 1 and state.moves[1] == []:
    (x, y) = (500, 750)
  elif state.timeLeft > 20 or len(state.moves[2]) == state.numberOfStones - 1:
    points = getPointsOnCircle((500, 500), 400, state.boardSize, alreadyPlayedMoves)
    innerPoints = getPointsOnCircle((500, 500), 150, state.boardSize, alreadyPlayedMoves)
    innerPoints2 = getPointsOnCircle((500, 500), 50, state.boardSize, alreadyPlayedMoves)
    points = innerPoints + innerPoints2 + points
    nextMoves = getBestMove(state.moves, points, state.playerId, state.numberOfStones)
    (x, y) = max(nextMoves, key = itemgetter(state.playerId+1))[0:2]
  elif state.timeLeft > 10:
    if state.playerId == 1:
      opponentMoves = state.moves[2]
    else:
      opponentMoves = state.moves[1]
    move = [getPointsOnCircle(move, 1, state.boardSize)
            for move in opponentMoves]
    points = list(itertools.chain(*move))
    nextMoves = getBestMove(state.moves, points, state.playerId, state.numberOfStones)
    (x, y) = max(nextMoves, key = itemgetter(state.playerId+1))[0:2]
  else:
    points = getPointsOnCircle((500, 500), 400, state.boardSize, alreadyPlayedMoves)
    index = random.randint(0, len(points)-1)
    (x, y) = points[index]
  return (x, y)

def getBestMove(previousMoves, points, playerId, numberOfStones):
  points = str(points)
  points = points.replace('(', '')
  points = points.replace(')', '')
  points = points.replace(' ', '')
  points = points.replace(']', '')
  points = points.replace('[', '')

  points = points + '\n' + str(playerId) + ',' + str(numberOfStones)

  playerOneMoves = str(previousMoves[1])
  playerOneMoves = playerOneMoves.replace('(', '1,')
  playerOneMoves = playerOneMoves.replace(')', '')
  playerOneMoves = playerOneMoves.replace('[', '')
  playerOneMoves = playerOneMoves.replace(']', '')
  playerOneMoves = playerOneMoves.replace(' ', '')
  if playerOneMoves != '':
    playerOneMoves = ',' + playerOneMoves
    
  playerTwoMoves = str(previousMoves[2])
  playerTwoMoves = playerTwoMoves.replace('(', '2,')
  playerTwoMoves = playerTwoMoves.replace(')', '')
  playerTwoMoves = playerTwoMoves.replace('[', '')
  playerTwoMoves = playerTwoMoves.replace(']', '')
  playerTwoMoves = playerTwoMoves.replace(' ', '')
  if playerTwoMoves != '':
    playerTwoMoves = ',' + playerTwoMoves

  input_ = points + playerOneMoves + playerTwoMoves
  p = subprocess.Popen(["./Voronoi"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  output = p.communicate(input_)[0]
  output = [int(x) for x in output.split(',')]
  output = zip(output, output[1:], output[2:], output[3:])[::4]
  return output

def getPointsOnCircle(center, radius, boardSize, excludeMoves = []):
  return [(x, y)
          for x in range(0, boardSize)
          for y in range(0, boardSize)
          if abs(getDistance(center, (x, y)) - radius) == 0
          if (x,y) not in excludeMoves]

def getDistance((x1, y1), (x2, y2)):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def calibrateRadis():
  pass

if __name__ == '__main__':
  points = getPointsOnCircle((500, 500), 100, 1000)
  print(points)
