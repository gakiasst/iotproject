import numpy as np
import os
subfolders = [ f.path for f in os.scandir('./raw_data/') if f.is_dir() ]
for folder in subfolders:
    bedroom_data = np.genfromtxt(folder+'/bedroom.csv', delimiter=',', usecols=(0,3,4))
    otherroom_data = np.genfromtxt(folder+'/'+folder.split("-")[1]+'.csv', usecols=(0,3,4), delimiter=',')
    X=[]
    Y=[]
    for i in range(1,bedroom_data.shape[0]):
        toX=[]
        toY=[]
        toX.append(bedroom_data[i][1])
        toX.append(bedroom_data[i][2])
        toY.append(otherroom_data[i][1])
        toY.append(otherroom_data[i][2])
        X.append(toX)
        Y.append(toY)
    X = np.array(X)
    Y = np.array(Y)
    if not os.path.exists('./datasets/'+folder.split("/")[2]):
        os.makedirs('./datasets/'+folder.split("/")[2])
    np.save('./datasets/'+folder.split("/")[2]+'/X.npy', X)
    np.save('./datasets/'+folder.split("/")[2]+'/Y.npy', Y)
