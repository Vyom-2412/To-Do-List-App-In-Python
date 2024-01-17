#-------------------- Imports and declaring variables--------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq
    
root = tk.Tk()
root.title('To-Do List')
root.geometry("500x450+750+250")
root.resizable(0,0)
root.configure(bg = "#FAEBD7")

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

header_label = ttk.Label(root,text = "The To-Do List", font = ("Brush Script MT", "30"), background = "#FAEBD7", foreground = "#8B4513")  
task_title_label = ttk.Label(root, text='Enter task title: ', background="#FAEBD7",font = ("Consolas", "11", "bold"), foreground="#000000")
entry1 = ttk.Entry(root, width=18)
lb = tk.Listbox(root, width=26,height=17, selectmode='SINGLE',background="#FFFFFF",foreground="#000000", selectbackground = "#CD853F", selectforeground = "#FFFFFF")
add_task_button = ttk.Button(root, text='Add task', width=24, command=addTask)
del_task_button = ttk.Button(root, text='Delete', width=24, command=delOne)
del_all_task_button = ttk.Button(root, text='Delete all', width=24, command=deleteAll)
exit_button = ttk.Button(root, text='Exit', width=24, command=bye)

retrieveDB()
listUpdate()

#Place geometry
header_label.pack(padx = 20, pady = 20)
task_title_label.place(x = 70, y = 120)
entry1.place(x = 70, y = 160)  
add_task_button.place(x=70, y=200)
del_task_button.place(x=70, y=240)
del_all_task_button.place(x=70, y=280)
exit_button.place(x=70, y =320)
lb.place(x=270, y = 100)
root.mainloop()

connection.commit()
cur.close()
