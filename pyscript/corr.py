#%%
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.linear_model import LinearRegression

#%%
home=os.path.dirname(__file__)+"/../"

#%%
reg = pd.read_csv(home+'/combined/regions_ts')
reg = reg[['Date','Region','Weekly Cases','Weekly Deaths']].rename(columns={'Weekly Cases': 'c','Weekly Deaths': 'd'})
reg = reg.groupby('Date', as_index=False).agg('sum')

#%%
def corr(x, y, lag=0):
  return x.corr(y.shift(lag))

fig=0

def plot(df, lag=0, title=""):
  cd=df['c'].to_frame()
  cd['d']=df['d'].shift(lag)
  cd=cd.dropna()

  x = cd['c'].values.reshape(-1, 1)  # values converts it into a numpy array
  y = cd['d'].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
  linear_regressor = LinearRegression(fit_intercept=False)  # create object for the class
  linear_regressor.fit(x, y)  # perform linear regression
  y_pred = linear_regressor.predict(x)  # make predictions

  lrcoeff = linear_regressor.predict([[1]])[0][0]

  global fig
  fig+=1
  plt.figure(fig)
  plt.title(title+" linreg coeff: {:.1f}%".format(lrcoeff*100))
  plt.scatter(x, y)
  plt.plot(x, y_pred, color='red')
#%%
def findlag(r, title):
  idx=range(31)
  df = pd.DataFrame({'lag': ['d-'+str(i) for i in idx], 'corr': [corr(r['c'], r['d'], -i) for i in idx]}, index=idx)

  lag = df['corr'].idxmax()
  t="Correlation coeff for %s: %.5f with lag %d days" % ( title, df['corr'].max(), lag )

  fatality = (r['d'].sum()/r['c'].sum())
  t+="\navg fatality rate: {:.1f}%".format(fatality*100)
  
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