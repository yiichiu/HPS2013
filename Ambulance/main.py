from person import Person
from cityMap import CityMap
from hospital import Hospital
from dispatcher import Dispatcher
from time import clock
from score import getScore
from score import readdata

<<<<<<< HEAD
import socket
from subprocess import call

=======
>>>>>>> f2da8660fcc2857eb2c91f988b5d53989b6820c4
def parseInput(fileName):
  addingPersonInfo = False
  addingHospitalInfo = False

  with open(fileName) as file_:
    cityMap = CityMap()

    for row in file_:
<<<<<<< HEAD
      if row == '\n' or '<' in row:
=======
      if row == '\n':
>>>>>>> f2da8660fcc2857eb2c91f988b5d53989b6820c4
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

def run(cityMap):
  import copy
  cityMap = copy.deepcopy(cityMap)
  hospitalsOutput = cityMap.placeHospitals()

  dispatcher = Dispatcher(cityMap)
  ambulanceOutput = dispatcher.startDipatch()

  output = hospitalsOutput + '\n' + ambulanceOutput
  return output

if __name__ == '__main__':
<<<<<<< HEAD
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('127.0.0.1', 5555))
  print 'connected to socket'
  s.send("White Truffle")
  print 'sent team name'
  input_data=''

  while True:
    chunk = s.recv(1000000)
    print chunk
    if not chunk: break
    if chunk == '':
        raise RuntimeError("socket connection broken")
    input_data = input_data + chunk
    if '<' in input_data:
        break

  print 'the input is ' + input_data
  f = open('input', 'w')
  f.write(input_data)
  f.close()

  
  call ('./ambulance')

  inputFile = 'input'
  cityMap = parseInput(inputFile)

  startTime = clock()
  scoreHelper = readdata(inputFile)
  bestOutput = None
  bestScore = None
  while clock() - startTime < 60:
    output = run(cityMap)
    score = getScore(output, scoreHelper)
    #print(score)
=======
  startTime = clock()
  inputFile = 'input'
  cityMap = parseInput(inputFile)

  scoreHelper = readdata(inputFile)
  bestOutput = None
  bestScore = None
  while clock() - startTime < 60 * 0.10:
    output = run(cityMap)
    score = getScore(output, scoreHelper)
    print(score)
>>>>>>> f2da8660fcc2857eb2c91f988b5d53989b6820c4
    if bestOutput == None:
      bestOutput = output
      bestScore = score
    elif bestScore < score:
      bestOutput = output
      bestScore = score

<<<<<<< HEAD
  #writeOutput(output)
  output += '\n<EOM>'
  
  totalsent=0
  MSGLEN = len(output) 
  while totalsent < MSGLEN:
    sent = s.send(output[totalsent:])
    if sent == 0:
        raise RuntimeError("socket connection broken")
    totalsent = totalsent + sent
  print 'sent result ' + output

  s.close()
=======
  writeOutput(output)
  print('Time remaining: ' + str(clock() - startTime))
>>>>>>> f2da8660fcc2857eb2c91f988b5d53989b6820c4
