import datetime
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
import xgboost as xgb
import random
import zipfile
import time
import shutil
from sklearn.metrics import log_loss


##Read the app_event
app_events = pd.read_csv("../input/app_events.csv")
##Read the app labels
app_labels = pd.read_csv("../input/app_labels.csv",dtype={'app_id': np.str,'label_id': np.str})
##Read the label descriptions
labels = pd.read_csv("../input/label_categories.csv",dtype={'label_id': np.str})

##Mearge the app_labels with the labels
app_total = pd.merge(app_labels, labels, how='left', left_on='label_id',right_on='label_id')

#Work on the app_events
convert_to_bin(app_events, 'is_active')

##drop the installed
app_events.drop("is_installed",axis=1,inplace=True)

##Now the merge the app events with the app descriptions
app_des = pd.merge(app_events,app_total,how="left", left_on = "app_id", right_on="app_id")

##Save it to the folder for future uses
app_des.to_csv("../input/app_info_merged.csv",index=False)

##Read it to test if that one works
app_info = pd.read_csv("../input/app_info_merged.csv",dtype={'event_id': np.str})

##Now read the event_data

df_events = pd.read_csv("../input/events.csv")

##convert the time feature
df_events['month'] = pd.to_datetime(df_events.timestamp).dt.month
df_events['year'] = pd.to_datetime(df_events.timestamp).dt.year
df_events['day'] = pd.to_datetime(df_events.timestamp).dt.day


##Group by device_id find out how much event_id for each count
df_events['counts'] = df_events.groupby(['device_id'])['event_id'].transform('count')

#Now merge the df_events with app_info
event_summary = pd.merge(df_events, app_info, how="left", on=["event_id"])
















def convert_to_bin(data, f):
    print "making bins of %s" % f
    for bin in range(min(data[f]), max(data[f]) + 1):
        data[f + "_" + str(bin)] = data[f].apply(lambda x: 1 if x == bin else 0)
    data.drop([f], axis=1, inplace=True)
