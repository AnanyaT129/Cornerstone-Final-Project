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

fig = plt.Figure()

x = np.arange(0, 2*np.pi, 0.01)        # x-array

def animate(i):
    line.set_ydata(np.sin(x+i/10.0))  # update the data
    return line,

canvas = FigureCanvasTkAgg(fig, ctr_mid)  # A tk.DrawingArea.
#canvas.draw()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, btm_frame)
toolbar.update()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

ax = fig.add_subplot(111)
line, = ax.plot(x, np.sin(x))
ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=True)

output_header = Label(ctr_left, text="Raw Output")
output_header.pack(side=TOP)

def readSensors():
    output_1.set(random.choice([0, 1, 2, 3, 4, 5]))
    output_2.set(random.choice([0, 1, 2, 3, 4, 5]))
    output_3.set(random.choice([0, 1, 2, 3, 4, 5]))
    output_4.set(random.choice([0, 1, 2, 3, 4, 5]))
    ctr_left.after(1000, readSensors)

output_1 = StringVar()
output_2 = StringVar()
output_3 = StringVar()
output_4 = StringVar()

measuredValues = [0, 1, 2, 3, 4, 5]
value0 = str(measuredValues[0])
value1 = str(measuredValues[1])
value2 = str(measuredValues[2])
value3 = str(measuredValues[3])

output_1.set(value0)
output_2.set(value1)
output_3.set(value2)
output_4.set(value3)

output_1_label = Label(ctr_left, textvariable=output_1)
output_1_label.pack(side=TOP)

output_2_label = Label(ctr_left, textvariable=output_2)
output_2_label.pack(side=TOP)

output_3_label = Label(ctr_left, textvariable=output_3)
output_3_label.pack(side=TOP)

output_4_label = Label(ctr_left, textvariable=output_4)
output_4_label.pack(side=TOP)

warning_header = Label(ctr_right, text="Status")
warning_header.pack(side=TOP)

ctr_left.after(1000,readSensors)
root.mainloop()
