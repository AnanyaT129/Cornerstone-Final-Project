from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from bluetooth_read_class import bluetoothMyoware as btm
import pandas as pd

myowearable = btm()

root = Tk()
root.title('Test Gui')
root.geometry('{}x{}'.format(460, 350))

# create all of the main containers
top_frame = Frame(root, bg='lavender', width=450, height=50, pady=3)
center = Frame(root, width=50, height=40, padx=3, pady=3)
btm_frame = Frame(root, bg='white', width=450, height=45, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=5, sticky="ew")

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

# create the widgets for the top frame
quit_button = Button(top_frame, text="Quit", command=_quit)
start_button = Button(top_frame, text="Start", command=start)
stop_button = Button(top_frame, text="Stop", command=stop)
connect_button = Button(top_frame, text="Connect",command=connect)
connect_label = Label(top_frame)
status_label = Label(top_frame, text="Connection Status: ")

# layout the widgets in the top frame
quit_button.grid(row=1, column=6)
start_button.grid(row=1, column=2)
stop_button.grid(row=1, column=4)
connect_button.grid(row=1, column=0)
status_label.grid(row=1, column=8)
connect_label.grid(row=1, column=10)
connection_label(connect_label)

# create the center widgets
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

ctr_left = Frame(center, width=100, height=190)
ctr_mid = Frame(center, width=250, height=190, padx=3, pady=3)
ctr_right = Frame(center, bg='green', width=100, height=190, padx=3, pady=3)

ctr_left.grid(row=0, column=0, sticky="ns")
ctr_mid.grid(row=0, column=1, sticky="nsew")
ctr_right.grid(row=0, column=2, sticky="ns")

output_header = Label(ctr_left, text="Raw Output")
output_header.pack(side=TOP)

ys = [0] * 200

def get_sensor_value():
    data = myowearable.data_collection()
    result = btm.convert_raw_data(data)
    return result

def readSensors():
    for x in range(0,200):
        if x < 199:
           ys[x] = ys[x+1] 
        else:
            ys[199] = get_sensor_value()
    
    output_1.set(ys[190])
    output_2.set(ys[191])
    output_3.set(ys[192])
    output_4.set(ys[193])
    output_5.set(ys[194])
    output_6.set(ys[195])
    output_7.set(ys[196])
    output_8.set(ys[197])
    output_9.set(ys[198])
    output_10.set(ys[199])
    
    ctr_left.after(25, readSensors)

output_1 = StringVar()
output_2 = StringVar()
output_3 = StringVar()
output_4 = StringVar()
output_5 = StringVar()
output_6 = StringVar()
output_7 = StringVar()
output_8 = StringVar()
output_9 = StringVar()
output_10 = StringVar()

value0 = str(0)

output_1.set(value0)
output_2.set(value0)
output_3.set(value0)
output_4.set(value0)
output_5.set(value0)
output_6.set(value0)
output_7.set(value0)
output_8.set(value0)
output_9.set(value0)
output_10.set(value0)

output_1_label = Label(ctr_left, textvariable=output_1)
output_1_label.pack(side=TOP)

output_2_label = Label(ctr_left, textvariable=output_2)
output_2_label.pack(side=TOP)

output_3_label = Label(ctr_left, textvariable=output_3)
output_3_label.pack(side=TOP)

output_4_label = Label(ctr_left, textvariable=output_4)
output_4_label.pack(side=TOP)

output_5_label = Label(ctr_left, textvariable=output_5)
output_5_label.pack(side=TOP)

output_6_label = Label(ctr_left, textvariable=output_6)
output_6_label.pack(side=TOP)

output_7_label = Label(ctr_left, textvariable=output_7)
output_7_label.pack(side=TOP)

output_8_label = Label(ctr_left, textvariable=output_8)
output_8_label.pack(side=TOP)

output_9_label = Label(ctr_left, textvariable=output_9)
output_9_label.pack(side=TOP)

output_10_label = Label(ctr_left, textvariable=output_10)
output_10_label.pack(side=TOP)

warning_header = Label(ctr_right, text="Status")
warning_header.pack(side=TOP)

fig = plt.Figure()

x = np.arange(0, 200, 1)        # x-array

def animate(i):
    line.set_ydata(ys)  # update the data
    line_2.set_ydata(rmsv)
    return line, line_2,

canvas = FigureCanvasTkAgg(fig, ctr_mid)  # A tk.DrawingArea.
#canvas.draw()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, btm_frame)
toolbar.update()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

ax = fig.add_subplot(211)
ax.set_ylim([0,6000])
ax.set_ylabel("milivolts")
line, = ax.plot(x, ys)
rmsv = pd.Series(np.array(ys)).rolling(window=15).mean()
line_2, = ax.plot(x,rmsv, 'r')
ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=True)

def start_sensor_collection():
    ctr_left.after(25,readSensors)

def stop_sensor_collection():
    ctr_left.after_cancel()

analysis = fig.add_subplot(212)
analysis.set_ylim([0,6000])

root.mainloop()