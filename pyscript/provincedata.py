# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import glob
import os

# %%
home=os.path.dirname(__file__)+"/../"

# %%
df = pd.read_csv(home+'/COVID-19/dati-province/dpc-covid19-ita-province.csv')
provdata = pd.read_csv(home+'/other_info/provinceData.csv')
regdata = pd.read_csv(home+'/other_info/regionData.csv')

# %%
# rename columns
df = df.rename(columns={
    'stato': 'Country',
    'codice_regione': 'Region Code',
    'denominazione_regione': 'Region',
    'codice_provincia': 'Province Code',
    'denominazione_provincia': 'Province',
    'sigla_provincia': 'Province Abbreviation',
    'totale_casi': 'Total Cases'
    })

df = df.astype({
    'Total Cases':'Int32'
    })

provdata = provdata.astype({
    'Population':'Int32'
    })


# %%
df['Last Update'] = pd.to_datetime(df['data'])
df['Date'] = pd.to_datetime(df['data']).dt.floor('D')

# %%
# 	Previous Total Cases	Previous Total Deaths	Previous Total Recovered  Previous Total Tests
prev = df[['Date','Region','Province','Total Cases']].\
    rename(columns={'Total Cases':'Prev Total Cases'})
prev['Date'] = prev['Date']+pd.to_timedelta(1,unit='D')

prev2 = df[['Date','Region','Province','Total Cases']].\
    rename(columns={'Total Cases':'Prev2 Total Cases'})
prev2['Date'] = prev2['Date']+pd.to_timedelta(2,unit='D')

prev3 = df[['Date','Region','Province','Total Cases']].\
    rename(columns={'Total Cases':'Prev3 Total Cases'})
prev3['Date'] = prev3['Date']+pd.to_timedelta(3,unit='D')

prev7 = df[['Date','Region','Province','Total Cases']].\
    rename(columns={'Total Cases':'Prev7 Total Cases'})
prev7['Date'] = prev7['Date']+pd.to_timedelta(7,unit='D')
# %%
merge=df.merge(prev, on=['Date','Region','Province'], how="left")\
    .merge(prev2, on=['Date','Region','Province'], how="left")\
    .merge(prev3, on=['Date','Region','Province'], how="left")\
    .merge(prev7, on=['Date','Region','Province'], how="left")\
    .merge(provdata, on=['Region','Province'], how='left')\
    .merge(regdata[['Region','Region code','Map Region']], on=['Region'], how='left')

# %%
# Daily Cases   Daily Deaths    Daily Recovered    Daily Tests  Previous Daily Cases
merge['Daily Cases'] = merge['Total Cases'] - merge['Prev Total Cases']
merge['Weekly Cases'] = merge['Total Cases'] - merge['Prev7 Total Cases']
merge['Daily Cases Avg 3 days'] = ((merge['Total Cases'] - merge['Prev3 Total Cases'])/3).astype(float).round().astype('Int32')

# %%
merge['Date'] = merge['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
merge['Last Update'] = merge['Last Update'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

# %%
outDF=merge[['Date', 'Country', 'Region', 'Region Code', 'Map Region', \
    'Province', 'Province Abbreviation', 'Province Code', 'lat', 'long', 'Population', 'Area', \
    'Total Cases', 'Prev Total Cases', 'Daily Cases', 'Weekly Cases', 'Daily Cases Avg 3 days', 'Last Update', 'note']]

# %%
outDF.to_csv(home+"/combined/provinces_ts", index=False)


# %%
lastDF = outDF.loc[outDF['Date'] == outDF['Date'].max()]


# %%
lastDF.to_csv(home+"/combined/provinces_last", index=False)

