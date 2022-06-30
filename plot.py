from flask import render_template,Flask
import mysql.connector
import mysql.connector
import functools
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass1234!",
    database="sensor_db"
)
hostName = "localhost"
serverPort = 8080
if mydb:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")


mycursor = mydb.cursor()

#=======PLOT GIA ROOM
mycursor.execute("SELECT date FROM data_room  ORDER BY id DESC LIMIT 21")
#mycursor.execute("SELECT * FROM ( SELECT date FROM data  ORDER BY id DESC LIMIT 20)var1 ORDER BY id ASC")
myresult1 = mycursor.fetchall()
datelist = []
for x in range (0,20):
    #print(myresult1[x])
    dateplot = functools.reduce(lambda sub, ele: sub * 10 + ele, myresult1[x])
    dateplot1 = str(dateplot)
    today = dateplot1[:10]
    dateplot2 = dateplot1[-9:]
    datelist.insert(x,dateplot2)
datelist.reverse()
print(datelist)
mycursor.execute("SELECT temperature FROM data_room  ORDER BY id DESC LIMIT 21")
myresult2 = mycursor.fetchall()
templist = []
for y in range (0,20):
    tempplot = functools.reduce(lambda sub, ele: sub * 10 + ele, myresult2[y])
    #temp1 = functools.reduce(lambda sub, ele: sub * 10 + ele, temp)
    #print(temp)
    tempplot2 = float(tempplot)
    templist.insert(y,tempplot2)
    #print(templist[y])
templist.reverse()
print(templist)
mycursor.execute("SELECT humidity FROM data_room ORDER BY id DESC LIMIT 21")
#mycursor.execute("SELECT humidity FROM data ORDER BY id ASC LIMIT 21") #FIRST
myresult3 = mycursor.fetchall()
humlist = []
for z in range (0,20):
    #print(humlist[z])
    humplot = functools.reduce(lambda sub, ele: sub * 10 + ele, myresult3[z])
    #um1 = functools.reduce(lambda sub, ele: sub * 10 + ele, hum)
    humplot2 = float(humplot)
    #print(hum2)
    humlist.insert(z,humplot2)
humlist.reverse()
print(humlist)
print(today)
xpoints = np.array(datelist)
ypoints = np.array(templist)
zpoints = np.array(humlist)
font1= {'family' : 'DejaVu Sans','color':'blue','size':15}
font2= {'family' : 'DejaVu Sans','color':'red','size':15}
font3= {'family' : 'DejaVu Sans','color':'black','size':20}
plt.title('DHT11 Sensor Data (ROOM)',fontdict = font3)
plt.xlabel( today)
plt.text(5,25,"Temperature", fontdict = font1)
plt.text(5,40,"Humidity",fontdict = font2)
plt.plot(xpoints, ypoints, marker = 'o')
plt.plot(xpoints, zpoints,'o:r')
plt.grid(axis='x')
plt.gcf().autofmt_xdate()


figplot = plt.gcf()
figplot.savefig('/home/gakias/Desktop/ΠΤΥΧΙΑΚΗ_ΕΡΓΑΣΙΑ/python/pythonserver/templates/figplot1.png' , dpi=100)
plt.show()


#my_path = os.path.abspath(__file__)
#plt.savefig('/home/gakias/Desktop/ΚΑΤΑΝΕΜΗΜΕΝΑ/pythonserver/server/templates/plotroom.png')