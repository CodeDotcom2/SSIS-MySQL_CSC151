from tkinter import *
from tkinter import ttk
from misc import create_rounded_rectangle
from header import top
from main import display_students, load_students, content_frame, is_form_visible, restore_content

# Global variables
sort_img = None
sort_canvas = None
sort_frame = None
sorting = None
sort_text = None
id_text = None

def create_sort_button():
    global sort_img, sort_canvas, sort_frame
    
    # Create canvas with adjusted position
    sort_canvas = Canvas(top, width=30, height=30, highlightthickness=0, bd=0, bg="red")
    sort_canvas.grid(row=0, column=1, padx=(0, 70), pady=(-5, 0), sticky="e")  # Moved up with negative pady
    
    # Create rounded rectangle background
    sort_frame = create_rounded_rectangle(sort_canvas, 0, 0, 30, 30, radius=20, fill="white") 
    
    # Load the image
    sort_img = PhotoImage(file="Images/sort.png")
    sort_canvas.create_image(15, 15, image=sort_img, anchor="center") 

    # Bind events
    sort_canvas.tag_bind(sort_frame, "<Enter>", on_enter)
    sort_canvas.tag_bind(sort_frame, "<Leave>", on_leave)
    sort_canvas.tag_bind(sort_frame, "<Button-1>", sort_clicked)
    sort_canvas.bind("<Enter>", on_enter)
    sort_canvas.bind("<Leave>", on_leave)
    sort_canvas.bind("<Button-1>", sort_clicked)
    sort_canvas.bind("<ButtonRelease-1>", sort_click_release)

    return sort_canvas

def on_enter(event):
    sort_canvas.itemconfig(sort_frame, fill="#A5CAEC")
    sort_canvas.config(cursor="hand2")

def on_leave(event):
    sort_canvas.itemconfig(sort_frame, fill="white")
    sort_canvas.config(cursor="")

def sort_clicked(event):
    global sorting
    if sorting:
        sorting.destroy()
        sorting = None
        sort_canvas.itemconfig(sort_frame, fill="white")
    else:
        show_sort_options()

def sort_click_release(event):
    sort_canvas.itemconfig(sort_frame, fill="#A5CAEC")

def show_sort_options():
    global sorting, sort_text, id_text
    
    if is_form_visible:
        restore_content()
    
    style = ttk.Style()
    style.configure("Custom.TCombobox", foreground="", relief="flat", foreground="gray")

    sorting = Canvas(content_frame, width=100, height=150, bg="white", highlightthickness=0)
    sorting_frame = create_rounded_rectangle(sorting, 0, 0, 100, 150, radius=20, fill="light gray") 
    sorting.grid(row=0, column=0, sticky="ne", padx=(0, 70))
    sorting.tag_bind(sorting_frame, "<Button-1>", lambda e: None)  # Prevent closing when clicking inside

    # Sort by label
    sort_by = Label(sorting, text="Sort By:", font=("Arial", 10, "bold"), bg="light gray", fg="#2363C6")
    sorting.create_window(30, 15, window=sort_by)

    # Name sort option
    name_sort = Label(sorting, text="Name", font=("Arial", 10, "bold"), bg="light gray", fg="black")
    sorting.create_window(25, 40, window=name_sort)

    name_sort_bg = Canvas(sorting, bg="lightgray", width=80, height=22, bd=0, highlightthickness=0)
    sorting.create_window(45, 65, window=name_sort_bg)

    sort_butt = create_rounded_rectangle(name_sort_bg, 0, 0, 80, 22, radius=20, fill="#2363C6") 
    sort_text = Label(name_sort_bg, text="Ascending", font=("Albert Sans", 8, "bold"), bg="#2363C6", fg="white")
    name_sort_bg.create_window(40, 11, window=sort_text)

    name_sort_bg.bind("<Button-1>", on_click)
    name_sort_bg.bind("<ButtonRelease-1>", name_release)
    sort_text.bind("<Button-1>", on_click)
    sort_text.bind("<ButtonRelease-1>", name_release)

    name_sort_bg.bind("<Enter>", name_sort_hover)
    name_sort_bg.bind("<Leave>", name_sort_leave)
    sort_text.bind("<Enter>", name_sort_hover)
    sort_text.bind("<Leave>", name_sort_leave)

    # ID sort option
    id_sort = Label(sorting, text="ID No.", font=("Arial", 10, "bold"), bg="light gray", fg="black")
    sorting.create_window(25, 90, window=id_sort)

    id_sort_bg = Canvas(sorting, bg="lightgray", width=80, height=22, bd=0, highlightthickness=0)
    sorting.create_window(45, 115, window=id_sort_bg)

    id_butt = create_rounded_rectangle(id_sort_bg, 0, 0, 80, 22, radius=20, fill="#2363C6") 
    id_text = Label(id_sort_bg, text="Ascending", font=("Albert Sans", 8, "bold"), bg="#2363C6", fg="white")
    id_sort_bg.create_window(40, 11, window=id_text)

    id_sort_bg.bind("<Button-1>", on_click)
    id_sort_bg.bind("<ButtonRelease-1>", id_release)
    id_text.bind("<Button-1>", on_click)
    id_text.bind("<ButtonRelease-1>", id_release)

    id_sort_bg.bind("<Enter>", id_sort_hover)
    id_sort_bg.bind("<Leave>", id_sort_leave)
    id_text.bind("<Enter>", id_sort_hover)
    id_text.bind("<Leave>", id_sort_leave)

def on_click(event):
    widget = event.widget 
    if widget in [sort_text, name_sort_bg]:  
        name_sort_bg.itemconfig(sort_butt, fill='#A5CAEC')
        sort_text.configure(bg="#A5CAEC", fg="#153E83")
    elif widget in [id_text, id_sort_bg]:  
        id_sort_bg.itemconfig(id_butt, fill='#A5CAEC')
        id_text.configure(bg="#A5CAEC", fg="#153E83")

def id_release(event):
    id_sort_bg.itemconfig(id_butt, fill='#153E83')
    id_text.config(bg='#153E83', fg='white')   
    sort_id()

def name_release(event):
    name_sort_bg.itemconfig(sort_butt, fill='#153E83')
    sort_text.config(bg='#153E83', fg='white')  
    sort_name()

def name_sort_hover(event):
    name_sort_bg.itemconfig(sort_butt, fill='#153E83')
    sort_text.config(bg='#153E83', fg='white')  
    name_sort_bg.config(cursor="hand2")
    sort_text.configure(cursor="hand2")

def name_sort_leave(event):
    name_sort_bg.itemconfig(sort_butt, fill='#2363C6') 
    sort_text.config(bg='#2363C6', fg='white') 
    name_sort_bg.config(cursor="")

def id_sort_hover(event):
    id_sort_bg.itemconfig(id_butt, fill='#153E83')
    id_text.config(bg='#153E83', fg='white')  
    id_sort_bg.config(cursor="hand2")
    id_text.configure(cursor="hand2")

def id_sort_leave(event):
    id_sort_bg.itemconfig(id_butt, fill='#2363C6') 
    id_text.config(bg='#2363C6', fg='white') 
    id_sort_bg.config(cursor="")

def sort_id():
    if not hasattr(display_students, 'original_students'):
        display_students.original_students = load_students()
    
    if not hasattr(sort_id, 'reverse'):
        sort_id.reverse = False
    sort_id.reverse = not sort_id.reverse

    def parse_id(id_str):
        try:
            year, number = map(int, id_str.split("-")) 
            return (year, number)
        except ValueError:
            return (float('inf'), float('inf')) 

    students_to_sort = display_students.current_students.copy() if len(display_students.current_students) < len(display_students.original_students) else display_students.original_students.copy()
    students_to_sort.sort(key=lambda x: parse_id(x[0]), reverse=sort_id.reverse)

    display_students.current_students = students_to_sort
    display_students(0)
    id_text.configure(text="Descending" if sort_id.reverse else "Ascending")

def sort_name():
    if not hasattr(display_students, 'original_students'):
        display_students.original_students = load_students()

    if not hasattr(sort_name, 'reverse'):
        sort_name.reverse = False
    sort_name.reverse = not sort_name.reverse

    if len(display_students.current_students) < len(display_students.original_students):
        students_to_sort = display_students.current_students.copy()
    else:
        students_to_sort = display_students.original_students.copy()

    students_to_sort.sort(key=lambda x: x[1].strip().casefold(), reverse=sort_name.reverse)

    display_students.current_students = students_to_sort
    display_students(0)
    sort_text.configure(text="Descending" if sort_name.reverse else "Ascending")

# Create the button when module is imported
create_sort_button()