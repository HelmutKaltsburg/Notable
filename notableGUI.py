import tkinter as tk
from tkinter import *
from tkinter import messagebox
from notableDB import Database
import datetime

db = Database('Notable.db')


class Application(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Notable')
        # Width and Height
        master.geometry("800x350")
        # Create widgets grid
        self.create_widgets()
        # Initialize selected item variable
        self.selected_note = 0
        # Populate note list
        self.populate_list()

    def create_widgets(self):
        # Author
        self.author_text = tk.StringVar()
        self.author_label = tk.Label(self.master, text='Author', font=14, pady=20)
        self.author_label.grid(row=0, column=0, sticky=W)
        self.author_entry = tk.Entry(self.master, textvariable=self.author_text, width=40)
        self.author_entry.grid(row=0, column=1)

        # Note
        self.note_text = tk.StringVar()
        self.note_label = tk.Label(self.master, text='Note', font=14)
        self.note_label.grid(row=1, column=0, sticky=W)
        self.note_entry = tk.Entry(self.master, textvariable=self.note_text, width=40)
        self.note_entry.grid(row=1, column=1)

        # Buttons
        self.add_btn = tk.Button(self.master, text="Add Note", width=12, command=self.add_note)
        self.add_btn.grid(row=2, column=0, pady=20)

        self.remove_btn = tk.Button(self.master, text="Remove Note", width=12, command=self.remove_note)
        self.remove_btn.grid(row=2, column=1)

        self.update_btn = tk.Button(self.master, text="Update Note", width=12, command=self.update_note)
        self.update_btn.grid(row=2, column=2)

        self.clear_btn = tk.Button(self.master, text="Clear Input", width=12, command=self.clear_text)
        self.clear_btn.grid(row=2, column=3)

        self.mark_btn = tk.Button(self.master, text="Mark As Done", width=12, command=self.mark_note)
        self.mark_btn.grid(row=2, column=4)

        self.show_marked_btn = tk.Button(self.master, text="Show Marked", width=12, command=self.show_marked_note)
        self.show_marked_btn.grid(row=2, column=5)

        # Notes List
        self.note_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.note_list.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

        # Create Scrollbars
        self.scrollbar_y = tk.Scrollbar(self.master)
        self.scrollbar_y.grid(row=3, column=3)
        self.scrollbar_x = tk.Scrollbar(self.master, orient='horizontal')
        self.scrollbar_x.grid(row=9, column=1)

        # Set Y Axis Scrollbar to Note List
        self.note_list.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.configure(command=self.note_list.yview)
        # Set X Axis Scrollbar to Note List
        self.note_list.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.configure(command=self.note_list.xview)

        # Bind Select
        self.note_list.bind('<<ListboxSelect>>', self.select_note)

    def populate_list(self):
        # Delete items in the list before updating
        self.note_list.delete(0, tk.END)
        # Loop through database table
        for row in db.fetch():
            # Insert into list
            self.note_list.insert(tk.END, row)

    def populate_list_marked(self):
        # Delete items in the list before updating
        self.note_list.delete(0, tk.END)
        # Loop through database table
        for row in db.fetch_marked():
            # Insert into list
            self.note_list.insert(tk.END, row)

    def add_note(self):
        if self.note_text.get() == '' or self.author_text.get() == '':
            messagebox.showerror("Required Fields", "Please include all fields")
            return
        # Insert into Database
        self.note_date = str(datetime.datetime.today())
        db.insert(self.author_text.get(), self.note_text.get(), self.note_date)
        # Clear list
        self.note_list.delete(0, tk.END)
        # Insert into list
        self.note_list.insert(tk.END, (self.author_text.get(), self.note_text.get(), self.note_date))
        self.clear_text()
        self.populate_list()

    def select_note(self, event):
        # Create global selected item to use in other functions
        # global self.selected_item
        try:
            # Get index
            index = self.note_list.curselection()[0]
            # Get selected item
            self.selected_item = self.note_list.get(index)
            # print(selected_item) # Print tuple

            # Add text to entries
            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(tk.END, self.selected_item[1])
            self.note_entry.delete(0, tk.END)
            self.note_entry.insert(tk.END, self.selected_item[2])

        except IndexError:
            pass

    def remove_note(self):
        btn_text = self.mark_btn.cget('text')
        if btn_text == "Mark As Done":
            db.remove(self.selected_item[0])
            self.clear_text()
            self.populate_list()
        if btn_text == "Unmark":
            db.remove(self.selected_item[0])
            self.clear_text()
            self.populate_list_marked()

    def update_note(self):
        btn_text = self.mark_btn.cget('text')
        if btn_text == "Mark As Done":
            self.note_date = str(datetime.datetime.today())
            db.update(self.selected_item[0], self.author_text.get(), self.note_text.get(), self.note_date)
            self.populate_list()
        if btn_text == "Unmark":
            self.note_date = str(datetime.datetime.today())
            db.update(self.selected_item[0], self.author_text.get(), self.note_text.get(), self.note_date)
            self.populate_list_marked()

    def clear_text(self):
        self.author_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)

    def mark_note(self):
        btn_text = self.mark_btn.cget('text')
        if btn_text == "Mark As Done":
            db.mark(self.selected_item[0])
            self.clear_text()
            self.populate_list()
        if btn_text == "Unmark":
            db.unmark(self.selected_item[0])
            self.clear_text()
            self.populate_list_marked()

    def show_marked_note(self):
        btn_text = self.show_marked_btn.cget('text')
        if btn_text == "Show Marked":
            self.clear_text()
            self.populate_list_marked()
            self.show_marked_btn.config(text='Show Unmarked')
            self.mark_btn.config(text='Unmark')
        if btn_text == "Show Unmarked":
            self.clear_text()
            self.populate_list()
            self.show_marked_btn.config(text='Show Marked')
            self.mark_btn.config(text='Mark As Done')


root = tk.Tk()
app = Application(master=root)
app.mainloop()
