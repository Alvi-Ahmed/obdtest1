import obd
import time

# connection = obd.OBD(protocol="7", baudrate="9600", fast=False)
#connection = obd.OBD(baudrate=38400, fast=False)
#connection = obd.OBD() # auto-connects to USB or RF port
connection = obd.OBD("/dev/pts/1")


r= connection.status()
print(r)
a=0
while (a<1):
    cmd = obd.commands.SPEED # select an OBD command (sensor)
    cmd3 = obd.commands.RPM
    response3 = connection.query(cmd3) # send the command, and parse the response
    print(response3.value)
    cmd2 = obd.commands.COOLANT_TEMP # select an OBD command (sensor)
    response2 = connection.query(cmd2) # send the command, and parse the response
    print(response2.value)
    response = connection.query(cmd) # send the command, and parse the response
    print(response.value) # returns unit-bearing values thanks to Pint
#time.sleep(0.5)