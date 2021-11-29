import numpy as np
from matplotlib import pyplot as plt
import math
from numpy.core.numeric import ones
import pandas as pd
from scipy import integrate
from matplotlib.backends.backend_pdf import PdfPages

# open data file
with open('bicep.txt') as f:
    voltage_list = f.read()

voltage_list = voltage_list[1:len(voltage_list)-2]
voltage_list = voltage_list.split(',')
voltage_list = list(map(float, voltage_list))
figure, axes = plt.subplots(2, 2)
figure.tight_layout(pad=2.5)

# pdf function (only taking created graphs as data inputs)
def make_pdf(x, y, title, xlabel, ylabel, style, page):
    plt.figure()
    plt.clf()

    plt.plot(x, y, style)
    graph = plt.title(title)
    plt.ylabel(ylabel) 
    plt.xlabel(xlabel)
    page.savefig(plt.gcf())

# analysis sampling rate, frequencies, etc. 
N = len(voltage_list)
samples = np.arange(0, N)
Fs = 40; # in Hz
Fnyq = Fs / 2
freqs = np.arange(0, Fnyq, Fs/N)


# GRAPH 1: Voltage vs. Samples (Myoware Output)
ax = plt.subplot(2, 2, 1)
ax.set_ylim([0,6000])
ax.set_xlim([0, 500])
plt.plot(samples, voltage_list, '-k')
ax.title.set_text('Myoware sEMG Data')
ax.set_ylabel('Voltage (mV)') 
ax.set_xlabel('Samples')

# GRAPH 2: RMS vs. Samples
# RMS to smooth out data
squared_data = [0] * N
rms = [0] * N
for i in range(0, N):
     squared_data[i] = voltage_list[i] ** 2
rms_squared = pd.Series(squared_data).rolling(window=15).mean()
rms = np.sqrt(rms_squared)

rms_ax = plt.subplot(2, 2, 2)
rms_ax.set_ylim([0, 6000])
rms_ax.set_xlim([0, 500])
plt.plot(samples, rms, '-r')
rms_ax.title.set_text('RMS of sEMG Data')
rms_ax.set_ylabel('Voltage (mV)') 
rms_ax.set_xlabel('Samples')

# GRAPH 3: Discrete Fourier Transform --> Frequency Domain
fft_ax = plt.subplot(2, 2, 3)
volt_fft = np.fft.fft(voltage_list-np.mean(voltage_list)) # filtering out mean
i = range(int(N/2))
volt_fft = abs(volt_fft[i])*2
fft_ax.set_xlim([0, Fnyq])
freqs = freqs[i]
plt.plot(freqs, volt_fft, '-b')
fft_ax.title.set_text('Fourier Analysis of sEMG Data')
fft_ax.set_ylabel('Amplitude') 
fft_ax.set_xlabel('Frequency (Hz)')

# GRAPH 4: Mean Frequency over Time 
t = int(N/Fs)
volt_per_sec = np.array_split(voltage_list, t)
medfreq = []
meanfreq = []
count = 0
for sec in volt_per_sec:
    fft = np.fft.fft(sec)
    i = range(int(len(sec)/2))
    fft = fft[i]
    fft[2:-2] = 2 * fft[2:-2]
    psd_per_sec = (1/(len(sec) * Fs)) * (abs(fft) ** 2) # psd function
    freq_per_sec = np.arange(0, Fnyq, Fs/len(sec))
    
    area_freq = integrate.cumtrapz(psd_per_sec, freq_per_sec[i], initial=0) # cumulative power at each frequency
    
    total_power = area_freq[-1] 
    mpf = sum(area_freq * freq_per_sec[i]) / sum(area_freq) # meanfrequency
    meanfreq.append(mpf) 
    medfreq.append([freqs[np.where(area_freq >= total_power / 2)[0][0]]]) # medfreq located where power/2

med_ax = plt.subplot(2, 2, 4)
t = range(t)

plt.plot(t, meanfreq, '-k') 
m, b = np.polyfit(t, meanfreq, 1) # returns slope of mean frequency 
meanfreq_func = m*t + b
plt.plot(t, meanfreq_func, '--b')

med_ax.title.set_text('Mean Frequency Over Time')
med_ax.set_ylabel('Frequency (Hz)') 
med_ax.set_xlabel('Time (s)') 
plt.show()

with PdfPages('Myowearable_Analysis.pdf') as page:
    make_pdf(samples, voltage_list, 'Myoware sEMG Data', 'Samples', 'Voltage (mV)', '-k', page)
    make_pdf(samples, rms, 'RMS of sEMG Data', 'Voltage (mV)', 'Samples', '-r', page)
    make_pdf(freqs, volt_fft, 'Fourier Analysis of sEMG Data', 'Amplitude', 'Frequency (Hz)', '-k', page)
    make_pdf(t, meanfreq, 'Mean Frequency Over Time', 'Time (s)', 'Frequency (Hz)', '-b', page)

# slope analysis 
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