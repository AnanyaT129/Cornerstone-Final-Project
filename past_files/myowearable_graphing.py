from bluetooth_read_class import bluetoothMyoware as btm
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

# Parameters
x_len = 200         # Number of points to display
y_range = [0, 300]  # Range of possible Y values to display


# Create figure for plotting
plt.style.use('ggplot')
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)
emg_values = [0] * 10
line, = ax.plot(xs, ys)

# Format plot
plt.xticks(rotation=45, ha='right')
plt.title('EMG Values over Time')

# This function is called periodically from FuncAnimation
def animate(i, ys):

    # Read temperature (Celsius) from TMP102
    data = myowearable.data_collection()

    string_data = str(data)
    while True:
        position = string_data.find('x')
        
        hex = string_data[position+1]+string_data[position+2]
        for x in range(0,10):
            try:
                point = btm.hex_to_dec(hex)
                print(point)
                emg_values[x] = point
            except:
                print("ERROR")
                print(hex)
                point = 0
            
            if len(string_data) < 5:
                break
            string_data = string_data[position+3:]
        
        if len(string_data) < 5:
            break
        string_data = string_data[position+3:]
        
        time.sleep(1)
        
        # Add x and y to lists
        # xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        ys.extend(emg_values)

        # Limit y list to set number of items
        ys = ys[-x_len:]

        # Update line with new Y values
        line.set_ydata(ys)

        return line,

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=50,
    blit=True)
plt.show()
