import threading
import tkinter as tk

import seaborn as sns
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
from configparser import ConfigParser
import numbers



def set_year_to_cluster_conf():
    parser = ConfigParser()
    parser.read('Configuration_stock_file.ini')
    parser.set('entry_values', 'Year_time', entry_time_per.get())
    with open('Configuration_stock_file.ini', 'w') as configfile:
        parser.write(configfile)

def set_number_to_cluster_conf():
    parser = ConfigParser()
    parser.read('Configuration_stock_file.ini')
    parser.set('entry_values', 'numb_clusters', entry_cluster_num.get())
    with open('Configuration_stock_file.ini', 'w') as configfile:
        parser.write(configfile)
        

def set_number_of_companies_conf():
    parser = ConfigParser()
    parser.read('Configuration_stock_file.ini')
    parser.set('entry_values', 'comp_to_show', entry_companies_num.get())
    with open('Configuration_stock_file.ini', 'w') as configfile:
        parser.write(configfile)


def get_from_config_file():
    saved_time = parser.get('entry_values', 'year_time')
    saved_cluster_nr = parser.get('entry_values', 'numb_clusters')
    saved_companies_num = parser.get('entry_values', 'comp_to_show')
    return saved_time, saved_cluster_nr, saved_companies_num







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
    global my_companies, clust_idx
    user_years = get_from_config_file()[0]
    cluster_nr = int(get_from_config_file()[1])
    NCI = int(get_from_config_file()[2])
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
    clust_idx = []
    for i in range(cluster_nr):
        cluster_i = clustered_df.groupby([0]).get_group(i)
        clust_perf_mean = cluster_i['Perfomance %'].mean(axis=0, skipna=True)
        cluster_m.append(clust_perf_mean)
        clust_idx.append(i)


    winner_clust = cluster_m.index(max(cluster_m))

    #dabar traukiam laimetojo klasterio dar nekilusias koompanijas

    df = clustered_df.groupby([0]).get_group(winner_clust)
    if len(df) > int(NCI):
        my_companies = df.sort_values(by=['Perfomance %'], ascending=False).iloc[0:int(NCI)]
    else:
        my_companies = df.sort_values(by=['Perfomance %'], ascending=False)

    my_companies = my_companies[['Ticker','Perfomance %']]
    print(my_companies)
    # max_of_my_companies = np.array(max(my_companies['Perfomance %']))
    # min_of_my_companies = np.array(min(my_companies['Perfomance %']))
    for i in range(cluster_nr):
        clust_i = clustered_df.groupby([0]).get_group(i)
        sns.boxplot(clust_i['Perfomance %'], orient = 'V')

    return my_companies, cluster_m, df

#
# def select_clusters_to_view():
#




def function_for_table_in_pages():      # sukrauna i lentele
    final_table = my_companies.to_dict('index')
    table_in_page2 = TableCanvas(frame_for_table, data=final_table, cellwidth=130, width=270, height = 300, pady=10)
    table_in_page2.show()


def refresh():
    # Reset var and delete all old options
    var.set('')
    cluster_menu['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to var)
    new_choices = [str(x) for x in str(list(range(int(entry_cluster_num.get())))) if x.isdigit()]
    for choice in new_choices:
        cluster_menu['menu'].add_command(label=choice, command=tk._setit(var, choice))


def combined_function():                # visu funkciju motina
    refresh()
    set_year_to_cluster_conf()
    set_number_to_cluster_conf()
    set_number_of_companies_conf()
    add_parameters_to_list()
    function_for_clustering()
    function_for_table_in_pages()

    print('viskas')

#=========================================================================================
#================================       Gaminam GUI  su Funkcijom      ===================
#=========================================================================================


root = Tk()
root.geometry('1300x520')
root.title('Companies Clustering Aplication')

var = StringVar(root)

parser = ConfigParser()
parser.read('Configuration_stock_file.ini')
saved_year_time = parser.get('entry_values', 'Year_time')
saved_numb_clusters = parser.get('entry_values', 'numb_clusters')
saved_comp_to_show = parser.get('entry_values', 'comp_to_show')
# nb = ttk.Notebook(root)
# page1 = ttk.Frame(nb)height
# nb.add(page1, text='Settings')
# page2 = ttk.Frame(nb)
# nb.add(page2, text = 'Result')

Entry_label_frame = LabelFrame(root, text = 'Enter Parameters')
Entry_label_frame.grid(row = 0,sticky = N)
two_button_frame = LabelFrame(root)
two_button_frame.grid(row = 3, column = 0, sticky = 'w')
checkbox_frame = LabelFrame(root, text = 'Select Parameters')
checkbox_frame.grid(row = 2, column = 0, sticky = 'w',padx = 10,pady = 10)


label_for_time = Label(Entry_label_frame, text = 'Enter For Year To Cluster')
label_for_time.grid(row = 0, column = 0, sticky=W)

label_for_cluster_num = Label(Entry_label_frame, text = 'Enter Number Of Clusters')
label_for_cluster_num.grid(row = 1, column = 0, sticky = W)

label_for_companies = Label(Entry_label_frame, text = 'Enter Number Of Companies To Show')
label_for_companies.grid(row = 0, column = 4, sticky = W)

label_for_coluster_to_show = Label(Entry_label_frame, text = 'Choose Cluster to Show')
label_for_coluster_to_show.grid(row = 1, column = 4, sticky = W)


entry_time_per = Entry(Entry_label_frame)
entry_time_per.grid(row = 0, column = 1)
entry_cluster_num = Entry(Entry_label_frame)
entry_cluster_num.grid(row = 1, column = 1)
entry_companies_num = Entry(Entry_label_frame)
entry_companies_num.grid(row = 0, column = 5)
cluster_menu = OptionMenu(Entry_label_frame, "Select an Option", *[str(x) for x in str(list(range(int(get_from_config_file()[1])))) if x.isdigit()])
cluster_menu.grid(row = 1, column = 5)


set_button_1 = Button(Entry_label_frame, text = 'SET',command = set_year_to_cluster_conf)
set_button_1.grid(row = 0, column = 2, sticky = E,padx = 5,pady = 5)
set_button_2 = Button(Entry_label_frame, text = 'SET', command = set_number_to_cluster_conf)
set_button_2.grid(row = 1, column = 2,sticky = E,padx = 5,pady = 5)
set_button_3 = Button(Entry_label_frame, text = 'SET', command = set_number_of_companies_conf)
set_button_3.grid(row = 0, column = 6,sticky = E,padx = 5,pady = 5)

# lambda: threading.Thread(target=start_auto).start()combined_function
button_calculate = Button(two_button_frame, text = 'Calculate',command=lambda: threading.Thread(target=combined_function, daemon=True).start())
button_calculate.grid(row = 1, column = 0, sticky = W)
button_quit = Button(two_button_frame, text = 'Quit', command = root.destroy)
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
frame_for_table.grid(row = 2, column = 0, sticky = E)
# table2 = TableCanvas(frame_for_table)
# # table2.grid(row = 2, column = 1, sticky = E)
# table2.show()



# nb.pack(fill=BOTH, expand=1)
root.mainloop()






# parser = ConfigParser()
# parser.read('Configuration_stock_file.ini')
# parser.set('entry_values', 'numb_clusters', entry_cluster_num.get())
# with open('Configuration_stock_file.ini', 'w') as configfile:
#     parser.write(configfile)










