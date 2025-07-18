import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style ('whitegrid')
import yfinance as yf
from datetime import datetime
tech_list = ['AAPL','GOOG','MSFT','AMZN']
end = datetime.now()
start = datetime(end.year-1,end.month,end.day)
for stock in tech_list:
    globals()[stock] = yf.download(stock,start,end)

# AAPL['Close'].plot(legend = True, figsize = (10,4))
# plt.show()
#Trung bình trượt
ma_day = [10,20,50]
for ma in ma_day:
    column_name = 'MA for %s days' %(str(ma))
    AAPL[column_name] = AAPL['Close'].rolling(window = ma).mean()
# AAPL[['Close','MA for 10 days','MA for 20 days','MA for 50 days']].plot(subplots = False,figsize = (10,4))
# plt.show()
# AAPL['Daily Return'] = AAPL['Close'].pct_change()
# AAPL['Daily Return'].plot(figsize = (10,4), legend = True,
#                           linestyle = '--', marker = 'o')
# plt.show()
##Biểu đồ phân phối
# sns.distplot(AAPL['Daily Return'].dropna(),bins = 100,color = 'purple')
# plt.show()

closing_df = yf.download(tech_list,start,end)['Close']
tech_rets = closing_df.pct_change()
# sns.jointplot(x='MSFT',y='AMZN',data=tech_rets,kind = 'scatter',color = 'seagreen')
# plt.show()

# returns_fig = sns.PairGrid(tech_rets.dropna())
# returns_fig.map_upper(plt.scatter,color = 'purple')
# returns_fig.map_lower(sns.kdeplot,cmap = 'cool_d')
# returns_fig.map_diag(plt.hist, bins = 30)
# plt.show()

# sns.heatmap(tech_rets.dropna().corr(), annot = True)
# plt.show()

rets = tech_rets.dropna()
area = np.pi*20
# plt.scatter(rets.mean(),rets.std(),s = area)
# plt.xlabel('Expected return')
# plt.ylabel('Risk')
# for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
#     plt.annotate(
#         label,
#         xy = (x,y), xytext = (50,50),
#         textcoords = 'offset points', ha = 'right', va = 'bottom',
#         arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3,rad = -0.3')
#     )
# plt.show()

# sns.distplot(AAPL['Daily Return'].dropna(), bins = 100, color = 'purple')
# plt.show()


days = 365
dt = 1/days
mu = rets.mean()['GOOG']
sigma = rets.std()['GOOG']
def stock_monte_carlo(start_price,days,mu,sigma):
    price = np.zeros(days)
    price[0] = start_price
    shock = np.zeros(days)
    drift = np.zeros(days)
    for x in range(1,days):
        shock[x] = np.random.normal(loc = mu*dt,scale = sigma*np.sqrt(dt))
        drift[x] = mu*dt
        price[x] = price[x-1] + (price[x-1] * (price[x] + shock[x]))
    return price
start_price = 540.74
# for run in range(100):
#     plt.plot(stock_monte_carlo(start_price,days,mu,sigma))
# plt.xlabel('Days')
# plt.ylabel('Price')
# plt.title('Monte Carlo Analysis for Google')
# plt.show()

runs = 10000
simulations = np.zeros(runs)
for run in range(runs):
    simulations[run] = stock_monte_carlo(start_price,days,mu,sigma)[days-1]
q = np.percentile(simulations,1)
plt.hist(simulations,bins = 200)
plt.figtext(0.6,0.8, s = 'Start price: $%.2f' %start_price)
plt.figtext(0.6,0.7, s = 'Mean final price: $%.2f' %simulations.mean())
plt.figtext(0.6,0.6, s = 'Var(0.99): $%.2f' %(start_price-q,))
plt.figtext(0.15,0.6, s = 'q(0.99): $%.2f' %q)
plt.axvline(x = q, linewidth = 4, color = 'r')
plt.title('Final price distribution for Google after %s days' %days, weight ='bold')
plt.show()