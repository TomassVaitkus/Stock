from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import sqlite3 as sql
import pandas as pd
import numpy as np
# import yfinance as yf
import datetime

def get_data_from_db(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT * FROM ' + inp2, conn)
    conn.close()
    return result


def set_to_database(inp1, inp2):
    conn = sql.connect('data_base.db')
    inp1.to_sql(inp2, conn, if_exists='append', index=False)
    conn.close()


data_Y = get_data_from_db('annual_data_p')      #pasiimu is db visa data
ticker = list(data_Y['Ticker'].unique() )       #pasiimu tickerius ir pasidarau juos unikalius ir tai bus inputas i
                                                    # istoriniu duomenu funkcija
# ticker= ['TSLA', 'AMZN']
date_start = get_data_from_db('differences_Y')['Date'].unique()#pasiimam datas is db
date_start = sorted(date_start)[-5:]
date_end = pd.Series(date_start).astype(int)+1 #pasidarompabaigos data pridedami vienus metus prie date_start


perfomace_list = []     #gautas perfomansas liste procentais
ticker_list = []        # naudotu tickeriu listas
perfomance_date= []     # perfomanso data listas

# count = 5
# for t in ticker:
#     try:
#         for i in date_start:
#             if count > 1:
#                 data_start_price = float(yf.download(t, str(i) + '-01-01', str(i) + '-01-06')['Adj Close'].values[0])
#                 data_end_price = float(yf.download(t, str(i) + '-12-25', str(i) + '-12-31')['Adj Close'].values[0])
#                 perfomance = ((data_end_price - data_start_price) * 100) / data_start_price
#                 print(perfomance)
#                 perfomace_list.append(perfomance)
#                 ticker_list.append(t)
#                 perfomance_date.append(i)
#                 count = count - 1
#             elif count ==1:
#                 data_start_price = float(yf.download(t, str(i) + '-01-01', str(i) + '-01-06')['Adj Close'].values[0])
#                 data_end_price = float(yf.download(t, str(i)+ (datetime.date.today() - datetime.timedelta(days=5)).strftime('-%m-%d'), str(i)+ (datetime.date.today() - datetime.timedelta(days=1)).strftime('-%m-%d'))['Adj Close'].values[0])
#                 perfomance = ((data_end_price - data_start_price) * 100) / data_start_price
#                 print(perfomance)
#                 perfomace_list.append(perfomance)
#                 ticker_list.append(t)
#                 perfomance_date.append(i)
#                 count = (count -1) +5
#             else:
#                 continue
#     except:
#         continue


# perfomance_df = pd.DataFrame({'Ticker': ticker_list, 'Perfomance Date': perfomance_date, 'Perfomance %': perfomace_list})

# set_to_database(perfomance_df, 'Perfomance_df')


column_list = ['Sales/Revenue','Sales Growth','Cost of Goods Sold (COGS) incl. D&A']
column_list.insert(0,'Date')
column_list1 = column_list.insert(1, 'Ticker')
user_years = 2020
cluster_nr = 3
NCI = 2                                                                 #cia Number of Companies to Invest




def check_and_drop_nan(inp1,inp2):
    new_df = inp1[inp2].dropna()
    return new_df

perfomance_df_from_db = get_data_from_db('Perfomance_df').groupby(['Perfomance Date']).get_group(str(user_years)).reset_index()

mydata = check_and_drop_nan(get_data_from_db('differences_Y'), column_list).reset_index(drop=True)
grouped_tmp = mydata.groupby(['Date']).get_group(str(user_years))
grouped_final = grouped_tmp.replace([np.inf, -np.inf], np.nan).dropna(axis=0).reset_index().iloc[:,1:]
mydata_numpy = grouped_final.iloc[:,2:].to_numpy()

mydata_prediction = KMeans(n_clusters=cluster_nr).fit_predict(mydata_numpy)

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")

ax.scatter3D(grouped_final['Sales/Revenue'], grouped_final['Sales Growth'], grouped_final['Cost of Goods Sold (COGS) incl. D&A'], c=mydata_prediction )
plt.title("3D ploting")
plt.show()

clustered_df = pd.concat([grouped_final, pd.DataFrame(mydata_prediction)], axis=1)   #cia priglaudziu labelius prie klasterizuojamu duomenu


perf_list = []

for i in clustered_df['Ticker']:
    print(i)
    try:
        perf = float(perfomance_df_from_db.groupby('Ticker').get_group(i)['Perfomance %'])
        perf_list.append(perf)

    except:
        perf_list.append(np.nan)



clustered_df['Perfomance %'] = perf_list

cluster_m = []
for i in range(cluster_nr):
    cluster_i = clustered_df.groupby([0]).get_group(i)
    clust_perf_mean = cluster_i['Perfomance %'].mean(axis=0, skipna=True)
    cluster_m.append(clust_perf_mean)


winner_clust = cluster_m.index(max(cluster_m))

#dabar traukiam laimetojo klasterio dar nekilusias koompanijas

df = clustered_df.groupby([0]).get_group(winner_clust)
if len(df) > NCI:
    my_companies = df.sort_values(by=['Perfomance %'], ascending=False).iloc[0:NCI]
else:
    my_companies = df.sort_values(by=['Perfomance %'], ascending=False)




print(my_companies[['Ticker','Perfomance %']])



























