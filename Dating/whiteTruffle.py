import socket
import copy
import sys
eom = '<EOM>\n'

def send(s, msg):
    print("sending")
    print(msg)
    msg += eom
    totalsent = 0
    while totalsent < len(msg):
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

def receive(s, timeout=0):
    msg = ''
    while eom not in msg:
        chunk = s.recv(1024)
        if not chunk:
          break
        if chunk == '':
            raise RuntimeError("socket connection broken")
        msg += chunk
    msg = msg.replace(eom, '')
    return msg

def parseCandidates(rawData):
  rawData = rawData.split('\n')

  # Check the header Data
  headerData = rawData[0].split(' ')
  playerType = headerData[0]
  numberOfAttributes = int(headerData[1])
  assert(playerType == 'M')

  # Parse Candidates
  candidates = [(
                  [float(attribute)
                   for attribute
                   in attributes.split(' ')[:numberOfAttributes]
                   if attribute != ''
                  ],
                  float(attributes.split(' ')[numberOfAttributes])
                )
                for attributes in rawData[1:]
                if attributes != '']
  return candidates

if __name__ == '__main__':
  port = 4567
  print(sys.argv)
  if len(sys.argv) > 1:
    port = int(sys.argv[1])
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(('127.0.0.1', port))

  try:
    question = receive(s)

    assert(question == 'Team Name?')
    send(s, 'WhiteTruffle')

    # Read in data
    while True:
      rawData = receive(s)
      if rawData == 'end':
        break

      candidates = parseCandidates(rawData)
    
  except:
    raise
  finally:
    print('Close socket')
    s.close()
