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

sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1
sock.connect((bd_addr, port))

try:
    while True:
        data = sock.recv(1024)
        if not data:
            print("no data")
            break
        print("Received", data)
except OSError:
    pass
