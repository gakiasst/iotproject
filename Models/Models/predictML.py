import numpy as np
import argparse
import joblib
from subprocess import call
from metrics import scale, descale


#parser = argparse.ArgumentParser(epilog='available rooms: all balcony_road balcony_yard bathroom kitchen livingroom')
#parser.add_argument("-r", "--room", help="select room for the model to be evaluated", required=True)
#parser.add_argument("-m", "--method",
# help="select regression method. Options are:\n   AdaBoost\n   BayesianRidge\n   CatBoost\n   ElasticNet\n   GradientBoosting\n   HistGradientBoosting\n   KernelRidge\n   LinearRegression\n   LGBM\n   RandomForest\n   SGD\n   SVR\n   XGB",
 #                   required=True)
#parser.add_argument("-tm", "--temperature", help="value for temperature", required=True)
#parser.add_argument("-hm", "--humidity", help="value for humidity", required=True)
#args = parser.parse_args()

rooms = ['balcony_road', 'balcony_yard', 'bathroom', 'kitchen', 'livingroom']
numbers = []

#parser.add_argument()

#if args.room == 'all':

#=PERNW TEMP KAI HUM APO SERVER
temperature = 31
humidity = 32
if 1==1 :
    for x in range(0,5):
         input = np.array([float(temperature), float(humidity)]).reshape(1, 2)
         input = scale(input)
         model = joblib.load('./models/' + 'RandomForest' + '/' + rooms[x] + '.h5')
         prediction = model.predict(input)
         prediction = descale(prediction)
         numbers.append(round(prediction[0][0]))
         numbers.append(round(prediction[0][1]))
    print(numbers)
    print('br temp = ', numbers[0])
    print('br hum = ', numbers[1])
    print('by temp = ', numbers[2])
    print('by hum = ', numbers[3])
    print('bath temp = ', numbers[4])
    print('bath hum = ', numbers[5])
    print('kit temp = ', numbers[6])
    print('kit hum = ', numbers[7])
    print('lr temp = ', numbers[8])
    print('lr hum = ', numbers[9])
else:
    input = np.array([float(args.temperature), float(args.humidity)]).reshape(1,2)
    input = scale(input)
    model = keras.models.load('./models/'+args.method+'/'+args.room+'.h5')
    prediction = model.predict(input)
    prediction = descale(prediction)
    print('predictions for ', args.room, ':')
    print('temperature: ', round(prediction[0][0]), '°C,    humidity: ', round(prediction[0][1]),'%')