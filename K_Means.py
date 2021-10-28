from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import sqlite3 as sql
import pandas as pd
import numpy as np

def get_data_from_db(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT * FROM ' + inp2, conn)
    conn.close()
    return result


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
print('kai issiaiskinsiu - plosiu rankom')



