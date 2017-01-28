from random import Random
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM

INPUT_FILE = "perms2.list"
OUTPUT_FILE = "output"
LOG_FILE = "log.out"

log = open(LOG_FILE, "a")

MAX_LEN = 31401/8
DATA_LEN = 769760/64

def hexToInt(hexIn):
  return np.frombuffer(hexIn, np.uint8)[0]

def hexToBinArray(hexIn):
  intForm = np.frombuffer(hexIn, np.uint8)[0]
  return list('{0:08b}'.format(intForm))

X = np.zeros((DATA_LEN*MAX_LEN, 3, 3), dtype=np.int8)
y = np.zeros((DATA_LEN*MAX_LEN, 8), dtype=np.int8)

perms = []

inFile = open(INPUT_FILE, "r")
index = 0
for line in inFile:
  if index >= DATA_LEN:
    break
  parts = line.split(":")
  files = parts[0].split(",")
  for i in range(0,len(files)):
    files[i] = files[i].strip()
  files.append(parts[1].strip())
  perms.append(files)

inFile.close()

i = 0
for combo in perms:
  if(i>=DATA_LEN*MAX_LEN):
    break
  f1 = open("merged/"+combo[0], "rb")
  f2 = open("merged/"+combo[1], "rb")
  f3 = open("merged/"+combo[2], "rb")
  fy = open("merged/"+combo[3], "rb")
  lbyte1 = 0
  lbyte2 = 0
  lbyte3 = 0
  byte1 = hexToInt(f1.read(1))
  byte2 = hexToInt(f2.read(1))
  byte3 = hexToInt(f3.read(1))
  rbyte1 = hexToInt(f1.read(1))
  rbyte2 = hexToInt(f2.read(1))
  rbyte3 = hexToInt(f3.read(1))
  done = False
  dataRead = 0
  log.write("{0}\n".format(i))
  while(True):
    if(i>=DATA_LEN*MAX_LEN or i >= len(X)):
      print "exit1"
      print i
      print DATA_LEN*MAX_LEN
      break
    if(rbyte1=='' or rbyte2=='' or rbyte3==''):
      rbyte1=0
      rbyte2=0
      rbyte3=0
      done = True
    X[i,0]=np.array([lbyte1,byte1,rbyte1]) #error from 47205975?
    X[i,1]=np.array([lbyte2,byte2,rbyte2])
    X[i,2]=np.array([lbyte3,byte3,rbyte3])
    y[i] = hexToBinArray(fy.read(1))
    lbyte1 = byte1
    lbyte2 = byte2
    lbyte3 = byte3
    byte1 = rbyte1
    byte2 = rbyte2
    byte3 = rbyte3
    rbyte1 = hexToInt(f1.read(1))
    rbyte2 = hexToInt(f2.read(1))
    rbyte3 = hexToInt(f3.read(1))
    dataRead+=1
    i+=1
    if(done or MAX_LEN <= dataRead):
      break
  f1.close()
  f2.close()
  f3.close()
  fy.close()

        

log.write("Building model...\n")

print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(3,3)))
model.add(Dense(8))
model.add(Activation('softmax'))
model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['accuracy'])

print "fit"
log.write("fit\n")
model.fit(X, y, batch_size=128, nb_epoch=1, validation_split=0.2)

model.save_weights("model.h5")
print("Saved model to disk")

log.close()
