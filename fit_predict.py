import pylab
import numpy as np
import pandas as pd

#多项式拟合函数，x为年份，y为提出安全问题总数，n为多项式次数
def polynomial(x,y,n):
    z1 = np.polyfit(x, y, n)              
    p1 = np.poly1d(z1)                    
    print(p1)
    y_pred = p1(x)    
    #print("2019 =" )  
    #print(np.polyval(p1, 2019))   #当测试用例中包含2019时取消注释
    #print("2020 =" )  
    #print(np.polyval(p1, 2020))   #当测试用例中包含2020时取消注释                 
    print("2021 =" )  
    print(np.polyval(p1, 2021))
    plot1 = pylab.plot(x, y, '*', label='original values')
    plot2 = pylab.plot(x, y_pred, 'r', label='fit values')
    pylab.xlabel('year')
    pylab.ylabel('total')
    pylab.legend(loc='best', borderaxespad=0., bbox_to_anchor=(0, 0))
    pylab.show()

#将Excel中数据除去每列列名，提取成变量x列表和变量y列表调用拟合函数进行拟合
def excel_one_line_to_list():
    df = pd.read_excel("debian_year.xlsx", usecols=[0,1],
                       engine='openpyxl')  
    df_li = df.values.tolist()
    x = []
    y = []
    for s_li in df_li:
        x.append(s_li[0])
        y.append(s_li[1])
    print(x)
    print(y)
    polynomial(x,y,2)

#index_test = range(1,6,1)    #寻找最适合拟合曲线时，测试一项式到五项式
index_ans = range(2,3,1)      #找到最适合拟合曲线为二项式
excel_one_line_to_list(index_ans)    
