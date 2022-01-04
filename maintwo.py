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
n=0
infdriving = 0
reckless= 0
overspeed =0
# with open('data.csv','a',newline='') as csvfile:
#     fieldnames = ['speed','coolent']
#    # writer = csv.DictWrite(csvfile)
#     writer.writeheader()
#     csvfile.close()    
with open('data.csv','a',newline='') as csvfile:
        pitter = csv.DictWriter(csvfile, fieldnames=["a","b","c"])
        pitter.writeheader()
        csvfile.close
with open('topspeed.csv','a',newline='') as csvfile:
        pitter = csv.DictWriter(csvfile, fieldnames=["date","topspeed"])
        pitter.writeheader()
        csvfile.close 
with open('reckless.csv','a',newline='') as csvfile:
        pitter = csv.DictWriter(csvfile, fieldnames=["date","reckless"])
        pitter.writeheader()
        csvfile.close
with open('ineffecient.csv','a',newline='') as csvfile:
        pitter = csv.DictWriter(csvfile, fieldnames=["date","inefficient"])
        pitter.writeheader()
        csvfile.close    
with open('overspeed.csv','a',newline='') as csvfile:
        pitter = csv.DictWriter(csvfile, fieldnames=["date","overspeed"])
        pitter.writeheader()
        csvfile.close              
while (a<2000):
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
        infdriving=infdriving+1
    if y2>4000:
        print('Recless Driving')
        reckless=reckless+1
    print(y)
    cmd2 = obd.commands.COOLANT_TEMP # select an OBD command (sensor)
    response2 = connection.query(cmd2) # send the command, and parse the response
    print(response2.value)
    response = connection.query(cmd) # send the command, and parse the response
    ref=db.reference('py/')
    now=datetime.now()

    dt_string = round(time.time()*1000)
# dtime=str(today)
    print(dt_string)

    #time.sleep(0.5)
    x = str(response.value)
    x1 = x.split(" ",1)
    x2 = float(x1[0])
    print(x2)
    if(x2>n):
        n=x2
    if(x2>110.0):
        overspeed=overspeed+1    
    a=a+1
    with open('data.csv','a',newline='') as csvfile:
        # pitter = csv.DictWriter(csvfile, fieldnames=["a","b","c"])
        # pitter.writeheader()
        writer = csv.writer(csvfile)
       # writer.writeheader()
        data=[dt_string,x2,response2]
        writer.writerow(data)
        csvfile.close() 

print(n)
dt_mili = round(time.time()*1000)
with open('topspeed.csv','a',newline='') as csvfile:
        # pitter = csv.DictWriter(csvfile, fieldnames=["a","b","c"])
        # pitter.writeheader()
        writer = csv.writer(csvfile)
       # writer.writeheader()
        data=[dt_mili,n]
        writer.writerow(data)
        csvfile.close() 
print(reckless)
with open('reckless.csv','a',newline='') as csvfile:
        # pitter = csv.DictWriter(csvfile, fieldnames=["a","b","c"])
        # pitter.writeheader()
        writer = csv.writer(csvfile)
       # writer.writeheader()
        data=[dt_mili,reckless]
        writer.writerow(data)
        csvfile.close() 
print(infdriving)
with open('ineffecient.csv','a',newline='') as csvfile:
        # pitter = csv.DictWriter(csvfile, fieldnames=["a","b","c"])
        # pitter.writeheader()
        writer = csv.writer(csvfile)
       # writer.writeheader()
        data=[dt_mili,infdriving]
        writer.writerow(data)
        csvfile.close()  
print(overspeed)
with open('overspeed.csv','a',newline='') as csvfile:
        # pitter = csv.DictWriter(csvfile, fieldnames=["a","b","c"])
        # pitter.writeheader()
        writer = csv.writer(csvfile)
       # writer.writeheader()
        data=[dt_mili,overspeed]
        writer.writerow(data)
        csvfile.close() 

data_ref.set({
    'Reckless': reckless,
    'fuelInefficient': infdriving
})