import tkinter as tk
import sqlite3

class manager:
    # init creates manager window and takes username from welcome
    def __init__(self, username):

        # unsername to identify user
        self.username = username

        # build windwo
        self.master = tk.Tk()

        # change window title
        self.master.title("Passwordmanager")

        # labels for entry forms
        tk.Label(self.master, text="Account").grid(row=0)
        tk.Label(self.master, text="Password").grid(row=1)
        tk.Label(self.master, text="E-Mail").grid(row=2)

        # entry forms
        self.entry_account = tk.Entry(self.master)
        self.entry_account.grid(row=0, column=1)
        self.entry_password = tk.Entry(self.master)
        self.entry_password.grid(row=1, column=1)
        self.entry_email = tk.Entry(self.master)
        self.entry_email.grid(row=2, column=1)

        # button to submit entry
        self.button_save = tk.Button(self.master, text='Save',
        width=25, command=self.save_info)
        self.button_save.grid(row=3, column=0)

        # button to create new account
        self.button_clear = tk.Button(self.master, text='Clear Forms',
        width=25, command=self.clear_info)
        self.button_clear.grid(row=3, column=1)

        # keep windoe opened
        self.master.mainloop()

    # takes entries and saves them into the db
    # needs to create table if not exists
    def save_info(self):
        print(self.username)

        self.account = self.entry_account.get()
        self.password = self.entry_password.get()
        self.email = self.entry_email.get()

        connection = sqlite3.connect("user_databases/" + self.username + ".db")
        cursor = connection.cursor()

        # create table if it is not already existing
        cursor.execute("CREATE TABLE IF NOT EXISTS data( \
                        account TEXT, \
                        password TEXT,\
                        email TEXT)")

        # insert information from entries into table
        cursor.execute("INSERT INTO data(account, password, email) \
                       VALUES (?, ?, ?)",
                      (self.account, self.password,self.email))

        # commit changes to table and close connection
        connection.commit()
        connection.close()

    # clears entries
    def clear_info(self):
        self.entry_account.delete(0, "end")
        self.entry_password.delete(0, "end")
        self.entry_email.delete(0, "end")
