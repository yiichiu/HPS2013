class Person:
  __coordinates = None
  __timeRemaining = None

  def __init__(self, xCoordinate, yCoordinate, timeRemaining):
    self.__coordinates = (xCoordinate, yCoordinate)
    self.__timeRemaining = timeRemaining

  def call911(self):
    # Return how much time is remaining for person
    (xCoordinate, yCoordinate) = self.__coordinates
    return (xCoordinate, yCoordinate, self.__timeRemaining)

  def incrementTime(self, timePassed = 1):
    self.__timeRemaining = max(-1, self.__timeRemaining - timePassed)
    return self.__timeRemaining

  def getLocation(self):
    return self.__coordinates

  def setLocation(self, xCoordinate, yCoordinate):
    self.__coordinates = (xCoordinate, yCoordinate)

if __name__ == '__main__':
  person = Person(3, 5, 29)
  for i in range(0, 35):
    timeRemaining = person.call911()
    print(timeRemaining)
    person.incrementTurn()

  coordinates = person.getLocation()
  print(coordinates)

  person.setLocation(9,5)
  coordinates = person.getLocation()
  print(coordinates)
