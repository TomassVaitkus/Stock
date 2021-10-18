import pandas as pd
import sqlite3 as sql


def get_data_from_db(inp2):
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT * FROM ' + inp2, conn)
    conn.close()
    return result


# def prep_data():


annual_from_db = get_data_from_db('annual_data')
annual_from_db = annual_from_db.drop(['index'], axis=1).astype(str)


for column in annual_from_db.iloc[:, 2:]:
    for i in range(len(annual_from_db[column])):
        if "(" in annual_from_db[column][i]:
            if 'M' in annual_from_db[column][i]:
                converted = float(annual_from_db[column][i].replace('(', '').replace(')', '').replace('M', ''))
                annual_from_db[column][i] = -abs(converted)   #cia gali buti daugyba is -1
            elif 'B' in annual_from_db[column][i]:
                converted1 = float(annual_from_db[column][i].replace('(', '').replace(')', '').replace('B', ''))
                annual_from_db[column][i] = -abs(converted1)* 1000
            elif 'K' in annual_from_db[column][i]:
                converted2 = float(annual_from_db[column][i].replace('(', '').replace(')', '').replace('K', ''))
                annual_from_db[column][i] = -abs(converted2)/1000
            else:
                continue
        else:
            if 'M' in annual_from_db[column][i]:
                converted = float(annual_from_db[column][i].replace('M', ''))
                annual_from_db[column][i] = converted
            elif 'B' in annual_from_db[column][i]:
                converted1 = float(annual_from_db[column][i].replace('B', ''))
                annual_from_db[column][i] = converted1* 1000
            elif 'K' in annual_from_db[column][i]:
                converted2 = float(annual_from_db[column][i].replace('K', ''))
                annual_from_db[column][i] = converted2/1000
            else:
                continue

            # cleaned_tmp = annual_from_db[column].loc[annual_from_db[column].str.contains('()', na=False, regex=True)][column].replace('(','').replace(')', '').replace('M', '')
            # annual_from_db[column][annual_from_db[column].str.contains('M')] = cleaned_tmp.astype(str)
# for column in annual_from_db.iloc[:, 4:]:
#     for i in range(len(annual_from_db[column])):
#         cleaned_tmp = annual_from_db[column].loc[annual_from_db[column].str.contains('B', na=False, regex=True)].str.strip('()')
#         naujas_tmp = cleaned_tmp.str.replace('B', '').astype(float)*1000
#         annual_from_db[column][annual_from_db[column].str.contains('B')] = naujas_tmp.astype(str)
#
#         cleaned1_tmp = annual_from_db[column].loc[annual_from_db[column].str.contains('M', na=False, regex=True)].str.strip('()')
#         naujas_tmp = cleaned1_tmp.str.replace('M', '').astype(float)
#         annual_from_db[column][annual_from_db[column].str.contains('M')] = naujas_tmp.astype(str)
#
#         cleaned2_tmp = annual_from_db[column].loc[annual_from_db[column].str.contains('K', na=False, regex=True)].str.strip('()')
#         naujas_tmp = cleaned2_tmp.str.replace('K', '').astype(float)/1000
#         annual_from_db[column][annual_from_db[column].str.contains('K')] = naujas_tmp.astype(str)
#
#         cleaned3_tmp = annual_from_db[column].loc[annual_from_db[column].str.contains('%', na=False, regex=True)].str.strip('()')
#         naujas_tmp = cleaned3_tmp.str.replace('%', '').astype(float)
#         annual_from_db[column][annual_from_db[column].str.contains('%')] = naujas_tmp.astype(str)

print(annual_from_db)
