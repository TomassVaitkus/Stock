import datetime

import pandas as pd
import sqlite3 as sql


def get_data_from_db(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT * FROM ' + inp2, conn)
    conn.close()
    return result

def set_to_database(inp1, inp2):
    conn = sql.connect('data_base.db')
    inp1.to_sql(inp2, conn, if_exists='append', index=False)
    conn.close()



annual_from_db = get_data_from_db('annual_data')
annual_from_db = annual_from_db.drop(['index'], axis=1).astype(str)

quater_from_db = get_data_from_db('quarter_data')
quater_from_db = quater_from_db.drop(['index'], axis=1).astype(str)

main_from_db = get_data_from_db('main_tbl')
main_from_db = main_from_db.drop(['index','No._x','Ticker','Company', 'Sector', 'Industry','Country'], axis=1).astype(str)

first = datetime.datetime.now()
# for column in annual_from_db.iloc[:, 2:]:
#     for i in range(len(annual_from_db[column])):
#         if "(" in annual_from_db[column][i]:
#             if 'M' in annual_from_db[column][i]:
#                 converted = float(annual_from_db[column][i].replace('(', '').replace(')', '').replace('M', ''))
#                 annual_from_db[column][i] = -abs(converted)   #cia gali buti daugyba is -1
#             elif 'B' in annual_from_db[column][i]:
#                 converted1 = float(annual_from_db[column][i].replace('(', '').replace(')', '').replace('B', ''))
#                 annual_from_db[column][i] = -abs(converted1)* 1000
#             elif 'K' in annual_from_db[column][i]:
#                 converted2 = float(annual_from_db[column][i].replace('(', '').replace(')', '').replace('K', ''))
#                 annual_from_db[column][i] = -abs(converted2)/1000
#             elif 'T' in annual_from_db[column][i]:
#                 converted3 = float(annual_from_db[column][i].replace('(', '').replace(')', '').replace('T', ''))
#                 annual_from_db[column][i] = -abs(converted3) * 1000000
#             elif ')' in annual_from_db[column][i]:
#                 converted0 = float(annual_from_db[column][i].replace('(', '').replace(')', ''))
#                 annual_from_db[column][i] = -abs(converted0)
#             else:
#                 continue
#         else:
#             if 'M' in annual_from_db[column][i]:
#                 converted = float(annual_from_db[column][i].replace('M', ''))
#                 annual_from_db[column][i] = converted
#             elif 'B' in annual_from_db[column][i]:
#                 converted1 = float(annual_from_db[column][i].replace('B', ''))
#                 annual_from_db[column][i] = converted1* 1000
#             elif 'K' in annual_from_db[column][i]:
#                 converted2 = float(annual_from_db[column][i].replace('K', ''))
#                 annual_from_db[column][i] = converted2/1000
#             elif '%' in annual_from_db[column][i]:
#                 converted3 = float(annual_from_db[column][i].replace('%', '').replace(',', ''))
#                 annual_from_db[column][i] = converted3
#             elif '-' in annual_from_db[column][i]:
#                 converted = float(annual_from_db[column][i].replace('-', 'nan'))
#                 annual_from_db[column][i] = converted
#             elif 'T' in annual_from_db[column][i]:
#                 converted3 = float(annual_from_db[column][i].replace('(', '').replace(')', '').replace('T', ''))
#                 annual_from_db[column][i] = -abs(converted3) * 1000000
#             else:
#                 continue
#
# set_to_database(annual_from_db, 'annual_data_p')
# print('Pirmas done')
# for column in quater_from_db.iloc[:, 2:]:
#     for i in range(len(quater_from_db[column])):
#         if "(" in quater_from_db[column][i]:
#             if 'M' in quater_from_db[column][i]:
#                 converted = float(quater_from_db[column][i].replace('(', '').replace(')', '').replace('M', ''))
#                 quater_from_db[column][i] = -abs(converted)   #cia gali buti daugyba is -1
#             elif 'B' in quater_from_db[column][i]:
#                 converted1 = float(quater_from_db[column][i].replace('(', '').replace(')', '').replace('B', ''))
#                 quater_from_db[column][i] = -abs(converted1)* 1000
#             elif 'K' in quater_from_db[column][i]:
#                 converted2 = float(quater_from_db[column][i].replace('(', '').replace(')', '').replace('K', ''))
#                 quater_from_db[column][i] = -abs(converted2)/1000
#             elif 'T' in quater_from_db[column][i]:
#                 converted3 = float(quater_from_db[column][i].replace('(', '').replace(')', '').replace('T', ''))
#                 quater_from_db[column][i] = -abs(converted3) * 1000000
#             elif ')' in quater_from_db[column][i]:
#                 converted0 = float(quater_from_db[column][i].replace('(', '').replace(')', ''))
#                 quater_from_db[column][i] = -abs(converted0)
#             else:
#                 continue
#         else:
#             if 'M' in quater_from_db[column][i]:
#                 converted = float(quater_from_db[column][i].replace('M', ''))
#                 quater_from_db[column][i] = converted
#             elif 'B' in quater_from_db[column][i]:
#                 converted1 = float(quater_from_db[column][i].replace('B', ''))
#                 quater_from_db[column][i] = converted1* 1000
#             elif 'K' in quater_from_db[column][i]:
#                 converted2 = float(quater_from_db[column][i].replace('K', ''))
#                 quater_from_db[column][i] = converted2/1000
#             elif '%' in quater_from_db[column][i]:
#                 converted3 = float(quater_from_db[column][i].replace('%', '').replace(',', ''))
#                 quater_from_db[column][i] = converted3
#             elif '-' in quater_from_db[column][i]:
#                 converted = float(quater_from_db[column][i].replace('-', 'nan'))
#                 quater_from_db[column][i] = converted
#             elif 'T' in quater_from_db[column][i]:
#                 converted3 = float(quater_from_db[column][i].replace('(', '').replace(')', '').replace('T', ''))
#                 quater_from_db[column][i] = -abs(converted3) * 1000000
#             else:
#                 continue
#
#
# print('Antras done')
# set_to_database(quater_from_db, 'quarter_data_p')

# for column in main_from_db:
#     print(column)


# einam per finvizo duomenis ir issivalom puses metu perfomansa, kad butu tvarkingi skaiciai.
for i in range(len(main_from_db['Perf Half'])):
    print(i)
    if "(" in main_from_db['Perf Half'][i]:
        if 'M' in main_from_db['Perf Half'][i]:
            converted = float(main_from_db['Perf Half'][i].replace('(', '').replace(')', '').replace('M', ''))
            main_from_db['Perf Half'][i] = -abs(converted)  # cia gali buti daugyba is -1
        elif 'B' in main_from_db['Perf Half'][i]:
            converted1 = float(main_from_db['Perf Half'][i].replace('(', '').replace(')', '').replace('B', ''))
            main_from_db['Perf Half'][i] = -abs(converted1) * 1000
        elif 'K' in main_from_db['Perf Half'][i]:
            converted2 = float(main_from_db['Perf Half'][i].replace('(', '').replace(')', '').replace('K', ''))
            main_from_db['Perf Half'][i] = -abs(converted2) / 1000
        elif 'T' in main_from_db['Perf Half'][i]:
            converted3 = float(main_from_db['Perf Half'][i].replace('(', '').replace(')', '').replace('T', ''))
            main_from_db['Perf Half'][i] = -abs(converted3) * 1000000
        elif ')' in main_from_db['Perf Half'][i]:
            converted0 = float(main_from_db['Perf Half'][i].replace('(', '').replace(')', ''))
            main_from_db['Perf Half'][i] = -abs(converted0)
        else:
            continue
    else:
        if 'M' in main_from_db['Perf Half'][i]:
            converted = float(main_from_db['Perf Half'][i].replace('M', ''))
            main_from_db['Perf Half'][i] = converted
        elif 'B' in main_from_db['Perf Half'][i]:
            converted1 = float(main_from_db['Perf Half'][i].replace('B', ''))
            main_from_db['Perf Half'][i] = converted1 * 1000
        elif 'K' in main_from_db['Perf Half'][i]:
            converted2 = float(main_from_db['Perf Half'][i].replace('K', ''))
            main_from_db['Perf Half'][i] = converted2 / 1000
        elif '%' in main_from_db['Perf Half'][i]:
            converted3 = float(main_from_db['Perf Half'][i].replace('%', '').replace(',', ''))
            main_from_db['Perf Half'][i] = converted3
        elif '-' in main_from_db['Perf Half'][i]:
            converted = float(main_from_db['Perf Half'][i].replace('-', 'nan'))
            main_from_db['Perf Half'][i] = converted
        elif 'T' in main_from_db['Perf Half'][i]:
            converted3 = float(main_from_db['Perf Half'][i].replace('(', '').replace(')', '').replace('T', ''))
            main_from_db['Perf Half'][i] = -abs(converted3) * 1000000
        else:
            continue


print('Trecias done')
set_to_database(main_from_db, 'main_tbl_p')
second = datetime.datetime.now()






print("laikas =  ", second - first)
