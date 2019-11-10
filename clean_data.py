import pandas as pd
import numpy as np
import pickle
from datetime import datetime
import os
import glob


def process_staging():
    # Processes all new data in staging folder
    # Spits out to processed folder

    print("Process Staging Data Begin")
    path = '/Users/matthewhwang/Galvanize/fightclub/data/staging'
    folders = []
    
    # Gets file paths for all folders in staging
    for r, d, f in os.walk(path):
        for folder in d:
            folders.append(os.path.join(r, folder))

    # From each folder get csv path for each accel and gyro
    # Calls Known Clean Data function to process and store
    for each in folders:
        files = [f for f in glob.glob(folders[0] + "**/*.csv")]
        accel_data = pd.read_csv(files[0])
        gyro_data = pd.read_csv(files[1])
        name = files[0].split('/')[-1].split(' ')
        category = name[0] + " " + name[1]
        count = int(name[2])
        user = name[3]
        known_clean_data(accel_data,gyro_data,count,8,category,user)
        print("Did one")
    print("Finished")
    pass


def known_clean_data(accel_data,gyro_data,num_punches,window,category,user):

    # Initial cleaning of data from raw accel to ID events.
    # Input data as Accel and Gyro data from Mbeint Labs Sensor App
    # Predetermined number of punches (num_punches)
    # Returns timestamp of event (punch) and windowed data at each event
    # for further processing prior to modeling.

    # INPUTS
    # -------------------------------------------------------------------
    # accel_data - pandas df
    # gyro_data - pandas df
    # num_punches - int - prescribed number of punches per this trial
    # window - int - how many data points before and after spike occurs
    # category - str - what category of punch (jab, left hook, etc.)
    # user - who dun it

    # OUTPUT
    # -------------------------------------------------------------------
    # punch_data - json object containing cleaning params and data of punches
    #              params - dict of dict {category, num_punches, window}
    #              data -  list of pandas dataframes containing sensor data with target labels.  

    # drop extraneous columns
    drop_cols = ['epoch (ms)','time (-08:00)']
    accel_data = accel_data.drop(drop_cols,axis=1)
    gyro_data = gyro_data.drop(drop_cols,axis=1)
    gyro_data = gyro_data.drop(['elapsed (s)'],axis=1)
    

    # join into single data set
    combined = accel_data.merge(gyro_data,how="outer", left_index=True, right_index=True)

    # calculate magnitude col to ID top events
    combined["magnitude"] = np.sqrt(combined["X-Axis (g)"]**2+combined["Y-Axis (g)"]**2+combined["Z-Axis (g)"]**2)

    # determine row indicies of num_punches number of events
    event_index = sorted(combined.sort_values(["magnitude"],ascending=False)["elapsed (s)"].head(num_punches).to_dict())

    # magnitude unnecessary once used to ID location of events
    combined = combined.drop(["elapsed (s)","magnitude"],axis=1)

    combined['category'] = category

    # find event and store window of data surrounding it
    punch_data = []
    for each in event_index:
        punch_data.append(combined.iloc[each-window:each+window+1])
    
    data_obj = {}
    data_obj['params'] = {}
    data_obj['params']['category'] = category
    data_obj['params']['num_punches'] = num_punches
    data_obj['params']['window'] = window
    data_obj['params']['fighter'] = user
    data_obj['data'] = punch_data
    
    current_time = datetime.now().strftime("%m.%d.%Y, %H.%M.%S")
    with open('/Users/matthewhwang/Galvanize/fightclub/data/processed/{}/{} {} win{} - {}.p'.format(category,category,num_punches,window,current_time), 'wb') as f:
        pickle.dump(data_obj, f)

    print("Stored {} {} win{} - {} successfully".format(category,num_punches,window,current_time))
    
    
    return data_obj