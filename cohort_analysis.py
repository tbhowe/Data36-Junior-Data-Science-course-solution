''' 
This script generates a cohort analysis of user retention, with cohorts specified by the week 
on which a user read their first article.

The user was considered "retained" in a given week if they returned to the site to perform any action.

Once loaded, the data are as follows: 

df_firstread - a PANDAS dataframe of first visits to the blog, with columns:  
 my_datetime 
 event
 country
 user_id
 source
 topic
 ch_group
 my_week

df_subs, df_buy, df_lateread - 3 PANDAS dataframes of subsequent actions taken on the blog, with columns:
 my_datetime
 event
 user_id
 my_week

Required INPUTS: 
Folder "CSV", placed inside the directory you run this script from, containing:
D_subs.csv
D_buy.csv 
D_firstreads.csv
D_latereads.csv  

script OUTPUTS:

PDF file "dilan_cohort_output.pdf"
 
'''


# Package management
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from datetime import datetime
import matplotlib.dates as mdates
import os

#load data from CSV
fileDir = os.path.dirname(os.path.realpath('__file__'))

filename = os.path.join(fileDir, 'CSV/D_subs.csv')
df_subs=pd.read_csv(filename, delimiter = ';', names = ['my_datetime', 'event', 'user_id'])

filename = os.path.join(fileDir, 'CSV/D_buy.csv')
df_buy=pd.read_csv(filename, delimiter = ';', names = ['my_datetime', 'event', 'user_id','price'])

filename = os.path.join(fileDir, 'CSV/D_firstreads.csv')
df_firstread=pd.read_csv(filename, delimiter = ';', names = ['my_datetime', 'event', 'country', 'user_id','source', 'topic'])

filename = os.path.join(fileDir, 'CSV/D_latereads.csv')
df_lateread=pd.read_csv(filename, delimiter = ';', names = ['my_datetime', 'event', 'country', 'user_id','topic'])



#datetime columns expanded to create cohort group (firstread only!) , and week on which event occurred.
df_firstread['my_datetime']=pd.to_datetime(df_firstread['my_datetime']) 
df_firstread['ch_group'] = df_firstread.my_datetime.dt.week.astype('int32')
df_firstread['my_week'] = df_firstread['ch_group']

df_lateread['my_datetime']=pd.to_datetime(df_lateread['my_datetime']) 
df_lateread['my_week'] = df_lateread.my_datetime.dt.week.astype('int32')

df_buy['my_datetime']=pd.to_datetime(df_buy['my_datetime']) 
df_buy['my_week'] = df_buy.my_datetime.dt.week.astype('int32')

df_subs['my_datetime']=pd.to_datetime(df_subs['my_datetime']) 
df_subs['my_week'] = df_subs.my_datetime.dt.week.astype('int32')

#combine all "read" events
df_allreads=pd.concat([df_firstread[['user_id', 'my_week']],df_lateread[['user_id','my_week']], df_subs[['user_id','my_week']],df_buy[['user_id','my_week']]], axis=0)

# merge with firstreads for additional info
df_allreads2=df_allreads.merge(df_firstread[['user_id', 'ch_group']],how='left', left_on = 'user_id', right_on = 'user_id')
df_lateread2=df_lateread.merge(df_firstread[['user_id', 'ch_group']],how='left', left_on = 'user_id', right_on = 'user_id')

#cohort dataframes
hortplot=df_allreads2.groupby(['ch_group','my_week']).user_id.nunique().reset_index(name='unique_users')
hortplot2=df_lateread2.groupby(['ch_group','my_week']).user_id.nunique().reset_index(name='unique_users')

# normalised by users and week
hortnormed=hortplot2.copy(deep=True)
hortnormed['unique_users']=hortnormed.groupby('ch_group').unique_users.transform(lambda x: (x  / x.max()))
hortnormed['my_week']=hortnormed.groupby('ch_group').my_week.transform(lambda x: (x- min(x)))

# ------ 'classic' cohort heatmap ------
cohortmap=hortnormed.pivot(index='ch_group',columns='my_week',values='unique_users')
sns.set(style='white')
sns.set_palette("YlOrBr", 10)
plt.figure(figsize=(12, 8))
plt.title('Cohorts: User Retention')

sns.heatmap(cohortmap, mask=cohortmap.isnull(), annot=True, fmt='.0%')

#save as pdf
plt.savefig('dilan_cohort_output.pdf')

