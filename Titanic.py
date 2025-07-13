import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
titanic_df = pd.read_csv('/Users/dd/Documents/Python/titanic_train.csv')
# #Cách 1 dùng trực tiếp countplot
# sns.countplot(x = 'Sex', data = titanic_df,hue = 'Pclass',)
# plt.show()
#Cách 2 group lại df rồi hiển thị
titanic_df_grouped = titanic_df.groupby(['Sex','Pclass'])['PassengerId'].nunique().reset_index()
sns.barplot(data = titanic_df_grouped,x = 'Sex',y = 'PassengerId', hue = 'Pclass')
plt.show()
