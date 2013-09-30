import board
import player

class Simulate:
  BOARD_OUTPUT = 'board.txt'
  __board = None
  __isFirstMove = None
  __enteredRemovalStage = None
  currentPlayer = None
  currentMode = None

  def __init__(self):
    self.__board = board.Board()
    self.__isFirstMove = True
    self.__enteredRemovalStage = False
    self.drawBoard()
    self.currentPlayer = 1
    self.currentMode = 1

  def drawBoard(self):
    boardEnd = int(self.__board.BOARD_LENGTH/2)
    locations = tuple(range(0-boardEnd, boardEnd + 1))
    playerOneMoves = self.__board.playerOneMoves
    playerTwoMoves = self.__board.playerTwoMoves
    with open(self.BOARD_OUTPUT, 'w') as file_:
      for index, location in enumerate(locations):
        if playerOneMoves[index] != 0:
          player = '1'
        elif playerTwoMoves[index] != 0:
          player = '2'
        else:
          player = '0'
        weight = str(self.__board.getWeightAtLocation(location))
        location = str(location)
        file_.write(location + ' ' + weight + ' ' + player + '\n')

  def updateBoard(self, location, weight):
    mode = self.currentMode
    currentPlayer = str(self.currentPlayer)

    if mode == 1:
      self.__board.addWeight(location, weight, self.currentPlayer)
    elif mode == 2:
      self.__board.removeWeight(location, weight)
    else:
      raise(Exception('Invalid mode'))

    # Delete the correct amount of lines
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2k'
    if self.__isFirstMove:
      self.__isFirstMove = False
    elif self.__enteredRemovalStage:
      print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
      print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
      print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
      print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    else:
      print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
      print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
      print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)

    # Display what happened
    torque = self.__board.getTorque()

    if mode == 1:
      if self.__board.checkIfTipped():
        print('The board has tipped adding weight: ' + str(weight) + 
              ' at location: ' + str(location) + ' resulting in torque: ' + str(torque))
        print('Player ' + currentPlayer + ' lost!' +
              '                                   ')
        self.drawBoard()
        return
      else:
        print('Player: ' + currentPlayer + ' Added weight: ' + str(weight) +
              ' at location: ' + str(location) + 
              ' resulting in torque: ' + str(torque) + '                                          ')
    else:
      if self.__board.checkIfTipped():
       print('The board has tipped removing weight: ' + str(weight) + 
             ' at location: ' + str(location) + ' resulting in torque: ' + str(torque))
       print('Player ' + currentPlayer + ' lost!' + 
             '                                  ')
       self.drawBoard()
       return
      else:
        print('Player: ' + currentPlayer + ' Removed weight: ' + str(weight) +
              ' at location: ' + str(location) + 
              ' resulting in torque: ' + str(torque) + '                                          ')

    # Display some information to help decide how to play
    self.__board.printBoard()
    if mode == 1:
      if self.currentPlayer == 1:
        opposingPlayer = '2'
        remainingWeights = self.__board.playerTwoWeights
      else:
        opposingPlayer = '1'
        remainingWeights = self.__board.playerOneWeights
      print('Player ' + opposingPlayer + ' has weights: ' + str(remainingWeights) +
            '                                                          ')
    else:
      print('Weights placed by player 1 remaining: ' + 
            '                                                          ')
      print(str(self.__board.playerOneMoves))

    # Update mode to remove if there are no more weights for player one
    if self.currentMode == 1 and self.__board.playerOneWeights == set():
      print('Entering Removal Stage')
      self.__enteredRemovalStage = True
      self.currentMode = 2

    # Mark the proper player
    if self.currentPlayer == 1:
      self.currentPlayer = 2
    elif self.currentPlayer == 2:
      self.currentPlayer = 1
    else:
      raise(Exception('Invalid Player'))

    # Keep playing as long as the board has not tipped
    self.drawBoard()
    if not self.__board.checkIfTipped():
      self.play()

  def callPlayer(self):
    thisPlayer = player.Player(self.currentPlayer, float('Inf'))
    (location, weight) = thisPlayer.play(self.currentMode)
    self.updateBoard(location, weight)

  def play(self):
    nextMove = input('Player' + str(self.currentPlayer) +
                     ' Enter "location weight" (or press enter to have player.py play): ')
    if nextMove == '':
      self.callPlayer()
    else:
      nextMove = nextMove.split()
      location = int(nextMove[0])
      weight = int(nextMove[1])
      self.updateBoard(location, weight)

if __name__ == '__main__':
  runTest = Simulate()
  runTest.play()
