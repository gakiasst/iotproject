import numpy as np
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
import os
from lightgbm import LGBMRegressor
from xgboost.sklearn import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.linear_model import LinearRegression, SGDRegressor, ElasticNet, BayesianRidge
from sklearn.kernel_ridge import KernelRidge

from sklearn.svm import SVR


from metrics import scale
from subprocess import call
import sys
import argparse
import joblib
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-r", "--room", help = "select room for the model to be trained. Available rooms:\n   balcony_road\n   balcony_yard\n   bathroom\n   kitchen\n   livingroom", required=True) 
parser.add_argument("-m", "--method", help = "select regression method. Options are:\n   AdaBoost\n   BayesianRidge\n   CatBoost\n   ElasticNet\n   GradientBoosting\n   HistGradientBoosting\n   KernelRidge\n   LinearRegression\n   LGBM\n   RandomForest\n   SGD\n   SVR\n   XGB", required=True) 
parser.add_argument("-hp", "--hide_prints", action=argparse.BooleanOptionalAction)
args = parser.parse_args()


if not args.hide_prints:
    open('./metrics.txt', 'w')


if args.room == 'all':
    rooms = ['balcony_road', 'balcony_yard', 'bathroom', 'kitchen', 'livingroom']
    for room in rooms:
        call(["python", "trainML.py", "-r", room, "-m", args.method, "-hp"])    

else:
    X = np.load('./datasets/bedroom-'+args.room+'/X.npy')
    Y = np.load('./datasets/bedroom-'+args.room+'/Y.npy')
    X = scale(X)
    Y = scale(Y)
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.2, random_state=1)

    max_depth = 30
    if args.method == 'RandomForest':
        model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, max_depth=max_depth, random_state=0))
    elif args.method == 'HistGradientBoosting':
        model = MultiOutputRegressor(HistGradientBoostingRegressor())
    elif args.method == 'GradientBoosting':
        model = MultiOutputRegressor(GradientBoostingRegressor(random_state=0))
    elif args.method == 'AdaBoost':
        model = MultiOutputRegressor(AdaBoostRegressor(random_state=0, n_estimators=100))
    elif args.method == 'SGD':
        model = MultiOutputRegressor(SGDRegressor(max_iter=1000, tol=1e-3))
    elif args.method == 'ElasticNet':
        model = MultiOutputRegressor(ElasticNet(random_state=0))
    elif args.method == 'BayesianRidge':
        model = MultiOutputRegressor(BayesianRidge())
    elif args.method == 'KernelRidge':
        model = MultiOutputRegressor(KernelRidge(alpha=1.0))
    elif args.method == 'XGB':
        model = MultiOutputRegressor(XGBRegressor(n_estimators=1000, max_depth=7, eta=0.1, subsample=0.7, colsample_bytree=0.8))
    elif args.method == 'CatBoost':
        model = MultiOutputRegressor(CatBoostRegressor(iterations=2,learning_rate=1,depth=2))                
    elif args.method == 'LGBM':
        model = MultiOutputRegressor(LGBMRegressor())
    elif args.method == 'LinearRegression':
        model = MultiOutputRegressor(LinearRegression())
    elif args.method == 'SVR':
        model = MultiOutputRegressor(SVR(C=1.0, epsilon=0.2))
    else:
        sys.exit("Invalid Regressor. Options are:\n   AdaBoost\n   BayesianRidge\n   CatBoost\n   ElasticNet\n   GradientBoosting\n   HistGradientBoosting\n   KernelRidge\n   LinearRegression\n   LGBM\n   RandomForest\n   SGD\n   SVR\n   XGB")
    model.fit(trainX, trainY)
    if not os.path.exists('./models/'+args.method+'/'):
        os.makedirs('./models/'+args.method+'/')
    
    joblib.dump(model, './models/'+args.method+'/'+args.room+'.h5')