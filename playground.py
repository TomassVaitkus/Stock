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
import tkinter as tk
from tkinter import  *

root = tk.Tk()
choices = ('network one', 'network two', 'network three')
var = tk.StringVar(root)
entry = Entry(root)
entry.grid()
def refresh():
    # Reset var and delete all old options
    var.set('')
    network_select['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to var)
    new_choices = [str(x) for x in str(list(range(int(entry.get())))) if x.isdigit()]
    for choice in new_choices:
        network_select['menu'].add_command(label=choice, command=tk._setit(var, choice))

network_select = tk.OptionMenu(root, var, *choices)
network_select.grid()

# I made this quick refresh button to demonstrate
tk.Button(root, text='Refresh', command=refresh).grid()

root.mainloop()