#%%
import pandas as pd

#%%
reg = pd.read_csv('../combined/regions_ts')
reg = reg[['Date','Region','Weekly Cases','Weekly Deaths']].rename(columns={'Weekly Cases': 'c','Weekly Deaths': 'd'})
reg = reg[reg['Date']>'2020-08-01']
reg = reg.groupby('Date').agg('sum')

#%%
def corr(x, y, lag=0):
  return x.corr(y.shift(lag))

def plot(df, lag=0):
  cd = df['c'].to_frame()
  lagcol='d'+str(lag)
  cd[lagcol] = df['d'].shift(lag)
  cd.plot.scatter(x='c',y=lagcol,title=lagcol)

#%%
idx=range(31)
df = pd.DataFrame({'lag': ['d-'+str(i) for i in idx], 'corr': [corr(reg['c'], reg['d'], -i) for i in idx]}, index=idx)

# %%
lag = df['corr'].idxmax()
print("max corr "+str(df['corr'].max())+" for lag -"+str(lag))
# %%
for l in range(31):
  plot(reg, -l)
# %%
