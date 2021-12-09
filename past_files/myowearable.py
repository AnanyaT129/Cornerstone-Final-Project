from bluetooth_read_class import bluetoothMyoware as btm
import datetime as dt

myowearable = btm()
myowearable.bluetooth_connect()
emg_values = []
x_time = []

for x in range(0,30):
    data = myowearable.data_collection()

    if len(str(data)) == 7:
        a = btm.getchar(str(data),5)
        b = btm.getchar(str(data),6)
        hex = a+b
        point = btm.hex_to_dec(hex)
        print(point)
        print(myowearable.data)
    else:
        print("ERROR")
        point = 0
    
    emg_values.append(point)
    x_time.append(dt.datetime.now().strftime('%H:%M:%S.%f'))

myowearable.plot_data(x_time,emg_values)
