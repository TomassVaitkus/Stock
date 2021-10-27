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


Data = get_data_from_db('differences_Y')

column_list = ['Sales/Revenue','Sales Growth','Cost of Goods Sold (COGS) incl. D&A']

def check_and_drop_nan(inp1,inp2):
    new_df = inp1[inp2].dropna()
    return new_df

mydata = check_and_drop_nan(get_data_from_db('differences_Y'), column_list).reset_index(drop=True)
mydata_numpy = mydata.to_numpy()

mydata_prediction = KMeans(n_clusters=3).fit_predict(mydata)
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")

ax.scatter3D(mydata['Sales/Revenue'], mydata['Sales Growth'], mydata['Cost of Goods Sold (COGS) incl. D&A'], c=mydata_prediction )
plt.title("3D ploting")
plt.show()
print('kai issiaiskinsiu - plosiu rankom')



