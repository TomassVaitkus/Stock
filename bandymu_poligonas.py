import pandas as pd
import sqlite3 as sql

df_quarter= pd.read_html('https://www.marketwatch.com/investing/stock/tsla/financials/income/quarter')
df_annual = pd.read_html('https://www.marketwatch.com/investing/stock/tsla/financials/income/')
data_frame_quarter = df_quarter[4]
data_frame_annual = df_annual[4]


new_row_data_quarter = []
new_row_data_annual = []

for row in data_frame_quarter['Item  Item']:
    new_row = row.rstrip()[:int(len(row) / 2)].rstrip()
    new_row_data_quarter.append(new_row)

for row1 in data_frame_annual['Item  Item']:
    new_row1 = row1.rstrip()[:int(len(row1) / 2)].rstrip()
    new_row_data_annual.append(new_row1)

table_for_quarter = pd.DataFrame(columns = new_row_data_quarter)
table_for_annual = pd.DataFrame(columns = new_row_data_annual)

def get_data_from_db(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT Ticker FROM ' + inp2, conn)
    conn.close()
    return result

table_2017  = get_data_from_db('main_tbl')
table_2018  = get_data_from_db('main_tbl')
table_2019  = get_data_from_db('main_tbl')
table_2020  = get_data_from_db('main_tbl')


