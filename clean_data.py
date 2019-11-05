import pandas as pd
import numpy as np

def known_clean_data(input_data_accel,input_data_gyro,num_punches,window,category):

    # Initial cleaning of data from raw accel to ID events.
    # Input data as Accel and Gyro data from Mbeint Labs Sensor App
    # Predetermined number of punches (num_punches)
    # Returns timestamp of event (punch) and windowed data at each event
    # for further processing prior to modeling.

    # INPUTS
    # -------------------------------------------------------------------
    # input_data_accel - .csv @ 25Hz
    # input_data_gyro - .csv @ 25Hz
    # num_punches - int - prescribed number of punches per this trial
    # window - int - how many data points before and after spike occurs
    # category - str - what category of punch (jab, left hook, etc.)


    # OUTPUT
    # -------------------------------------------------------------------
    # punch_data - list of pandas dataframes truncated into individual events
    #              with labeles and reset time for given interval

    # drop extraneous columns
    drop_cols = ['epoch (ms)','timestamp (-0800)']
    input_data_accel = input_data_accel.drop(drop_cols)
    input_data_gyro = input_data_gyro.drop(drop_cols)

    # join into single data set
    combined = pd.merge(input_data_accel,input_data_gyro,how='left',on='elapsed (s)')

    # calculate magnitude col to ID top events
    combined["magnitude"] = np.sqrt(combined["x-axis (g)"]**2+combined["y-axis (g)"]**2+combined["z-axis (g)"]**2)

    # determine row indicies of num_punches number of events
    event_index = sorted(combined.sort_values(["magnitude"],ascending=False)["elapsed (s)"].head(num_punches).to_dict())

    # find event and store window of data surrounding it
    punch_data = []
    for each in event_index:
        data_pts = window * 2 + 1
        dummy = combined.iloc[each-window:each+window+1]
        dummy["time"] = list(np.linspace(0 , data_pts * 0.04 , data_pts))
        dummy.drop('elapsed (s)')
        dummy['target'] = category
        punch_data.append(dummy)
        
    return punch_data