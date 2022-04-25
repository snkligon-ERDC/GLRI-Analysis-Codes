#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys


# In[2]:


# This installs the python library that is necessary to be able to easily and automatically retrieve the USGS water data
get_ipython().run_line_magic('pip', 'install -U dataretrieval')


# In[3]:


# Here are all the necessary packages to make sure that python can do all the things we want it too
from scipy import stats
import pandas as pd
import numpy as np
import datetime as dt
#from mpl_toolkits.basemap import Basemap, cm
import matplotlib.pyplot as plt
import dataretrieval.nwis as nwis


# In[4]:


#import dataretrieval.nwis as nwis


# In[5]:


# In this cell, I am specifying the site that I want to pull data in for, I have a list below with all of the site numbers and 
# there reference names. This is so that we dont need more than 1 work book for each site. However, we will have to have an 
# idea of the first retreival date, as those will need changed with each run, an estimation is enough because we can get rid
# of any nan data. They are listed beside the sum number and names. The 'end' date is the most recent rate or the current day. 


# specify the USGS site code for which we want data.
site = '411605084240800' #site name - Upstream #2021-05-21,2021-06-21
#site = '411606084240800' #site name - Diversion #2021-09-01, 2021-06-21
#site = '411607084241200' #site name - Inflow/Pumps # 021-06-21, 021-06-21
#site = '411610084240800' #site name - Outflow #2021-09-01, 2021-06-21
#site = '411607084241201' #site name - Weather Station #2021- 09-01



# get instantaneous values (iv) ( i.e. gage height, discharge where applicable)
df = nwis.get_record(sites=site, service='iv', start='2021-05-21', end='2022-01-05')

# get water quality samples (qwdata) (all nutrient and SSC data found here)
df2 = nwis.get_record(sites=site, service='qwdata', start='2021-06-21', end='2021-12-15')

# get basic info about the site including long/lat data
df3 = nwis.get_record(sites=site, service='site')


# # Basic information key cell - for any indexing problems
# #00065 = gage height data 
# #00060 = Discharge ft3/s
# #p00600 = Total Nitrogen [nitrogen + Nitrate + ammonia + organic N]
# #p00605 = Organic nitrogen
# #p00608 = Ammonia [NH3 + NH4] as N
# #p00625 = Ammonia + Organic N
# #p00631 = Nitrate + Nitrite as N
# #p00660 = Orthophosphate as PO4
# #p00665 = Phosphorus as P
# #p00671 = Orthophosphate as P
# #p00940 = Chloride
# #p71846 = Ammonia (NH3 + NH4) as NH4
# #p80154 = Suspended Sediment Concentration

# In[6]:


# Here is a check to make sure that the data is all pulling correctly, if these do not print out, reconfirm the date cell 5

print(df)
#print(df2)
#print (df3)


# ### Here is where we are going to append all of this information to a series of dataframes for us to pull later ###
# 

# In[ ]:





# In[7]:


# starting with the basic information, get lists of all the column headers
display(list(df.columns.values))
display(list(df2.columns.values))
#display(list(df3.columns.values))


# In[8]:


# starting with the basic information, get lists of all the column headers

# Remove unnecessary columns - we are going to broadly ignore the 3rd data frame as it is just holistic information
df.drop('99234', inplace=True, axis=1)
df.drop('99234_cd', inplace=True, axis=1)
df.drop('00065_cd', inplace=True, axis=1)

df2.drop(['agency_cd', 'site_no','sample_end_dt','sample_end_tm','tm_datum_rlbty_cd','coll_ent_cd','medium_cd','project_cd',
 'aqfr_cd','tu_id','body_part_id','hyd_cond_cd','samp_type_cd','hyd_event_cd','sample_lab_cm_txt'], inplace=True, axis = 1)


# In[9]:


# double check that columns were dropped
display(list(df.columns.values))
display(list(df2.columns.values))
#display(list(df3.columns.values))


# In[10]:


df.rename(columns={'00065': 'gageH', 'site_no':'site_no'}, inplace=True) #,'00060':'discharge'#
df.dropna()


# In[11]:


df['datetime'] = df.index


# In[12]:


df['datetime'] = pd.to_datetime(df['datetime'])
df


# In[13]:


df2.rename(columns={ 'p00600': "totalnitrogen", 'p00605': "organicnitrogen",'p00608': "Ammonia_N", 
                    'p00625': "AmmoniaplusOrgNitro", 'p00631': "NitrateNitrite", 'p00660': "OrthoPhos_PO4",
                    'p00665': "PasP", 'p00671': "OrthoPasP", 'p00940': "Chloride", 'p71846': "ammoniaNH4",
                    'p80154': "SSC"}, inplace=True)
df2.dropna()


# In[14]:


df2['datetime'] = df2.index


# In[15]:


df2['datetime'] = pd.to_datetime(df2['datetime'])
df2
df2.dropna()


# ### Here is the plotting code that spits out plots for gage height, discharge (where applicable), all nutrient data individually and suspended sediment concentration ###
# 

# In[16]:


# For gage height plot: 
df.plot(x='datetime', y="gageH");
plt.title('USGS Station: 411605084240800'); # station numbers will have to be copy and pasted
plt.legend(['Instanteous Gage Height'],loc='lower right');
plt.xlabel('Time');
plt.ylabel('Height (ft)');
#plt.locator_params(axis="x", nbins=10)


# In[17]:


#when discharge data is avialable - include this plot :

#df.plot(x='datetime', y="discharge");
#plt.title('USGS Station: 411605084240800');
#plt.legend(['Instanteous Discharge Values'],loc='lower right');
#plt.xlabel('Time');
#plt.ylabel('Discharge (ft^3/s)');


# In[18]:


# Nutrients Plots

df2.dtypes


# In[19]:


df2['totalnitrogen'] = df2['totalnitrogen'].str.replace('[#,<,>,*,/,d,@,&]', '')
#df2['organicnitrogen'] = df2['organicnitrogen'].str.replace('[#,,*,/,d,@,&]', '')
df2['Ammonia_N'] = df2['Ammonia_N'].str.replace('[#,,*,d,/,@,&]', '')
df2['AmmoniaplusOrgNitro'] = df2['AmmoniaplusOrgNitro'].str.replace('[#,,*,d,/,@,&]', '')
df2['NitrateNitrite'] = df2['NitrateNitrite'].str.replace('[#,<,>,*,/,d,@,&]', '')
#df2['OrthoPhos_PO4'] = df2['OrthoPhos_PO4'].str.replace('[#,,*,@,/,d,&]', '')
df2['PasP'] = df2['PasP'].str.replace('[#,,*,d,@,/,&]', '')
df2['OrthoPasP'] = df2['OrthoPasP'].str.replace('[#,,/,*,@,d,&]', '')
df2['Chloride'] = df2['Chloride'].str.replace('[#,,*,d,@,/,&]', '')
#df2['ammoniaNH4'] = df2['ammoniaNH4'].str.replace('[#,,*,/,d,@,&]', '')
df2['SSC'] = df2['SSC'].str.replace('[#,,*,d,@,/,&]', '')

df2
df2.dropna()


# In[20]:


df2.dtypes


# In[21]:


df2['totalnitrogen'] = df2['totalnitrogen'].astype(float)
#df2['organicnitrogen'] = df2['organicnitrogen'].astype(float)
df2['Ammonia_N'] = df2['Ammonia_N'].astype(float)
df2['AmmoniaplusOrgNitro'] = df2['AmmoniaplusOrgNitro'].astype(float)
df2['NitrateNitrite'] = df2['NitrateNitrite'].astype(float)
#df2['OrthoPhos_PO4'] = df2['OrthoPhos_PO4'].astype(float)
df2['PasP'] = df2['PasP'].astype(float)
df2['OrthoPasP'] = df2['OrthoPasP'].astype(float)
df2['Chloride']=df2['Chloride'].astype(float)
#df2['ammoniaNH4'] = df2['ammoniaNH4'].astype(float)
df2['SSC'] = df2['SSC'].astype(float)


# # Start of actual Nutrient Plots

# In[46]:


# Total Nitrogen
df2.plot(x='datetime', y="totalnitrogen");
plt.title('USGS Station: 411605084240800 \n Nutrient Data - Total Nitrogen '); # station numbers will have to be copy and pasted
plt.legend(['Total Nitrogen'],loc='upper right');
plt.xlabel('Time');
plt.ylabel('Total Nitrogen (mg/L)');

#organicnitrogen
df2.plot(x='datetime', y="organicnitrogen");
plt.title('USGS Station: 411605084240800 \n Nutrient Data - Organic Nitrogen'); # station numbers will have to be copy and pasted
plt.legend(['Organic Nitrogen'],loc='upper right');
plt.xlabel('Time');
plt.ylabel('Organic Nitrogen (mg/L)');

#Ammonia_N  
df2.plot(x='datetime', y="Ammonia_N");
plt.title('USGS Station: 411605084240800 \n Nutrient Data - Ammonia as Nitrogen'); # station numbers will have to be copy and pasted
plt.legend(['Ammonia as N'],loc='upper right');
plt.xlabel('Time');
plt.ylabel('Ammonia as N (mg/L)');

#AmmoniaplusOrgNitro
df2.plot(x='datetime', y="AmmoniaplusOrgNitro");
plt.title('USGS Station: 411605084240800 \n Nutrient Data - Ammonia Plus Organic Nitrogen'); # station numbers will have to be copy and pasted
plt.legend(['Ammonia + N'],loc='upper right');
plt.xlabel('Time');
plt.ylabel('Ammonia plus Organic Nitrogen (mg/L)');

#NitrateNitrite 
df2.plot(x='datetime', y="NitrateNitrite");
plt.title('USGS Station:411605084240800 \n Nutrient Data - Nitrate + Nitrite'); # station numbers will have to be copy and pasted
plt.legend(['Nitrate + Nitrite'],loc='upper right');
plt.xlabel('Time');
plt.ylabel('Nitrate + Nitrite (mg/L)');


# In[47]:


#OrthoPhos_PO4 
df2.plot(x='datetime', y="OrthoPhos_PO4");
plt.title('USGS Station: 411605084240800 \n Nutrient Data - Orthophosphate as PO4'); # station numbers will have to be copy and pasted
plt.legend(['PO4'],loc='upper right');
plt.xlabel('Time');
plt.ylabel('Orthophosphate as PO4 (mg/L)');


#PasP      
df2.plot(x='datetime', y="PasP");
plt.title('USGS Station: 411605084240800 \n Nutrient Data - Phosphorus'); # station numbers will have to be copy and pasted
plt.legend(['Phosphorus'],loc='upper right');
plt.xlabel('Time');
plt.ylabel('Phosphorus as Phosphorus (mg/L)');

#OrthoPasP
df2.plot(x='datetime', y="OrthoPasP");
plt.title('USGS Station: 411605084240800 \n Nutrient Data - Orthophosphate as Phosphorus'); # station numbers will have to be copy and pasted
plt.legend(['Phosphorus'],loc='upper right');
plt.xlabel('Time');
plt.ylabel('Orthophosphate as Phosphorus (mg/L)');

# Chloride
df2.plot(x='datetime', y="Chloride");
plt.title('USGS Station: 411605084240800 \n Nutrient Data - Chloride '); # station numbers will have to be copy and pasted
plt.legend(['Instanteous Gage Height'],loc='upper right');
plt.xlabel('Time');
plt.ylabel('Chloride (mg/L)');

#AmmoniaNH4
df2.plot(x='datetime', y="ammoniaNH4");
plt.title('USGS Station: 411605084240800 \n Nutrient Data - Ammonia as NH4'); # station numbers will have to be copy and pasted
plt.legend(['NH4'],loc='upper right');
plt.xlabel('Time');
plt.ylabel('Ammonia as NH4 (mg/L)');


# In[49]:



#SSC
df2.plot(x='datetime', y="SSC");
plt.title('USGS Station: 411605084240800 \n Nutrient Data - Suspended Sediment Concentration'); # station numbers will have to be copy and pasted
plt.legend(['Susp. Sed. Conc.'],loc='upper right');
plt.xlabel('Time');
plt.ylabel('SSC (mg/L)');

#### This command can be used to save any of the plots to the receiving folder - make sure to include the site name in title
####plt.savefig("output.png")


# In[ ]:





# In[ ]:




