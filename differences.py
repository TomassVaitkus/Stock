import datetime

import pandas as pd
import sqlite3 as sql


def set_to_database(inp1, inp2):
    conn = sql.connect('data_base.db')
    inp1.to_sql(inp2, conn, if_exists='append', index=False)
    conn.close()


def get_data_from_db(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT * FROM ' + inp2, conn)
    conn.close()
    return result

print("Pradedu metinius skirtumus formuot")
first = datetime.datetime.now()
preprocesed_data_Y = get_data_from_db('annual_data_p')
unique_tickers_Y = preprocesed_data_Y['Ticker'].unique()
differences_Y = pd.DataFrame()

for t in unique_tickers_Y:
    t_tmp = preprocesed_data_Y.groupby(['Ticker']).get_group(t)
    t_tmp_ticker = t_tmp.iloc[:, :2]
    t_tmp = t_tmp.iloc[:, 2:].apply(pd.to_numeric)
    for idx in range(len(t_tmp) - 1):
        date_ticker_tmp = pd.DataFrame(t_tmp_ticker.iloc[idx+1]).transpose()
        if len(str(float(date_ticker_tmp['Date'].iloc[:]))) > 4:
            date_ticker_tmp['Date'] = str(float(date_ticker_tmp['Date'].iloc[:]))[:4]
        res1 = t_tmp.iloc[idx + 1]
        res2 = t_tmp.iloc[idx]
        difference = ((res1 - res2) * 100) / res2
        difference = pd.DataFrame(difference).transpose()  # apskaiciuotas skirtumas
        date_ticker_tmp.index = difference.index
        # dabar sujungiu abu df ir turiu gauti viena vietisa eilute su data, tickeriu ir skirtumais
        final_tmp = pd.concat([date_ticker_tmp, difference], axis=1)
        differences_Y = differences_Y.append(final_tmp)



differences_Y = differences_Y.reset_index()
set_to_database(differences_Y, 'differences_Y')
print("Metini praejau ir i db sudejau")

#======================================================================================

print("Pradedu ketvirtinius skirtumus formuot")
preprocesed_data_Q = get_data_from_db('quarter_data_p')
unique_tickers_Q = preprocesed_data_Q['Ticker'].unique()
differences_Q = pd.DataFrame()

for t in unique_tickers_Q:
    t_tmp = preprocesed_data_Q.groupby(['Ticker']).get_group(t)
    t_tmp_ticker = t_tmp.iloc[:, :2]
    t_tmp = t_tmp.iloc[:, 2:].apply(pd.to_numeric)
    for idx in range(len(t_tmp) - 1):
        date_ticker_tmp = pd.DataFrame(t_tmp_ticker.iloc[idx+1]).transpose()      #data ir tickeris
        res1 = t_tmp.iloc[idx + 1]
        res2 = t_tmp.iloc[idx]
        difference = ((res1 - res2) *100)/res2
        difference = pd.DataFrame(difference).transpose()   #apskaiciuotas skirtumas
        date_ticker_tmp.index = difference.index
        # dabar sujungiu abu df ir turiu gauti viena vietisa eilute su data, tickeriu ir skirtumais
        final_tmp = pd.concat([date_ticker_tmp, difference], axis=1)
        differences_Q = differences_Q.append(final_tmp)

differences_Q = differences_Q.reset_index()
set_to_database(differences_Q, 'differences_Q')
second = datetime.datetime.now()
print("Ketvirtinius praejau ir i db sudejau")
print('Laikas lygus:  ', second - first)













