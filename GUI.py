import tkinter as tk
from tkinter import *



root = Tk()
root.geometry('500x500')
root.title('Companies Clustering Aplication')


Entry_label_frame = LabelFrame(root, text = 'Enter Parameters')
Entry_label_frame.grid(row = 0, sticky = N)
tree_button_frame = LabelFrame(root)
tree_button_frame.grid(row = 1, sticky = 'w')
label_for_time = Label(Entry_label_frame, text = 'Enter For Year To Cluster')
label_for_time.grid(row = 0, column = 0, sticky=W)
label_for_cluster_num = Label(Entry_label_frame, text = 'Enter Number Of Clusters')
label_for_cluster_num.grid(row = 1, column = 0, sticky = W)
label_for_companies = Label(Entry_label_frame, text = 'Enter Number Of Companies To Show')
label_for_companies.grid(row = 2, column = 0, sticky = W)

entry_time_per = Entry(Entry_label_frame).grid(row = 0, column = 1)
entry_cluster_num = Entry(Entry_label_frame).grid(row = 1, column = 1)
entry_companies_num = Entry(Entry_label_frame).grid(row = 2, column = 1)

set_button_1 = Button(Entry_label_frame, text = 'SET')
set_button_1.grid(row = 0, column = 2, sticky = E,padx = 5,pady = 5)
set_button_2 = Button(Entry_label_frame, text = 'SET')
set_button_2.grid(row = 1, column = 2,sticky = E,padx = 5,pady = 5)
set_button_3 = Button(Entry_label_frame, text = 'SET')
set_button_3.grid(row = 2, column = 2,sticky = E,padx = 5,pady = 5)

button_calculate = Button(tree_button_frame, text = 'Calculate').grid(row = 1, column = 0, sticky = W)
button_stop = Button(tree_button_frame, text = 'Stop').grid(row = 1, column = 1)
button_quit = Button(tree_button_frame, text = 'Quit').grid(row = 1, column = 2, sticky = W)





root.mainloop()