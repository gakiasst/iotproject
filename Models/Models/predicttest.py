import numpy as np
import argparse
import joblib
from subprocess import call
from metrics import scale, descale
parser = argparse.ArgumentParser(epilog='available rooms: all balcony_road balcony_yard bathroom kitchen livingroom')
parser.add_argument("-r", "--room", help = "select room for the model to be evaluated", required=True)
parser.add_argument("-m", "--method", help = "select regression method. Options are:\n   AdaBoost\n   BayesianRidge\n   CatBoost\n   ElasticNet\n   GradientBoosting\n   HistGradientBoosting\n   KernelRidge\n   LinearRegression\n   LGBM\n   RandomForest\n   SGD\n   SVR\n   XGB", required=True)
parser.add_argument("-tm", "--temperature", help = "value for temperature", required=True)
parser.add_argument("-hm", "--humidity", help = "value for humidity", required=True)
args = parser.parse_args()

if args.room == 'all':
    rooms = ['balcony_road', 'balcony_yard', 'bathroom', 'kitchen', 'livingroom']
    for room in rooms:
        call(["python3", "./predictDL.py", "-r", room, "-tm", args.temperature, "-hm", args.humidity])
else:
    input = np.array([float(args.temperature), float(args.humidity)]).reshape(1,2)
    input = scale(input)
    model = joblib.load('./models/'+args.method+'/'+args.room+'.h5')
    prediction = model.predict(input)
    prediction = descale(prediction)
    print('predictions for ', args.room, ':')
    print('temperature: ', round(prediction[0][0]), '°C,    humidity: ', round(prediction[0][1]),'%')