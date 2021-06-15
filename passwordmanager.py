import tkinter as tk
from tkinter import ttk
import sqlite3

# class to get scrollable frame to show content
# https://blog.tecladocode.com/tkinter-scrollable-frames/
class ScrollableFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

# main class
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

        # frame to display content
        self.content_frame = ScrollableFrame(self.master)
        self.content_frame.grid(row=4, columnspan=2, rowspan=5)

        # update scrollable frame
        self.show_content()

        # keep window opened
        self.master.mainloop()

    # takes entries and saves them into the db
    # needs to create table if not exists
    def save_info(self):
        print(self.username)

        # get entered information
        self.account = self.entry_account.get()
        self.password = self.entry_password.get()
        self.email = self.entry_email.get()

        # conncet to user specific db
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

        # update frame
        self.show_content()

    # clears entries
    def clear_info(self):
        self.entry_account.delete(0, "end")
        self.entry_password.delete(0, "end")
        self.entry_email.delete(0, "end")

    # method to show passwords and other information in frame
    # needs to connect to db and read information
    # for every row in db it should create labels with text in the scrollable_frame
    def show_content(self):

        # clear frame
        for child in self.content_frame.scrollable_frame.winfo_children():
            child.destroy()

        # conncet to user specific db
        connection = sqlite3.connect("user_databases/" + self.username + ".db")
        cursor = connection.cursor()

        # select db entry where username is equal to typed in username
        cursor.execute("SELECT * FROM data")

        # get entry as strings
        rows = cursor.fetchall()

        connection.close()

        ttk.Label(self.content_frame.scrollable_frame, text="Accountname").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self.content_frame.scrollable_frame, text="Passwort").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.content_frame.scrollable_frame, text="E-Mail-Adresse").grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.content_frame.scrollable_frame, text="").grid(row=1, column=0, padx=5, pady=5)

        counter = 1
        for row in rows:
            counter += 1
            ttk.Label(self.content_frame.scrollable_frame, text=row[0]).grid(row=counter, column=0, padx=5, pady=5)
            ttk.Label(self.content_frame.scrollable_frame, text=row[1]).grid(row=counter, column=1, padx=5, pady=5)
            ttk.Label(self.content_frame.scrollable_frame, text=row[2]).grid(row=counter, column=2, padx=5, pady=5)
