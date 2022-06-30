import numpy as np
from sklearn.model_selection import train_test_split


import joblib
from metrics import metrics, print_metrics, scale
from subprocess import call
import argparse
import sys
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-r", "--room", help = "select room for the model to be trained. Available rooms:\n   balcony_road\n   balcony_yard\n   bathroom\n   kitchen\n   livingroom", required=True) 
parser.add_argument("-m", "--method", help = "select regression method. Options are:\n   AdaBoost\n   BayesianRidge\n   CatBoost\n   ElasticNet\n   GradientBoosting\n   HistGradientBoosting\n   KernelRidge\n   LinearRegression\n   LGBM\n   RandomForest\n   SGD\n   SVR\n   XGB", required=True) 
parser.add_argument("-hp", "--hide_prints", action=argparse.BooleanOptionalAction)
args = parser.parse_args()


regressors =    ['AdaBoost','BayesianRidge','CatBoost','ElasticNet','GradientBoosting','HistGradientBoosting','KernelRidge','LinearRegression','LGBM','RandomForest','SGD','SVR','XGB']
if args.method not in regressors:
    sys.exit("Invalid Regressor. Options are:\n   AdaBoost\n   BayesianRidge\n   CatBoost\n   ElasticNet\n   GradientBoosting\n   HistGradientBoosting\n   KernelRidge\n   LinearRegression\n   LGBM\n   RandomForest\n   SGD\n   SVR\n   XGB")
if not args.hide_prints:
    open('./metrics.csv', 'w')


if args.room == 'all':
    print('Results for '+args.method+' models:')
    rooms = ['balcony_road', 'balcony_yard', 'bathroom', 'kitchen', 'livingroom']
    for room in rooms:
        call(["python", "evaluateML.py", "-r", room, "-m", args.method, "-hp"])
    print_metrics()

else:
    X = np.load('./datasets/bedroom-'+args.room+'/X.npy')
    Y = np.load('./datasets/bedroom-'+args.room+'/Y.npy')
    X = scale(X)
    Y = scale(Y)
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.2, random_state=1)
    model = joblib.load('./models/'+args.method+'/'+args.room+'.h5')
    metrics(args.method, args.room, model, testX, testY, args.hide_prints)