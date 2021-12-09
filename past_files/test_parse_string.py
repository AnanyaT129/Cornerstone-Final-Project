from bluetooth_read_class import bluetoothMyoware as btm
import datetime as dt
import time

myowearable = btm()
while True:
    try:
        myowearable.bluetooth_connect()
        print("connected")
        break
    except:
        print("FAILED")
        continue

# Create figure for plotting
xs = []
ys = []

# Read temperature (Celsius) from TMP102
data = myowearable.data_collection()

string_data = str(data)
#print(string_data)
while True:
    position = string_data.find('x')
    #print(position)
    
    hex = string_data[position+1]+string_data[position+2]
    print(hex)
    try:
        point = btm.hex_to_dec(hex)
    except:
        print("ERROR")
        print(hex)
        point = 0
    
    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(point)
    #print(ys)
    
    string_data = string_data[position+3:]
    #print(string_data)
    
    #print(len(string_data))
    if len(string_data) < 5:
        break
    
    time.sleep(1)
        
