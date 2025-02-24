import tkinter as tk
from tkinter import ttk
import csv

# Function to load students from CSV
def load_students(filename):
    students = []
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            students.append(row)  # Append [ID No., Name]
    return students

# Function to parse ID for sorting
def parse_id(id_str):
    try:
        year, number = map(int, id_str.split("-"))
        return (year, number)
    except ValueError:
        return (float('inf'), float('inf'))

# Function to sort students
def sort_students():
    global students
    sort_by = sort_by_dropdown.get().strip()
    order = order_dropdown.get().strip()
    
    if not sort_by or not order:
        return
    
    reverse_order = (order == "Descending")
    
    if sort_by == "ID No.":
        students.sort(key=lambda x: parse_id(x[0]), reverse=reverse_order)
    elif sort_by == "Name":
        students.sort(key=lambda x: x[1].strip().lower(), reverse=reverse_order)
    
    update_treeview()

# Function to update Treeview
def update_treeview():
    tree.delete(*tree.get_children())  # Clear tree
    for student in students:
        tree.insert("", "end", values=student)
    root.update()  # Force UI refresh

# Tkinter GUI setup
root = tk.Tk()
root.title("Student Sorting Test")
root.geometry("400x400")

# Load students
students = load_students("students.csv")

# Dropdowns for sorting
sort_by_dropdown = ttk.Combobox(root, values=["ID No.", "Name"], state="readonly")
sort_by_dropdown.set("Select")
sort_by_dropdown.pack(pady=5)

order_dropdown = ttk.Combobox(root, values=["Ascending", "Descending"], state="readonly")
order_dropdown.set("Ascending")
order_dropdown.pack(pady=5)

sort_button = tk.Button(root, text="Sort", command=sort_students)
sort_button.pack(pady=5)

# Treeview setup
tree = ttk.Treeview(root, columns=("ID No.", "Name"), show="headings")
tree.heading("ID No.", text="ID No.")
tree.heading("Name", text="Name")
tree.pack(expand=True, fill="both")

update_treeview()  # Initial display

root.mainloop()
