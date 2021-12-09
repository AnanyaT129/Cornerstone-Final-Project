import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy import integrate
from scipy import signal
from matplotlib.backends.backend_pdf import PdfPages

# open data file
with open('output.txt') as f:
    voltage_list = f.read()

voltage_list = voltage_list[1:len(voltage_list)-2]
voltage_list = voltage_list.split(',')
voltage_list = list(map(float, voltage_list))

figure, axes = plt.subplots(2, 2)
figure.tight_layout(pad=2.5)

# pdf function (only taking created graphs as data inputs)
def make_pdf(x, y, title, xlabel, ylabel, page):
    plt.figure()
    plt.clf()

    plt.plot(x,y)
    graph = plt.title(title)
    plt.ylabel(xlabel) 
    plt.xlabel(ylabel)
    page.savefig(plt.gcf())

# analysis sampling rate, frequencies, etc. 
N = len(voltage_list)
samples = range(N)
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
plt.plot(samples, rms, '-b')
rms_ax.title.set_text('RMS of sEMG Data')
rms_ax.set_ylabel('Voltage (mV)') 
rms_ax.set_xlabel('Samples')

# GRAPH 3: Discrete Fourier Transform --> Frequency Domain
fft_ax = plt.subplot(2, 2, 3)
volt_fft = np.fft.fft(voltage_list-np.mean(voltage_list)) # filtering out mean
i = range(int(N/2)+1)

volt_fft = abs(volt_fft[i])*2
fft_ax.set_xlim([0, Fnyq])
plt.plot(freqs, volt_fft, '-b')
fft_ax.title.set_text('Fourier Analysis of sEMG Data')
fft_ax.set_ylabel('Amplitude') 
fft_ax.set_xlabel('Frequency (Hz)')

# GRAPH 4: Median Frequency over Time - kind of sketchy atm
freq, psd = signal.periodogram(voltage_list, fs = Fs)
psd_per_sec = np.array_split(psd, int(len(psd) / (N/Fs))) # break PSD into arrays containing 1s of data
medfreq = []

for power in psd_per_sec:
    
    freq_per_sec = np.arange(0, Fnyq, Fnyq/len(power)) 
    area_freq = integrate.cumtrapz(power, freq_per_sec, initial=0) # cumulative power at each frequency
    total_power = area_freq[-1] 
    medfreq.append([freqs[np.where(area_freq >= total_power / 2)[0][0]]]) # medfreq located where power/2

med_ax = plt.subplot(2, 2, 4)
t = np.arange(len(medfreq))
plt.plot(t, medfreq, 'o') # need to figure out why len(medfreq) != 16...
m, b = np.polyfit(t, medfreq, 1) # returns slope of median frequency <- can use this for..more analysis :,)
medfreq_func = m*t + b
plt.plot(t, medfreq_func, 'g')
med_ax.title.set_text('Median Frequency Over Time')
med_ax.set_ylabel('Frequency (Hz)') 
med_ax.set_xlabel('Time (s)') 

plt.show()

with PdfPages('Myowearable_Analysis.pdf') as page:
    make_pdf(samples, voltage_list, 'Myoware sEMG Data', 'Samples', 'Voltage (mV)', page)
    make_pdf(samples, rms, 'RMS of sEMG Data', 'Voltage (mV)', 'Samples', page)
    make_pdf(freqs, volt_fft, 'Fourier Analysis of sEMG Data', 'Amplitude', 'Frequency (Hz)', page)
    make_pdf(t, medfreq, 'Median Frequency Over Time', 'Time (s)', 'Frequency (Hz)', page)
