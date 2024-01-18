#-------------------- Imports and declaring variables--------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq

#Root is a commonly used variable name to tkinter to make the window
root = tk.Tk()
#Giving title to the window
root.title('To-Do List')
#Setting the size
root.geometry("500x450+750+250")
#Make it so that it cant be fullscreened
root.resizable(0,0)
#Set the background color
root.configure(bg = "#FAEBD7")

#Establish connection to a database using sql's connect() function
connection = sq.connect('todo.db')
#The cursor makes the changes in the database
cur = connection.cursor()
#Creates a table in the database if there is not one already with the name 'tasks'
#(title text) defines the columns of the table. It has only one columns 'title' with 'text' datatype.
cur.execute('create table if not exists tasks (title text)')
#Make an empty task list
task = []
#------------------------------- Functions--------------------------------
def clearList():
    #Deletes all items in the listbox
    lb.delete(0,'end')
    
def listUpdate():
    #Call the clearList() function
    clearList()
    #Call a loop which updates the listbox
    for i in task:
        lb.insert('end', i)
        
def addTask():
    #Getting the task from entry
    word = entry1.get()
    if len(word)==0:
        #If there is no word added, a popup window will open with title "Empty Entry" and content as "Enter task name".
        #showinfo() function opens a popup with 'Ok' button to close it.
        messagebox.showinfo('Empty Entry', 'Enter task name')
    else:
        #append 'word' to task list
        task.append(word)
        #Add the word into the 'tasks' table. 'values' is the value which we will provide (word in this case).
        #(word,) is necessary to define a tuple being added.
        cur.execute('insert into tasks values (?)', (word,))
        #Call the listUpdate() function
        listUpdate()
        #Clear the entry box
        entry1.delete(0,'end')

def delOne():
    #Using try-except block to catch abnormalities/errors
    try:
        #Getting the selected value
        val = lb.get(lb.curselection())
        if val in task:
            #If it is present in the database, then remove it and call listUpdate()
            task.remove(val)
            listUpdate()
            #Remove the value from tasks in database
            cur.execute('delete from tasks where title = ?', (val,))
    except:
        #Incase no item is selected, show a message with title "Cannot delete" and 'No Task item Selected' inside it
        messagebox.showinfo('Cannot Delete', 'No Task Item Selected')
    
def deleteAll():
    #Ask from the user whether they want to delete all items or not
    mb = messagebox.askyesno('Delete All','Are you sure?')
    if mb==True:
        #Run a while loop to remove all tasks
        while(len(task)!=0):
            task.pop()
        #delete from tasks database and call listUpdate()
        cur.execute('delete from tasks')
        listUpdate()

def bye():
    #print the current task list and destroy the window
    print(task)
    root.destroy()

def retrieveDB():
    #remove all the items from task list
    while(len(task)!=0):
        task.pop()
    for row in cur.execute('select title from tasks'):
        #add those items which are currently there in the database
        task.append(row[0])
      
#------------------------------- Formatting--------------------------------

#ttk.Label creates a text inside the 'root' which is the main window
header_label = ttk.Label(root,text = "The To-Do List", font = ("Brush Script MT", "30"), background = "#FAEBD7", foreground = "#8B4513")  
task_title_label = ttk.Label(root, text='Enter task title: ', background="#FAEBD7",font = ("Consolas", "11", "bold"), foreground="#000000")

#ttk.Entry creates a textbox to get the entry
entry1 = ttk.Entry(root, width=18)

#tk.Listbox creates a listbox item to display all current items
#selectmode='SINGLE' ensures that only 1 item is selected at a time
lb = tk.Listbox(root, width=26,height=17, selectmode='SINGLE',background="#FFFFFF",foreground="#000000", selectbackground = "#CD853F", selectforeground = "#FFFFFF")

#ttk.Button creates buttons with their respective functionalities under 'command' property
add_task_button = ttk.Button(root, text='Add task', width=24, command=addTask)
del_task_button = ttk.Button(root, text='Delete', width=24, command=delOne)
del_all_task_button = ttk.Button(root, text='Delete all', width=24, command=deleteAll)
exit_button = ttk.Button(root, text='Exit', width=24, command=bye)

#Call the retrieveDB() and listUpdate() functions
retrieveDB()
listUpdate()

#Defining the placing for the elements
header_label.pack(padx = 20, pady = 20)
task_title_label.place(x = 70, y = 120)
entry1.place(x = 70, y = 160)  
add_task_button.place(x=70, y=200)
del_task_button.place(x=70, y=240)
del_all_task_button.place(x=70, y=280)
exit_button.place(x=70, y =320)
lb.place(x=270, y = 100)
root.mainloop()

#Commit all changes
connection.commit()
#Dont allow any more changes to the database
cur.close()
