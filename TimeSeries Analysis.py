
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')
tran = pd.read_csv("transactions.csv")
#RESHAPING DATA
df1 = tran['date'].unique()
l=[]
for i in df1:
    date=tran[tran['date']==i]
    l.append(date['category'].value_counts())
f = pd.DataFrame(l)
f.fillna(0,inplace = True)
f['date']=df1
f['date'] = pd.to_datetime(f['date'])
f = f.set_index(['date'], drop=True)
def generate_seasonal_score(search_category):
    result = seasonal_decompose(f[search_category], model='additive',freq=30)
    obj = result.seasonal
    obj_df = obj.to_frame()
    obj_df.columns=["Seasonal Pattern"]
    print("*****************************SEASONAL PATTERN************************************\n")
    print("Example : -9.550253 means decrease(negative values in pattern) in sales by 9 to 10(~approx) because of seasonality\n")
    print("Example : 59.980051 means Increase(positive values in pattern) in sales by 59 to 60(~approx) because of seasonality\n")
    print(obj_df[:31])
    print("\nSimilar Repeated sesonal cyclic pattern is observed for all months\n")
    print("\n\n SEASONAL SCORE GENERATION FOR ALL MONTHS\n")
    ax = f.resample('m')[search_category].count()
    m_mean = 0
    mean_list = []
    count_ = 0
    for i in range(0,12):
        m_mean=0
        for j in range(count_,count_+ax[i]):
            m_mean = m_mean + f[search_category][j]
        m_mean = m_mean/ax[i]
        mean_list.append(m_mean)
        count_ = count_ + ax[i]
    min_ = min(mean_list)
    max_ = max(mean_list)
    max_min = max_ - min_
    norm = []
    for i in mean_list:
        temp = (i - min_)/max_min
        norm.append(temp)
    idx_list = list(ax.index.values)
    se = pd.Series(norm,name=" Seasonal Score",index=idx_list)
    rank_results = pd.concat([ax, se], axis=1)
    rank_results.columns = ['NO OF DAYS','SEASONAL SCORE']
    print(rank_results)
choice=0
while(choice!=5):
    print("     CHECK SEASONAL PATTERN AND GENERATE SESONAL SCORE FOR CATEGORY      \n")
    print("                  1) CASUAL DRESS                        \n")
    print("                  2) PULLOVER SWEATER                    \n")
    print("                  3) SLEEVELESS BLOUSE                   \n")
    print("                  4) FLEECE JACKET                       \n")
    print("                  5) EXIT                                \n")
    print("   Enter your choice (1 to 5)  \n")
    try:
        choice = int(input())
        if(choice == 1):
            generate_seasonal_score("Casual Dress")
        elif(choice == 2):
            generate_seasonal_score("Pullover Sweater")
        elif(choice == 3):
            generate_seasonal_score("Sleeveless Blouse")
        elif(choice == 4):
            generate_seasonal_score("Fleece Jacket")
        elif(choice == 5):
            break
        else:
            print("    Please Enter Correct choice (1 to 5)  \n")
    except:
        print("    Please Enter Valid choice between (1 to 5)  \n")

