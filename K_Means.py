import threading

from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import sqlite3 as sql
import pandas as pd
import numpy as np
from tkinter import *
from tkinter import ttk
from tkintertable import TableCanvas


def get_data_from_db(inp2):            # pasiima is duomenu bazes
    conn = sql.connect('data_base.db')
    result = pd.read_sql('SELECT * FROM ' + inp2, conn)
    conn.close()
    return result


def add_parameters_to_list():       # sukrauna i lista is GUI uzselektintus checkboxus
    global List
    List = []
    for item in Varlist:
        if item.get() != "":
            List.append(item.get())
    print(List)
    return List


def get_entry_values():             # pasiima entry lauku reiksmes
    clustering_time = entry_time_per.get()
    cluster_numb = entry_cluster_num.get()
    companies_num = entry_companies_num.get()

    return clustering_time, cluster_numb, companies_num


def get_column_list():              #pasiima sarasa parametru, kuriuos naudoja klasterizavimui is GUI
    column_list = add_parameters_to_list()
    column_list.insert(0, 'Date')
    column_list.insert(1, 'Ticker')

    return column_list


def function_for_clustering():      #klasterizavimo funkcija
    global my_companies
    user_years = get_entry_values()[0]
    cluster_nr = int(get_entry_values()[1])
    NCI = int(get_entry_values()[2])
    def check_and_drop_nan(inp1,inp2):
        new_df = inp1[inp2].dropna()
        return new_df

    perfomance_df_from_db = get_data_from_db('Perfomance_df').groupby(['Perfomance Date']).get_group(str(user_years)).reset_index()

    mydata = check_and_drop_nan(get_data_from_db('differences_Y'), get_column_list()).reset_index(drop=True)
    grouped_tmp = mydata.groupby(['Date']).get_group(str(user_years))
    grouped_final = grouped_tmp.replace([np.inf, -np.inf], np.nan).dropna(axis=0).reset_index().iloc[:,1:]
    mydata_numpy = grouped_final.iloc[:,2:].to_numpy()

    mydata_prediction = KMeans(n_clusters=cluster_nr).fit_predict(mydata_numpy)

    # fig = plt.figure(figsize = (10, 7))
    # ax = plt.axes(projection ="3d")
    #
    # ax.scatter3D(grouped_final['Sales/Revenue'], grouped_final['Sales Growth'], grouped_final['Cost of Goods Sold (COGS) incl. D&A'], c=mydata_prediction )
    # plt.title("3D ploting")
    # plt.show()

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
    if len(df) > int(NCI):
        my_companies = df.sort_values(by=['Perfomance %'], ascending=False).iloc[0:int(NCI)]
    else:
        my_companies = df.sort_values(by=['Perfomance %'], ascending=False)

    my_companies = my_companies[['Ticker','Perfomance %']]
    print(my_companies)

    return my_companies, cluster_m, df

def function_for_table_in_pages():      # sukrauna i lentele
    final_table = my_companies.to_dict('index')
    table_in_page2 = TableCanvas(frame_for_table, data=final_table, cellwidth=150, width=750, pady=10)
    table_in_page2.show()


def combined_function():                # visu funkciju motina
    add_parameters_to_list()
    function_for_clustering()
    function_for_table_in_pages()
    print('viskas')

#=========================================================================================
#================================       Gaminam GUI  su Funkcijom      ===================
#=========================================================================================


root = Tk()
root.geometry('700x700')
root.title('Companies Clustering Aplication')

# nb = ttk.Notebook(root)
# page1 = ttk.Frame(nb)
# nb.add(page1, text='Settings')
# page2 = ttk.Frame(nb)
# nb.add(page2, text = 'Result')

Entry_label_frame = LabelFrame(root, text = 'Enter Parameters')
Entry_label_frame.grid(row = 0, column = 0,sticky = N)
three_button_frame = LabelFrame(root)
three_button_frame.grid(row = 3, column = 0, sticky = 'w')
checkbox_frame = LabelFrame(root, text = 'Select Parameters')
checkbox_frame.grid(row = 2, column = 0, sticky = 'w',padx = 10,pady = 10)


label_for_time = Label(Entry_label_frame, text = 'Enter For Year To Cluster')
label_for_time.grid(row = 0, column = 0, sticky=W)
label_for_cluster_num = Label(Entry_label_frame, text = 'Enter Number Of Clusters')
label_for_cluster_num.grid(row = 1, column = 0, sticky = W)
label_for_companies = Label(Entry_label_frame, text = 'Enter Number Of Companies To Show')
label_for_companies.grid(row = 2, column = 0, sticky = W)


entry_time_per = Entry(Entry_label_frame)
entry_time_per.grid(row = 0, column = 1)
entry_cluster_num = Entry(Entry_label_frame)
entry_cluster_num.grid(row = 1, column = 1)
entry_companies_num = Entry(Entry_label_frame)
entry_companies_num.grid(row = 2, column = 1)


set_button_1 = Button(Entry_label_frame, text = 'SET')
set_button_1.grid(row = 0, column = 2, sticky = E,padx = 5,pady = 5)
set_button_2 = Button(Entry_label_frame, text = 'SET')
set_button_2.grid(row = 1, column = 2,sticky = E,padx = 5,pady = 5)
set_button_3 = Button(Entry_label_frame, text = 'SET')
set_button_3.grid(row = 2, column = 2,sticky = E,padx = 5,pady = 5)

# lambda: threading.Thread(target=start_auto).start()combined_function
button_calculate = Button(three_button_frame, text = 'Calculate',command=lambda: threading.Thread(target=combined_function, daemon=True).start())
button_calculate.grid(row = 1, column = 0, sticky = W)
button_quit = Button(three_button_frame, text = 'Quit', command = root.destroy)
button_quit.grid(row = 1, column = 1, sticky = W)

Varlist = []
sb = Scrollbar(orient="vertical")
text = Text(checkbox_frame, width=40, height=20, yscrollcommand=sb.set)
text.grid(row = 2, column = 0,sticky = E,padx = 5,pady = 5)
for i in list(get_data_from_db('differences_Y'))[3:]:
    var = StringVar()
    cb = Checkbutton(text="%s" % i, variable=var, onvalue=i, offvalue="",padx=0,pady=0,bd=0)
    text.window_create("end", window=cb)
    text.insert("end", "\n")
    Varlist.append(var)
print(Varlist)

#======================================== Page2 =====================
frame_for_table = LabelFrame(root, text = 'Table')
frame_for_table.grid(row = 2, column = 1, sticky = E)
table2 = TableCanvas(frame_for_table)
# table2.grid(row = 2, column = 1, sticky = E)
table2.show()



# nb.pack(fill=BOTH, expand=1)
root.mainloop()
















