from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
import mysql.connector

#Database connectivity
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhi@123", 
    database="To_Do_List"
)
the_cursor = mydb.cursor()


#Add Button Function
def add_item():
    task_value = task_entry.get()
    if len(task_value) == 0:  #check if entry box is empty or not
        messagebox.showinfo('Error', 'Task is not entered.')
    else:
        task.append(task_value)
        insert_query = "INSERT INTO Task (Task_List) values (%s)"
        the_cursor.execute(insert_query, (task_value,))
        mydb.commit()
        task_list.delete(0, 'end')
        for x in task:
            task_list.insert('end', x)
        task_entry.delete(0, 'end')
        messagebox.showinfo('To Do List', 'Added Successfully.')


#View Button Function
def view_task():
    try:
        selected_task = task_list.get(task_list.curselection())
        if selected_task:
            messagebox.showinfo('Task Details', f'Task: {selected_task}')
    except TclError:
        messagebox.showinfo('Error', 'No Task Selected.')

#Edit Button Function
def edit_task():
    try:
        selected_task_indices = task_list.curselection()
        if selected_task_indices:
            selected_task_index = selected_task_indices[0]

            if 0 <= selected_task_index < len(task):
                selected_task = task[selected_task_index]
                edited_task = simpledialog.askstring('Edit Task', 'Edit Task:', initialvalue=selected_task)

                if edited_task is not None:
                    if len(edited_task) == 0:
                        messagebox.showinfo('Error', 'Task is not entered.')
                    else:
                        task[selected_task_index] = edited_task
                        update_query = "UPDATE Task SET Task_List=(%s) WHERE Task_List=(%s)"
                        the_cursor.execute(update_query, (edited_task, selected_task))
                        mydb.commit()
                        task_list.delete(0, 'end')
                        for x in task:
                            task_list.insert('end', x)
                        messagebox.showinfo('To Do List', 'Edited Successfully.')
            else:
                messagebox.showinfo('Error', 'Invalid Task Index.')
        else:
            messagebox.showinfo('Error', 'No Task Selected.')
    except TclError:
        messagebox.showinfo('Error', 'No Task Selected.')


#Delete Button Function
def delete_item():
    try:
        the_value = task_list.get(task_list.curselection())
        if the_value in task:
            message = messagebox.askyesno('Delete All', 'Are you sure?') #Delete Confirmation
            if message is True:
                the_cursor.execute("delete from Task where Task_List= %s", (the_value,))
                mydb.commit()
                task.remove(the_value)
                task_list.delete(0, 'end')
                for x in task:
                    task_list.insert('end', x)

    except:
        messagebox.showinfo('Error', 'No Task Selected.')


#Delete All Button Function
def clear_item():
    if len(task) != 0:
        message = messagebox.askyesno('Delete All', 'Are you sure?')
        while len(task) != 0: #check if any task is in tasklist or not
            if message is True:
                task.pop()
                the_cursor.execute('delete from Task')
                mydb.commit()
                task_list.delete(0, 'end')
                for x in task:
                    task_list.insert('end', x)
    else:
        messagebox.showinfo('Error', 'No Task Found')


#Update data from database
def retrieve_database():
    task = []
    try:
        the_cursor.execute('SELECT * FROM Task')
        rows = the_cursor.fetchall()
        for row in rows:
            task.append(row[0])
    except Exception as e:
        print(f"Error: {e}")
    return task


#Main Function
if __name__ == "__main__":
    root = Tk()
    root.geometry("657x500")
    root.title("To Do List")
    root.minsize(350, 400)
    root.maxsize(800, 600)
    root.configure(bg="white")
    img = PhotoImage(file="D:\proj\icon.png")  #Adding Icon
    root.iconphoto(False, img)

    task = []

    #Frames
    header_frame = Frame(root, bg="cyan")
    list_frame = Frame(root, bg="sky blue")
    button_frame = Frame(root, bg="light green")

    header_frame.pack(side="top", fill="both", pady=20)
    list_frame.pack(side="left", expand=True, fill="both")
    button_frame.pack(side="right", expand=True, fill="both")

    header = Label(header_frame, text="To Do List", bg="white", font=("Helvetica", "25", "bold"))

    task_list = Listbox(list_frame, width=30, height=15, selectmode='SINGLE', selectbackground="blue",
                        selectforeground="white")

    item_label = Label(button_frame, text="Enter Tasks", bg="light green", font=("Arial", "15", "bold"))

    task_entry = Entry(button_frame, font=("Consolas", "12"), width=18)

    add_button = Button(button_frame, text="Add Task", width=20, bg="blue", fg="white", font=("arial", "10", "bold"),
                        command=add_item)

    view_button = Button(button_frame, text="View Task", width=20, bg="blue", fg="white", font=("arial", "10", "bold"),
                         command=view_task)

    edit_button = Button(button_frame, text="Edit Task", width=20, bg="blue", fg="white", font=("arial", "10", "bold"),
                         command=edit_task)

    delete_button = Button(button_frame, text="Delete Task", width=20, bg="blue", fg="white",
                           font=("arial", "10", "bold"), command=delete_item)

    clear_button = Button(button_frame, text="Delete All Task", width=20, bg="blue", fg="white",
                          font=("arial", "10", "bold"), command=clear_item)

    exit_button = Button(button_frame, text="Exit", width=20, bg="red", fg="white", font=("arial", "10", "bold"),
                         command=root.destroy)
    task = retrieve_database()
    for row in task:
        task_list.insert('end', row)

    header.pack()
    task_list.pack(pady=10)
    item_label.pack()
    task_entry.pack(pady=10)
    add_button.pack(pady=10)
    view_button.pack(pady=10)
    edit_button.pack(pady=10)
    delete_button.pack(pady=10)
    clear_button.pack(pady=10)
    exit_button.pack(pady=10)

    root.mainloop()
