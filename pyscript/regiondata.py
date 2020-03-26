# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import glob
import argparse

# %%
parser = argparse.ArgumentParser(description='Merge and elaborate regions files')
parser.add_argument('--cwd','-d', metavar='homedir', required=True, help='home directory')

args = parser.parse_args()


# %%
home=args.cwd


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
    'totale_attualmente_positivi': 'Active Cases',
    'nuovi_attualmente_positivi': 'Daily Active Cases',
    'dimessi_guariti': 'Recovered',
    'deceduti': 'Deaths',
    'totale_casi': 'Total Cases',
    'tamponi': 'Tests'
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
    'Tests':'Int32'
    })


# %%
df['Last Update'] = pd.to_datetime(df['data'])
df['Date'] = pd.to_datetime(df['data']).dt.floor('D')


# %%
df.dtypes


# %%
# 	Previous Total Cases	Previous Total Deaths	Previous Total Recovered  Previous Total Tests
prev = df[['Date','Region','Total Cases','Deaths','Recovered','Tests','Active Cases', 'Hospitalized', 'Quarantined', 'Intensive Care',  'Other Hospitalized']]

prev = prev.rename(columns={'Total Cases':'Prev Total Cases', 'Deaths':'Prev Deaths', 'Recovered':'Prev Recovered', 'Tests':'Prev Tests',     'Active Cases':'Prev Active Cases', 'Hospitalized':'Prev Hospitalized', 'Quarantined':'Prev Quarantined',     'Intensive Care':'Prev Intensive Care',  'Other Hospitalized':'Prev Other Hospitalized'})
prev['Date'] = prev['Date']+pd.to_timedelta(1,unit='D')


# %%
prev2 = df[['Date','Region','Total Cases','Tests']]
prev2 = prev2.rename(columns={'Total Cases':'Prev2 Total Cases', 'Tests':'Prev2 Tests'})
prev2['Date'] = prev2['Date']+pd.to_timedelta(2,unit='D')


# %%
prev3 = df[['Date','Region','Total Cases','Tests']]
prev3 = prev3.rename(columns={'Total Cases':'Prev3 Total Cases', 'Tests':'Prev3 Tests'})
prev3['Date'] = prev3['Date']+pd.to_timedelta(3,unit='D')


# %%
merge=df.merge(prev, on=['Date','Region'], how="left")    .merge(prev2, on=['Date','Region'], how="left")    .merge(prev3, on=['Date','Region'], how="left")    .merge(regdata, on=['Region'], how='left')


# %%
# Daily Cases   Daily Deaths    Daily Recovered    Daily Tests  Previous Daily Cases
merge['Daily Cases'] = merge['Total Cases'] - merge['Prev Total Cases']
merge['Daily Deaths'] = merge['Deaths'] - merge['Prev Deaths']
merge['Daily Recovered'] = merge['Recovered'] - merge['Prev Recovered']
merge['Daily Tests'] = merge['Tests'] - merge['Prev Tests']
merge['Daily Hospitalized'] = merge['Hospitalized'] - merge['Prev Hospitalized']
merge['Daily Quarantined'] = merge['Quarantined'] - merge['Prev Quarantined']
merge['Daily Intensive Care'] = merge['Intensive Care'] - merge['Prev Intensive Care']
merge['Daily Other Hospitalized'] = merge['Other Hospitalized'] - merge['Prev Other Hospitalized']

merge['Previous Daily Cases'] = merge['Prev Total Cases'] - merge['Prev2 Total Cases']

# New cases in last 3 days  Test in last 3 days
merge['New cases in last 3 days'] = merge['Total Cases'] - merge['Prev3 Total Cases']
merge['Test in last 3 days'] = merge['Tests'] - merge['Prev3 Tests']


# %%
outDF=merge[['Date', 'Country', 'Region', 'Region Code', 'lat', 'long',     'Region code', 'ISO Code', 'Map Region', 'Population', 'Area',     'Total Cases', 'Deaths', 'Recovered', 'Tests',     'Active Cases', 'Hospitalized', 'Quarantined', 'Intensive Care',  'Other Hospitalized',     'Prev Total Cases', 'Prev Deaths', 'Prev Recovered', 'Prev Tests',     'Prev Active Cases', 'Prev Hospitalized', 'Prev Quarantined', 'Prev Intensive Care',  'Prev Other Hospitalized',     'Previous Daily Cases',     'Daily Cases', 'Daily Deaths', 'Daily Recovered', 'Daily Tests',     'Daily Active Cases', 'Daily Hospitalized', 'Daily Quarantined', 'Daily Intensive Care',  'Daily Other Hospitalized',     'New cases in last 3 days', 'Test in last 3 days',     'Last Update', 'note_it', 'note_en']]


# %%
outDF.to_csv(home+"/combined/regions_ts.csv", index=False)


# %%
lastDF = outDF.loc[outDF['Date'] == outDF['Date'].max()]


# %%
lastDF.to_csv(home+"/combined/regions_last.csv", index=False)

