from tkinter import *
import bluetooth
import matplotlib.pyplot as plt

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
            tens_digit = int(bluetoothMyoware.getchar(hex,1))
        except:
            if bluetoothMyoware.getchar(hex,1) == 'a':
                tens_digit = 10
            if bluetoothMyoware.getchar(hex,1) == 'b':
                tens_digit = 11
            if bluetoothMyoware.getchar(hex,1) == 'c':
                tens_digit = 12
            if bluetoothMyoware.getchar(hex,1) == 'd':
                tens_digit = 13
            if bluetoothMyoware.getchar(hex,1) == 'e':
                tens_digit = 14
            if bluetoothMyoware.getchar(hex,1) == 'f':
                tens_digit = 15
        
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
        
        number = 16*tens_digit + ones_digit
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