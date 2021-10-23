import time

import pandas as pd
import sqlite3 as sql


def set_to_database(inp1, inp2):
    conn = sql.connect('data_base.db')
    inp1.to_sql(inp2, conn, if_exists='append')
    conn.close()

def get_ticker_from_db_table(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT Ticker FROM ' + inp2, conn)
    conn.close()
    return result

tickers = get_ticker_from_db_table('main_tbl')

sample_quarter = pd.read_html('https://www.marketwatch.com/investing/stock/amzn/financials/income/quarter')
sample_table_quarter = sample_quarter[4]
sample_annual = pd.read_html('https://www.marketwatch.com/investing/stock/amzn/financials/income')
sample_table_annual = sample_annual[4]

for ticker in tickers['Ticker']:
    list_of_features_quarter = []
    try:
        df_quarter = pd.read_html(f'https://www.marketwatch.com/investing/stock/{ticker}/financials/income/quarter')
        if len(df_quarter) > 4:
            data_frame_quarter_tmp = df_quarter[4]
            if 'Item  Item' in data_frame_quarter_tmp and '5- qtr trend' in data_frame_quarter_tmp:
                if data_frame_quarter_tmp['Item  Item'].equals(sample_table_quarter['Item  Item']):
                    for row in data_frame_quarter_tmp['Item  Item']:
                        feature_name = row.rstrip()[:int(len(row) / 2)].rstrip()
                        list_of_features_quarter.append(feature_name)
                    data_frame_quarter_tmp['Features'] = list(list_of_features_quarter)
                    data_frame_quarter_tmp = data_frame_quarter_tmp.drop(['Item  Item', '5- qtr trend'], axis=1)
                    first_col_quarter = data_frame_quarter_tmp.pop('Features')
                    data_frame_quarter_tmp.insert(0, 'Features', first_col_quarter)
                    data_frame_quarter = data_frame_quarter_tmp.transpose()
                    data_frame_quarter.columns = data_frame_quarter.iloc[0]
                    data_frame_quarter = data_frame_quarter.drop(data_frame_quarter.index[0])
                    data_frame_quarter.index.name = 'Date'
                    data_frame_quarter.insert(0, 'Ticker', ticker)
                    data_frame_quarter.reset_index(inplace=True)
                    data_frame_quarter = pd.DataFrame(data = data_frame_quarter)
                    set_to_database(data_frame_quarter, 'quarter_data')
                else:
                    print("nelygus stulpas Item Item / " + ticker)
                    continue
            else:
                print("tuscia / " + ticker)
                continue
        else:
            print('nerado lentos / ' + ticker)
            continue
    except:
        time.sleep(5)


for ticker in tickers['Ticker']:
    list_of_features_annual = []
    try:
        df_annual = pd.read_html(f'https://www.marketwatch.com/investing/stock/{ticker}/financials/income')
        if len(df_annual) > 4:
            data_frame_annual_tmp = df_annual[4]
            if 'Item  Item' in data_frame_annual_tmp and '5-year trend' in data_frame_annual_tmp:
                if data_frame_annual_tmp['Item  Item'].equals(sample_table_annual['Item  Item']):
                    for row in data_frame_annual_tmp['Item  Item']:
                        feature_name = row.rstrip()[:int(len(row) / 2)].rstrip()
                        list_of_features_annual.append(feature_name)
                    data_frame_annual_tmp['Features'] = list(list_of_features_annual)
                    data_frame_annual_tmp = data_frame_annual_tmp.drop(['Item  Item', '5-year trend'], axis=1)
                    first_col_quarter = data_frame_annual_tmp.pop('Features')
                    data_frame_annual_tmp.insert(0, 'Features', first_col_quarter)
                    data_frame_annual = data_frame_annual_tmp.transpose()
                    data_frame_annual.columns = data_frame_annual.iloc[0]
                    data_frame_annual = data_frame_annual.drop(data_frame_annual.index[0])
                    data_frame_annual.index.name = 'Date'
                    data_frame_annual.insert(0, 'Ticker', ticker)
                    data_frame_annual.reset_index(inplace=True)
                    data_frame_annual = pd.DataFrame(data = data_frame_annual)
                    set_to_database(data_frame_annual, 'annual_data')
                else:
                    print("nelygus stulpas Item Item / " + ticker)
                    continue
            else:
                print("tuscia / " + ticker)
                continue
        else:
            print('nerado lentos / ' + ticker)
            continue
    except:
        time.sleep(5)




