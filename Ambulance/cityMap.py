from person import Person
from hospital import Hospital

class CityMap:
  __personList = None
  __hospitalList = None
  __ambulanceList = None

  __maxPersonNumber = None
  __maxHospitalNumber = None
  __maxAmbulanceNumber = None

  def __init__(self):
    self.__personList = dict()
    self.__hospitalList = dict()
    self.__ambulanceList = dict()
    self.__maxPersonNumber = 0
    self.__maxHospitalNumber = 0
    self.__maxAmbulanceNumber = 0

  def getPersonList(self):
    return self.__personList

  def getDistance(self, personCoordinates, ambulanceCoordinates):
    distanceX = abs(personCoordinates[0] - ambulanceCoordinates[0])
    distanceY = abs(personCoordinates[1] - ambulanceCoordinates[1])
    return distanceX + distanceY

  def getAmbulance(self, ambulanceNumber):
    return self.__ambulanceList[ambulanceNumber]

  def pickupPerson(self, personNumber):
    if personNumber < 0:
      return None

    person = self.__personList[personNumber]
    del(self.__personList[personNumber])
    return person

  def incrementTime(self):
    for personNumber in list(self.__personList.keys()):
      # Increment persons
      person = self.__personList[personNumber]
      remainingTime = person.incrementTime()
      if remainingTime < 0:
        del(self.__personList[personNumber])

    for ambulance in self.__ambulanceList.values():
      # Increment ambulances
      person = ambulance.incrementTime()

  def get911Calls(self):
    calls = set()
    for personNumber, person in self.__personList.items():
      (xCoordinate, yCoordinate, timeRemaining) = person.call911()
      call = (personNumber, xCoordinate, yCoordinate, timeRemaining)
      calls.add(call)
    return calls

  def callAmbulances(self):
    calls = set()
    for ambulanceNumber, ambulance in self.__ambulanceList.items():
      (xCoordinate, yCoordinate, numberOfPassengers) = ambulance.respondToCall()
      call = (ambulanceNumber, xCoordinate, yCoordinate, numberOfPassengers)
      if numberOfPassengers < 4:
        calls.add(call)
    return calls

  def addPerson(self, person):
    personNumber = self.__maxPersonNumber
    self.__maxPersonNumber = self.__maxPersonNumber + 1
    self.__personList[personNumber] = person

  def addHospital(self, hospital):
    hospitalNumber = self.__maxHospitalNumber
    self.__maxHospitalNumber = self.__maxHospitalNumber + 1
    self.__hospitalList[hospitalNumber] = hospital

  def placeHospitals(self):
    (xCoordinate, yCoordinate) = (1, 5)
    outputString = 'hospitals'

    for (hospitalNumber, hospital) in self.__hospitalList.items():
      hospital.place(xCoordinate, yCoordinate)
      ambulances = hospital.initializeAmbulances()
      for ambulance in ambulances:
        self.addAmbulance(ambulance)
      outputString = (outputString + ' ' + str(hospitalNumber) +
                     ' (' + str(xCoordinate) + ',' + str(yCoordinate) + ');')
    return outputString

  def addAmbulance(self, ambulance):
    ambulanceNumber = self.__maxAmbulanceNumber
    self.__maxAmbulanceNumber = self.__maxAmbulanceNumber + 1
    self.__ambulanceList[ambulanceNumber] = ambulance

if __name__ == '__main__':
  person1 = Person(3, 5, 29)
  person2 = Person(3, 6, 29)

  hospital1 = Hospital(4)
  hospital2 = Hospital(2)

  cityMap = CityMap()
  cityMap.addPerson(person1)
  cityMap.addPerson(person2)

  cityMap.addHospital(hospital1)
  cityMap.addHospital(hospital2)
  cityMap.placeHospitals()

  print(cityMap.get911Calls())
