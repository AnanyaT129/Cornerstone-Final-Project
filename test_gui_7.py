from tkinter import *
from matplotlib import pyplot as plt
from matplotlib import animation as animation
import numpy as np
from bluetooth_read_class import bluetoothMyoware as btm
import pandas as pd

myowearable = btm()
raw_data_full = []

root = Tk()
root.title('Test Gui 7')

# create all of the main containers
top_frame = Frame(root, bg='lavender', width=450, height=50, pady=3)
btm_frame = Frame(root, bg='white', width=450, height=45, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
btm_frame.grid(row=1, sticky="ew")

# Functions for top frame
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
def start():
    start_sensor_collection()

def stop():
    print("STOPPED")
    stop_sensor_collection()

def connect():
    try:
        myowearable.bluetooth_connect()
        result = "connected"
        print(result)
    except:
        result = "FAILED"
        print(result)
    return result

def connection_label(label):
    def update():
        result = connect()
        if result == "connected":
            label.config(text=str(result))
        else:
            label.config(text=str(result))
            label.after(1000, update)
    update()

def save_data():
    with open('output.txt', 'w') as output:
        output.write(str(raw_data_full))

def get_sensor_value():
    data = myowearable.data_collection()
    result = btm.convert_raw_data(data)
    return result

# Parameters
x_len = 200         # Number of points to display
y_range = [0, 6000]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
ax.set_ylim(y_range)

analysis = fig.add_subplot(212)
analysis.set_ylim([0,6000])

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

# Add labels
plt.title('TMP102 Temperature over Time')
plt.xlabel('Samples')
plt.ylabel('Temperature (deg C)')

# This function is called periodically from FuncAnimation
def animate(i, ys):

    # Read temperature (Celsius) from TMP102
    emg_value = get_sensor_value()
    
    raw_data_full.append(emg_value)

    # Add y to list
    ys.append(emg_value)

    # Limit y list to set number of items
    ys = ys[-x_len:]

    # Update line with new Y values
    line.set_ydata(ys)

    return line,

def start_sensor_collection():
    raw_data_full.clear()
    ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=50,
    blit=True)
    plt.show()

def stop_sensor_collection():
    plt.close(fig)

# create the widgets for the top frame
quit_button = Button(top_frame, text="Quit", command=_quit)
start_button = Button(top_frame, text="Start", command=start)
stop_button = Button(top_frame, text="Stop", command=stop)
connect_button = Button(top_frame, text="Connect",command=connect)
connect_label = Label(top_frame)
status_label = Label(top_frame, text="Connection Status: ")
save_button = Button(top_frame, text="Save", command=save_data)

# layout the widgets in the top frame
quit_button.grid(row=1, column=6)
start_button.grid(row=1, column=2)
stop_button.grid(row=1, column=4)
connect_button.grid(row=1, column=0)
status_label.grid(row=1, column=8)
connect_label.grid(row=1, column=10)
connection_label(connect_label)
save_button.grid(row=1, column = 14)

root.mainloop()