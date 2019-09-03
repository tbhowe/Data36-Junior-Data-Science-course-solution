# Package management
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
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


# create DFs of unique user actions by country

#unique first reads
uniq_first=df_firstread.groupby('country').user_id.nunique().reset_index(name='distincts').sort_values(['country'])
uniq_first['funnel']='first read'
uniq_first['rel']=1*100
#unique re-reads
uniq_re=df_lateread.groupby('country').user_id.nunique().reset_index(name='distincts').sort_values(['country'])
uniq_re['funnel']='re-read'
uniq_re['rel']=uniq_re['distincts']/uniq_first['distincts']*100
#unique subs
uniq_sub=df_subs.merge(df_firstread, how='left', left_on = 'user_id', right_on = 'user_id').groupby('country').user_id.nunique().reset_index(name='distincts').sort_values(['distincts'])
uniq_sub['funnel']='subscribe'
uniq_sub['rel']=uniq_sub['distincts']/uniq_first['distincts']*100
# unique purchasers
uniq_buy=df_buy.merge(df_firstread, how='left', left_on = 'user_id', right_on = 'user_id').groupby('country').user_id.nunique().reset_index(name='distincts').sort_values(['distincts'])
uniq_buy['funnel']='buy'
uniq_buy['rel']=uniq_buy['distincts']/uniq_first['distincts']*100

# funnel with absolute values
funnel_setup=pd.concat([uniq_first, uniq_re, uniq_sub, uniq_buy], axis=0)

#funnel by percentage of first-readers from a given country
rel_funnel_setup=pd.concat([ uniq_re, uniq_sub, uniq_buy], axis=0)

#plot absolute country funnel graph
fg=sns.catplot(x="country", y="distincts", hue="funnel", data=funnel_setup,
                height=6,aspect=3, kind="bar", palette="muted")

#save as pdf
plt.savefig('dilan_funnel_by_country_abs.pdf')