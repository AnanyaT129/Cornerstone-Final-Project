from tkinter import *
from matplotlib import pyplot as plt
from matplotlib import animation as animation
import numpy as np
import sys

sys.path.append("/Users/sakib/OneDrive/Desktop/Final_Project_Cornerstone")

from bluetooth_read_class import bluetoothMyoware as btm

myowearable = btm()
raw_data_full = [1.0] * 40

root = Tk()
root.title('Test Gui 9')

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
    with open('/Users/sakib/OneDrive/Desktop/Final_Project_Cornerstone/output.txt', 'w') as output:
        output.write(str(raw_data_full))
    
    plt.close()
    myowearable.bluetooth_disconnect()
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def start():
    start_sensor_collection()

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

def get_sensor_value():
    data = myowearable.data_collection()
    result = btm.convert_raw_data(data)
    return result

# Parameters
x_len = 200         # Number of points to display
y_range = [0, 6000]  # Range of possible Y values to display

# Create figure for plotting
fig = plt.figure()
fig.tight_layout(pad=2.5)
ax = fig.add_subplot(2, 1, 1)
xs = list(range(0, 200))
ys = [0] * x_len
y_rms = [0] * x_len
ax.set_ylim(y_range)

analysis = fig.add_subplot(212)
analysis.set_ylim([0,18000])
analysis.axes.get_yaxis().set_visible(False)

# Create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)
line_2, = analysis.plot(xs, y_rms, 'r')

# Add labels
ax.set_title('SEMG Over Time')
ax.set_xlabel('Samples')
ax.set_ylabel('Voltage (mV)')

analysis.set_title('RMS Smoothing of Data')
analysis.set_xlabel('Samples')

def animate_setup(ys, y_rms, raw_data_full):
    # Read SEMG Value from sensor
    emg_value = get_sensor_value()
    raw_data_full.append(emg_value)

    # Add y to list
    ys.append(emg_value)

    new_rms = btm.root_mean_square(ys[-15:])
    y_rms.append(new_rms)

    # Limit y list to set number of items
    ys = ys[-x_len:]
    y_rms = y_rms[-x_len:]

    point_dict = {"ys_points": ys, "y_rms_points": y_rms}
    
    return point_dict

# This function is called periodically from FuncAnimation
def animate(i, ys):
    points = animate_setup(ys, y_rms, raw_data_full)

    ys_points = points["ys_points"]
    y_2_points = points["y_rms_points"]

    # Update line with new Y values
    line.set_ydata(ys_points)
    line_2.set_ydata(y_2_points)

    return line, line_2,

def start_sensor_collection():
    raw_data_full.clear()
    ani = animation.FuncAnimation(fig,
    animate,
    fargs=(ys,),
    interval=50,
    blit=True)
    plt.show()

# analysis sampling rate, frequencies, etc. 
list_of_data = btm.open_data_file('/Users/sakib/OneDrive/Desktop/Final_Project_Cornerstone/output.txt')
N = len(list_of_data)
samples = range(N)
Fs = 40; # in Hz
Fnyq = Fs / 2
freqs = np.arange(0, Fnyq, Fs/N)

rms = btm.rms(N, list_of_data)
volt_fft = btm.fft(list_of_data, N)
meanfreq = btm.meanfreq(list_of_data, Fs, Fnyq, freqs, N)
t = range(int(N/Fs))
meanfreq_func = btm.analyze_slope(t, meanfreq)

def analysis_setup(list_of_data, N, samples, Fnyq, freqs, rms, volt_fft, meanfreq, t):
    figure, axes = plt.subplots(2, 2)
    figure.tight_layout(pad=2.5)

    # GRAPH 1: Voltage vs. Samples (Myoware Output)
    ax = plt.subplot(2, 2, 1)
    ax.set_ylim([0,6000])
    ax.set_xlim([0, 500])
    plt.plot(samples, list_of_data, '-k')
    ax.title.set_text('Myoware sEMG Data')
    ax.set_ylabel('Voltage (mV)') 
    ax.set_xlabel('Samples')

    # GRAPH 2: RMS vs. Samples
    # RMS to smooth out data
    rms_ax = plt.subplot(2, 2, 2)
    rms_ax.set_ylim([0, 6000])
    rms_ax.set_xlim([0, 500])
    plt.plot(samples, rms, '-b')
    rms_ax.title.set_text('RMS of sEMG Data')
    rms_ax.set_ylabel('Voltage (mV)') 
    rms_ax.set_xlabel('Samples')

    # GRAPH 3: Discrete Fourier Transform --> Frequency Domain
    fft_ax = plt.subplot(2, 2, 3)
    fft_ax.set_xlim([0, Fnyq])
    i = range(int(N/2))
    freqs = freqs[i]
    plt.plot(freqs, volt_fft, '-b')
    fft_ax.title.set_text('Fourier Analysis of sEMG Data')
    fft_ax.set_ylabel('Amplitude') 
    fft_ax.set_xlabel('Frequency (Hz)')

    # GRAPH 4: Mean Frequency over Time 
    med_ax = plt.subplot(2, 2, 4)
    plt.plot(t, meanfreq, '-k') 
    plt.plot(t, meanfreq_func, '--b')
    med_ax.title.set_text('Mean Frequency Over Time')
    med_ax.set_ylabel('Frequency (Hz)') 
    med_ax.set_xlabel('Time (s)')

    plt.show()

def analyze():
    analysis_setup(list_of_data, N, samples, Fnyq, freqs, rms, volt_fft, meanfreq, t)

def save_data_pdf():
    btm.make_pdf(samples, list_of_data, rms, freqs[range(int(N/2))], volt_fft, t, meanfreq, meanfreq_func)

# create the widgets for the top frame
quit_button = Button(top_frame, text="Quit and Save", command=_quit)
start_button = Button(top_frame, text="Start", command=start)
connect_button = Button(top_frame, text="Connect",command=connect)
connect_label = Label(top_frame)
status_label = Label(top_frame, text="Connection Status: ")
analysis_button = Button(top_frame, text="Open Graphs", command=analyze)
save_data_button = Button(top_frame, text="Save Data to PDF", command=save_data_pdf)

# layout the widgets in the top frame
quit_button.grid(row=1, column=6)
start_button.grid(row=1, column=2)
connect_button.grid(row=1, column=0)
status_label.grid(row=1, column=10)
connect_label.grid(row=1, column=12)
connection_label(connect_label)
analysis_button.grid(row=2, column = 0)
save_data_button.grid(row=2, column = 6)

# bottom frame function
def threshold_color(frame, ys):
    def update():
        value = ys[-1]
        if value >= 2443.79276637:
            frame.config(bg = 'red')
            frame.after(100, update)
        elif value >= 2000 and value < 2443.79276637:
            frame.config(bg = 'yellow')
            frame.after(100, update)
        else:
            frame.config(bg = 'green')
            frame.after(25, update)
    update()

threshold_color(btm_frame, ys)

root.mainloop()