import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import numpy as np
import keras
import argparse
from metrics import metrics, print_metrics
from sklearn.model_selection import train_test_split
from subprocess import call
from metrics import scale, descale
 
parser = argparse.ArgumentParser(epilog='available rooms: balcony_road balcony_yard bathroom kitchen livingroom')
parser.add_argument("-r", "--room", help = "select room for the model to be evaluated", required=True) 
parser.add_argument("-v", "--verbose", action=argparse.BooleanOptionalAction)
parser.add_argument("-hp", "--hide_prints", action=argparse.BooleanOptionalAction)
args = parser.parse_args()

if not args.hide_prints:
    open('./metrics.csv', 'w')

if args.room == 'all':
    print('Results for DL models:')
    rooms = ['balcony_road', 'balcony_yard', 'bathroom', 'kitchen', 'livingroom']
    for room in rooms:
        call(["python", "evaluateDL.py", "-r", room, "-hp"])
    print_metrics()
else:
    model = keras.models.load_model('./models/DL/'+args.room+'.h5')
    X = np.load('./datasets/bedroom-'+args.room+'/X.npy')
    Y = np.load('./datasets/bedroom-'+args.room+'/Y.npy')
    X = scale(X)
    Y = scale(Y)
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.2, random_state=1)

    if args.verbose:
        for i in range(testX.shape[0]):        
            pred = np.round(descale(model.predict(testX[i].reshape(1,X[0].shape[0]))))
            true = descale(testY[i])
            print('prediction: ', pred, 'true values: ', true)    
    metrics('DL model', args.room, model, testX, testY, args.hide_prints)