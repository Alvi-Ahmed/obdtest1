from re import X
import obd
import time
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin import db
import csv

cred=credentials.Certificate('ServiceAccountKey.json')

firebase_admin.initialize_app(cred,{
    'databaseURL':'https://driver-analysis-273c5-default-rtdb.firebaseio.com/'
})
ref=db.reference('py/')
now=datetime.now()

dt_string = now.strftime('%d-%m-%Y %H-%M-%S')
# dtime=str(today)
print(dt_string)

data_ref=ref.child(dt_string)
# data_ref=ref.c hild('Data_Collection')


# connection = obd.OBD(protocol="7", baudrate="9600", fast=False)
#connection = obd.OBD(baudrate=38400, fast=False)
#connection = obd.OBD() # auto-connects to USB or RF port
connection = obd.OBD("/dev/pts/2")


r= connection.status()
print(r)
a=0
i=1
infdriving = False
reckless= True
# with open('data.csv','a',newline='') as csvfile:
#     fieldnames = ['speed','coolent']
#    # writer = csv.DictWrite(csvfile)
#     writer.writeheader()
#     csvfile.close()    
while (a<100):
    cmd = obd.commands.SPEED # select an OBD command (sensor)
    cmd3 = obd.commands.RPM
    cmd4=obd.commands.THROTTLE_ACTUATOR
    response3 = connection.query(cmd3) # send the command, and parse the response
    response4 = connection.query(cmd4) # send the command, and parse the response
    print(response4.value)
    y = str(response3.value)
    y1=y.split(" ",1)
    y2=float(y1[0])
    if y2>3000:
        print('fuel inefficient Driving')
        infdriving=True
    if y2>4000:
        print('Recless Driving')
        reckless=True
    print(y)
    cmd2 = obd.commands.COOLANT_TEMP # select an OBD command (sensor)
    response2 = connection.query(cmd2) # send the command, and parse the response
    print(response2.value)
    response = connection.query(cmd) # send the command, and parse the response
    ref=db.reference('py/')
    now=datetime.now()

    dt_string = now.strftime('%d-%m-%Y %H-%M-%S')
# dtime=str(today)
    print(dt_string)

    #time.sleep(0.5)
    x = str(response.value)
    print(x)
    a=a+1
    with open('data.csv','a',newline='') as csvfile:
        pitter = csv.DictWriter(csvfile, fieldnames=["a","b","c"])
        pitter.writeheader()
        writer = csv.writer(csvfile)
       # writer.writeheader()
        data=[dt_string,response,response2]
        writer.writerow(data)
        csvfile.close() 

 

data_ref.set({
    'Reckless': reckless,
    'fuelInefficient': infdriving
})