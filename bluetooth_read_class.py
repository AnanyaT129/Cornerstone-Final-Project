from tkinter import *
import bluetooth
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import integrate
from scipy import signal
from matplotlib.backends.backend_pdf import PdfPages
import math

class bluetoothMyoware:
    def __init__(self):
        self.addr = '00:14:03:05:0B:E7'
        self.port = 1
        self.sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    
    def bluetooth_connect(self):
        self.sock.connect((self.addr, self.port))
    
    def data_collection(self):
        self.data = self.sock.recv(1024) #what is going on w this number
        return self.data
    
    def getchar(string, n):
        return str(string)[n - 1]
    
    def hex_to_dec(hex):
                        
        try:
            sixteen_digit = int(bluetoothMyoware.getchar(hex,1))
        except:
            if bluetoothMyoware.getchar(hex,1) == 'a':
                sixteen_digit = 10
            if bluetoothMyoware.getchar(hex,1) == 'b':
                sixteen_digit = 11
            if bluetoothMyoware.getchar(hex,1) == 'c':
                sixteen_digit = 12
            if bluetoothMyoware.getchar(hex,1) == 'd':
                sixteen_digit = 13
            if bluetoothMyoware.getchar(hex,1) == 'e':
                sixteen_digit = 14
            if bluetoothMyoware.getchar(hex,1) == 'f':
                sixteen_digit = 15
        
        try:
            ones_digit = int(bluetoothMyoware.getchar(hex,2))
        except:
            if bluetoothMyoware.getchar(hex,2) == 'a':
                ones_digit = 10
            if bluetoothMyoware.getchar(hex,2) == 'b':
                ones_digit = 11
            if bluetoothMyoware.getchar(hex,2) == 'c':
                ones_digit = 12
            if bluetoothMyoware.getchar(hex,2) == 'd':
                ones_digit = 13
            if bluetoothMyoware.getchar(hex,2) == 'e':
                ones_digit = 14
            if bluetoothMyoware.getchar(hex,2) == 'f':
                ones_digit = 15
        
        number = 16*sixteen_digit + ones_digit
        return number

    def plot_data(self, x_data, y_data):
        # Create figure for plotting
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        
        # Draw plot
        ax.plot(x_data, y_data)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('EMG Data')

        # Draw the graph
        plt.show()
    
    def convert_raw_data(raw_data):
        string_data = str(raw_data)

        position = string_data.find("b'")
        
        try:
            hex = string_data[position+4]+string_data[position+5]
            value = 8*bluetoothMyoware.hex_to_dec(hex)
            print(value)
        except:
            try:
                hex = string_data[position+2]
                value = 8*ord(hex)
            except:
                value = 0
        
        value = value*5000/1023
        return value
    
    def open_data_file(filename):
        # open data file
        with open(filename) as f:
            voltage_list = f.read()

        voltage_list = voltage_list[1:len(voltage_list)-2]
        voltage_list = voltage_list.split(',')
        voltage_list = list(map(float, voltage_list))
        
        return voltage_list
    
    def make_pdf(samples, voltage_list, rms, freqs, volt_fft, t, meanfreq):
        # pdf function (only taking created graphs as data inputs)
        def make_pdf(x, y, title, xlabel, ylabel, page):
            plt.figure()
            plt.clf()

            plt.plot(x,y)
            graph = plt.title(title)
            plt.xlabel(xlabel) 
            plt.ylabel(ylabel)
            page.savefig(plt.gcf())
        
        with PdfPages('Myowearable_Analysis.pdf') as page:
            make_pdf(samples, voltage_list, 'Myoware sEMG Data', 'Samples', 'Voltage (mV)', page)
            make_pdf(samples, rms, 'RMS of sEMG Data', 'Samples', 'Voltage (mV)', page)
            make_pdf(freqs, volt_fft, 'Fourier Analysis of sEMG Data', 'Amplitude', 'Frequency (Hz)', page)
            make_pdf(t, meanfreq, 'Mean Frequency Over Time', 'Time (s)', 'Frequency (Hz)', page)
    
    def rms(N, voltage_list):
        squared_data = [0] * N
        rms = [0] * N
        for i in range(0, N):
            squared_data[i] = voltage_list[i] ** 2
        rms_squared = pd.Series(squared_data).rolling(window=15).mean()
        rms = np.sqrt(rms_squared)

        return rms
    
    def fft(voltage_list, N):

        volt_fft = np.fft.fft(voltage_list-np.mean(voltage_list)) # filtering out mean
        i = range(int(N/2))
        volt_fft = abs(volt_fft[i])*2
        
        return volt_fft
    
    def meanfreq(voltage_list, Fs, Fnyq, freqs, N):
        t = int(N/Fs)
        volt_per_sec = np.array_split(voltage_list, t)
        medfreq = []
        meanfreq = []
        for sec in volt_per_sec:
            fft = np.fft.fft(sec)
            i = range(int(len(sec)/2))
            fft = fft[i]
            fft[2:-2] = 2 * fft[2:-2]
            psd_per_sec = (1/(len(sec) * Fs)) * (abs(fft) ** 2) # psd function
            freq_per_sec = np.arange(0, Fnyq, Fs/len(sec))
            
            area_freq = integrate.cumtrapz(psd_per_sec, freq_per_sec[i], initial=0) # cumulative power at each frequency
            
            # total_power = area_freq[-1] 
            mpf = sum(area_freq * freq_per_sec[i]) / sum(area_freq) # meanfrequency
            meanfreq.append(mpf) 
            # medfreq.append([freqs[np.where(area_freq >= total_power / 2)[0][0]]]) # medfreq located where power/2
        

        return meanfreq

    def analyze_slope(t, meanfreq):
        # slope analysis 
        m, b = np.polyfit(t, meanfreq, 1) # returns slope of median frequency <- can use this for..more analysis :,)
        meanfreq_func = m*t + b
        m = np.around(m, 3)
        if m < 0 and m >= -0.5:
            print('Rate of change in MNF:', m)
            print('Slight progression of muscle fatigue. Keep going.')
        elif m < -0.5 and m < -1:
            print('Rate of change in MNF:', m)
            print('Increased progression of muscle fatigue. Consider the difficulty of the past activity as your current peak ability.')
        elif m <= -1:
            print('Rate of change in MNF:', m)
            print('Extreme progression of muscle fatigue. Take a break or choose a less strenuous activity.')
        elif m >= 0:
            print('Decrease in muscle fatigue is unexpected. Fixing sensor placement recommended.')
        else:
            print('Check sensor placement and try data collection / analysis again.')
        
        return meanfreq_func