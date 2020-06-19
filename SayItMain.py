import sqlite3
from tkinter import *

root = Tk()
root.geometry("400x400")
root.title("Social Anxiety Exposure Therapy")

#Create a Database or Connect to One
conn = sqlite3.connect('/home/brandon/SayIt/Ladder.db')
#Create Cursor
c = conn.cursor()

#Creates Table
'''
c.execute("""CREATE TABLE Steps (   
title text,
fearLvl integer
)""")
'''
#Create submit function for database
def initsubmit():
    #Create a Database or Connect to One
    conn = sqlite3.connect('/home/brandon/SayIt/Ladder.db')
    #Create Cursor
    c = conn.cursor()
    
    #Insert Into Table
    c.execute(""" INSERT INTO Steps Values (:title, :fearLvl)
    """,
    {
        'title' : title.get(),
        'fearLvl' : fearLvl.get()
    }
    )

    #Commit Changes
    conn.commit()
    #Close Accessing DataBase
    conn.close()
    
    title.delete(0, END)
    fearLvl.delete(0, END)

#Create a Show Ladder Button
def query():
    #Create a Database or Connect to One
    conn = sqlite3.connect('/home/brandon/SayIt/Ladder.db')
    #Create Cursor
    c = conn.cursor()
    
    #Show Ladder
    c.execute("SELECT *, oid FROM Steps ORDER BY fearLvl ASC")
    ladder = c.fetchall()

    print_steps = ''
    for step in ladder:
        print_steps += "Title: "+  str(step[0]) + "     Fear Level: " + str(step[1]) +"     ID NUMBER: " + str(step[2]) + "\n"

    query_label = Label(root, text=print_steps) 
    query_label.grid(row=6, column=0, columnspan=2)

    #Commit Changes
    conn.commit()
    #Close Accessing DataBase
    conn.close()

def delete():
    #Create a Database or Connect to One
    conn = sqlite3.connect('/home/brandon/SayIt/Ladder.db')
    #Create Cursor
    c = conn.cursor()
    
    #Delete Step
    c.execute("DELETE from steps where oid=" + delete_box.get())

    #Commit Changes
    conn.commit()
    #Close Accessing DataBase
    conn.close()

#Create Text Boxes
title = Entry(root, width=30)
title.grid(row=0,column=1, padx=20)
fearLvl = Entry(root, width=30)
fearLvl.grid(row=1,column=1, padx=20)
delete_box = Entry(root, width=30)
delete_box.grid(row=8, column=1)

#Create Text Box Labels
title_label = Label(root, text="Step/Goal Title")
title_label.grid(row=0,column=0)
fearLvl_label = Label(root, text="How anxious would this make you?")
fearLvl_label.grid(row=1,column=0)
delete_box_label = Label(root, text="Delete ID")
delete_box_label.grid(row=8, column=0)

#Create Submit Button
submit_btn = Button(root, text="Add Step to Ladder",command=initsubmit)
submit_btn.grid(row=4,column=0,columnspan=2, pady=10, padx=10, ipadx=100)

#Create Query Function
query_btn = Button(root, text="Show Full Ladder",command=query)
query_btn.grid(row=5,column=0,columnspan=2, pady=10, padx=10, ipadx=100)

#Create a Delete Button
del_btn = Button(root, text="Delete Step",command=delete)
del_btn.grid(row=10,column=0,columnspan=2, pady=10, padx=10,ipadx=100)


#Commit Changes
conn.commit()

#Close Accessing DataBase
conn.close()

root.mainloop()