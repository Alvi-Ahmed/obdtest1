from re import X
import obd
import time
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore

from firebase_admin import db
import google.cloud

import csv

cred=credentials.Certificate('ServiceAccountKey.json')

firebase_admin.initialize_app(cred,{
    'databaseURL':'https://sampledatabasedevexpert.firebaseio.com/'
})
store = firestore.client()
ref=db.reference('py/')
now=datetime.now()

file_path = "take1.csv"

collection_name = "newData"





def batch_data(iterable, n=1):

    l = len(iterable)

    for ndx in range(0, l, n):

        yield iterable[ndx:min(ndx + n, l)]





data = []

headers = []

with open(file_path) as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')

    line_count = 0

    for row in csv_reader:

        if line_count == 0:

            for header in row:

                headers.append(header)

            line_count += 1

        else:

            obj = {}

            for idx, item in enumerate(row):

                obj[headers[idx]] = item

            data.append(obj)

            line_count += 1

    print(f'Processed {line_count} lines.')



for batched_data in batch_data(data, 499):

    batch = store.batch()

    for data_item in batched_data:

        doc_ref = store.collection(collection_name).document()

        batch.set(doc_ref, data_item)

    batch.commit()



print('Done')

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
        writer = csv.writer(csvfile)
       # writer.writeheader()
        data=[dt_string,response,response2]
        writer.writerow(data)
        csvfile.close() 

 

data_ref.set({
    'Reckless': reckless,
    'fuelInefficient': infdriving
})