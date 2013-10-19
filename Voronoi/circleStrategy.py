import math

class CircleStrategy:

  def __init__(self):
    pass

def parseMoves(moves):
  moves = moves.replace('(', '')
  moves = set(
              [tuple(
                     [int(value) for value in move.split(',')
                     if value != '']
                    )
               for move in moves.split(')')
               if move != '']
             )
  return moves

def getScore(moves, playerNumber):
  playerOneMoves = [(x, y)
                    for (playerNum, x, y)
                    in moves if playerNum == playerNumber]
  [(x, y) for x in range(0, 1000) for y in range(0, 1000)]
  print(playerOneMoves)

def getDistance(distance1, distnace2):
  (x1, y1) = distance1
  (x2, y2) = distance2
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

if __name__ == '__main__':
  import sys

  #moves = sys.argv[1]
  moves = '(1,32,53),(2,542,352)'
  moves = parseMoves(moves)

  score = getScore(moves, 1)

  player = CircleStrategy()
      
