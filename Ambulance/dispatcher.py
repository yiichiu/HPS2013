import operator

class Dispatcher:
  __cityMap = None
  output = None

  def __init__(self, cityMap):
    self.__cityMap = cityMap
    self.output = ''

  def startDipatch(self):
    while self.anyPersonsLeftToRescue():
      if self.anyAmbulancesFree():
        self.route()
      self.__cityMap.incrementTime()
    return self.output

  def route(self):
    # person = (personNumber, xCoordinate, yCoordinate, timeRemaining)
    # ambulancesReport = (ambulanceNumber, xCoordinate, yCoordinate, numberOfPassengers)
    # distance = (distance, personNumber, xCoordinateTarget, yCoordinateTarget, timeRemaining)
    ambulancesReport = sorted(list(self.__cityMap.callAmbulances()))

    for ambulanceReport in ambulancesReport:
      ambulanceNumber = ambulanceReport[0]
      numberOfPassengers = ambulanceReport[3]
      ambulance = self.__cityMap.getAmbulance(ambulanceNumber)

      if numberOfPassengers < 1:
        persons = sorted(list(self.__cityMap.get911Calls()))
        distances = self.getDistancesAndRemainingTime(persons, ambulanceReport)

        (xCoordinate, yCoordinate, personNumber) = self.getLocationToSendAmbulance(distances)
        ambulance.sendToLocation(xCoordinate, yCoordinate)

        person = self.__cityMap.pickupPerson(personNumber)
        ambulance.pickupPerson(person)
        self.getOutput(ambulanceNumber, personNumber)
      else:
        (xCoordinate, yCoordinate) = self.getHospitalCoordinates(ambulanceReport)
        ambulance.sendToLocation(xCoordinate, yCoordinate, True)
        self.getHospitalOutput(ambulanceNumber, xCoordinate, yCoordinate)

  def getHospitalCoordinates(self, ambulanceReport):
    minDistance = min(self.__getHospitalDistance(ambulanceReport), key=operator.itemgetter(1))
    return minDistance[1]

  def __getHospitalDistance(self, ambulanceReport):
    xCoordinate = ambulanceReport[1]
    yCoordinate = ambulanceReport[2]

    ambulanceCoordinates = (xCoordinate, yCoordinate)
    hosptialCoordinatesList = self.__cityMap.getHospitalLocations()

    distances = [(self.__cityMap.getDistance(ambulanceCoordinates, hosptialCoordinates), hosptialCoordinates)
                 for hosptialCoordinates in hosptialCoordinatesList]
    return distances

  def getHospitalOutput(self, ambulanceNumber, xCoordinate, yCoordinate):
    self.output = (self.output + 'ambulance ' + str(ambulanceNumber)
                  + ' (' + str(xCoordinate) + ',' + str(yCoordinate) + ')\n')

  def getOutput(self, ambulanceNumber, personNumber):
    if personNumber > 0:
      personOutput = self.__cityMap.originalPersonList[personNumber].getOutput()
      self.output = (self.output + 'ambulance ' + str(ambulanceNumber) + ' '
                    + str(personNumber) + ' ' + str(personOutput) + '\n' )

  def getLocationToSendAmbulance(self, distances):
    # distance = (distance, personNumber, xCoordinateTarget, yCoordinateTarget, timeRemaining)
    distances = list(distance
                     for distance in distances
                     if distance[0] < distance[4])
    if len(distances) <= 0:
      return (-1, -1, -1)

    distance = min(distances)

    personNumber = distance[1]
    xCoordinate = distance[2]
    yCoordinate = distance[3]
    return (xCoordinate, yCoordinate, personNumber)

  def getDistancesAndRemainingTime(self, persons, ambulance):
    # distance = (distance, personNumber, xCoordinateTarget, yCoordinateTarget, timeRemaining)
    distances = list(((self.getDistance(person, ambulance),) + person)
                          for person in sorted(persons))
    return distances

  def getDistance(self, person, ambulance):
    personCoordinates = (person[1], person[2])
    ambulanceCoordinates = (ambulance[1], ambulance[2])
    distance = self.__cityMap.getDistance(personCoordinates, ambulanceCoordinates)
    return distance

  def anyPersonsLeftToRescue(self):
    personsToRescue = self.__cityMap.get911Calls()
    if personsToRescue == set():
      return False
    else:
      return True

  def anyAmbulancesFree(self):
    ambulances = self.__cityMap.callAmbulances()
    if ambulances == set():
      return False
    else:
      return True

if __name__ == '__main__':
  import main
  cityMap = main.parseInput('input')
  cityMap.placeHospitals()
  dispatcher = Dispatcher(cityMap)
  dispatcher.route()
