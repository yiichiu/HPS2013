from ambulance import Ambulance

class Hospital:
  __numberOfAmbulances = None
  __coordinates = None

  def __init__(self, numberOfAmbulances):
    self.__numberOfAmbulances = numberOfAmbulances

  def getNumberOfAmbulances(self):
    return self.__numberOfAmbulances

  def place(self, xCoordinate, yCoordinate):
    self.__setLocation(xCoordinate, yCoordinate)

  def initializeAmbulances(self):
    ambulances = set()
    (xCoordinate, yCoordinate) = self.getLocation()
    for i in range(0, self.__numberOfAmbulances):
      ambulance = Ambulance(xCoordinate, yCoordinate)
      ambulances.add(ambulance)
    return ambulances

  def getLocation(self):
    return self.__coordinates

  def __setLocation(self, xCoordinate, yCoordinate):
    self.__coordinates = (xCoordinate, yCoordinate)
  
if __name__ == '__main__':
  hospital = Hospital(5)
  numberOfAmbulances = hospital.getNumberOfAmbulances()

  hospital.setLocation(4, 5)
  coordinates = hospital.getLocation()

  print(numberOfAmbulances)
  print(coordinates)
