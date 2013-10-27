import sys
import socket

port = 4567
maxlen = 999999
eom = '\n'
print(sys.argv)
if len(sys.argv) > 1:
  port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', port))

def readSocket(sock, timeout=0):
  inputData = ''
  while True:
    chunk = sock.recv(maxlen)
    if not chunk:
      break
    elif chunk == '':
      raise RuntimeError('socket connection broken')
    inputData = inputData + chunk
    if eom in inputData:
      break
  if inputData == '':
    return eom
  serverSaid(inputData)
  return inputData.strip()

def sendSocket(sock, msg):
  msg += eom
  totalsent = 0
  MSGLEN = len(msg) 
  while totalsent < MSGLEN:
    sent = sock.send(msg[totalsent:])
    if sent == 0:
      raise RuntimeError('socket connection broken')
    totalsent = totalsent + sent
  iSaid(msg)

def parseData(msg):
  msgList = msg.split('\n')
  if msgList[0] != 'Walls':
    return msg
  # Parse Walls
  wallOffset = int(msgList[1])

  # Parse Moves to Next Wall Build
  assert(msgList[2+wallOffset] == 'Moves to Next Wall Build')
  movesToNextWallBuild = msgList[3+wallOffset]

  # Parse Hunter and Prey Location
  hunterLocation = msgList[4+wallOffset]
  preyLocation = msgList[5+wallOffset]

  # Parse Remaining Time
  remainingTime = msgList[6+wallOffset]
  return (movesToNextWallBuild, hunterLocation, preyLocation, remainingTime)

def makeMove(socket, direction):
  sendSocket(socket,'%s'%(direction))

def serverSaid(msg):
  msg = stripNewLine(msg)
  print('Server: %s'%msg[:80])
def iSaid(msg):
  msg = stripNewLine(msg)
  print('Client: %s'%msg[:80])

def stripNewLine(msg):
  if msg[-1] == '\n':
    return msg[:-1]
  return msg

if __name__=='__main__':
  from hunter import playHunter

  try:
    # Return Team Name
    question = readSocket(s, 1)
    assert(question == 'Team Name?')
    sendSocket(s, 'WhiteTruffle')

    # Read N (Time steps to build the next wall)
    #      M (Max number of walls)
    (N, M) = [int(x) for x in readSocket(s).split(' ')] 

    # Play Game
    while True:
      data = ''
      while True:
        dataNew = readSocket(s)
        data += dataNew + '\n'
        if '.' in data:
          break

      if data == '':
        break
      (movesToNextWallBuild, hunterLocation, preyLocation, remainingTime) = parseData(data)
      move = playHunter(movesToNextWallBuild, hunterLocation, preyLocation, remainingTime)
      makeMove(s, move)
  finally:
    print('Close socket')
    s.close()
