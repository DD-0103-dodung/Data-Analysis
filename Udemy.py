import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from numpy.random import randn
import yfinance as yf
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import sys
import json
from pandas import read_html
from io import StringIO
# df = yf.download(['CVX','XOM','BP'], start = datetime.datetime(2010,1,1),
                 # end = datetime.datetime(2013,1,1))['Close']
# rets = df.pct_change()
# corr = rets.corr
# df.plot()
# plt.show()
# sns.corrplot(rets,annot = False, diag_names = False)

#Index Hierarchy
# ser = Series(randn(6), index = [[1,1,1,2,2,2] ,['a','b','c','a','b','c']])
# df = ser.unstack()
# print(df)
#
# df2 = DataFrame(np.arange(16).reshape(4,4),
#                 index = [['a','a','b','b'],[1,2,1,2]],
#                 columns = [['NY','NY','LA','SF'],['cold','hot','cold','hot']])
# df2.index.names = ['ix1','ix2']
# df2.columns.names = ['Cities','Temp']
# # df2.swaplevel('Cities','Temp', axis = 1)
# df2.sum(level='Temp', axis = 1)
# print(df2)
#
# xlsfile = pd.ExcelFile('.xlsx')
# df = xlsfile.parse('Sheets')
#
# df1 = DataFrame({'key' :['X','Z','Y','Z','X','X'], 'data_set_1':np.arange(6)})
# df2 = DataFrame({'key' :['Q','Y','Z'], 'data_set_2':[1,2,3]})
# print(pd.merge(df1,df2, ))

# years = [1990,1991,1992,1993,2008,2012,2015,1987,1969,2013,2008,1999]
# decade_bins = [1960,1970,1980,1990,2000,2010,2020]
# decade_cat = pd.cut(years, decade_bins)
# # print(decade_cat.categories)
# # print(pd.value_counts(decade_cat))
# print(pd.cut(years,2,precision = 1))
#
# df = DataFrame(np.random.randn(1000,4))
# print(df.describe())
# print(df[0].head())

# df = DataFrame(np.arange(16).reshape(4,4))
# blender = np.random.permutation(4)
# # print(df.take(blender))
# box = np.array([1,2,3])
#
# shaker = np.random.randint(0,len(box), size = 10)
# print(shaker)
#
# animals = DataFrame(np.arange(16).reshape(4,4),
#                     columns = ['W','X','Y','Z'],
#                     index = ['Dog','Cat','Bird','Mouse'])
# animals.loc['Cat',['W','Y']] = np.nan
# behavior_map = {'W':'good','X':'bad','Y':'good','Z':'bad'}
# animal_col = animals.groupby(behavior_map,axis = 1)
# print(animal_col.sum())
#
# data = """\
# Sample Animal Intelligence
# 1 Dog Smart
# 2 Dog Smart
# 3 Cat Dumb
# 4 Cat Dumb
# 5 Dog Dumb
# 6 Cat Smart"""
#
# df = pd.read_table(StringIO(data), sep = r"\s+")
# print(pd.crosstab(df.Animal, df.Intelligence, margins = True))
# print(df)
#
# dataset1 = randn(100)
# dataset2 = randn(80)
#
# # plt.hist(dataset2,color = 'indianred')
# plt.hist(dataset1,density = True, color = 'indianred', alpha = 0.5, bins = 20,)
# plt.hist(dataset2,density = True, alpha = 0.5, bins = 20)
# plt.title('Biểu đồ histogram đã được normalize')
# plt.show()

# data1 = randn(1000)
# data2 = randn(1000)
# df = pd.DataFrame({'df1': data1, 'df2':data2})
# # sns.jointplot(x = 'df1', y = 'df2', data = df, kind = 'scatter')
# sns.jointplot(x = 'df1', y = 'df2', data = df, kind = 'hex')
# plt.show()

# df = randn(25)
# sns.rugplot(df)
# x_min = df.min() - 2
# x_max = df.max() + 2
# x_axis = np.linspace(x_min, x_max, 100)
# bandwidth = ((4*df.std() **5)/(3*len(df))) **0.2
# kernel_list = []
# for data_point in df:
#     #Create a kernel for each point and append it to the kernel_list
#     kernel = stats.norm(data_point,bandwidth).pdf(x_axis)
#     kernel_list.append(kernel)
#     # Scale for plotting
#     kernel = kernel/ kernel.max()
#     kernel = kernel * 0.4
#     plt.plot(x_axis, kernel, color = 'grey', alpha = 0.5)
# plt.ylim(0,1)
# plt.show()
#
# sum_of_kde = np.sum(kernel_list, axis = 0)
# fig = plt.plot(x_axis,sum_of_kde, color = 'indianred')
# sns.rugplot(df)
# plt.yticks([])
# plt.suptitle("Sum of the basic functions")
# plt.show()

#
# sns.rugplot(df,color = 'black')
# for bw in np.arange(0.5,2,0.25):
#     sns.kdeplot(df,bw = bw, lw = 1.8, label = bw)
# plt.show()

# mean = [0,0]
# cov = [[1,0],[0,100]]
# dataset = np.random.multivariate_normal(mean,cov,1000)
# df = pd.DataFrame(dataset, columns = ['x','y'])
# sns.kdeplot(df)
# plt.show()

# dataset = randn(100)
# sns.distplot(dataset, bins = 25, rug = False, hist = True,
#              kde_kws = {'color':'indianred', 'label' :'kde plot'},
#              hist_kws ={'color':'blue', 'label' :'hist'}
#              )
# plt.show()

