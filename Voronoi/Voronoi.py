import Moves
import random
import Algorithm
    
class Voronoi:
  TOTAL_MOVES = 20
  GRID_LENGTH = 25
  PLAYER_ONE = 1
  PLAYER_TWO = 2
  __moves = None
  
  def __init__(self):
    self.__moves = Moves.Moves(self.GRID_LENGTH, self.TOTAL_MOVES)

  def __colorForPlayer(self, player):
    # player number corresponds to color number (red, blue)
    return player
  
  def __playIteration(self, player, moves_left):
    # pick coordinates to play
    x = 0
    y = 0
    movesToPlay = []
    while (len(movesToPlay) < 3):
      x = random.randint(0, self.GRID_LENGTH - 1)
      y = random.randint(0, self.GRID_LENGTH - 1)
      if self.__grid.isValidMove(x, y):
        movesToPlay.append((x, y))

    for (x, y) in movesToPlay:
      self.__grid.addMove(self.__colorForPlayer(player), x, y)
      scores = self.__grid.calcGrid()
      print 'Player = ' + str(player) + ' move = ' + str(self.TOTAL_MOVES - moves_left) \
            + ' score = ' + str(scores)
      #raw_input('enter to continue')
    
      if (moves_left <= 0 and player == self.PLAYER_TWO):
        # calculate best score
        a = 1 + 1
      else:
        if (player == self.PLAYER_TWO):
          self.__playIteration(self.__otherPlayer(player), moves_left - 1)
        else:
          self.__playIteration(self.__otherPlayer(player), moves_left)

      self.__grid.unplayMove()
    
  def playGame(self):
    scores = ()
    r1 = Algorithm.RandomAlgorithmLookAhead(self.PLAYER_ONE)
    r2 = Algorithm.RandomAlgorithmImp(self.PLAYER_TWO)
    
    for i in range(0, self.TOTAL_MOVES):
      r1.playMove(self.__moves)
      r2.playMove(self.__moves)

      scores = self.__moves.calcScore()
      print str(scores)
      print str(self.__moves.getMoves())

    if (scores[0] > scores[1]):
      print 'the winner is player 1'
    elif (scores[0] < scores[1]):
      print 'the winner is player 2'
    else:
      print 'it''s a tie!'


if __name__ == '__main__':
  v = Voronoi()
  v.playGame()
