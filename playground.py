# import pandas as pd
# # import numpy as np
# # import random
# import sqlite3 as sql
# # from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
#
#
# def get_data_from_db(inp2):
#     conn = sql.connect('data_base.db')
#     result = pd.read_sql('SELECT * FROM ' + inp2, conn)
#     conn.close()
#     return result

# df = pd.DataFrame(np.random.randn(20, 5), columns=['one', 'two', 'three','four','five'])
# ix = [(row, col) for row in range(df.shape[0]) for col in range(df.shape[1])]
# for row, col in random.sample(ix, int(round(0.3*len(ix)))):
#     df.iat[row, col] = np.nan
#
# new_df =df[['one','three','five']].dropna().reset_index(drop=True)
#
#
#
# model = KMeans(n_clusters=5).fit(new_df)
# print(model.labels_)
#
# print(new_df)

# count = 5
# l = ['a','b','c','d','e','f','g','h']
# while count > 1:
#     for i in l:
#         print(i)
#         count = count -1
#         if count == 1:
#             break

# import sqlite3 as sql
# import pandas as pd
#
#
# def get_data_from_db(inp2):
#     conn = sql.connect('data_base.db')
#     result = pd.read_sql('SELECT * FROM ' + inp2, conn)
#     conn.close()
#     return result
#
#
# a = get_data_from_db('differences_Y')
#
#
# print('la')

#=================================================================================
#=============== klasterio isskyrimas=====================================
#
# points_5C = []
# for point in points_5C:
#     if kmeans_label==5:
#         points_5C.append(point)
#

#=========================================================================
# user_years = 2020
# perfomance_df_from_db = get_data_from_db('Perfomance_df').groupby(['Perfomance Date']).get_group(str(user_years))
#
#
# for i in range(len(perfomance_df_from_db)):
#     print(perfomance_df_from_db.iloc[:]['Ticker'][i])
#
#
# print("l")
# Import Tkinter library
# importing only those functions
# which are needed
