import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
import argparse
from metrics import scale, descale
 
parser = argparse.ArgumentParser(epilog='available rooms: balcony_road balcony_yard bathroom kitchen livingroom')
parser.add_argument("-r", "--room", help = "select room for the model to be trained", required=True) 
parser.add_argument("-v", "--verbose", help = "training verbosity", default=0) 
args = parser.parse_args()
arg = args.room

X = np.load('./datasets/bedroom-'+arg+'/X.npy')
Y = np.load('./datasets/bedroom-'+arg+'/Y.npy')
dim = X[0].shape[0]
X = scale(X)
Y = scale(Y)
trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.2, random_state=1)

model = Sequential()
model.add(Dense(240, input_dim=dim, activation='relu'))
model.add(Dense(160, activation='relu'))
model.add(Dense(2, activation='relu'))
model.compile(loss='mae', optimizer='adam', metrics='mse')
model.fit(trainX, trainY, epochs=1000, batch_size=10, verbose=int(args.verbose))

model.save('./models/DL/'+arg+'.h5')