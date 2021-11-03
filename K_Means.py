from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import sqlite3 as sql
import pandas as pd
import numpy as np
import yfinance as yf

def get_data_from_db(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT * FROM ' + inp2, conn)
    conn.close()
    return result
def get_data_from_db_Y(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT "Date" FROM ' + inp2, conn)
    conn.close()
    return result

# data_Y = get_data_from_db('annual_data_p')      #pasiimu is db visa data
# unique_tickers_Y = list(data_Y['Ticker'].unique() )       #pasiimu tickerius ir pasidarau juos unikalius ir tai bus inputas i
                                                    # istoriniu duomenu funkcija
ticker= ['TSLA', 'AMZN']
date_start = get_data_from_db_Y('differences_Y') #
date_end = date_start + 1 #str(input('ivesk pabaigos data: '))

def get_price_perfomance(inp_tick, inp_date_start, inp_date_end):
    perfomace_list = []
    for i in inp_tick:
        data_start_price = float(yf.download(i, inp_date_start, inp_date_start)['Adj Close'].values)
        data_end_price = float(yf.download(i, inp_date_end, inp_date_end)['Adj Close'].values)
        perfomance = ((data_end_price - data_start_price)*100)/data_start_price
        print(perfomance)
        perfomace_list.append(perfomance)
    return perfomace_list


perfomance_df = pd.DataFrame(get_price_perfomance(ticker, date_start, date_end))







column_list = ['Sales/Revenue','Sales Growth','Cost of Goods Sold (COGS) incl. D&A']
column_list.insert(0,'Date')
column_list1 = column_list.insert(1, 'Ticker')
user_years = 2020

def check_and_drop_nan(inp1,inp2):
    new_df = inp1[inp2].dropna()
    return new_df


mydata = check_and_drop_nan(get_data_from_db('differences_Y'), column_list).reset_index(drop=True)
grouped_tmp = mydata.groupby(['Date']).get_group(str(user_years))
grouped_final = grouped_tmp.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
mydata_numpy = grouped_final.iloc[:,2:].to_numpy()

mydata_prediction = KMeans(n_clusters=3).fit_predict(mydata_numpy)

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")

ax.scatter3D(grouped_final['Sales/Revenue'], grouped_final['Sales Growth'], grouped_final['Cost of Goods Sold (COGS) incl. D&A'], c=mydata_prediction )
plt.title("3D ploting")
plt.show()




