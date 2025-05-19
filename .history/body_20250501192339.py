from tkinter import *
from tkinter import ttk
import math
from database import get_all_students, get_student_by_id
from misc import create_rounded_rectangle, remove_focus

student_table = None
current_page = 0
items_per_page = 10
total_pages = 1
selected_student_id = None
search_text = None
body_frame = None
table_frame = None
sort_column = "id_number"
sort_direction = "asc"
all_students = []

def body(root):
    global student_table, current_page, items_per_page, total_pages, page_label
    global pagination_frame, total_records, filtered_records, search_function, body_frame, table_frame
    global prev_button, next_button, total_students_label, all_students

    body_frame = Frame(root, bg="white")
    body_frame.grid(row=1, column=1, sticky="nsew")
    body_frame.columnconfigure(0, weight=1)
    body_frame.rowconfigure(0, weight=1)
    body_frame.rowconfigure(1, weight=0)

    student_text = Label(body_frame, background="white", text="STUDENTS", font=("AlbertSans", 20, "bold"))
    student_text.grid(row=0, column=0, sticky="nw", pady=0, padx=20)

    table_frame = Frame(body_frame, bg="white")
    table_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=50)
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    initialize_table()
    setup_pagination()
    
    all_students, total_count = get_all_students()
    initialize_display()

    return body_frame

def initialize_table():
    global student_table

    style = ttk.Style()
    style_name = "StudentTable.Treeview"
    
    style.configure(style_name,
                  background="white",
                  foreground="black",
                  rowheight=40,
                  fieldbackground="white",
                  font=("Albert Sans", 12),
                  borderwidth=0,
                  relief="flat",
                  padding=5)
    
    style.configure(style_name + ".Heading",
                  font=("Albert Sans", 15, "bold"),
                  background="#f0f0f0",
                  foreground="#9F9EA1",
                  borderwidth=0,
                  relief="flat",
                  anchor='w',
                  padding=(1, 8))
    
    style.map(style_name,
              background=[('selected', '#3A7FF6')],
              foreground=[('selected', 'white')])

    style.layout(style_name, [('Treeview.treearea', {'sticky': 'nswe'})])

    columns = ("ID", "ID No.", "Name", "Gender", "Yr. Level", "College", "Program")
    student_table = ttk.Treeview(table_frame,
                               columns=columns,
                               show="headings",
                               style=style_name,
                               selectmode="browse")

    student_table.heading("ID No.", text="ID No.", anchor=W, command=lambda: sort_table("id_number"))
    student_table.heading("Name", text="Name (Last, First)", anchor=W, command=lambda: sort_table("last_name"))
    student_table.heading("Gender", text="Gender", anchor=W)
    student_table.heading("Yr. Level", text="Yr. Level", anchor=W)
    student_table.heading("College", text="College", anchor=W)
    student_table.heading("Program", text="Program", anchor=W)

    student_table.column("ID", width=0, stretch=NO)
    student_table.column("ID No.", width=100, anchor=W)
    student_table.column("Name", width=250, anchor=W)
    student_table.column("Gender", width=100, anchor=W)
    student_table.column("Yr. Level", width=100, anchor=CENTER)
    student_table.column("College", width=100, anchor=W)
    student_table.column("Program", width=250, anchor=W)

    student_table.tag_configure('hover', background='#e6f0ff')
    student_table.tag_configure('selected', background='#3A7FF6', foreground='white')

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=student_table.yview)
    student_table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    student_table.pack(fill=BOTH, expand=1)

    student_table.bind("<Motion>", on_hover)
    student_table.bind("<Leave>", on_leave)
    student_table.bind("<Button-1>", on_click)
    table_frame.bind("<Configure>", lambda e: display_students(current_page))

def setup_pagination():
    global pagination_frame, prev_button, next_button, page_label, total_students_label

    pagination_frame = Frame(body_frame, bg="white")
    pagination_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

    def on_enter(e):
        e.widget['background'] = '#e0e0e0'
        e.widget['foreground'] = 'black'

    def on_leave_prev(e):
        e.widget['background'] = 'white'
        e.widget['foreground'] = 'black'

    def on_leave_next(e):
        e.widget['background'] = 'white'
        e.widget['foreground'] = 'black'

    prev_button = Button(pagination_frame, text="◀ Prev", bg="white", fg="black",
                         font=("Albert Sans", 10), padx=5, pady=2, relief="flat",
                         borderwidth=0, activebackground="#e0e0e0", cursor="hand2",
                         command=lambda: change_page(-1))
    prev_button.pack(side=LEFT, padx=(20, 5))
    prev_button.bind("<Enter>", on_enter)
    prev_button.bind("<Leave>", on_leave_prev)

    page_label = Label(pagination_frame, text="Page 1 of 1", bg="white", font=("Albert Sans", 10))
    page_label.pack(side=LEFT)

    next_button = Button(pagination_frame, text="Next ▶", bg="white", fg="black",
                         font=("Albert Sans", 10), padx=5, pady=2, relief="flat",
                         borderwidth=0, activebackground="#e0e0e0", cursor="hand2",
                         command=lambda: change_page(1))
    next_button.pack(side=LEFT, padx=5)
    next_button.bind("<Enter>", on_enter)
    next_button.bind("<Leave>", on_leave_next)

    total_students_label = Label(pagination_frame, text="Total Students: 0",
                                font=("Albert Sans", 10, "normal"), bg="white")
    total_students_label.pack(side=RIGHT, padx=50)

def calculate_rows_per_page():
    table_frame.update_idletasks()
    table_height = table_frame.winfo_height()
    
    if table_height <= 1:
        return 10
    
    row_height = 40
    header_height = 50
    padding = 100
    available_height = table_height - header_height - padding
    max_rows = max(1, available_height // row_height)
    return min(max_rows, 20)

def sort_students(students, sort_by, direction):
    reverse = (direction == "desc")
    if sort_by == "id_number":
        return sorted(students, key=lambda x: x['id_number'], reverse=reverse)
    elif sort_by == "last_name":
        return sorted(students, key=lambda x: x['last_name'].lower(), reverse=reverse)
    return students

def display_students(page=0):
    global current_page, items_per_page, total_pages, total_records, filtered_records
    global student_table, page_label, prev_button, next_button, total_students_label
    global sort_column, sort_direction, search_text, all_students

    items_per_page = calculate_rows_per_page()
    
    for item in student_table.get_children():
        student_table.delete(item)

    filtered = all_students
    if search_text:
        search_lower = search_text.lower()
        filtered = [s for s in all_students 
                   if (search_lower in s['id_number'].lower() or 
                       search_lower in s['last_name'].lower() or 
                       search_lower in s['first_name'].lower())]

    filtered = sort_students(filtered, sort_column, sort_direction)

    total_count = len(filtered)
    filtered_records = total_count
    total_records = len(all_students)
    total_pages = math.ceil(total_count / items_per_page) if total_count > 0 else 1
    current_page = min(page, max(0, total_pages - 1))

    start_idx = current_page * items_per_page
    end_idx = start_idx + items_per_page
    students_to_display = filtered[start_idx:end_idx]

    for student in students_to_display:
        year_mapping = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5+"}
        year_level = year_mapping.get(student['year_level'], "")
        
        student_table.insert('', 'end', values=(
            student['id'],
            student['id_number'],
            f"{student['last_name']}, {student['first_name']}",
            student['gender'],
            year_level,
            student['college_code'],
            student['program_code']
        ))

    total_students_label.config(text=f"Total Students: {filtered_records}" + 
                               (" (filtered)" if search_text else ""))
    page_label.config(text=f"Page {current_page + 1} of {total_pages}")
    prev_button.config(state=NORMAL if current_page > 0 else DISABLED)
    next_button.config(state=NORMAL if current_page < total_pages - 1 else DISABLED)

def initialize_display():
    table_frame.update_idletasks()
    display_students(0)

def change_page(direction):
    global current_page
    new_page = current_page + direction
    if 0 <= new_page < total_pages:
        current_page = new_page
        display_students(current_page)

def sort_table(column):
    global sort_column, sort_direction
    if column == sort_column:
        sort_direction = "desc" if sort_direction == "asc" else "asc"
    else:
        sort_column = column
        sort_direction = "asc"
    display_students(current_page)

def on_hover(event):
    item = student_table.identify_row(event.y)
    if item:
        for child in student_table.get_children():
            if 'hover' in student_table.item(child, 'tags'):
                student_table.item(child, tags=())
        if item not in student_table.selection():
            student_table.item(item, tags=('hover',))

def on_leave(event):
    for item in student_table.get_children():
        if 'hover' in student_table.item(item, 'tags'):
            student_table.item(item, tags=())

def on_click(event):
    item = student_table.identify_row(event.y)
    if item:
        student_table.selection_set(item)
        on_student_select(event)
    else:
        student_table.selection_remove(student_table.selection())
        selected_student_id = None

def on_student_select(event):
    global selected_student_id
    selected_items = student_table.selection()
    if selected_items:
        item = selected_items[0]
        values = student_table.item(item, "values")
        selected_student_id = values[0]
    else:
        selected_student_id = None

def get_selected_student_data():
    global selected_student_id
    if selected_student_id:
        return get_student_by_id(selected_student_id)
    return None

def set_search_text(text):
    global search_text, current_page
    search_text = text if text != "" else None
    current_page = 0
    display_students(current_page)

def set_search_function(func):
    global search_function
    search_function = func

def refresh_students():
    global all_students
    all_students, _ = get_all_students()
    display_students(current_page)