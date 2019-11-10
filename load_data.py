import pandas as pd
import numpy as np
import pickle
from datetime import datetime
import glob

def load_data():
    # Combines all data in load data folder in processed directory
    # Standardizes data accross all
    # Returns X and Y numpy arrays ready to be split into test and training sets

    print("Load Data Begin")
    path = '/Users/matthewhwang/Galvanize/fightclub/data/processed/load_data/'

    cypher = {"Left Jab": 1,
              "Right Cross": 2,
              "Left Hook": 3,
              "Right Hook": 4}

    files = [f for f in glob.glob(path + "*.p")]

    master = []
    labels = []
    megaframe = pd.DataFrame()
    for each in files:
        data = pickle.load(open(each,'rb'))
        category = cypher[data['params']['category']]
        for i in range(len(data['data'])):
            labels.append(category)
        for event in data['data']:
            master.append(event)
            megaframe = megaframe.append(event)
    
    std = megaframe.std()
    mean = megaframe.mean()

    standardized = []
    for each in master:
        standardized.append(standardize(each,std,mean))

    return np.array(standardized),np.array(labels)

def standardize(df,std,mean):
    return np.array((df-mean)/std)