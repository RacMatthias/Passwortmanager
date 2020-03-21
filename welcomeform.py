import tkinter as tk
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
        tk.Label(self.master, text="Username").grid(row=0)
        tk.Label(self.master, text="Password").grid(row=1)

        # entry forms
        self.entry_username = tk.Entry(self.master)
        self.entry_username.grid(row=0, column=1)
        self.entry_password = tk.Entry(self.master, show="*")
        self.entry_password.grid(row=1, column=1)

        # Label for user feedback such as "username does not exist"
        self.feedback = tk.Label(self.master, text="", fg="red")
        self.feedback.grid(row=2)

        # button to submit entry
        self.button_submit = tk.Button(self.master, text='Submit',
        width=25, command=self.submit)
        self.button_submit.grid(row=3, column=0)

        # button to create new account
        self.button_create = tk.Button(self.master, text='Create Account',
        width=25, command=self.create_account)
        self.button_create.grid(row=3, column=1)

        # runs window
        self.master.mainloop()

    # function to create sqlite-File if not existing and write the account
    # information the user submits into that file
    def create_account(self):
        print("create account")

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

        # insert information from entries into table
        cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)",
                      (self.username, self.password))

        # commit changes to table and close connection
        connection.commit()
        connection.close()

        # creates instance of manager an gives username for identification
        pwm.manager(self.username)

    # function to check weather the submitted informations match with existing
    # account informations or not, needs also to start the the password manager
    # via calling another class for that window
    def submit(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()
        print(self.username, self.password)

        # creates instance of manager an gives username for identification
        pwm.manager(self.username)


if __name__ == '__main__':
    app = welcome()
