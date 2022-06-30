try:
    import socket
    import threading
    import time
    import mysql.connector
except:
    print('library not found ')

HOST1 = '192.168.2.3'  # The server's hostname or IP address
PORT1 = 5008 # The port used by the server

HOST2 = '192.168.2.2'  # The server's hostname or IP address
PORT2 = 5002 # The port used by the server

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass1234!",
    database="sensor_db"
)


def my_client():
    threading.Timer(50, my_client).start()
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM ,socket.SOL_TCP)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM ,socket.SOL_TCP)
    s1.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,True)
    s1.connect((HOST1, PORT1))
    s2.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,True)
    s2.connect((HOST2, PORT2))

    if s1 :
        print("Connected 1 !")

    if s2 :
        print("Connected 2 !")
    #i = 0
    while (True):
        my_inp = 'Data'
        my_inp = my_inp.encode('utf-8')
        s1.sendall(my_inp)
        s2.sendall(my_inp)
        data1 = s1.recv(1024).decode('utf-8')
        data2 = s2.recv(1024).decode('utf-8')
        d1_d, t1_t, tmp1_tmp, h1_h = data1.split(",")
        d2_d, t2_t, tmp2_tmp, h2_h = data2.split(",")
        print("__1__ Date: " + d1_d,'Time: ' + t1_t,"Temperature: " + tmp1_tmp + " C", "Humidity: "+h1_h  + " %")
        print("__2__ Date: " + d2_d,'Time: ' + t2_t,"Temperature: " + tmp2_tmp + " C", "Humidity: "+h2_h  + " %")
        mycursor = mydb.cursor()
        sql1 = "INSERT INTO bedroom_liv (date,time,temperature,humidity) VALUES (%s,%s,%s, %s)"
        sql2 = "INSERT INTO livingroom (date,time,temperature,humidity) VALUES (%s,%s,%s, %s)"
        val1 =  [(d1_d,t1_t,tmp1_tmp,h1_h)]
        val2 =  [(d2_d,t2_t,tmp2_tmp,h2_h)]
        mycursor.executemany(sql1,val1)
        mycursor.executemany(sql2,val2)
        mydb.commit()
        print(mycursor.rowcount,"record inserted.")
        time.sleep(59.5)

if __name__ == "__main__":
    while 1:
        my_client()