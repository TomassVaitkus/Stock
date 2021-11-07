import pandas as pd
import sqlite3 as sql
import yfinance as yf
import datetime


def get_data_from_db(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT * FROM ' + inp2, conn)
    conn.close()
    return result


def set_to_database(inp1, inp2):
    conn = sql.connect('data_base.db')
    inp1.to_sql(inp2, conn, if_exists='replace', index=False)
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

count = 5
for t in ticker:
    try:
        for i in date_start:
            if count > 1:
                data_start_price = float(yf.download(t, str(i) + '-01-01', str(i) + '-01-06')['Adj Close'].values[0])
                data_end_price = float(yf.download(t, str(i) + '-12-25', str(i) + '-12-31')['Adj Close'].values[0])
                perfomance = ((data_end_price - data_start_price) * 100) / data_start_price
                print(perfomance)
                perfomace_list.append(perfomance)
                ticker_list.append(t)
                perfomance_date.append(i)
                count = count - 1
            elif count ==1:
                data_start_price = float(yf.download(t, str(i) + '-01-01', str(i) + '-01-06')['Adj Close'].values[0])
                data_end_price = float(yf.download(t, str(i)+ (datetime.date.today() - datetime.timedelta(days=5)).strftime('-%m-%d'), str(i)+ (datetime.date.today() - datetime.timedelta(days=1)).strftime('-%m-%d'))['Adj Close'].values[0])
                perfomance = ((data_end_price - data_start_price) * 100) / data_start_price
                print(perfomance)
                perfomace_list.append(perfomance)
                ticker_list.append(t)
                perfomance_date.append(i)
                count = (count -1) +5
            else:
                continue
    except:
        continue


perfomance_df = pd.DataFrame({'Ticker': ticker_list, 'Perfomance Date': perfomance_date, 'Perfomance %': perfomace_list})

set_to_database(perfomance_df, 'Perfomance_df')