# This project requires PyBluez
from tkinter import *
import bluetooth

#Look for all Bluetooth devices
#the computer knows about.
print("Searching for devices...")
print("")
#Create an array with all the MAC
#addresses of the detected devices
nearby_devices = bluetooth.discover_devices()
#Run through all the devices found and list their name
num = 0
print("Select your device by entering its coresponding number...")
for i in nearby_devices:
	num+=1
	print(num , ": " , bluetooth.lookup_name( i ))

#Allow the user to select their Arduino
#bluetooth module. They must have paired
#it before hand.
selection = int(input("> ")) - 1
print("You have selected", bluetooth.lookup_name(nearby_devices[selection]))
bd_addr = nearby_devices[selection]

port = 1

sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

def getchar(string, n):
    return str(string)[n - 1]

def hex_to_dec(hex):
    try:
        tens_digit = int(getchar(hex,1))
    except:
        if getchar(hex,1) == 'a':
            tens_digit = 10
        if getchar(hex,1) == 'b':
            tens_digit = 11
        if getchar(hex,1) == 'c':
            tens_digit = 12
        if getchar(hex,1) == 'd':
            tens_digit = 13
        if getchar(hex,1) == 'e':
            tens_digit = 14
        if getchar(hex,1) == 'f':
            tens_digit = 15
    
    try:
        ones_digit = int(getchar(hex,2))
    except:
        if getchar(hex,2) == 'a':
            ones_digit = 10
        if getchar(hex,2) == 'b':
            ones_digit = 11
        if getchar(hex,2) == 'c':
            ones_digit = 12
        if getchar(hex,2) == 'd':
            ones_digit = 13
        if getchar(hex,2) == 'e':
            ones_digit = 14
        if getchar(hex,2) == 'f':
            ones_digit = 15
    
    number = 16*tens_digit + ones_digit
    return number

while True:
    data = sock.recv(1024)
    if len(str(data)) == 7:
        a = getchar(str(data),5)
        b = getchar(str(data),6)
        hex = a+b
        print(hex_to_dec(hex))
    else:
        print("ERROR")
