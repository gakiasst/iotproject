import time
import mysql.connector
import mysql.connector
import datetime
import functools
import numpy as np
import matplotlib.pyplot as plt
import os
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass1234!",
    database="sensor_db"
)
if mydb:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")

#============== DATA FROM DATA_HOUSE KAI UPDATE STATS ROOM
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
        #print('SAME DATE')
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
        #print('> DATE')
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
#print('ROOM')
print(datelist)
count += 1
datadates = count
print(datadates, ' DIFFERENT DATES IN DATA_HOUSE ')
for y in range(0, datadates):
    fulldate = datelist[y]
    finalldate = fulldate.strftime('%Y-%m-%d')
    mxt = str(maxtemplist[y])
    mnt = str(mintemplist[y])
    mxh = str(maxhumlist[y])
    mnh = str(minhumlist[y])
    avt = str(avtemplist[y])
    avh = str(avhumlist[y])
    print("DATE: " + finalldate,
          'MAXTEMP: ' + mxt,
          'MINTEMP: ' + mnt,
          'MAXHUM: ' + mxh,
          'MINHUM: ' + mnh,
          'AVTEMP: ' + avt,
          'AVHUM: ' + avh)

mycursor = mydb.cursor()
mycursor.execute("SELECT COUNT(*) FROM stats_room")
number = mycursor.fetchall()
totalrows = functools.reduce(lambda sub, ele: sub * 10 + ele, number)
statsrows = functools.reduce(lambda sub, ele: sub * 10 + ele, totalrows)
print(statsrows)
for k in range(statsrows, datadates):
    fulldate1 = datelist[k]
    finalldate = fulldate1.strftime('%Y-%m-%d')
    mxt = str(maxtemplist[k])
    mnt = str(mintemplist[k])
    mxh = str(maxhumlist[k])
    mnh = str(minhumlist[k])
    avt = str(avtemplist[k])
    avh = str(avhumlist[k])
    datadb = (finalldate, avt, avh, mxt, mnt, mxh, mnh)
    sql = "INSERT INTO stats_room (date,av_temperature," \
          "av_humidity,max_temperature,min_temperature," \
          "max_humidity,min_humidity) VALUES (%s, %s,%s,%s, %s, %s, %s)"
    mycursor.execute(sql, datadb)
    mydb.commit()



#============== DATA FROM DATA_OUT KAI UPDATE STATS_OUT===========================
#=================================================================================


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
avtemplistout.insert(countout, 0)
avhumlistout.insert(countout, 0)
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
        #print('SAME DATE')
        if   tempout < mintemplistout[countout]:
            mintemplistout[countout] = tempout
        if   tempout > maxtemplistout[countout]:
            maxtemplistout[countout] = tempout
        if   humout < minhumlistout[countout]:
            minhumlistout[countout] = humout
        if   humout > maxhumlistout[countout]:
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
        synolotempout = ftempout
        synolohumout = fhumout
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
#print('OUT')
print(datelistout)
countout += 1
dataoutdates = countout
print(dataoutdates,' DIFFERENT DATES IN DATA_OUT')
for y in range(0, dataoutdates):
    fulldateout = datelistout[y]
    finalldateout = fulldateout.strftime('%Y-%m-%d')
    mxtout = str(maxtemplistout[y])
    mntout = str(mintemplistout[y])
    mxhout = str(maxhumlistout[y])
    mnhout = str(minhumlistout[y])
    avtout = str(avtemplistout[y])
    avhout = str(avhumlistout[y])
    print("DATE: " + finalldateout,
          'MAXTEMP: ' + mxtout,
          'MINTEMP: ' + mntout,
          'MAXHUM: ' + mxhout,
          'MINHUM: ' + mnhout,
          'AVTEMP: ' + avtout,
          'AVHUM: ' + avhout)

mycursor = mydb.cursor()
mycursor.execute("SELECT COUNT(*) FROM stats_out")
numberout = mycursor.fetchall()
totalrowsout = functools.reduce(lambda sub, ele: sub * 10 + ele, numberout)
statsoutrows = functools.reduce(lambda sub, ele: sub * 10 + ele, totalrowsout)
print(statsoutrows)
for k in range(statsoutrows, dataoutdates):
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

#finalldate, mxt, mnt, mxh, mnh
