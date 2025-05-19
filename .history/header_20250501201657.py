from tkinter import *
from tkinter import ttk
from misc import remove_focus, create_rounded_rectangle
import search

top = None
x1, y1 = 0, 0
sort_img = None  # Global variable to store the sort image

def header(root):
    global search_frame, icon_label, text_label, search_var, cancel, search_bar
    global icon1, text_image, cancel_butt, search_field_var, search_field_combo
    global top, sort_img
    
    top = Frame(root, bg="violet", height=60)
    top.grid(row=0, column=0, sticky="nsew", columnspan=2)
    top.rowconfigure(0, weight=0)
    top.columnconfigure(0, weight=0)
    top.columnconfigure(1, weight=1)
    top.grid_propagate(False)

    text_stud = Label(top, text="Student Information", font=('Albert Sans', 15, 'bold'), bg='white')
    text_stud.grid(row=0, column=0, padx=20)
    text_stud.bind("<Button-1>", remove_focus)

    # Search field dropdown
    search_frame = Frame(top, bg="red")
    search_frame.grid(row=0, column=1, sticky="nsew", padx=(50, 120), pady=5)
    search_frame.columnconfigure(0, weight=0)
    search_frame.columnconfigure(1, weight=1)

    # Create dropdown to select search field
    search_field_var = StringVar()
    search_fields = search.get_search_fields()
    search_field_var.set("all")  # Default to search all
    
    search_field_combo = ttk.Combobox(search_frame, 
                                     textvariable=search_field_var,
                                     values=list(search_fields.values()),
                                     width=15,
                                     state="readonly",
                                     font=('Albert Sans', 10))
    search_field_combo.current(0)
    search_field_combo.grid(row=0, column=2, padx=0, pady=5)
    search_field_combo.bind("<<ComboboxSelected>>", on_field_change)

    # Create a style for the combobox
    style = ttk.Style()
    style.configure('TCombobox', 
                   background='#F1F3F8',
                   fieldbackground='#F1F3F8',
                   foreground='black')

    # Search text entry
    search_var = StringVar()
    search_var.trace_add("write", on_input_change)

    search_canvas = Canvas(search_frame, bg="white", height=30, bd=0, highlightthickness=0)
    search_canvas.grid(row=0, column=1, sticky="nsew", pady=5,padx=(0, 100))

    # Create the rounded rectangle on the canvas
    radius = 15
    create_rounded_rectangle(search_canvas, 2, 2, 550, 30, radius=radius, fill='blue', outline="#E4EBF5")

    # Place the entry widget on the canvas
    search_bar = Entry(search_canvas, textvariable=search_var, bg="#F1F3F8", 
                     font=('Albert Sans', 10, 'normal'), fg="gray", 
                     borderwidth=0, highlightthickness=0)
    search_canvas.create_window(10, 16, anchor="w", window=search_bar, width=270, height=25)

    # Search icon and placeholder text
    icon1 = PhotoImage(file="Images/SearchIcon.png")
    icon_label = Label(search_bar, image=icon1, bg="#F1F3F8", bd=0)
    icon_label.place(x=2, y=0)

    text_image = PhotoImage(file="Images/Search In Here.png")
    text_label = Label(search_bar, image=text_image, bg="#F1F3F8", bd=0) 
    text_label.place(x=24, y=3)

    # Cancel/clear button
    cancel = PhotoImage(file='Images/cancel.png')
    cancel_butt = Button(search_bar, image=cancel, bg="#F1F3F8", bd=0, 
                         cursor="hand2", command=delete_entry)
    
    # Add sort button
    sort_canvas = Canvas(top, width=40, height=40, highlightthickness=0, bd=0, bg="white")
    sort_canvas.grid(row=0, column=1, padx=(0, 70), pady=0, sticky="e")
    sort_frame = create_rounded_rectangle(sort_canvas, 4, 7, 35, 35, radius=20, fill="white") 
    
    # Load the image and store it in the global variable
    sort_img = PhotoImage(file="Images/sort.png")
    sort_canvas.create_image(20, 16, image=sort_img, anchor="center")
    
    # Bindings
    search_bar.bind("<FocusIn>", clear_placeholder)
    search_bar.bind("<FocusOut>", restore_placeholder)
    icon_label.bind("<Button-1>", clear_placeholder)
    text_label.bind("<Button-1>", clear_placeholder)
    top.bind("<Button-1>", remove_focus)

    setup_search_connection()

# Rest of the header.py code remains the same
def clear_placeholder(event=None):
    if search_var.get() == "":
        icon_label.place_forget()
        text_label.place_forget()
    search_bar.focus_set()

def restore_placeholder(event=None):
    if search_var.get() == "":
        icon_label.place(x=2, y=0)
        text_label.place(x=24, y=3)

def on_input_change(*args):
    if search_var.get():
        cancel_butt.lift()
        cancel_butt.pack(side="right", padx=2)
    else:
        cancel_butt.pack_forget()
    filter_students()

def on_field_change(event=None):
    field_display = search_field_var.get()
    field_key = "all"  # Default
    
    for key, value in search.get_search_fields().items():
        if value == field_display:
            field_key = key
            break
    
    search.set_search_field(field_key)

def delete_entry():
    search_var.set("")
    search_bar.focus_set()
    cancel_butt.pack_forget()
    filter_students()

def filter_students():
    search.set_search_text(search_var.get())

def get_search_term():
    return search_var.get()

def get_search_field():
    field_display = search_field_var.get()
    
    for key, value in search.get_search_fields().items():
        if value == field_display:
            return key
    
    return "all"  # Default

def setup_search_connection():
    pass