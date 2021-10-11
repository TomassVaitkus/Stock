import pandas as pd
import sqlite3 as sql

df_quarter = pd.read_html('https://www.marketwatch.com/investing/stock/tsla/financials/income/quarter')
df_annual = pd.read_html('https://www.marketwatch.com/investing/stock/tsla/financials/income/')
data_frame_quarter_tmp = df_quarter[4]
data_frame_annual_tmp = df_annual[4]

new_row_data_quarter = []
new_row_data_annual = []

for row in data_frame_quarter_tmp['Item  Item']:
    new_row = row.rstrip()[:int(len(row) / 2)].rstrip()
    new_row_data_quarter.append(new_row)


for row1 in data_frame_annual_tmp['Item  Item']:
    new_row1 = row1.rstrip()[:int(len(row1) / 2)].rstrip()
    new_row_data_annual.append(new_row1)


data_frame_quarter_tmp['Item'] = list(new_row_data_quarter)
data_frame_quarter_tmp = data_frame_quarter_tmp.drop(['Item  Item', '5- qtr trend'], axis=1)
first_col_quarter = data_frame_quarter_tmp.pop('Item')
data_frame_quarter_tmp.insert(0, 'Item', first_col_quarter)
data_frame_quarter = data_frame_quarter_tmp.transpose()
data_frame_quarter.columns = data_frame_quarter.iloc[0]
data_frame_quarter = data_frame_quarter.drop(data_frame_quarter.index[0])


data_frame_annual_tmp['Item'] = list(new_row_data_annual)
data_frame_annual_tmp = data_frame_annual_tmp.drop(['Item  Item', '5-year trend'], axis=1)
first_col_quarter = data_frame_annual_tmp.pop('Item')
data_frame_annual_tmp.insert(0, 'Item', first_col_quarter)
data_frame_annual = data_frame_annual_tmp.transpose()
data_frame_annual.columns = data_frame_annual.iloc[0]
data_frame_annual = data_frame_annual.drop(data_frame_annual.index[0])





def get_data_from_db(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT Ticker FROM ' + inp2, conn)
    conn.close()
    return result


table_2017_annual = get_data_from_db('main_tbl')
table_2018_annual = get_data_from_db('main_tbl')
table_2019_annual = get_data_from_db('main_tbl')
table_2020_annual= get_data_from_db('main_tbl')
