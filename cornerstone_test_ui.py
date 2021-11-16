from tkinter import *

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np


root = Tk()
frame = Frame(root)
frame.pack()

root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=TOP, anchor=NW, fill=Y, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=TOP, anchor=NW, fill=Y, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def start():
    print("Hello World")

def stop():
    print("STOPPED")

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

button = Button(bottomframe, text="Quit", command=_quit)
button.pack(side=RIGHT)

button = Button(bottomframe, text="Start", command=start)
button.pack(side=LEFT)

button = Button(bottomframe, text="Stop", command=stop)
button.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(side = RIGHT)

def printData(point):
    label = Label(rightframe, text=point)
    label.pack()

printData(2)

mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.