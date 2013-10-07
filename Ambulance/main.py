from person import Person
from cityMap import CityMap
from hospital import Hospital
from dispatcher import Dispatcher
from time import clock

def parseInput(fileName):
  addingPersonInfo = False
  addingHospitalInfo = False

  with open(fileName) as file_:
    cityMap = CityMap()

    for row in file_:
      if row == '\n':
        # Empty rows should trigger a new header type
        addingPersonInfo = False
        addingHospitalInfo = False
        continue
      if row[-1] == '\n':
        # Format to remove the newline character
        row = row[0:-1]

      if addingPersonInfo:
        # Add data for a person to save
        row = row.split(',')
        xlocation = int(row[0])
        ylocation = int(row[1])
        timeRemaining = int(row[2])
        person = Person(xlocation, ylocation, timeRemaining)
        cityMap.addPerson(person)

      if addingHospitalInfo:
        # Add data for a hospital
        numberOfAmbulance = int(row)
        hospital = Hospital(numberOfAmbulance)
        cityMap.addHospital(hospital)

      # Set what kind of data we are dealing with based on the latest header
      if row == 'person(xloc,yloc,rescuetime)':
        addingPersonInfo = True
        addingHospitalInfo = False
      elif row == 'hospital(numambulance)':
        addingPersonInfo = False
        addingHospitalInfo = True
  return cityMap

def writeOutput(output):
  with open('output', 'w') as file_:
    data = file_.write(output)

if __name__ == '__main__':
  startTime = clock()

  cityMap = parseInput('input')
  hospitalsOutput = cityMap.placeHospitals()

  dispatcher = Dispatcher(cityMap)
  ambulanceOutput = dispatcher.startDipatch()

  output = hospitalsOutput + '\n' + ambulanceOutput
  writeOutput(output)
  print('Time remaining: ' + str(clock() - startTime))
