'''This file contains the entire MEA_analyzer pipeline, contained in functions'''
# Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy.stats import norm
import h5py
import os

# Global values
global electrode_amnt
global well_amnt
global filename
global threshold_value
global spike_values


'''Test the library functions with a nice message'''
def get_nice_message(message="Enjoy your day!"):
    print(message)
    return message


'''Bandpass function'''
def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Call this one
def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


'''Threshold function - returns threshold value'''
def threshold(data, hertz):
    measurements=data.shape[0]
    # The amount is samples needed to for a 50ms window is calculated
    windowsize = 0.05 * hertz
    windowsize = int(windowsize)
    # Create a temporary list that will contain 50ms windows of data
    windows = []

    # Iterate over the electrode data and create x amount of windows containing *windowsize* samples each
    # For this it is pretty important that the data consists of a multitude of 1000 datapoints
    for j in range(0, measurements, windowsize):
        windows.append(data[j:j+windowsize])
    windows = np.array(windows) #convert into np.array
    # Create an empty list where all the data identified as spike-free noise will be stored
    noise=[]

    # Now iterate over every 50ms time window and check whether it is "spike-free noise"
    for j in range(0,windows.shape[0]):
        # Calculate the mean and standard deviation
        mu, std = norm.fit(windows[j])
        stdevmultiplier = 5
        # Check whether the minimum/maximal value lies outside the range of x (defined above) times the standard deviation - if this is not the case, this 50ms box can be seen as 'spike-free noise'
        if not(np.min(windows[j])<(-1*stdevmultiplier*std) or np.max(windows[j])>(stdevmultiplier*std)):
            # 50ms has been identified as noise and will be added to the noise paremeter
            noise = np.append(noise, windows[j][:])

    # Calculate the RMS
    RMS=np.sqrt(np.mean(noise**2))
    threshold_value=5*RMS

    # Calculate the % of the file that was noise
    noisepercentage=noise.shape[0]/data.shape[0]
    print(f'{noisepercentage*100}% of data identified as noise')
    return threshold_value


'''Spike detection and validation'''
def spikes(data, electrode, threshold, hertz, spikeduration, exit_time_s, amplitude_drop, plot_validation):
    # Identify points above and beneath the threshold
    above_threshold = data > threshold
    beneath_threshold = data < -threshold

    # Half of the spike duration in amount of samples, used to establish the window around a spike
    half_spikeduration_samples = int((spikeduration * hertz)/2)

    # Iterate over the data
    for j in range(0, data.shape[0]):
    # Check whether a positive or negative spike is detected at this datapoint
        if above_threshold[j] or beneath_threshold[j]:
            # Calculate the the upper and lower boundary
            lower_boundary = j-half_spikeduration_samples
            upper_boundary = j+half_spikeduration_samples
            # Make sure that the boundaries do not go out of bound of the dataset (e.g. when there is a spike in the first or last milisecond of the dataset)
            if lower_boundary < 0:
                lower_boundary = 0
            if upper_boundary > data.shape[0]:
                upper_boundary = data.shape[0]
            # Checks whether this is the absolute maximum value within the give timeframe, if it is not, the peak will be removed
            if (np.max(abs(data[(lower_boundary):(upper_boundary)])))>(abs(data[j])):
                above_threshold[j]=False
                beneath_threshold[j]=False
    for j in range(0, data.shape[0]):
        # Remove cases where 2 consecutive values are exactly the same, leading to a single ap registering as 2
        if (above_threshold[j] and above_threshold[j+1]):
            above_threshold[j]=False
        if (beneath_threshold[j] and beneath_threshold[j+1]):
            beneath_threshold[j]=False
    spikes=np.logical_or(above_threshold, beneath_threshold)
    spikes_before_DMP=spikes.copy()
    time_seconds = np.arange(0, data.shape[0]) / hertz

    # Implement dynamic multi-phasic event detection method
    # The exit time in amount of samples, used to establish the window around a spike
    exit_time = round(exit_time_s * hertz)
    thresholdmultiplier=amplitude_drop
    heightexception=2
    for j in range(0, data.shape[0]):
        # Checks whether there is a spike detected here
        if spikes[j]:
            # Check if there is a window of data to be checked after the spike. If the spike happens too close to the start or end of the measurement-
            # it cannot be confirmed, and will be removed.
            if j+exit_time>data.shape[0]:
                spikes[j]=False
            if j-exit_time<0:
                spikes[j]=False
            # Check if the voltage has reached a minimal change value of 2*Treshold since the detected spike
            # For positive spikes
            if data[j]>0:
                if not(np.min(data[j-exit_time:j+exit_time+1])<(data[j]-thresholdmultiplier*threshold)):
                    # Spikes that have an amplitude of twice the threshold, do not have to drop amplitude in a short time
                    if not(data[j]>heightexception*threshold):
                        # If not, the spike will be removed
                        spikes[j]=False
            else:
            # For negative spikes
                if not(np.max(data[j-exit_time:j+exit_time+1])>(data[j]+thresholdmultiplier*threshold)):
                    # Spikes that have an amplitude of twice the threshold, do not have to drop amplitude in a short time
                    if not(data[j]<heightexception*-1*threshold):
                        # If not, the spike will be removed
                        spikes[j]=False
    if plot_validation:
        # Plot the MEA signal
        plt.cla()

        time_seconds = np.arange(0, data.shape[0]) / hertz
        plt.plot(time_seconds, data, linewidth=0.2, zorder=-1)
        
        # Plot the threshold
        plt.axhline(y=threshold, color='k', linestyle='-', linewidth=1) 
        plt.axhline(y=-threshold, color='k', linestyle='-', linewidth=1) 

        # Plot red dots at rejected spikes
        plt.scatter(time_seconds[spikes_before_DMP], data[spikes_before_DMP], color='red', marker='o', s=3)

        # Plot green dots at accepted spikes
        plt.scatter(time_seconds[spikes], data[spikes], color='green', marker='o', s=3)
        
        # Calculate MEA electrode
        electrode_nr = electrode % electrode_amnt + 1
        well = round(electrode / electrode_amnt + 0.505)

        # Plot layout
        # Enlarge size of plot figure
        plt.rcParams["figure.figsize"] = (22,5)
        plt.title(f"Dataset: {filename} - Well: {well} - Electrode: {electrode_nr} - Threshold: {threshold} - Spikes detected before DMP: {np.sum(spikes_before_DMP)}, after: {np.sum(spikes)}")
        plt.xlabel("Time in seconds")
        plt.ylabel("Micro voltage")
        plt.xlim([time_seconds.min(), time_seconds.max()])
        plt.ylim([np.min(data)*1.2, np.max(data)*1.2])
        plt.show()
    return spikes
                    

'''Open the HDF5 file'''
def openHDF5(adress):
    with h5py.File(adress, "r") as file_data:
        # Returns HDF5 dataset objects
        dataset = file_data["Data"]["Recording_0"]["AnalogStream"]["Stream_0"]["ChannelData"] 
        # Convert to numpy array: (Adding [:] returns a numpy array)
        data = dataset[:]
    return data


'''Analyse a single electrode'''
def analyse_electrode(data, electrodes, low_cutoff, high_cutoff, order, hertz, spikeduration, exit_time_s, amplitude_drop, plot_validation):
    for electrode in electrodes:
        print(f'Analyzing {filename} - Electrode: {electrode}')
        # Filter the data
        data[electrode]=butter_bandpass_filter(data[electrode], low_cutoff, high_cutoff, hertz, order)
        # Calculate the threshold
        print(f'Calculating the threshold')
        threshold_value=threshold(data[electrode], hertz)
        print(f'Threshold for {filename} set at: {threshold_value}')
        # Calculate spike values
        print('Validating the spikes')
        spike_values=spikes(data[electrode], electrode, threshold_value, hertz, spikeduration, exit_time_s, amplitude_drop, plot_validation)


'''Analyse the entire dataset'''
def analyse_dataset(data, low_cutoff, high_cutoff, order, hertz, spikeduration, exit_time_s, amplitude_drop, plot_validation):
    return


''' Get all of the MEA files in a folder '''
def get_files(MEA_folder):
    # Get all files from MEA folder 
    all_files = os.listdir(MEA_folder)

    MEA_files = []
    # Get all HDF5 files
    for file in all_files:
        # Convert file to right format
        file = "{0}/{1}".format(MEA_folder, file)

        # Check if file is HDF5 file
        if not file.endswith(".h5"):
            print("'{0}' is no HDF5 file!".format(file))
            continue

        # Check if HDF5 file can be opened
        try:
            h5_file = h5py.File(file, "r")
        except:
            print("'{0}' can not be opened as HDF5 file!".format(file))
            continue

        # Check if HDF5 MEA dataset object exist
        try:
            h5_file["Data"]["Recording_0"]["AnalogStream"]["Stream_0"]["ChannelData"]
        except:
            print("'{0}' has no MEA dataset object!".format(file))
            continue

        # Create list with all MEA files
        MEA_files.append(file)

    # Print all HDF5 MEA files
    print("\nList with all HDF5 MEA files:")
    for file in MEA_files:
        print(file)
    
    return MEA_files