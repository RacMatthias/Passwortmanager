import tkinter as tk
from tkinter import ttk
import passwordmanager as pwm
import sqlite3

class welcome:
    # init creates the app window
    def __init__(self):
        # creating instance of tkinter object
        self.master = tk.Tk()

        # changing title of window
        self.master.title("Log in")

        # labels for entry forms
        ttk.Label(self.master, text="Username").grid(row=0)
        ttk.Label(self.master, text="Password").grid(row=1)

        # entry forms
        self.entry_username = ttk.Entry(self.master)
        self.entry_username.grid(row=0, column=1)
        self.entry_password = ttk.Entry(self.master, show="*")
        self.entry_password.grid(row=1, column=1)

        # Label for user feedback such as "username does not exist"
        self.feedback = tk.Label(self.master, text="", fg="red")
        self.feedback.grid(row=2)

        # button to submit entry
        self.button_submit = ttk.Button(self.master, text='Submit',
        width=25, command=self.submit)
        self.button_submit.grid(row=3, column=0)

        # button to create new account
        self.button_create = ttk.Button(self.master, text='Create Account',
        width=25, command=self.create_account)
        self.button_create.grid(row=3, column=1)

        # runs window
        self.master.mainloop()

    # function to create sqlite-File if not existing and write the account
    # information the user submits into that file
    def create_account(self):
        self.feedback["text"] = ""

        # get informations from entries
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()

        # connect to database and create instance of cursor
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        # create table if it is not already existing
        cursor.execute("CREATE TABLE IF NOT EXISTS users( \
                        username TEXT PRIMARY KEY, \
                        password TEXT)")

        try:
            # insert information from entries into table
            cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)",
                          (self.username, self.password))
        except:
            self.feedback["text"] = "username already exists"
        # commit changes to table and close connection
        connection.commit()
        connection.close()

        # if account could not be created then dont open manager
        if not self.feedback["text"] == "username already exists":
            # creates instance of manager an gives username for identification
            pwm.manager(self.username)

    # function to check weather the submitted informations match with existing
    # account informations or not, needs also to start the the password manager
    # via calling another class for that window
    def submit(self):
        # get informations from entries
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()
        print(self.username, self.password)

        # connect to database and create instance of cursor
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        # select db entry where username is equal to typed in username
        cursor.execute("SELECT * FROM users WHERE username =(?)", (self.username,))

        # get entry as strings
        rows = cursor.fetchall()
        try:
            print(rows[0][1])
            self.feedback["text"] = ""
        except:
            self.feedback["text"] = "username does not exist"

        # close connection
        connection.close()

        # check if password fits to username
        if rows[0][1] == self.password:
            # creates instance of manager an gives username for identification
            pwm.manager(self.username)
            self.feedback["text"] = ""
        else:
            self.feedback["text"] = "incorrect password"



if __name__ == '__main__':
    app = welcome()
