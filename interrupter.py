import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import pymysql
import os
import pandas as pd
import numpy as np
import sys
import time
from PIL import ImageTk, Image
import APIManager.api
import CatalogManager.catalog
import IndexManager.index


class DataBase(object):
    intro = 'Welcome to the MiniSQL database server.\nType help or ? to list commands.\n'
    def do_select(self,sentence):
        # APIManager.api.select(args.replace(';', ''))
        try:
            APIManager.api.select(sentence.replace(';',''))
        except Exception as e:
            print(str(e))

    def do_create(self,sentence):
        try:
            APIManager.api.create(sentence.replace(';',''))
        except Exception as e:
            print(str(e))

    def do_drop(self,sentence):
        try:
            APIManager.api.drop(sentence.replace(';',''))
        except Exception as e:
            print(str(e))

    def do_insert(self,sentence):
        try:
            APIManager.api.insert(sentence.replace(';',''))
        except Exception as e:
            print(str(e))

    def do_delete(self,sentence):
        try:
            APIManager.api.delete(sentence.replace(';',''))
        except Exception as e:
            print(str(e))

    def do_commit(self,sentence):
        time_start = time.time()
        __finalize__()
        time_end = time.time()
        print('Modifications has been commited to local files,',end='')
        print(" time elapsed : %fs." % (time_end - time_start))

    def do_quit(self,sentence):
        __finalize__()
        print('Goodbye.')
        sys.exit()

    def emptyline(self):
        pass

    def default(self):
        print('Unrecognized command.\nNo such symbol : ')

    def help_commit(self):
        print()
        text = "To reduce file transfer's time, this SQL server is designed to "+\
        "'lasy' write changes to local files, which means it will not store changes "+\
        "until you type 'quit' to normally exit the server. if this server exit "+\
        "unnormally, all changes will be lost. If you want to write changes to "+\
        "local files immediately, please use 'commit' command.\n"
        print(text)

    def help_quit(self):
        print()
        print('Quit the program and write changes to local file.')

    def help_select(self):
        print()
        print("select * from student;")
        print("select num from student where num >= 2 and num < 10 and gender = 'male';")

    def help_create(self):
        print()
        print("create table student (ID int, name char(10),gender char(10)"
              ",enroll_date char(10),primary key(ID));")

    def help_drop(self):
        print()
        print("drop table student;")

    def help_insert(self):
        print('''
insert into student values ( 1,'Alan','male','2017.9.1');
insert into student values ( 2,'rose','female','2016.9.1');
insert into student values ( 3,'Robert','male','2016.9.1');
insert into student values ( 4,'jack','male','2015.9.1');
insert into student values ( 5,'jason','male','2015.9.1');
insert into student values ( 6,'Hans','female','2015.9.1');
insert into student values ( 7,'rosa','male','2014.9.1');
insert into student values ( 8,'messi','female','2013.9.1');
insert into student values ( 9,'Neymar','male','2013.9.1');
insert into student values ( 10,'Christ','male','2011.9.1');
insert into student values ( 11,'shaw','female','2010.9.1');
''')

    def help_delete(self):
        print()
        print("delete from students")
        print("delete from student where sno = '88888888';")



def __initialize__():
    CatalogManager.catalog.__initialize__(os.getcwd())
    IndexManager.index.__initialize__(os.getcwd())

def __finalize__():
    CatalogManager.catalog.__finalize__()
    IndexManager.index.__finalize__()


def QueryDB(window,sentence):
    a = DataBase()
    print(sentence.get())
    sentence_string = sentence.get()
    APIManager.api.__root = True
    __initialize__()
    sentence_string = sentence_string.replace('select ','')
    a.do_select(sentence_string)


def movelabel(window,info):
    info.place(x=1000, y=1000, anchor='sw')


def createquery():
    # create window
    querywindow = tk.Toplevel(window)
    querywindow.title('MiniSQL Query')
    querywindow.geometry('800x800')

    imgpath = 'background.png'
    img = Image.open(imgpath)
    photo = ImageTk.PhotoImage(img)

    canvas = tk.Canvas(querywindow,width=900, height=1100, highlightthickness=0, borderwidth=0)
    canvas.place(x=0, y=0)
    background = tk.PhotoImage(file='background.png')
    bgid = canvas.create_image(150, 350, image=background, anchor='nw')

    input_module = tk.Frame(querywindow, width=600, height=600)
    input_module.place(x = 100,y = 10)
    title = tk.Label(input_module, text='SQL Sentence Input', font=('Arial', 20), width=50, height=2)
    title.grid(row = 0,column = 0,columnspan = 4,pady = 10)

    query_sentence = tk.Entry(input_module, width=20)
    query_sentence.grid(row = 1, column = 1)

    #due to the existence of parameter, we need to add lamda in order to do the right function
    query_button = tk.Button(input_module,text="Query",width = 20,command = lambda: QueryDB(querywindow,query_sentence))
    query_button.grid(row = 1,column = 2,columnspan = 3,padx = 20, pady = 10,sticky = 'ne')

    querywindow.mainloop()
    return 0

def createhelp():
    return 0

def createinfo():
    return 0


if __name__ == '__main__':

    # ======================
    #
    # create the main window
    #
    # ======================

    # init window
    WIDTH = '800'
    HEIGHT = '800'
    WINDOW_TITLE = 'MiniSQL'
    window = tk.Tk()
    window.title(WINDOW_TITLE)
    window.geometry(WIDTH+'x'+ HEIGHT)

    #init background picture
    imgpath = 'background.png'
    img = Image.open(imgpath)
    photo = ImageTk.PhotoImage(img)

    # show background picture
    canvas = tk.Canvas(width=900, height=1100, highlightthickness=0, borderwidth=0)
    canvas.place(x=0, y=0)
    background = tk.PhotoImage(file=imgpath)
    bgid = canvas.create_image(150, 400, image=background, anchor='nw')

    # create title component
    title = tk.Label(window, text='MiniSQL Project', font=('Arial', 30), width=50, height=2)
    title.pack(pady = 0)

    # create query button
    query_button = tk.Button(text="SQL Query",command = createquery,width =20,height = 2,font=('Helvetica 12 bold'),relief='flat')
    query_button.pack(padx=10, pady=10)

    # create help button
    return_button = tk.Button(text="Help",command = createhelp,width =20,height = 2,font=('Helvetica 12 bold'),relief = "flat")
    return_button.pack(padx=10, pady=10)

    # create project information button
    borrow_button = tk.Button(text="Project Information",command = createinfo,width =20,height = 2,font=('Helvetica 12 bold'))
    borrow_button.pack(padx=10, pady=10)

    # temporarily show the welcome quote to the UI
    quote = tk.Label(window, text='Welcome to MiniSQL', font=('Arial', 40), width=30, height=2,fg = 'red')
    quote.place(x = 400,y= 400,anchor= 's')
    window.after(1500,lambda: movelabel(window,quote))

    # create the mainloop of the main UI window
    window.mainloop()

