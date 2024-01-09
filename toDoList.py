#-------------------- Imports and declaring variables--------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq
    
root = tk.Tk()
root.title('To-Do List')
root.geometry("400x250+500+300")

connection = sq.connect('todo.db')
cur = connection.cursor()
cur.execute('create table if not exists tasks (title text)')

task = []
#------------------------------- Functions--------------------------------
def addTask():
    word = entry1.get()
    if len(word)==0:
        messagebox.showinfo('Empty Entry', 'Enter task name')
    else:
        task.append(word)
        cur.execute('insert into tasks values (?)', (word,))
        listUpdate()
        entry1.delete(0,'end')

def listUpdate():
    clearList()
    for i in task:
        lb.insert('end', i)

def delOne():
    try:
        val = lb.get(lb.curselection())
        if val in task:
            task.remove(val)
            listUpdate()
            cur.execute('delete from tasks where title = ?', (val,))
    except:
        messagebox.showinfo('Cannot Delete', 'No Task Item Selected')
    
def deleteAll():
    mb = messagebox.askyesno('Delete All','Are you sure?')
    if mb==True:
        while(len(task)!=0):
            task.pop()
        cur.execute('delete from tasks')
        listUpdate()

def clearList():
    lb.delete(0,'end')

def bye():
    print(task)
    root.destroy()

def retrieveDB():
    while(len(task)!=0):
        task.pop()
    for row in cur.execute('select title from tasks'):
        task.append(row[0])
      
#------------------------------- Formatting--------------------------------

task_title_label = ttk.Label(root, text='Enter task title: ')
entry1 = ttk.Entry(root, width=21)
lb = tk.Listbox(root, height=11, selectmode='SINGLE')
add_task_button = ttk.Button(root, text='Add task', width=20, command=addTask)
del_task_button = ttk.Button(root, text='Delete', width=20, command=delOne)
del_all_task_button = ttk.Button(root, text='Delete all', width=20, command=deleteAll)
exit_button = ttk.Button(root, text='Exit', width=20, command=bye)

retrieveDB()
listUpdate()

#Place geometry
task_title_label.place(x=50, y=50)
entry1.place(x=50, y=80)
add_task_button.place(x=50, y=110)
del_task_button.place(x=50, y=140)
del_all_task_button.place(x=50, y=170)
exit_button.place(x=50, y =200)
lb.place(x=220, y = 50)
root.mainloop()

connection.commit()
cur.close()