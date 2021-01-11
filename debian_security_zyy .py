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

import re #文本内容清洗
re_obj = re.compile('dsa|update|security|vulnerabilities|input|error|missing|denial|service|insecure|overflows|insufficient|chromiumbrowser|iceweasel|escalation|files|icedove|firefoxesr|multiple|[,-]')
re_obj2 = re.compile('\\[|\\]')
def clear(text):
    return re_obj.sub('',str(text))
def clear_d(text_d):
    return re_obj2.sub('',text_d)
def low(text):
    return text.lower()

debian['security_advisory'] = debian['security_advisory'].apply(low)
debian['security_advisory'] = debian['security_advisory'].apply(clear)
debian['date'] = debian['date'].apply(clear_d)
debian.sample(5)

#分词
import nltk
import nltk.tokenize as tk
import re
from nltk.tokenize import word_tokenize

def cut_word(text):
    return word_tokenize(text)
debian['security_advisory'] = debian['security_advisory'].apply(cut_word)
debian.sample(5)
def get_stopword(): #停用词处理
    s = set()
    with open('D:\大三上\开源软件基础\大作业\ENstopwords.txt','r',encoding='UTF-8') as f:
        for line in f:
            s.add(line.strip())
    return s
def remove_stopword(words):
    return [word for word in words if word not in stopword]

stopword = get_stopword()
debian['security_advisory'] = debian['security_advisory'].apply(remove_stopword)
debian.sample(5)

t = debian['vulnerable'].value_counts()
print(t)
t.plot(kind = 'bar')

t = debian['date'].str.split(' ',expand=True)
print(t[2].value_counts())
t[2].value_counts().plot(kind='bar')

from itertools import chain #词汇统计
from collections import Counter

li_2d = debian['security_advisory'].tolist()
li_1d = list(chain.from_iterable(li_2d))
print(f'总词汇量:{len(li_1d)}')#二维列表转换为一维列表
c = Counter(li_1d)
print(f'不重复词汇量:{len(c)}')
common = c.most_common(15)
print(common)

d = dict(common) #可视化
print(d)
plt.figure(figsize=(27,5))
plt.bar(d.keys(),d.values())

total = len(li_1d)
percentage = [v*100/total for v in d.values()]
plt.figure(figsize=(27,5))
plt.bar(d.keys(),percentage)

#词汇频数分布直方图
plt.figure(figsize=(15,5))
t = pd.Series(c)
print(t)
plt.hist(c.values(),bins=15,log=True)#log=True：纵坐标对数显示，降低数量级相差较大产生的影响

from wordcloud import WordCloud
wc = WordCloud(font_path=r'D:\大三上\开源软件基础\大作业\simfang.ttf',width=800,height=600)
plt.figure(figsize=(15,10))
img = wc.generate_from_frequencies(c)
plt.imshow(img)
plt.axis('off')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

count = CountVectorizer()
docs = [
    'Where there is a will, there is a way.',
    'There is no royal road to learning.',
]
bag = count.fit_transform(docs)
tfdif = TfidfTransformer()
t = tfdif.fit_transform(bag)
#def get_bag(words):
    #return count.fit_transform(words)
#bag = debian['security_advisory'].apply(get_bag)
print(bag)
print(bag.toarray())
print(count.get_feature_names())
print(count.vocabulary_)
print(t.toarray())

from sklearn.feature_extraction.text import TfidfVectorizer
docs = [
    'Where there is a will, there is a way.',
    'There is no royal road to learning.',
]
tfdif = TfidfVectorizer()
t = tfdif.fit_transform(docs)
print(t.toarray())

def join(text_list):
    return " ".join(text_list)
debian['security_advisory'] = debian['security_advisory'].apply(join)
debian.sample(5)

doc = ['buffer','overflow','programming','sanitising','integer','file','temporary','privilege','remote',
       'format','exploit','string','chromiumbrowser','linux','firefoxesr']
def is_sub_string(s1, s2):
    tag = False
    if s2.find(s1) != -1:
        tag = True
    return tag
    #return s1 in s2
def classify(text):
    for value in doc:
        if is_sub_string(value,text) is True:
            return value
    return 'else problem'    
  
debian['category'] = debian['security_advisory'].apply(classify)
debian.sample(5)

t = debian['category'].value_counts()
print(t)
t.plot(kind = 'bar')

debian['vulnerable'] = debian['vulnerable'].map({'Yes':1,'No':0})
debian['vulnerable'].value_counts()

from sklearn.model_selection import train_test_split
X = debian['security_advisory']
y = debian['vulnerable']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25)
print('训练集样本数：',y_train.shape[0],'测试集样本数：',y_test.shape[0])

from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer(ngram_range=(1,2))
X_train_tran = vec.fit_transform(X_train)
X_test_tran = vec.transform(X_test)
display(X_train_tran,X_test_tran)

from sklearn.feature_selection import f_classif
f_classif(X_train_tran,y_train)

from sklearn.feature_selection import SelectKBest
X_train_tran = X_train_tran.astype(np.float32)
X_test_tran = X_test_tran.astype(np.float32)
selector = SelectKBest(f_classif,k=min(20000,X_train_tran.shape[1]))
selector.fit(X_train_tran,y_train)
X_train_tran = selector.transform(X_train_tran)
X_test_tran = selector.transform(X_test_tran)
print(X_train_tran.shape,X_test_tran.shape)

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

param = [{'penalty':['l1','l2'],'C':[0.1,1,10],
          'solver':['liblinear']},
         {'penalty':['elasticnet'],'C':[0.1,1,10],
          'solver':['saga'],'l1_ratio':[0.5]}
        ]

gs = GridSearchCV(estimator=LogisticRegression(),param_grid=param,
                 cv=2, scoring='f1', n_jobs=-1, verbose=10)
gs.fit(X_train_tran,y_train)
print(gs.best_params_)
y_hat = gs.best_estimator_.predict(X_test_tran)
print(classification_report(y_test,y_hat))

# KNN
from sklearn.neighbors import KNeighborsClassifier
param = {'n_neighbors':[5,7],
          'weights':['uniform','distance'],
         'p':[2]
        }

gs = GridSearchCV(estimator=KNeighborsClassifier(),param_grid=param,
                 cv=2, scoring='f1', n_jobs=-1, verbose=10)
gs.fit(X_train_tran,y_train)
print(gs.best_params_)
y_hat = gs.best_estimator_.predict(X_test_tran)
print(classification_report(y_test,y_hat))

# 决策树
from sklearn.tree import DecisionTreeClassifier
param = {'criterion':['gini','entropy'],
        'max_depth':[10,15]
        }

gs = GridSearchCV(estimator=DecisionTreeClassifier(),param_grid=param,
                 cv=2, scoring='f1', n_jobs=-1, verbose=10)
gs.fit(X_train_tran,y_train)
print(gs.best_params_)
y_hat = gs.best_estimator_.predict(X_test_tran)
print(classification_report(y_test,y_hat))

#多层感知器
from sklearn.neural_network import MLPClassifier
param = {'hidden_layer_sizes':[(8,),(4,)]}

gs = GridSearchCV(estimator=MLPClassifier(),param_grid=param,
                 cv=2, scoring='f1', n_jobs=-1, verbose=10)
gs.fit(X_train_tran,y_train)
print(gs.best_params_)
y_hat = gs.best_estimator_.predict(X_test_tran)
print(classification_report(y_test,y_hat))

from sklearn.naive_bayes import GaussianNB,BernoulliNB,MultinomialNB,ComplementNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

steps = [('dense',FunctionTransformer(func=lambda X: X.toarray(),accept_sparse=True)),('model',None)]
pipe = Pipeline(steps=steps)
param = {'model':[GaussianNB(),BernoulliNB(),MultinomialNB(),ComplementNB()]}

gs = GridSearchCV(estimator=pipe,param_grid=param,
                 cv=2, scoring='f1', n_jobs=-1, verbose=10)
gs.fit(X_train_tran,y_train)
print(gs.best_params_)
y_hat = gs.best_estimator_.predict(X_test_tran)
print(classification_report(y_test,y_hat))
