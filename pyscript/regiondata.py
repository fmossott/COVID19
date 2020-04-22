# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import glob
import argparse
import os

# %%
home=os.path.dirname(__file__)+"/../"

# %%
df = pd.read_csv(home+'/COVID-19/dati-regioni/dpc-covid19-ita-regioni.csv')
regdata = pd.read_csv(home+'/other_info/regionData.csv')


# %%
files=glob.glob(home+'/addons-dati-regioni/*.csv')
files.sort()

dfs = [ pd.read_csv(f) for f in files ]


# %%
df = pd.concat(dfs+[df],ignore_index=True)


# %%
# rename columns
df = df.rename(columns={
    'stato': 'Country',
    'codice_regione': 'Region Code',
    'denominazione_regione': 'Region',
    'ricoverati_con_sintomi': 'Other Hospitalized',
    'terapia_intensiva': 'Intensive Care', 
    'totale_ospedalizzati': 'Hospitalized',
    'isolamento_domiciliare': 'Quarantined',
    'totale_positivi': 'Active Cases',
    'variazione_totale_positivi': 'Daily Active Cases',
    'dimessi_guariti': 'Recovered',
    'deceduti': 'Deaths',
    'totale_casi': 'Total Cases',
    'tamponi': 'Tests',
    'casi_testati': 'Tested People'
    })

df = df.astype({
    'Other Hospitalized':'Int32', 
    'Intensive Care':'Int32', 
    'Hospitalized':'Int32', 
    'Quarantined': 'Int32', 
    'Active Cases': 'Int32', 
    'Daily Active Cases': 'Int32', 
    'Recovered':'Int32',
    'Deaths':'Int32',
    'Total Cases':'Int32',
    'Tests':'Int32',
    'Tested People':'Int32'
    })


# %%
df['Last Update'] = pd.to_datetime(df['data'])
df['Date'] = pd.to_datetime(df['data']).dt.floor('D')


# %%
df.dtypes


# %%
prev = df[['Date', 'Region', 'Total Cases', 'Deaths', 'Recovered', 'Tests', 'Active Cases',\
    'Hospitalized', 'Quarantined', 'Intensive Care', 'Other Hospitalized', 'Tested People']]

prev = prev.rename(columns={'Total Cases':'Prev Total Cases', 'Deaths':'Prev Deaths', 'Recovered':'Prev Recovered', 'Tests':'Prev Tests',\
    'Active Cases':'Prev Active Cases', 'Hospitalized':'Prev Hospitalized', 'Quarantined':'Prev Quarantined',\
    'Intensive Care':'Prev Intensive Care', 'Other Hospitalized':'Prev Other Hospitalized', 'Tested People':'Prev Tested People'})
prev['Date'] = prev['Date']+pd.to_timedelta(1,unit='D')

# %%
prev2 = df[['Date','Region','Total Cases','Tests']]
prev2 = prev2.rename(columns={'Total Cases':'Prev2 Total Cases', 'Tests':'Prev2 Tests'})
prev2['Date'] = prev2['Date']+pd.to_timedelta(2,unit='D')


# %%
prev7 = df[['Date','Region','Total Cases','Deaths','Recovered','Tests','Active Cases', 'Hospitalized', 'Quarantined', 'Intensive Care', 'Other Hospitalized', 'Tested People']]

prev7 = prev7.rename(columns={\
    'Total Cases':'Prev7 Total Cases', 'Deaths':'Prev7 Deaths', 'Recovered':'Prev7 Recovered', 'Tests':'Prev7 Tests',\
    'Active Cases':'Prev7 Active Cases', 'Hospitalized':'Prev7 Hospitalized', 'Quarantined':'Prev7 Quarantined',\
    'Intensive Care':'Prev7 Intensive Care',  'Other Hospitalized':'Prev7 Other Hospitalized', 'Tested People':'Prev7 Tested People'})
prev7['Date'] = prev7['Date']+pd.to_timedelta(7,unit='D')

# %%
merge=df.merge(prev, on=['Date','Region'], how="left")\
    .merge(prev2, on=['Date','Region'], how="left")\
    .merge(prev7, on=['Date','Region'], how="left")\
    .merge(regdata, on=['Region'], how='left')


# %%
merge['Daily Cases'] = merge['Total Cases'] - merge['Prev Total Cases']
merge['Daily Deaths'] = merge['Deaths'] - merge['Prev Deaths']
merge['Daily Recovered'] = merge['Recovered'] - merge['Prev Recovered']
merge['Daily Tests'] = merge['Tests'] - merge['Prev Tests']
merge['Daily Hospitalized'] = merge['Hospitalized'] - merge['Prev Hospitalized']
merge['Daily Quarantined'] = merge['Quarantined'] - merge['Prev Quarantined']
merge['Daily Intensive Care'] = merge['Intensive Care'] - merge['Prev Intensive Care']
merge['Daily Other Hospitalized'] = merge['Other Hospitalized'] - merge['Prev Other Hospitalized']
merge['Daily Tested People'] = merge['Tested People'] - merge['Prev Tested People']

merge['Previous Daily Cases'] = merge['Prev Total Cases'] - merge['Prev2 Total Cases']

merge['Weekly Cases'] = merge['Total Cases'] - merge['Prev7 Total Cases']
merge['Weekly Deaths'] = merge['Deaths'] - merge['Prev7 Deaths']
merge['Weekly Recovered'] = merge['Recovered'] - merge['Prev7 Recovered']
merge['Weekly Tests'] = merge['Tests'] - merge['Prev7 Tests']
merge['Weekly Active Cases'] = merge['Active Cases'] - merge['Prev7 Active Cases']
merge['Weekly Hospitalized'] = merge['Hospitalized'] - merge['Prev7 Hospitalized']
merge['Weekly Quarantined'] = merge['Quarantined'] - merge['Prev7 Quarantined']
merge['Weekly Intensive Care'] = merge['Intensive Care'] - merge['Prev7 Intensive Care']
merge['Weekly Other Hospitalized'] = merge['Other Hospitalized'] - merge['Prev7 Other Hospitalized']
merge['Weekly Tested People'] = merge['Tested People'] - merge['Prev7 Tested People']

# %%
merge['Date'] = merge['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
merge['Last Update'] = merge['Last Update'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

# %%
outDF=merge[['Date', 'Country', 'Region', 'Region Code', 'lat', 'long',\
    'Region code', 'ISO Code', 'Map Region', 'Population', 'Area',\
    'Total Cases', 'Deaths', 'Recovered', 'Tests',\
    'Active Cases', 'Hospitalized', 'Quarantined', 'Intensive Care',  'Other Hospitalized',\
    'Prev Total Cases', 'Prev Deaths', 'Prev Recovered', 'Prev Tests',\
    'Prev Active Cases', 'Prev Hospitalized', 'Prev Quarantined', 'Prev Intensive Care',  'Prev Other Hospitalized', 'Previous Daily Cases',\
    'Daily Cases', 'Daily Deaths', 'Daily Recovered', 'Daily Tests',\
    'Daily Active Cases', 'Daily Hospitalized', 'Daily Quarantined', 'Daily Intensive Care',  'Daily Other Hospitalized', 'Daily Tested People',\
    'Weekly Cases', 'Weekly Deaths', 'Weekly Recovered', 'Weekly Tests',\
    'Weekly Active Cases', 'Weekly Hospitalized', 'Weekly Quarantined', 'Weekly Intensive Care', 'Weekly Other Hospitalized', \
    'Last Update', 'note_it', 'note_en', 'Tested People', 'Weekly Tested People']]
#    'Prev Total Cases', 'Previous Daily Cases',\


# %%
outDF.to_csv(home+"/combined/regions_ts.csv", index=False)


# %%
lastDF = outDF.loc[outDF['Date'] == outDF['Date'].max()]


# %%
lastDF.to_csv(home+"/combined/regions_last.csv", index=False)

