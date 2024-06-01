import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        address TEXT
    )
''')
conn.commit()

# Functions
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if not name or not phone:
        messagebox.showwarning("Input Error", "Name and Phone number are required.")
        return

    cursor.execute('INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)', (name, phone, email, address))
    conn.commit()
    clear_entries()
    load_contacts()

def load_contacts():
    for row in contact_list.get_children():
        contact_list.delete(row)
    cursor.execute('SELECT id, name, phone FROM contacts')
    for row in cursor.fetchall():
        contact_list.insert('', 'end', values=row)

def search_contact():
    search_term = search_entry.get()
    for row in contact_list.get_children():
        contact_list.delete(row)
    cursor.execute('SELECT id, name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?', ('%' + search_term + '%', '%' + search_term + '%'))
    for row in cursor.fetchall():
        contact_list.insert('', 'end', values=row)

def update_contact():
    try:
        selected_item = contact_list.selection()[0]
        contact_id = contact_list.item(selected_item)['values'][0]
    except IndexError:
        messagebox.showwarning("Selection Error", "No contact selected.")
        return

    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    cursor.execute('UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?', (name, phone, email, address, contact_id))
    conn.commit()
    clear_entries()
    load_contacts()

def delete_contact():
    try:
        selected_item = contact_list.selection()[0]
        contact_id = contact_list.item(selected_item)['values'][0]
    except IndexError:
        messagebox.showwarning("Selection Error", "No contact selected.")
        return

    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    load_contacts()

def clear_entries():
    name_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')
    email_entry.delete(0, 'end')
    address_entry.delete(0, 'end')

def on_contact_select(event):
    try:
        selected_item = contact_list.selection()[0]
        contact_id = contact_list.item(selected_item)['values'][0]

        cursor.execute('SELECT name, phone, email, address FROM contacts WHERE id = ?', (contact_id,))
        contact = cursor.fetchone()

        clear_entries()
        name_entry.insert(0, contact[0])
        phone_entry.insert(0, contact[1])
        email_entry.insert(0, contact[2])
        address_entry.insert(0, contact[3])
    except IndexError:
        pass

# GUI Setup
root = tk.Tk()
root.title("Contact Manager")
root.geometry("700x500")
root.configure(background='violet')

# Styles
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), background='violet', foreground='black')
style.configure("TButton", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12), fieldbackground='cream')
style.configure("Treeview", font=("Arial", 12), rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

# Frames
input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill='x', padx=10, pady=5)

button_frame = ttk.Frame(root, padding="10")
button_frame.pack(fill='x', padx=10, pady=5)

search_frame = ttk.Frame(root, padding="10")
search_frame.pack(fill='x', padx=10, pady=5)

list_frame = ttk.Frame(root, padding="10")
list_frame.pack(fill='both', expand=True, padx=10, pady=5)

# Input Fields
ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
name_entry = ttk.Entry(input_frame, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
phone_entry = ttk.Entry(input_frame, width=30)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
email_entry = ttk.Entry(input_frame, width=30)
email_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Address:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
address_entry = ttk.Entry(input_frame, width=30)
address_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons
add_button = ttk.Button(button_frame, text="Add Contact", command=add_contact)
add_button.grid(row=0, column=0, padx=5, pady=5)

update_button = ttk.Button(button_frame, text="Update Contact", command=update_contact)
update_button.grid(row=0, column=1, padx=5, pady=5)

delete_button = ttk.Button(button_frame, text="Delete Contact", command=delete_contact)
delete_button.grid(row=0, column=2, padx=5, pady=5)

# Search Field
ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
search_entry = ttk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=5, pady=5)
search_button = ttk.Button(search_frame, text="Search", command=search_contact)
search_button.grid(row=0, column=2, padx=5, pady=5)

# Contact List
columns = ("id", "name", "phone")
contact_list = ttk.Treeview(list_frame, columns=columns, show='headings')
contact_list.heading("id", text="ID")
contact_list.heading("name", text="Name")
contact_list.heading("phone", text="Phone")
contact_list.column("id", width=50)
contact_list.column("name", width=200)
contact_list.column("phone", width=150)
contact_list.pack(fill='both', expand=True)
contact_list.bind('<<TreeviewSelect>>', on_contact_select)

# Load contacts initially
load_contacts()

# Start the GUI loop
root.mainloop()

# Close the database connection when the GUI is closed
conn.close()
