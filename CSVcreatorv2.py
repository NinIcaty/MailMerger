import tkinter as tk
from tkinter import filedialog, messagebox
import csv

def add_column():
    column_name = column_entry.get()
    if not column_name:
        messagebox.showerror("Error", "Column name cannot be empty!")
        return

    if column_name in columns:
        messagebox.showerror("Error", "Column already exists!")
        return

    columns.append(column_name)
    column_entry.delete(0, tk.END)
    update_column_labels()
    #Not must messagebox.showinfo("Success", f"Column '{column_name}' added successfully!")

def update_column_labels():
    for widget in entry_frame.winfo_children():
        widget.destroy()

    for column in columns:
        tk.Label(entry_frame, text=column).pack()
        entry = tk.Entry(entry_frame)
        entry.pack()
        entries[column] = entry

def add_entry():
    entry_data = {}
    for column, entry in entries.items():
        value = entry.get()
        if not value:
            messagebox.showerror("Error", f"All fields are required! Missing value for '{column}'")
            return
        entry_data[column] = value

    data.append(entry_data)
    for entry in entries.values():
        entry.delete(0, tk.END)
    update_listbox()
    #Not must messagebox.showinfo("Success", "Entry added successfully!")

def update_listbox():
    listbox.delete(0, tk.END)
    for i, entry in enumerate(data):
        listbox.insert(tk.END, f"{i+1}. " + " | ".join(f"{k}: {v}" for k, v in entry.items()))

def save_to_csv():
    if not data:
        messagebox.showerror("Error", "No data to save!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)
        #Not must messagebox.showinfo("Success", "CSV file saved successfully!")

def create_csv_file():
    global data, columns
    if not data:
        messagebox.showerror("Error", "No data to save!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)
        messagebox.showinfo("Success", "New CSV file created successfully!")
        # Reset data and columns for new CSV file
        data = []
        columns = ["First Name", "Last Name", "Profession"]
        update_column_labels()
        listbox.delete(0, tk.END)

def load_csv():
    global data, columns
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames
        data = list(reader)

    update_column_labels()
    update_listbox()
    messagebox.showinfo("Success", "CSV file loaded successfully!")

def edit_entry():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No entry selected!")
        return

    index = selected[0]
    entry_data = data[index]

    for column, entry in entries.items():
        entry.delete(0, tk.END)
        entry.insert(0, entry_data[column])

    def save_edit():
        for column, entry in entries.items():
            data[index][column] = entry.get()
        update_listbox()
        for entry in entries.values():
            entry.delete(0, tk.END)
        #Not must messagebox.showinfo("Success", "Entry edited successfully!")
        edit_window.destroy()

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Entry")
    tk.Button(edit_window, text="Save", command=save_edit).pack(pady=10)

def delete_entry():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "No entry selected!")
        return

    index = selected[0]
    del data[index]
    update_listbox()
    #Not must messagebox.showinfo("Success", "Entry deleted successfully!")

def customize_column_order():
    def save_order():
        global columns
        new_order = [entry.get() for entry in order_entries]
        if set(new_order) != set(columns):
            messagebox.showerror("Error", "Column names do not match!")
            return
        columns = new_order
        update_listbox()
        #Not must messagebox.showinfo("Success", "Column order updated successfully!")
        order_window.destroy()

    order_window = tk.Toplevel(root)
    order_window.title("Customize Column Order")

    order_entries = []
    for column in columns:
        tk.Label(order_window, text=column).pack()
        entry = tk.Entry(order_window)
        entry.insert(0, column)
        entry.pack()
        order_entries.append(entry)

    tk.Button(order_window, text="Save Order", command=save_order).pack(pady=10)

root = tk.Tk()
root.title("CSV Creator")

# Center the window on the screen
window_width = 600
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

columns = []
data = []
entries = {}

column_frame = tk.Frame(scrollable_frame)
column_frame.pack(pady=10)

tk.Label(column_frame, text="New Column Name").pack(side=tk.LEFT)
column_entry = tk.Entry(column_frame)
column_entry.pack(side=tk.LEFT, padx=5)
add_column_button = tk.Button(column_frame, text="Add Column", command=add_column)
add_column_button.pack(side=tk.LEFT)

entry_frame = tk.Frame(scrollable_frame)
entry_frame.pack(pady=10)
update_column_labels()

add_button = tk.Button(scrollable_frame, text="Add Entry", command=add_entry)
add_button.pack(pady=10)

listbox_frame = tk.Frame(scrollable_frame)
listbox_frame.pack(pady=10)

listbox_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
listbox = tk.Listbox(listbox_frame, width=80, yscrollcommand=listbox_scrollbar.set)
listbox_scrollbar.config(command=listbox.yview)
listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

edit_button = tk.Button(scrollable_frame, text="Edit Entry", command=edit_entry)
edit_button.pack(pady=5)

delete_button = tk.Button(scrollable_frame, text="Delete Entry", command=delete_entry)
delete_button.pack(pady=5)

save_button = tk.Button(scrollable_frame, text="Save to CSV", command=save_to_csv)
save_button.pack(pady=10)

create_csv_button = tk.Button(scrollable_frame, text="Create CSV File", command=create_csv_file)
create_csv_button.pack(pady=10)

load_csv_button = tk.Button(scrollable_frame, text="Load CSV", command=load_csv)
load_csv_button.pack(pady=10)

customize_order_button = tk.Button(scrollable_frame, text="Customize Column Order", command=customize_column_order)
customize_order_button.pack(pady=10)

canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()
