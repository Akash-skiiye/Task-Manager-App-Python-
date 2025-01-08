from tkinter import *
from tkinter import messagebox ,ttk
from tkcalendar import DateEntry
from database import data
import datetime
import mysql.connector

# Login Page (First page) 
def entry_screen():
    global login_id, password_entry,root

    root = Tk()
    root.geometry("400x400")
    root.title('Task manager')
    root.config(bg="linen")
    connection()

    label1 = Label(root, text="Task manager", font=("arial", 12,"bold"),bg="linen")
    label1.pack(padx=40, pady=10)

    label2 = Label(root, text="Login ID:",font=("Times"),bg="linen")
    label2.pack(pady=10)

    username = StringVar()
    login_id = Entry(root,width=35,textvariable=username)
    login_id.pack(pady=0)

    label3 = Label(root, text= "Password:",pady=10,font=("Times"),bg="linen")
    label3.pack()

    password=StringVar()
    password_entry = Entry(root, width=35,textvariable=password,show="*")
    password_entry.pack()

    login=Button(root, text="Login",font=("Times",10),width= 10,command=check_login)
    login.pack(pady=20)
    root.mainloop()


# Python - MySQL connection
def connection():
    global con
    try:
        con = mysql.connector.connect(
            host = data[0],
            user = data[1],
            password = data[2],
            database = data[3]
    )
    except mysql.connector.Error as e:
        messagebox.showerror("Error",f"error - {e}")

# Check Entered Credentails to the Database
def check_login():
    global id
    id = login_id.get()
    passs = password_entry.get()

    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{id}'")
    result = cursor.fetchall()

    if result:  # User ID exists
        if passs == result[0][2]:  # Password matches
            root.destroy()
            main_screen(id)
        else:  # Password incorrect
            messagebox.showerror("Error!", "Incorrect Password")
    else:  # User ID not found
        messagebox.showerror("Error!", "User ID does not exist")


# Main Working Screen
def main_screen(id):
    global main, left_frame,right_frame

    main = Tk()
    main.title("Task manager")
    main.geometry("800x500")

    # Left Frame
    left_frame = Frame(main, width=200, bg="bisque2")
    left_frame.pack(side=LEFT, fill=Y)
    
    label1 = Label(left_frame, text=f"User: {id}", font=("Times", 12), bg="lightgrey")
    label1.pack(pady=10)
    my_tasks = Button(left_frame, text="My Tasks", width=15,command=lambda:show_tasks(id))
    my_tasks.pack(pady=5)
    history = Button(left_frame, text="History", width=15,command=show_history)
    history.pack(pady=5)
    exit_button = Button(left_frame, text="Exit", width=15,command=end)
    exit_button.pack(side=LEFT, anchor="s", pady= 10)

    # Right Frame
    right_frame = Frame(main, width=600,bg="lavender")
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    show_tasks(id)
    main.mainloop()

# Gets tasks from the database
def fetch_tasks():
    connection()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tasks")
    task = cursor.fetchall()
    cursor.close()
    return task

# Displays tasks on the Window
def show_tasks(id):
    global v, checkbox, Status_heading, sublist
    for widgets in right_frame.winfo_children():
        widgets.destroy()

    # Get the current date dynamically
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    label2 = Label(right_frame, text=f"Today's Date: {current_date}", font=("Times", 12), anchor="w",bg="light goldenrod")
    label2.pack(fill=X, pady=5)

    # Task List Section
    task_list_frame = Frame(right_frame)
    task_list_frame.pack(fill=BOTH, expand=True)
    
    no_heading = Label(task_list_frame, text="No.", font=("Times", 10, "bold"),width=10,bg="lavender")
    no_heading.grid(row=0,column=0,padx=10,pady=10)
    title_heading = Label(task_list_frame, text="Title", font=("Times", 10, "bold"),width=10,bg="lavender")
    title_heading.grid(row=0,column=1,padx=10,pady=10)
    DueDate_heading = Label(task_list_frame, text="Due Date", font=("Times", 10, "bold"),width=10,bg="lavender")
    DueDate_heading.grid(row=0,column=2,padx=10,pady=10)
    PriorityLevel_heading = Label(task_list_frame, text="Priority Level", font=("Times", 10, "bold"),width=10,bg="lavender")
    PriorityLevel_heading.grid(row=0,column=3,padx=10,pady=10)
    Status_heading = Label(task_list_frame, text="Click when done", font=("Times", 10, "bold"),bg="lavender")
    Status_heading.grid(row=0,column=4,padx=10,pady=10)

    task_list = fetch_tasks()

    if task_list:
        for i ,sublist in enumerate(task_list,start=1):
            # task_id=sublist[0]
            title=sublist[1]
            due_date=sublist[2]
            priority_level=sublist[3]

            # Numbering
            id_label = Label(task_list_frame, text=i, font=("Times", 10))
            id_label.grid(row=i, column=0, padx=10, pady=10)

            # Title
            title_label = Label(task_list_frame, text=title, font=("Times", 10))
            title_label.grid(row=i, column=1, padx=10, pady=10)

            # Due Date
            due_date_label = Label(task_list_frame, text=due_date, font=("Times", 10))
            due_date_label.grid(row=i, column=2, padx=10, pady=10)

            # Priority Level
            priority_label = Label(task_list_frame, text=priority_level, font=("Times", 10))
            priority_label.grid(row=i, column=3, padx=10, pady=10)

            # Status
            v = IntVar()
            checkbox = Checkbutton(task_list_frame, variable=v, onvalue=1, offvalue=0, command=lambda var=v, task=sublist: move(var, task))
            checkbox.grid(row=i,column=4,padx=10,pady=10) 

    # Buttons
    button_frame=Frame(right_frame, height=2, bg="light goldenrod")
    button_frame.pack(fill=X, pady=5)

    add=Button(button_frame, text="Add Task",command=add_task)
    add.pack(side=LEFT, padx=10)

    delete=Button(button_frame,text = "Delete Task", command=delete_task)
    delete.pack(side=LEFT,padx=10)

# Gets tasks history from the database
def fetch_history():
    cursor = con.cursor()
    cursor.execute("SELECT * FROM history")
    history = cursor.fetchall()
    cursor.close()
    return history

# Displays tasks history on the Window
def show_history():
    global hist_sublist

    # Clear the right frame
    for widgets in right_frame.winfo_children():
        widgets.destroy()
    
    # Add History Columns
    no_label = Label(right_frame, text="No.", font=("Times", 10,"bold"),bg="lavender")
    no_label.grid(row=0, column=0, padx=10, pady=10)
    
    title_heading = Label(right_frame, text="Task Title", font=("Times", 10, "bold"), width=20,bg="lavender")
    title_heading.grid(row=0, column=1, padx=10, pady=10)
    
    status_heading = Label(right_frame, text="Completion Status", font=("Times", 10, "bold"), width=20,bg="lavender")
    status_heading.grid(row=0, column=2, padx=10, pady=10)

    action_heading = Label(right_frame, text="Date Of Completion", font=("Times", 10, "bold"), width=10,bg="lavender")
    action_heading.grid(row=0, column=3, padx=10, pady=10)

    history_list = fetch_history()

    if history_list:
        for i , hist_sublist in enumerate(history_list,start=1):
            # history_id = hist_sublist[0]
            histor_title = hist_sublist[1]
            completion_status = hist_sublist[2]
            completion_date = hist_sublist[3]


            # Numbering
            id_label = Label(right_frame, text=i, font=("Times", 10),bg="lavender")
            id_label.grid(row=i, column=0, padx=10, pady=10)

            # title
            title_label = Label(right_frame, text=histor_title, font=("Times", 10),bg="lavender")
            title_label.grid(row=i, column=1, padx=10, pady=10)

            # Completion Status 
            if completion_status == 1:
                comp_status_label = Label(right_frame, text= "Sucessfull", font=("Times", 10),bg="lavender")
                comp_status_label.grid(row=i, column=2, padx=10, pady=10)
            else :
                unsccessful_tasks =hist_sublist
                retry = Button(right_frame,text="Retry task", font=("Times", 10), bg="red", command=lambda:retry_task(unsccessful_tasks))
                retry.grid(row=i, column=2, padx=10, pady=10)

            comp_date_label = Label(right_frame, text=completion_date, font=("Times", 10),bg="lavender")
            comp_date_label.grid(row=i, column=3, padx=10, pady=10)


# Different Options To Operate

# Enter a New Task
def add_task():
    global date_entry

    for widgets in right_frame.winfo_children():
        widgets.destroy()

    label1 = Label(right_frame, text = "New Task - ",font=("Vendana", 20, "bold"))
    label1.grid(row=0, column=0,padx=10,pady=10,columnspan=3)

    label1 = Label(right_frame, text = "Enter Task Title - ")
    label1.grid(row=1, column=0,padx=10,pady=10)

    title = StringVar()
    title_entry = Entry(right_frame, width= 30, textvariable= title)
    title_entry.grid(row=1, column=1,padx=10,pady=10)

    label2 = Label(right_frame, text = "Enter Task Due Date - ")
    label2.grid(row=2, column=0,padx=10,pady=10)

    date_entry = DateEntry(right_frame, width= 30)
    date_entry.grid(row=2, column=1,padx=10,pady=10)

    date_enter=Button(right_frame, text="Enter Date",command= get_d)
    date_enter.grid(row=2,column=2,pady=10, padx=10)

    add_task = Button(right_frame, text = "Add Task",width=10, padx=20,pady=20, command = lambda: add_task_to_database(title.get(),cal))
    add_task.grid(row=3,column=1)
# Actually Update the Database
def add_task_to_database(title,cal):
    try:
        days_remaining = (cal - datetime.datetime.now().date()).days
        if days_remaining>=0:
            if days_remaining <= 3:
                priority = "High"
            elif 4 <= days_remaining <= 7:
                priority = "Moderate"
            else:
                priority = "Low"
        else:
            messagebox.showerror("Date Not Found","Incorrect Date")
            add_task()
    except e:
        messagebox.showerror("Date?", "Enter the date and 'Click' the Enter date button!")

    cursor = con.cursor()
    try:
        cursor.execute(
            "INSERT INTO tasks (title, due_date, priority_level) VALUES (%s, %s, %s)",
            (title, cal, priority)
        )
        con.commit()
        show_tasks(id)
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
def get_d():
    global cal
    cal = date_entry.get_date()  # Fetch selected date
    messagebox.showinfo("Selected Date", f"You selected {cal}")


# Delete Existing tasks
def delete_task():
    Status_heading.config(text="Select the one you want to delete", font= ("Vendana",10))
    d=IntVar()
    checkbox.config( variable=d, onvalue=1, offvalue=0, command=lambda tar=d, mask=sublist: remove(tar.get(), mask,"tasks"))
# Actually Delete the task from the Database
def remove (d,task_to_remove,table):
    if d == 1:
        cursor = con.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE title = '{task_to_remove[1]}' ")
        con.commit()
        show_tasks(id)


# Move the task From Tasks To History Once labelled as Completed
def move(v, done_sublist):
    if v.get() == 1:
        cursor = con.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=%s", (done_sublist[0],))
        cursor.execute("INSERT INTO history (title, Completion_status, completion_date) VALUES (%s, %s, %s)", 
                       (done_sublist[1], v.get(), datetime.datetime.now().strftime("%Y-%m-%d")))
        con.commit()
        show_tasks(id)
    else:
        messagebox.showinfo("Info", "Deselected")

# Retry a certain task that is failled with a new Due Date
def retry_task(task):
    global dialog
    dialog = Toplevel(main)
    dialog.title("Enter New Due Date")
    dialog.geometry("200x200")

    label = Label(dialog, text="enter date-")
    label.pack(pady=10)
    new_date= DateEntry(dialog, width=12, background='darkblue',foreground='white', borderwidth=2)
    new_date.pack(pady=20)
    
    ok_button = Button(dialog, text="OK", command=lambda: add_task_to_database(task[1],new_date.get_date()))
    ok_button.pack(pady = 10)

    dialog.grab_set()  # Make the dialog modal
    remove(1,task,"history")

# Exit the Application
def end():
    con.close()
    main.quit() 

# First line of code
entry_screen()