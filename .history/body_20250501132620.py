from tkinter import *
from tkinter import ttk
import math
from database import get_all_students, get_student_by_id
from misc import create_rounded_rectangle, remove_focus

student_table = None
current_page = 1
items_per_page = 10
total_pages = 1
selected_student_id = None
search_text = None
body_frame = None

from tkinter import *
from tkinter import ttk
import math
from database import get_all_students, get_student_by_id
from misc import create_rounded_rectangle, remove_focus

student_table = None
current_page = 1
items_per_page = 10
total_pages = 1
selected_student_id = None
search_text = None
body_frame = None

def body(root):
    global student_table, current_page, items_per_page, total_pages, page_label
    global pagination_frame, total_records, filtered_records, search_function, body_frame, table_frame
    global prev_button, next_button, total_students_label

    body_frame = None

    current_page = 1
    items_per_page = 10
    total_records = 0
    filtered_records = 0
    search_function = None

    if not hasattr(body, 'original_students'):
        body.original_students = []

    if not hasattr(body, 'current_students'):
        body.current_students = []

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

    # Create a unique style name for this table only
    style = ttk.Style()
    style_name = "StudentTable.Treeview"
    
    # Configure the treeview style without affecting other widgets
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

    # Remove all borders from the treeview
    style.layout(style_name, [('Treeview.treearea', {'sticky': 'nswe'})])

    columns = ("ID", "ID No.", "Name", "Gender", "Yr. Level", "College", "Program")
    scrollbar = Scrollbar(table_frame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    student_table = ttk.Treeview(table_frame,
                               columns=columns,
                               show="headings",
                               yscrollcommand=scrollbar.set,
                               style=style_name,
                               selectmode="browse")
    scrollbar.config(command=student_table.yview)

    # Configure columns
    student_table.heading("ID No.", text="ID No.", anchor=W)
    student_table.heading("Name", text="Name (Last, First)", anchor=W)
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

    last_clicked_item = None

    def on_hover(event):
        item = student_table.identify_row(event.y)
        if item:
            for child in student_table.get_children():
                if 'hover' in student_table.item(child, 'tags'):
                    student_table.item(child, tags=())
            
            if item not in student_table.selection():
                student_table.item(item, tags=('hover',))

    def on_leave(event):
        # Remove hover from all items
        for item in student_table.get_children():
            if 'hover' in student_table.item(item, 'tags'):
                student_table.item(item, tags=())

    def on_click(event):
        nonlocal last_clicked_item
        item = student_table.identify_row(event.y)
        
        if item:
            if item == last_clicked_item:
                if item in student_table.selection():
                    student_table.selection_remove(item)
                    global selected_student_id
                    selected_student_id = None
                else:
                    student_table.selection_set(item)
                    on_student_select(event)
            else:
                student_table.selection_set(item)
                on_student_select(event)
            
            last_clicked_item = item
        else:
            student_table.selection_remove(student_table.selection())
            selected_student_id = None
            last_clicked_item = None

    def on_frame_click(event):
        if not student_table.identify_row(event.y):
            student_table.selection_remove(student_table.selection())
            global selected_student_id
            selected_student_id = None
            nonlocal last_clicked_item
            last_clicked_item = None

    # Bind events
    student_table.bind("<Motion>", on_hover)
    student_table.bind("<Leave>", on_leave)
    student_table.bind("<Button-1>", on_click)
    table_frame.bind("<Button-1>", on_frame_click)
    
    table_frame.config(takefocus=1)
    table_frame.focus_set()

    student_table.pack(fill=BOTH, expand=1)

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
                         command=lambda: go_to_page(current_page - 1))
    prev_button.pack(side=LEFT, padx=(20, 5))
    prev_button.bind("<Enter>", on_enter)
    prev_button.bind("<Leave>", on_leave_prev)

    page_label = Label(pagination_frame, text="Page 1 of 1", bg="white", font=("Albert Sans", 10))
    page_label.pack(side=LEFT)

    next_button = Button(pagination_frame, text="Next ▶", bg="white", fg="black",
                         font=("Albert Sans", 10), padx=5, pady=2, relief="flat",
                         borderwidth=0, activebackground="#e0e0e0", cursor="hand2",
                         command=lambda: go_to_page(current_page + 1))
    next_button.pack(side=LEFT, padx=5)
    next_button.bind("<Enter>", on_enter)
    next_button.bind("<Leave>", on_leave_next)

    total_students_label = Label(pagination_frame, text="Total Students: 0",
                                font=("Albert Sans", 10, "normal"), bg="white")
    total_students_label.pack(side=RIGHT, padx=50)

    root.bind("<Configure>", on_resize)
    load_students()

    return body_frame

def calculate_rows_per_page():
    height = table_frame.winfo_height()
    row_height = 40
    header_height = 50
    padding = 100
    max_rows = (height - header_height - padding) // row_height
    return max(1, min(max_rows, 20))

def on_resize(event):
    global items_per_page
    if event and event.widget == event.widget.winfo_toplevel():
        if hasattr(table_frame, 'winfo_height'):
            table_frame.update_idletasks()
            new_items = calculate_rows_per_page()
            if new_items != items_per_page:
                items_per_page = new_items
                load_students()

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

def load_students(search_term=None):
    global current_page, items_per_page, total_pages, total_records, filtered_records
    global total_students_label, page_label, prev_button, next_button

    for item in student_table.get_children():
        student_table.delete(item)

    if search_term is None and search_function:
        search_term = search_function()

    students, total_count = get_all_students(
        page=current_page,
        items_per_page=items_per_page,
        search_term=search_term
    )

    if not search_term and not hasattr(body, 'original_students'):
        body.original_students = list(students)

    body.current_students = list(students)

    filtered_records = total_count
    total_records = total_count if not search_term else total_count
    total_pages = math.ceil(total_count / items_per_page) if total_count > 0 else 1

    if current_page > total_pages:
        current_page = total_pages
        return load_students(search_term)

    for student in students:
        year_mapping = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5+"}
        year_level = year_mapping.get(student['year_level'], "")

        program_display = student['program_code'] if student['program_code'] != 'N/A' else "No Program Assigned"
        college_display = student['college_code'] if student['college_code'] != 'N/A' else "No College Assigned"
        full_name = f"{student['last_name']}, {student['first_name']}"

        student_table.insert('', 'end', values=(
            student['id'],
            student['id_number'],
            full_name,
            student['gender'],
            year_level,
            college_display,
            program_display
        ))

    if search_term:
        total_students_label.config(text=f"Total Students: {filtered_records} (filtered)")
    else:
        total_students_label.config(text=f"Total Students: {total_records}")

    page_label.config(text=f"Page {current_page} of {total_pages}")
    prev_button.config(state=NORMAL if current_page > 1 else DISABLED)
    next_button.config(state=NORMAL if current_page < total_pages else DISABLED)

def go_to_page(page):
    global current_page
    total_pages = math.ceil(filtered_records / items_per_page) if filtered_records > 0 else 1
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    if current_page != page:
        current_page = page
        load_students()

def refresh_students():
    load_students()

def set_search_function(func):
    global search_function
    search_function = func
