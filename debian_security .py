import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = 'False'
plt.rcParams['font.size'] = 15

os.chdir('D:\大三上\开源软件基础\大作业')
debian = pd.read_excel('debian_data.xlsx')
print(debian.shape)
debian.head()

debian.isnull().sum()#缺失值处理
index = debian[debian['fixed_in'].isnull()].index
debian['fixed_in'][index] = 'none'
debian.isnull().sum()
debian.loc[index].sample(5)

print(debian.duplicated().sum())#重复值处理
display(debian[debian.duplicated()])#查找重复值
debian.drop_duplicates(inplace=True)#删除重复值
print(debian.duplicated().sum())
