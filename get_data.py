import requests
import pandas as pd
import sqlite3 as sql





# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def set_to_database(inp1, inp2):
    conn = sql.connect('data_base.db')
    inp1.to_sql(str(inp2), conn, if_exists='append')
    conn.close()


def get_data_from_db(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT * FROM ' + inp2, conn)
    conn.close()
    return result


def get_screener(version, page_num):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    screen = requests.get(f'https://finviz.com/screener.ashx?v={version}&r={page_num}', headers = headers).text

    tables = pd.read_html(screen)
    tables = tables[-2]
    tables.columns = tables.iloc[0]
    tables = tables[1:]

    return tables

for num in range(1, 8341, 20):
    tables111 = get_screener('111', num)
    tables161 = get_screener('161', num)
    tables121 = get_screener('121', num)
    tables131 = get_screener('131', num)
    tables141 = get_screener('141', num)
    tables171 = get_screener('171', num)
    consolidatedtables = pd.merge(tables111,tables161,how='outer',left_on='Ticker',right_on='Ticker')
    consolidatedtables1 = pd.merge(consolidatedtables,tables121,how='outer',left_on='Ticker',right_on='Ticker')
    consolidatedtables2 = pd.merge(consolidatedtables1, tables131, how='outer', left_on='Ticker', right_on='Ticker')
    consolidatedtables3 = pd.merge(consolidatedtables2, tables141, how='outer', left_on='Ticker', right_on='Ticker')
    consolidatedtables4 = pd.merge(consolidatedtables3, tables171, how='outer', left_on='Ticker', right_on='Ticker')
    consolidatedtables4 = consolidatedtables4.loc[:, ~consolidatedtables4.columns.duplicated()]

    set_to_database(consolidatedtables4, 'main_tbl')
