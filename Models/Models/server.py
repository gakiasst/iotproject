import json
from flask import render_template, Flask
import mysql.connector
import functools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import socket
import threading
import time
import numpy as np
import argparse
import joblib
from subprocess import call
from metrics import scale, descale
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template
from io import BytesIO
import base64
import os
import matplotlib
# creating connection Object which will contain SQL Server Connection
app = Flask(__name__, template_folder="templates" )
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass1234!",
    database="sensor_db"
)
HOST = '192.168.2.31'  # The server's hostname or IP address
PORT = 5002  # The port used by the server
hostName = "localhost"
serverPort = 8080
if mydb:
    print("DB Connected Successfully")
else:
    print("DB Connection Not Established")
#============== DATA FROM data_house KAI UPDATE stats_room
mycursor = mydb.cursor()
mycursor.execute("SELECT date,temperature,humidity FROM data_house  LIMIT 1 ")
first = mycursor.fetchall()
for row in first:
    fdate, ftemp, fhum = row
datelist = []
maxtemplist = []
mintemplist = []
maxhumlist = []
minhumlist = []
avtemplist = []
avhumlist = []
count = 0
datelist.insert(count, fdate)
maxtemplist.insert(count, ftemp)
mintemplist.insert(count, ftemp)
maxhumlist.insert(count, fhum)
minhumlist.insert(count, fhum)
avtemplist.insert(count, fhum)
avhumlist.insert(count, ftemp)
motemp = 0
mohum = 0
synolotemp = ftemp
synolohum = fhum
plithostemp = 1
plithoshum = 1
mycursor.execute("SELECT date,temperature,humidity FROM data_house ")
data = mycursor.fetchall()
for row in data:
    date, temp, hum = row
    if date == datelist[count]:
        if temp < mintemplist[count]:
            mintemplist[count] = temp
        if temp > maxtemplist[count]:
            maxtemplist[count] = temp
        if hum < minhumlist[count]:
            minhumlist[count] = hum
        if hum > maxhumlist[count]:
            maxhumlist[count] = hum
        plithostemp += 1
        plithoshum += 1
        synolotemp += temp
        synolohum += hum
        motemp = (synolotemp/plithostemp)
        mohum = (synolohum/plithoshum)
        avtemplist[count] = "{:.1f}".format(motemp)
        avhumlist[count] = "{:.1f}".format(mohum)
    elif date > datelist[count]:
        motemp = 0
        mohum = 0
        synolotemp = temp
        synolohum = hum
        plithostemp = 1
        plithoshum = 1
        count += 1
        datelist.insert(count, date)
        maxtemplist.insert(count, temp)
        mintemplist.insert(count, temp)
        maxhumlist.insert(count, hum)
        minhumlist.insert(count, hum)
        avtemplist.insert(count, temp)
        avhumlist.insert(count, hum)
        motemp = (synolotemp/plithostemp)
        mohum = (synolohum/plithoshum)
        avtemplist[count] = "{:.1f}".format(motemp)
        avhumlist[count] = "{:.1f}".format(mohum)
#print(datelist)
count += 1
datadates = count
#print(datadates, ' DIFFERENT DATES IN DATA_HOUSE ')
for y in range(0, datadates):
    fulldate = datelist[y]
    finalldate = fulldate.strftime('%Y-%m-%d')
    mxt = str(maxtemplist[y])
    mnt = str(mintemplist[y])
    mxh = str(maxhumlist[y])
    mnh = str(minhumlist[y])
    avt = str(avtemplist[y])
    avh = str(avhumlist[y])
    #print("DATE: " + finalldate,
    #      'MAXTEMP: ' + mxt,
    #      'MINTEMP: ' + mnt,
    #      'MAXHUM: ' + mxh,
    #      'MINHUM: ' + mnh,
    #      'AVTEMP: ' + avt,
    #      'AVHUM: ' + avh)

mycursor = mydb.cursor()
mycursor.execute("DELETE  FROM stats_room")
mydb.commit()
#print('delete stats room done!')

for k in range(datadates):
    fulldate1 = datelist[k]
    finaldate = fulldate1.strftime('%Y-%m-%d')
    mxt = str(maxtemplist[k])
    mnt = str(mintemplist[k])
    mxh = str(maxhumlist[k])
    mnh = str(minhumlist[k])
    avt = str(avtemplist[k])
    avh = str(avhumlist[k])
    datadb = (finaldate, avt, avh, mxt, mnt, mxh, mnh)
    sql = "INSERT INTO stats_room (date,av_temperature," \
          "av_humidity,max_temperature,min_temperature," \
          "max_humidity,min_humidity) VALUES (%s, %s,%s,%s, %s, %s, %s)"
    mycursor.execute(sql, datadb)
    mydb.commit()

#============== DATA FROM data_out KAI UPDATE stats_out===========================
mycursor = mydb.cursor()
mycursor.execute("SELECT date,temperature,humidity FROM data_out  LIMIT 1 ")
firstout = mycursor.fetchall()
for row in firstout:
    fdateout , ftempout , fhumout  = row
datelistout = []
maxtemplistout = []
mintemplistout = []
maxhumlistout = []
minhumlistout = []
avtemplistout = []
avhumlistout = []
countout = 0
datelistout.insert(countout,  fdateout)
maxtemplistout.insert(countout, ftempout)
mintemplistout.insert(countout, ftempout)
maxhumlistout.insert(countout, fhumout)
minhumlistout.insert(countout, fhumout)
avtemplistout.insert(countout, ftempout)
avhumlistout.insert(countout, fhumout)
motempout = 0
mohumout = 0
synolotempout = ftempout
synolohumout = fhumout
plithostempout = 1
plithoshumout = 1
mycursor.execute("SELECT date,temperature,humidity FROM data_out ")
dataout = mycursor.fetchall()
for row in dataout:
    dateout, tempout, humout = row
    if dateout == datelistout[countout]:
        if tempout < mintemplistout[countout]:
            mintemplistout[countout] = tempout
        if tempout > maxtemplistout[countout]:
            maxtemplistout[countout] = tempout
        if humout < minhumlistout[countout]:
            minhumlistout[countout] = humout
        if humout > maxhumlistout[countout]:
            maxhumlistout[countout] = humout
        plithostempout += 1
        plithoshumout += 1
        synolotempout += tempout
        synolohumout += humout
        motempout = (synolotempout/plithostempout)
        mohumout = (synolohumout/plithoshumout)
        avtemplistout[countout] = "{:.1f}".format(motempout)
        avhumlistout[countout] = "{:.1f}".format(mohumout)
    elif dateout > datelistout[countout]:
        motempout = 0
        mohumout = 0
        synolotempout = tempout
        synolohumout = humout
        plithostempout = 1
        plithoshumout = 1
        countout += 1
        datelistout.insert(countout, dateout)
        maxtemplistout.insert(countout, tempout)
        mintemplistout.insert(countout, tempout)
        maxhumlistout.insert(countout, humout)
        minhumlistout.insert(countout, humout)
        avtemplistout.insert(countout, tempout)
        avhumlistout.insert(countout, humout)
        motempout = (synolotempout/plithostempout)
        mohumout = (synolohumout/plithoshumout)
        avtemplistout[countout] = "{:.1f}".format(motempout)
        avhumlistout[countout] = "{:.1f}".format(mohumout)
#print(datelistout)
countout += 1
dataoutdates = countout
#print(dataoutdates, ' DIFFERENT DATES IN DATA_OUT')
for y in range(0, dataoutdates):
    fulldateout = datelistout[y]
    finalldateout = fulldateout.strftime('%Y-%m-%d')
    mxtout = str(maxtemplistout[y])
    mntout = str(mintemplistout[y])
    mxhout = str(maxhumlistout[y])
    mnhout = str(minhumlistout[y])
    avtout = str(avtemplistout[y])
    avhout = str(avhumlistout[y])
    #print("DATE: " + finalldateout,
    #      'MAXTEMP: ' + mxtout,
    #      'MINTEMP: ' + mntout,
    #      'MAXHUM: ' + mxhout,
    #      'MINHUM: ' + mnhout,
    #      'AVTEMP: ' + avtout,
    #      'AVHUM: ' + avhout)

mycursor = mydb.cursor()
mycursor.execute("DELETE  FROM stats_out")
mydb.commit()
#print('delete out  done!')
for k in range(dataoutdates):
    fulldateout1 = datelistout[k]
    finalldateout = fulldateout1.strftime('%Y-%m-%d')
    mxtout = str(maxtemplistout[k])
    mntout = str(mintemplistout[k])
    mxhout = str(maxhumlistout[k])
    mnhout = str(minhumlistout[k])
    avtout = str(avtemplistout[k])
    avhout = str(avhumlistout[k])
    datadbout = (finalldateout, avtout, avhout, mxtout, mntout, mxhout, mnhout)
    sql = "INSERT INTO stats_out (date,av_temperature," \
          "av_humidity,max_temperature,min_temperature," \
          "max_humidity,min_humidity) VALUES (%s, %s,%s,%s, %s, %s, %s)"
    mycursor.execute(sql, datadbout)
    mydb.commit()

@app.route('/')
def predictions():
            # pernw thn teleftaia metrhsh kai ypologizw ta alla dwmatia
            mycursor = mydb.cursor()
            mycursor.execute("SELECT date,time,temperature,humidity FROM data_house  ORDER BY id DESC LIMIT 1") #LAST
            last = mycursor.fetchall()
            data = functools.reduce(lambda sub, ele: sub * 10 + ele, last)
            date, time, temp, hum = data
            #======EDW KANW THN MIA TIMH PREDICTION GIA TA ALLA DWMATIA
            rooms = ['balcony_road', 'balcony_yard', 'bathroom', 'kitchen', 'livingroom']
            numbers = []
            temperature = temp
            humidity = hum
            print(temp)
            print(hum)
            for x in range(0,5):
                input = np.array([float(temperature), float(humidity)]).reshape(1, 2)
                input = scale(input)
                model = joblib.load('./models/' + 'RandomForest' + '/' + rooms[x] + '.h5')
                prediction = model.predict(input)
                prediction = descale(prediction)
                numbers.append(round(prediction[0][0]))
                numbers.append(round(prediction[0][1]))
            #print(numbers)
            #print('br temp = ', numbers[0])
            #print('br hum = ', numbers[1])
            #print('by temp = ', numbers[2])
            #print('by hum = ', numbers[3])
            #print('bath temp = ', numbers[4])
            #print('bath hum = ', numbers[5])
            #print('kit temp = ', numbers[6])
            #print('kit hum = ', numbers[7])
            #print('lr temp = ', numbers[8])
            #print('lr hum = ', numbers[9])

            return render_template( 'prediction.html',
                            roomdate=date, roomtime=time, roomtemp=temp, roomhum=hum,
                            brt=numbers[0], brh=numbers[1],
                            byt=numbers[2], byh=numbers[3],
                            bt=numbers[4], bh=numbers[5],
                            kt=numbers[6], kh=numbers[7],
                            lt=numbers[8], lh=numbers[9])



@app.route('/historicaldata')
def historical():
    #edw pernw ta dedomena apo stats room kai stats out kai ta emfanizw mazi me plots
    mycursor = mydb.cursor()
    #==============  last ROW update FROM DATA_house
    mycursor.execute("SELECT date,time,temperature,humidity FROM data_house ORDER BY id DESC LIMIT 1")    #last
    lastrowroom = mycursor.fetchall()
    datalast = functools.reduce(lambda sub, ele: sub * 10 + ele, lastrowroom)
    dateroom, timeroom, temproom,  humroom = datalast
    #==========LAST ROW UPDATE  FROM DATA_OUT
    mycursor = mydb.cursor()
    mycursor.execute("SELECT date,time,temperature,humidity FROM data_out ORDER BY id DESC LIMIT 1")
    lastrowout = mycursor.fetchall()
    datalastout = functools.reduce(lambda sub, ele: sub * 10 + ele, lastrowout)
    outdate,outtime, outtemp, outhum = datalastout
    ## pernw ta dedomena apo stats kai stats_out kai ta emfanizw se plot kai pinaka (OLA)
    #======DATA FROM STATS_ROOM
    sdatelist = []
    smaxtemplist  = []
    smintemplist  = []
    smaxhumlist  = []
    sminhumlist  = []
    savtemplist = []
    savhumlist = []
    mycursor.execute("SELECT date,av_temperature,av_humidity,max_temperature,"
                     "min_temperature,max_humidity,min_humidity FROM stats_room")
    sts = mycursor.fetchall()
    for row in sts:
        sdate,savtmp,savhum,smxtmp,smntmp,smxh,smnh = row
        savtemplist.append(savtmp)
        savhumlist.append(savhum)
        sdatelist.append(sdate)
        smaxtemplist.append(smxtmp)
        smintemplist.append(smntmp)
        smaxhumlist.append(smxh)
        sminhumlist.append(smnh)
    #mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM stats_room")
    number = mycursor.fetchall()
    totalrows = functools.reduce(lambda sub, ele: sub * 10 + ele, number)
    statsrowsroom = functools.reduce(lambda sub, ele: sub * 10 + ele, totalrows)

    #======DATA FROM STATS_OUT
    sdatelistout = []
    smaxtemplistout = []
    smintemplistout = []
    smaxhumlistout = []
    sminhumlistout = []
    savtemplistout = []
    savhumlistout = []
    #mycursor = mydb.cursor()
    mycursor.execute("SELECT date,av_temperature,av_humidity,max_temperature,"
                     "min_temperature,max_humidity,min_humidity FROM stats_out")
    stsout = mycursor.fetchall()
    for row in stsout:
        sdateout,savtempout,savhumout,smxtmpout,smntmpout,smxhout,smnhout = row
        sdatelistout.append(sdateout)
        savtemplistout.append(savtempout)
        savhumlistout.append(savhumout)
        smaxtemplistout.append(smxtmpout)
        smintemplistout.append(smntmpout)
        smaxhumlistout.append(smxhout)
        sminhumlistout.append(smnhout)
    #mycursor1 = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM stats_out")
    numberout = mycursor.fetchall()
    totalrowsout1 = functools.reduce(lambda sub, ele: sub * 10 + ele, numberout)
    statsrowsout = functools.reduce(lambda sub, ele: sub * 10 + ele, totalrowsout1)

    #print(sdatelist)
    #print(savtemplist)
    #print(savhumlist)
    xpoints = np.array(sdatelist)
    ypoints = np.array(savtemplist)
    zpoints = np.array(savhumlist)

    xpoints1 = np.array(sdatelistout)
    ypoints1 = np.array(savtemplistout)
    zpoints1 = np.array(savhumlistout)

    #ypoints2 = np.array(savtemplistout)
    #zpoints = np.array(savhumlist)
    #zpoints2 = np.array(savhumlistout)

    #gyrnaw anapoda tis listes gia na provlh8oun anapoda stoys pinakes
    sdatelist.reverse()
    savtemplist.reverse()
    savhumlist.reverse()
    smaxtemplist.reverse()
    smintemplist.reverse()
    smaxhumlist.reverse()
    sminhumlist.reverse()

    sdatelistout.reverse()
    savtemplistout.reverse()
    savhumlistout.reverse()
    smaxtemplistout.reverse()
    smintemplistout.reverse()
    smaxhumlistout.reverse()
    sminhumlistout.reverse()

    #=========== PLOTS =======================
    font1 = {'family': 'DejaVu Sans', 'color': 'blue', 'size': 15}
    font2 = {'family': 'DejaVu Sans', 'color': 'red', 'size': 15}
    font3 = {'family': 'DejaVu Sans', 'color': 'black', 'size': 20}


    p1 = plt
    p2 = plt
    f = p1.figure()
    f.set_figwidth(12)
    f.set_figheight(4)
    f2 = p2.figure()
    f2.set_figwidth(12)
    f2.set_figheight(4)

    p1.suptitle('ROOM SENSOR AVERAGE TEMPERATURE-HUMIDITY', fontdict=font3)
    #p1.text(5, 25, "Temperature", fontdict=font1)
    #p1.text(5, 40, "Humidity", fontdict=font2)
    #p1.axis([xpoints[0], xpoints[(statsrowsroom - 1)], 0, 80])
    p1.plot(xpoints, ypoints, 'o:b')
    p1.plot(xpoints, zpoints, 'o:r')
    p1.grid(axis='y')
    p1.gcf().autofmt_xdate()
    #plt.show()
    img = BytesIO()
    figplot = p1.gcf()
    figplot.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    p1.close()
    #fig , ax  = plt.subplots()

    p2.suptitle('EXTERNAL SENSOR AVERAGE TEMPERATURE-HUMIDITY', fontdict=font3)
    #p2.text( 0,5 , "Temperature", fontdict=font1)
    # p2.text(0,5,"Humidity",  fontdict=font2)
    #p2.axis([xpoints1[0], xpoints[(statsrowsout - 1)], 0, 80])
    p2.plot(xpoints1, ypoints1, 'o:b')
    p2.plot(xpoints1, zpoints1, 'o:r')
    p2.grid(axis='y')
    p2.gcf().autofmt_xdate()
    img2 = BytesIO()
    figplot2 = p2.gcf()
    figplot2.savefig(img2, format='png')
    img2.seek(0)
    plot_url1 = base64.b64encode(img2.getvalue()).decode('utf8')
    p2.close()
    #emfanizw ta dedomena apo stats room stats out

    return render_template( 'history.html',plot_url=plot_url, plot_url1=plot_url1,
                            htmldateroom=dateroom, htmltimeroom=timeroom, htmltemproom=temproom, htmlhumroom=humroom,
                            htmldateout=outdate, htmltimeout=outtime, htmlhumout=outhum, htmltempout=outtemp ,

                            stsdatein=sdatelist, stsavtempin=savtemplist, stsavhumin=savhumlist,
                            stsmxtmpin=smaxtemplist, stsmntmpin=smintemplist,
                            stsmxhin=smaxhumlist, stsmnhin=sminhumlist, stsroomrows=statsrowsroom,

                            stsdateout=sdatelistout, stsavtempout=savtemplistout, stsavhumout=savhumlistout,
                            stsmxtmpout=smaxtemplistout, stsmntmpout=smintemplistout,
                            stsmxhout=smaxhumlistout, stsmnhout=sminhumlistout, stsoutrows=statsrowsout )


if __name__ == "__main__":
   while 1:
    app.run(debug=True, port=serverPort, host=hostName)















