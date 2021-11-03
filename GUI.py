import tkinter as tk
from tkinter import *



root = Tk()
root.geometry('500x500')
root.title('Companies Clustering Aplication')


entry_time_per = Entry(root).grid()
entry_cluster = Entry(root).grid()

button_calculate = Button(root, text = 'Calculate').grid()
button_stop = Button(root, text = 'Stop').grid()
button_quit = Button(root, text = 'Quit').grid()





root.mainloop()