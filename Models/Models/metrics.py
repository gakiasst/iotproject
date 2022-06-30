import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tabulate import tabulate

def scale(X):    
    return X*0.01

def descale(X):
    return X*100

def percentage(model, testX, testY):
    correct_temp=0
    correct_hum=0
    close_temp=0
    close_hum=0
    for i in range(testX.shape[0]):        
        pred = np.round(descale(model.predict(testX[i].reshape(1,testX[0].shape[0]))))
        true = descale(testY[i])
        if pred[0][0]==true[0]:
            correct_temp+=1
        if pred[0][1]==true[1]:
            correct_hum+=1                        
        if abs(pred[0][0]-true[0])<2:
            close_temp+=1
        if abs(pred[0][1]-true[1])<2:
            close_hum+=1          
    return round(100*(correct_temp/testX.shape[0]),2), round(100*(correct_hum/testX.shape[0]),2), round(100*(close_temp/testX.shape[0]),2), round(100*(close_hum/testX.shape[0]),2)

def mae(model, testX, testY):
    pred = descale(model.predict(testX))
    true = descale(testY)
    return round(mean_absolute_error(true, pred), 4)

def mse(model, testX, testY):
    pred = descale(model.predict(testX))
    true = descale(testY)
    return round(mean_squared_error(true, pred), 4)

def metrics(method, room, model, testX, testY, hide_prints):
    mymse = mse(model, testX, testY)
    mymae = mae(model, testX, testY)
    pt, ph, ct, ch = percentage(model, testX, testY)
    with open('./metrics.csv', 'a') as f:
        f.write(method+','+room+','+str(mymae)+','+str(mymse)+','+str(pt)+'%,'+str(ph)+'%,'+str(ct)+'%,'+str(ch)+'%\n')
    if not hide_prints:
        print('Model:', method)
        print('Room:', room)
        print('MAE:', mymae)
        print('MSE:', mymse)
        print('perfect temperature:', pt)
        print('perfect humidity:', ph)
        print('±1 temperature:', ct)
        print('±1 humidity:', ch)

def print_metrics():
    my_metrics = np.genfromtxt('./metrics.csv', delimiter=',', dtype=(str))
    print(tabulate(my_metrics, headers=['Room', 'MAE', 'MSE', 'perfect temperature', 'perfect humidity', '±1 temperature', '±1 humidity']))