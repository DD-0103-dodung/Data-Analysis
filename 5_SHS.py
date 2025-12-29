import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

path = '/Users/dd/Downloads/SHS_Matched.xlsx'

df = pd.read_excel(path)
df['Giá'] = df['Giá'].str.replace(',','').astype(float).astype(int)
df['Giá Trị'] = (df['KL'] * df['Giá'])
df['Giá Trị'] = pd.to_numeric(df['Giá Trị'] ,errors = 'coerce')
df['Thời gian'] = pd.to_datetime(df['Thời gian'].astype(str), format = '%H:%M:%S')
df['Thời gian 15'] = df['Thời gian'].dt.floor('15min').dt.strftime('%H:%M')

df_group = df.groupby(['Thời gian 15','M/B'])['Giá Trị'].sum().reset_index()
plt.figure(figsize = (10,6))
ax1 = sns.lineplot(data = df_group,x = 'Thời gian 15', y = 'Giá Trị', hue = 'M/B', marker = 'o',
             )
ax2 = ax1.twinx()
sns.lineplot(data = df, x = 'Thời gian 15', y = 'Giá', ax = ax2, color = 'green',
             linestyle = '--')

plt.show()