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
# titanic_df_grouped = titanic_df.groupby(['Sex','Pclass'])['PassengerId'].nunique().reset_index()
# sns.barplot(data = titanic_df_grouped,x = 'Sex',y = 'PassengerId', hue = 'Pclass')
# sns.barplot(data = titanic_df_grouped,x = 'Pclass',y = 'PassengerId', hue = 'Sex')
# plt.show()

#Tạo function để phân nhóm lại Sex
def male_female_child(passenger):
    age,sex = passenger
    if age < 16:
        return 'child'
    else:
        return sex
titanic_df['person'] = titanic_df[['Age','Sex']].apply(male_female_child,axis = 1)
# print(titanic_df[titanic_df['Age']>= 16][['PassengerId','Age','Sex','person']])
# sns.countplot(x = 'Pclass', data = titanic_df,hue = 'person',)

#Biểu đồ phân phối của độ tuổi
# titanic_df['Age'].hist(bins = 70,grid = False,)
# plt.show()
# print(titanic_df['Age'].mean())

# fig = sns.FacetGrid(titanic_df,hue = 'Pclass', aspect = 4,) #Sex person
# fig.map(sns.kdeplot, 'Age', fill = True)
# oldest = titanic_df['Age'].max()
# fig.set(xlim = (0,oldest))
# fig.add_legend()
# plt.show()

# deck = titanic_df['Cabin'].dropna()
# levels = []
# for level in deck:
#     levels.append(level[0])
# cabin_df = DataFrame(levels)
# cabin_df.columns = ['Cabin']
# sns.countplot(x = 'Cabin',data = cabin_df,palette='winter_d')
# sns.countplot(x = 'Embarked',data = titanic_df,hue = 'Pclass',palette='winter_d', hue_order = ['C','Q','S'])
# plt.show()

titanic_df['Alone'] = titanic_df.SibSp + titanic_df.Parch
titanic_df['Alone'].loc[titanic_df['Alone'] > 0 ] = 'With Family'
titanic_df['Alone'].loc[titanic_df['Alone'] ==0 ] = 'Alone'
# sns.countplot(x = 'Alone', data = titanic_df,palette='Blues')
# plt.show()

titanic_df['Survivor'] = titanic_df.Survived.map({0:'no', 1:'yes'})
# sns.countplot(x = 'Survivor', data = titanic_df,palette='Set1')
# sns.catplot(x = 'Pclass',y = 'Survived', data = titanic_df,kind='point',hue = 'person')
# plt.show()

generations = [10,20,40,60,80]
sns.lmplot(x = 'Age', y = 'Survived', hue = 'Sex',#Pclass
           data = titanic_df, palette = 'winter', x_bins = generations)
plt.show()



