from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from numpy import False_, arange, sin, pi
import random

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
btm_frame.grid(row=3, sticky="ew")

# create the widgets for the top frame
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
def start():
    print("Hello World")

def stop():
    print("STOPPED")

quit_button = Button(top_frame, text="Quit", command=_quit)
start_button = Button(top_frame, text="Start", command=start)
stop_button = Button(top_frame, text="Stop", command=stop)

# layout the widgets in the top frame
quit_button.grid(row=1, column=4)
start_button.grid(row=1, column=0)
stop_button.grid(row=1, column=2)

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

ys = [0] * 30

def readSensors():
    for x in range(0,30):
        if x < 29:
           ys[x] = ys[x+1] 
        else:
            ys[29] = random.choice([0, 1, 2, 3, 4, 5])
    
    output_1.set(ys[20])
    output_2.set(ys[21])
    output_3.set(ys[22])
    output_4.set(ys[23])
    output_5.set(ys[24])
    output_6.set(ys[25])
    output_7.set(ys[26])
    output_8.set(ys[27])
    output_9.set(ys[28])
    output_10.set(ys[29])
    
    ctr_left.after(100, readSensors)

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

value0 = str(1)

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

x = np.arange(0, 30, 1)        # x-array

def animate(i):
    line.set_ydata(ys)  # update the data
    return line,

canvas = FigureCanvasTkAgg(fig, ctr_mid)  # A tk.DrawingArea.
#canvas.draw()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, btm_frame)
toolbar.update()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

ax = fig.add_subplot(111)
ax.set_ylim([0,6])
line, = ax.plot(x, ys)
ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=True)

ctr_left.after(100,readSensors)
root.mainloop()