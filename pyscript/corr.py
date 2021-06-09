#%%
import pandas as pd
import matplotlib.pyplot as plt
import os

#%%
home=os.path.dirname(__file__)+"/../"

#%%
reg = pd.read_csv(home+'/combined/regions_ts')
reg = reg[['Date','Region','Weekly Cases','Weekly Deaths']].rename(columns={'Weekly Cases': 'c','Weekly Deaths': 'd'})
reg = reg.groupby('Date', as_index=False).agg('sum')

#%%
def corr(x, y, lag=0):
  return x.corr(y.shift(lag))

def plot(df, lag=0, title=""):
  cd = df['c'].to_frame()
  lagcol='d'+str(lag)
  cd[lagcol] = df['d'].shift(lag)
  cd.plot.scatter(x='c',y=lagcol,title=title)

#%%
def findlag(r, title):
  idx=range(31)
  df = pd.DataFrame({'lag': ['d-'+str(i) for i in idx], 'corr': [corr(r['c'], r['d'], -i) for i in idx]}, index=idx)

  lag = df['corr'].idxmax()
  t="Corelation coeff for %s: %.5f with lag %d days" % ( title, df['corr'].max(), lag )

  fatality = (r['d'].shift(lag)/r['c']).mean()
  fatality2 = (r['d'].sum()/r['c'].sum())
  t+="\navg fatality rate {:.1f}% / fatality rate: {:.1f}%".format(fatality*100,fatality2*100)
  
  print(t)
  plot(r, -lag, t)

# %%
findlag(reg,'all')

# %%
findlag(reg[reg['Date']<='2020-07-31'],'1st (until 2020-07-31)')
# %%
findlag(reg[(reg['Date']>='2020-08-01')],'2nd and 3rd (since 2020-08-01)')

# %%
findlag(reg[(reg['Date']>='2020-08-01') & (reg['Date']<='2021-02-28')],'2nd (2020-08-01 to 2021-02-28')

# %%
findlag(reg[reg['Date']>='2021-03-01'],'3nd (since 2021-03-01')

#%%
plt.show()