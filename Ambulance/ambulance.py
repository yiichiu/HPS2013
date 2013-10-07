class Ambulance:
  __goToHospital = None
  __coordinates = None
  __personList = None
  __targetCoordinates = None
  __targetPerson = None

  def __init__(self, xCoordinate, yCoordinate):
    self.__coordinates = (xCoordinate, yCoordinate)
    self.__targetCoordinates = (xCoordinate, yCoordinate)
    self.__personList = set()

  def getMostUrgentPatientTime(self):
    if self.__personList == set():
      return float('Inf')
    return min([person.getTimeRemaining() for person in self.__personList])

  def pickupPerson(self, person):
    if person != None:
      self.__targetPerson = person

  def incrementTime(self):
    (xCoordinate, yCoordinate) = self.__coordinates
    (xCoordinateTarget, yCoordinateTarget) = self.__targetCoordinates

    if xCoordinate != xCoordinateTarget:
      xCoordinate = xCoordinate + 1 if xCoordinateTarget > xCoordinate else xCoordinate - 1
      self.__coordinates = (xCoordinate, yCoordinate)
    elif yCoordinate != yCoordinateTarget:
      yCoordinate = yCoordinate + 1 if yCoordinateTarget > yCoordinate else yCoordinate - 1
      self.__coordinates = (xCoordinate, yCoordinate)
    elif self.__targetPerson != None:
      self.__personList.add(self.__targetPerson)
      self.__targetPerson = None
    elif self.__goToHospital:
      self.__personList.pop()
      if len(self.__personList) <= 0:
        self.__goToHospital = False

  def respondToCall(self):
    if self.__targetPerson != None:
      return None

    (xCoordinate, yCoordinate) = self.__coordinates
    numberOfPassengers = len(self.__personList)
    return (xCoordinate, yCoordinate, numberOfPassengers)

  def sendToLocation(self, xCoordinate, yCoordinate, isHospital = False):
    if xCoordinate >= 0 and yCoordinate >= 0:
      self.__targetCoordinates = (xCoordinate, yCoordinate)
    self.__goToHospital = isHospital

if __name__ == '__main__':
  ambulance = Ambulance(3)
