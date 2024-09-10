import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            global data
            data = pd.read_csv(file_path)
            messagebox.showinfo("Success", "CSV file loaded successfully!")
            show_csv_in_window(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")

def show_csv_in_window(data):
    csv_window = tk.Toplevel(root)
    csv_window.title("CSV Data")

    text = tk.Text(csv_window, wrap='none')
    text.pack(expand=True, fill='both')

    scrollbar_y = tk.Scrollbar(csv_window, orient='vertical', command=text.yview)
    scrollbar_y.pack(side='right', fill='y')
    text.configure(yscrollcommand=scrollbar_y.set)

    scrollbar_x = tk.Scrollbar(csv_window, orient='horizontal', command=text.xview)
    scrollbar_x.pack(side='bottom', fill='x')
    text.configure(xscrollcommand=scrollbar_x.set)

    # Display column names and types
    column_info = ', '.join([f"{col} ({dtype})" for col, dtype in zip(data.columns, data.dtypes)])
    text.insert(tk.END, column_info + '\n\n')

    for index, row in data.iterrows():
        text.insert(tk.END, ', '.join(map(str, row.values)) + '\n')

def generate_messages():
    if data is None:
        messagebox.showerror("Error", "No CSV file loaded!")
        return

    template = template_text.get("1.0", tk.END).strip()
    if not template:
        messagebox.showerror("Error", "Template is empty!")
        return

    messages = []
    for _, row in data.iterrows():
        message = template.format(**row)
        messages.append(message)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "\n\n\n\n\n//////New merge\n".join(messages))  # Add 5 lines gap

root = tk.Tk()
root.title("Mail Merge")

data = None

load_button = tk.Button(root, text="Load CSV", command=load_csv)
load_button.pack(pady=10)

template_label = tk.Label(root, text="Template:")
template_label.pack()

template_text = tk.Text(root, height=10, width=50)
template_text.pack(pady=10)

generate_button = tk.Button(root, text="Generate Messages", command=generate_messages)
generate_button.pack(pady=10)

output_label = tk.Label(root, text="Output:")
output_label.pack()

output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=10)

root.mainloop()
