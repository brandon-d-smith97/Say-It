#####
# SayIt version 0.9.1 Objective: Create User Functionality (courageXP) 
#####

import sqlite3
from tkinter import *

#    #    # General Database Information #    #    #

conn = sqlite3.connect('/home/brandon/Dev/SayIt/Ladder.db')
c = conn.cursor()

try:
    c.execute("""CREATE TABLE Steps (     
    title text,
    fearLvl integer
    )""")    
except sqlite3.OperationalError as err:
    pass

try:
    c.execute("""CREATE TABLE User (     
    name text,
    courageCoins integer
    )""")    
except sqlite3.OperationalError as err:
    pass

#    #    # General Gui Information #    #    #
root = Tk()
root.geometry("500x500")
root.configure(background = 'light blue')
root.title("Social Anxiety Exposure Therapy")

def courageCoinAlg():
    conn = sqlite3.connect('/home/brandon/Dev/SayIt/Ladder.db')
    c = conn.cursor()

    c.execute('Select * from steps where oid = ' + select_box.get())
    before = c.fetchall()
    before = int(before[0][1])
    after = before - int(fearLvl_editor.get())
    print(after)

    c.execute('select courageCoins from User')
    courageCoins = c.fetchall()
    courageCoins = courageCoins[0][0]

    c.execute('Update User set courageCoins = :after where oid = 1',
    {
     'after' : after + courageCoins  
    })

    conn.commit()
    conn.close()

    print('done')



def Update():
    # Create a database and make cursor
	conn = sqlite3.connect('/home/brandon/Dev/SayIt/Ladder.db')
	c = conn.cursor()

	record_id = select_box.get()
    
    
	c.execute("""UPDATE Steps SET
		title = :title,
		fearLvl = :fearLvl
		WHERE oid = :oid""",
		{
		'title': title_editor.get(),
		'fearLvl': fearLvl_editor.get(),
		'oid': record_id
		})
    


	# Commit Changes and Close
	conn.commit()

	# Close Connection 
	conn.close()

	editor.destroy()
	root.deiconify()

def initsubmit():
    conn = sqlite3.connect('/home/brandon/Dev/SayIt/Ladder.db')
    c = conn.cursor()
    
    # Inserts into db from entry boxes
    c.execute(""" INSERT INTO Steps Values (:title, :fearLvl)
    """,
    {
        'title' : title.get(),
        'fearLvl' : fearLvl.get()
    }
    )

    conn.commit()
    conn.close()
    
    # Deletes old text from text box.
    title.delete(0, END)
    fearLvl.delete(0, END)

def query():
    conn = sqlite3.connect('/home/brandon/Dev/SayIt/Ladder.db')
    c = conn.cursor()
    
    # Get all steps sorted by fear level
    c.execute("SELECT *, oid FROM Steps ORDER BY fearLvl ASC")
    ladder = c.fetchall()

    # Parses fetchall() results
    print_steps = ''
    for step in ladder:
        print_steps += "Title: "+  str(step[0]) + "     Fear Level: " + str(step[1]) +"     ID NUMBER: " + str(step[2]) + "\n"

    # To be replaced by listbox
    #query_label = Label(root, text=print_steps) 
    #query_label.grid(row=6, column=0, columnspan=2)

    showLadder = Listbox(root, width=60)
    showLadder.grid(row=6, column=0,columnspan=3)
    showLadder.insert(0, "Goal  :  Level of Aversion")    

    for step in ladder:
        showLadder.insert(1,step[0] + "  :  " + str(step[1]))

    conn.commit()
    conn.close()

def delete():
    conn = sqlite3.connect('/home/brandon/Dev/SayIt/Ladder.db')
    c = conn.cursor()
    
    #Delete Step
    c.execute("DELETE from steps where oid=" + select_box.get())

    #Delete text from box
    select_box.delete(0, END)

    conn.commit()
    conn.close()

def edit():
    root.withdraw() # take away main window
    global editor # create global var for new window
    editor = Tk() # New frame
    editor.geometry("400x600") # Size
    editor.title("Social Anxiety Exposure Therapy") # Title

    conn = sqlite3.connect('/home/brandon/Dev/SayIt/Ladder.db') # Connect to DB
    c = conn.cursor()

    record_id = select_box.get()
    c.execute("SELECT * FROM Steps WHERE oid = " + record_id)
    records = c.fetchall()

    global title_editor
    global fearLvl_editor

    # Entry Boxes
    title_editor = Entry(editor, width=30)
    title_editor.grid(row=0,column=1, padx=20)
    fearLvl_editor = Entry(editor, width=30)
    fearLvl_editor.grid(row=1,column=1, padx=20)

    # Labels
    title_label = Label(editor, text="Step/Goal Title")
    title_label.grid(row=0,column=0)
    fearLvl_label = Label(editor, text="How anxious would this make you?")
    fearLvl_label.grid(row=1,column=0)
    
    for record in records:
	    title_editor.insert(0, record[0])
	    fearLvl_editor.insert(0, record[1])

    edit_btn = Button(editor, text="Save Record", command=Update)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)
    log_btn = Button(editor, text="Log Progress", command=courageCoinAlg)
    log_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

def saveName():

    conn = sqlite3.connect('/home/brandon/Dev/SayIt/Ladder.db')
    c = conn.cursor()
    
    c.execute(""" INSERT INTO User Values (:name, :cc)
    """,
    {
        'name' : name.get(),
        'cc' : 0
    }
    )
    name.delete(0, END)

    conn.commit()
    conn.close()

def createProfile():
    global createName
    createName = Tk()
    createName.configure(background = 'light green') 
    createName.geometry("400x350") 
    createName.title("Say It/profile")
    global name
    name_label = Label(createName, text="Name:").grid(row=0,column=0)
    name = Entry(createName, width=30)
    name.grid(row=0,column=1, padx=20)
    submit = Button(createName, text="Change name",command=saveName).grid(row=4,column=0,columnspan=2, pady=10, padx=10, ipadx=100)

def goToProfile():
    conn = sqlite3.connect('/home/brandon/Dev/SayIt/Ladder.db')
    c = conn.cursor()
    
    global profileHome
    profileHome = Tk()
    profileHome.configure(background = 'light green') 
    profileHome.geometry("400x350") 
    profileHome.title("Say It/profile")

    createProfile_button = Button(profileHome, text="Edit Profile Name", command=createProfile, bg="Pink").grid(row=3,column=0, columnspan=2)

    c.execute("SELECT * FROM User")
    ladder = c.fetchall()
    name = ladder[0][0]
    ccAmt = ladder[0][1]
    
    name_label = Label(profileHome, text="Name:").grid(row=0,column=0)
    courageCoin_label = Label(profileHome, text="Number of Courage Coins:")
    courageCoin_label.grid(row=1,column=0)
    actualNameLabel = Label(profileHome,text=name).grid(row=0, column=1)
    actualCCLabel = Label(profileHome, text=ccAmt).grid(row=1,column=1)


#    #    # Specific GUI Widgets #    #    #
# Creates Entry Boxes for title, number fear level, select box
title = Entry(root, width=30)
title.grid(row=0,column=1, padx=20)
fearLvl = Entry(root, width=30)
fearLvl.grid(row=1,column=1, padx=20)
select_box = Entry(root, width=30)
select_box.grid(row=8, column=1)

# Create Text Box Labels fo title, fearLvl, and select box
title_label = Label(root, text="Step/Goal Title")
title_label.grid(row=0,column=0)
fearLvl_label = Label(root, text="How anxious would this make you?")
fearLvl_label.grid(row=1,column=0)
select_box_label = Label(root, text="Select ID")
select_box_label.grid(row=8, column=0)

# Buttons
submit_btn = Button(root, text="Add Step to Ladder",command=initsubmit)
submit_btn.grid(row=4,column=0,columnspan=2, pady=10, padx=10, ipadx=100)
query_btn = Button(root, text="Show Full Ladder",command=query)
query_btn.grid(row=5,column=0,columnspan=2, pady=10, padx=10, ipadx=100)
del_btn = Button(root, text="Delete Step",command=delete)
del_btn.grid(row=10,column=0,columnspan=2, pady=10, padx=10,ipadx=100)
edit_btn = Button(root, text="Edit Step",command=edit)
edit_btn.grid(row=11,column=0,columnspan=2, pady=10, padx=10,ipadx=125)
goProfile_button = Button(root, text="View Profile", command=goToProfile, bg="orange")
goProfile_button.grid(row=12,column=0, columnspan=2)


conn.commit()
conn.close()

#    #    # Testing #    #    #
root.mainloop()
