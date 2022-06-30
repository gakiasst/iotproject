try:
    import socket
    import threading
    import time
    import mysql.connector
except:
    print('library not found ')
HOST = '192.168.2.7'   # The server's hostname or IP address
PORT = 5006  # The port used by the server
#connection with Database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass1234!",
    database="sensor_db"
)
def my_client():
    threading.Timer(50, my_client).start()    # giving thread parameters
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)  # define socket TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)   # keep socket open
    s.connect((HOST, PORT))     # connect with server
    if s:
        print("Connected with Raspberry!")
    while (True):
        my_inp = 'Data'
        my_inp = my_inp.encode('utf-8')
        s.sendall(my_inp)   #  sending to server a message to get Data (temperature/humidity)
        data = s.recv(1024).decode('utf-8')   # getting  server Data
        dt1_dt , tim1_t, t1_t, h1_h = data.split(",")   #  spliting Incoming Data
        print("Date: " + dt1_dt, 'Time: ' + tim1_t, "Temperature: " + t1_t + " C", "Humidity: "+h1_h + " %")
        # saving Data in Database
        mycursor = mydb.cursor()
        sql1 = "INSERT INTO data_out (date,time,temperature,humidity) VALUES (%s,%s,%s, %s)"
        #sql2 = "INSERT INTO last_room (date,time,temperature,humidity) VALUES (%s,%s,%s, %s)"
        val = [(dt1_dt, tim1_t, t1_t, h1_h)]
        mycursor.executemany(sql1, val)
        #mycursor.executemany(sql2, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        time.sleep(59.5)  # wait 1 minute for the next Data

if __name__ == "__main__":
    while 1:
        my_client()

