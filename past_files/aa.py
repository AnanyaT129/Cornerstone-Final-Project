# This project requires PyBluez
from tkinter import *
import bluetooth

#Look for all Bluetooth devices the computer knows about.
print("Searching for devices...")
print("")
#Create an array with all the MAC addresses of the detected devices
nearby_devices = bluetooth.discover_devices()
#Run through all the devices found and list their name
num = 0
print("Select your device by entering its coresponding number...")
for i in nearby_devices:
	num+=1
	print(num , ": " , bluetooth.lookup_name( i ))

#Allow the user to select their Arduino bluetooth module. They must have paired it before hand.
selection = int(input("> ")) - 1
print("You have selected", bluetooth.lookup_name(nearby_devices[selection]))
bd_addr = nearby_devices[selection]

port = 1

sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))


# Python3 code to demonstrate converting hexadecimal string to decimal
# Using ast.literal_eval()
from ast import literal_eval
    
data =(sock.recv(1024))
print(data)
while True:
    def getchar(string, n):
        return str(string)[n - 1]
    data=(sock.recv(1024))
    a=getchar(data,3)
    b=getchar(data,4)
    c=getchar(data,5)
    d=getchar(data,6)
    hex=a+b+c+d
    print(hex)
    
