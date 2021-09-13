import obd
import time

# connection = obd.OBD(protocol="7", baudrate="9600", fast=False)
connection = obd.OBD(baudrate=38400, fast=False)
r= connection.status()
print(r)
# connection = obd.OBD() # auto-connects to USB or RF port

cmd = obd.commands.SPEED # select an OBD command (sensor)
cmd2 = obd.commands.COOLANT_TEMP # select an OBD command (sensor)
response2 = connection.query(cmd2) # send the command, and parse the response
print(response2.value)

response = connection.query(cmd) # send the command, and parse the response

print(response.value) # returns unit-bearing values thanks to Pint
print(response.value.to("mph")) # user-friendly unit conversions
time.sleep(0.5)