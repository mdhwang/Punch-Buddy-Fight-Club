import pandas as pd
import numpy as np
import pickle
from datetime import datetime

def known_clean_data(input_data_accel,input_data_gyro,num_punches,window,category):

    # Initial cleaning of data from raw accel to ID events.
    # Input data as Accel and Gyro data from Mbeint Labs Sensor App
    # Predetermined number of punches (num_punches)
    # Returns timestamp of event (punch) and windowed data at each event
    # for further processing prior to modeling.

    # INPUTS
    # -------------------------------------------------------------------
    # input_data_accel - pandas df
    # input_data_gyro - pandas df
    # num_punches - int - prescribed number of punches per this trial
    # window - int - how many data points before and after spike occurs
    # category - str - what category of punch (jab, left hook, etc.)


    # OUTPUT
    # -------------------------------------------------------------------
    # punch_data - json object containing cleaning params and data of punches
    #              params - dict of dict {category, num_punches, window}
    #              data -  list of pandas dataframes containing sensor data with target labels.  

    # drop extraneous columns
    drop_cols = ['epoch (ms)','time (-08:00)']
    input_data_accel = input_data_accel.drop(drop_cols,axis=1)
    input_data_gyro = input_data_gyro.drop(drop_cols,axis=1)
    input_data_gyro = input_data_gyro.drop(['elapsed (s)'],axis=1)
    

    # join into single data set
    combined = input_data_accel.merge(input_data_gyro,how="outer", left_index=True, right_index=True)

    # calculate magnitude col to ID top events
    combined["magnitude"] = np.sqrt(combined["X-Axis (g)"]**2+combined["Y-Axis (g)"]**2+combined["Z-Axis (g)"]**2)

    # determine row indicies of num_punches number of events
    event_index = sorted(combined.sort_values(["magnitude"],ascending=False)["elapsed (s)"].head(num_punches).to_dict())

    # find event and store window of data surrounding it
    punch_data = []
    for each in event_index:
        data_pts = window * 2 + 1
        dummy = combined.iloc[each-window:each+window+1]
        dummy["time step"] = list(np.linspace(0 , data_pts * 0.04 , data_pts))
        dummy['target'] = category
        dummy = dummy.drop(['elapsed (s)'],axis=1)
        punch_data.append(dummy)
    
    data_obj = {}
    data_obj['params'] = {}
    data_obj['params']['category'] = category
    data_obj['params']['num_punches'] = num_punches
    data_obj['params']['window'] = window
    data_obj['data'] = punch_data
    
    current_time = datetime.now().strftime("%m.%d.%Y, %H.%M.%S")
    with open('/Users/matthewhwang/Galvanize/fightclub/data/processed/{}/{} {} win{} - {}.p'.format(category,category,num_punches,window,current_time), 'wb') as f:
        pickle.dump(data_obj, f)

    print("Stored {} {} win{} - {} successfully".format(category,num_punches,window,current_time))
    
    
    return data_obj