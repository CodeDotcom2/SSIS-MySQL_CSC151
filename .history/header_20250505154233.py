from tkinter import *
from tkinter import ttk
from misc import remove_focus, create_rounded_rectangle
from sorting import sort_function
import search

top = None
x1, y1 = 0, 0
sort_img = None  # Global variable to store the sort image

def header(root):
    global search_frame, icon_label, text_label, search_var, cancel, search_bar
    global icon1,icon2, text_image, cancel_butt, search_field_var, search_field_combo,sort_button
    global top, sort_img, search_canvas

    top = Frame(root, bg="white", height=60)
    top.grid(row=0, column=0, sticky="nsew", columnspan=2)
    top.rowconfigure(0, weight=0)
    top.columnconfigure(0, weight=0)
    top.columnconfigure(1, weight=1)
    top.grid_propagate(False)

    text_stud = Label(top, text="Student Information", font=('Albert Sans', 15, 'bold'), bg='white')
    text_stud.grid(row=0, column=0, padx=20)
    text_stud.bind("<Button-1>", remove_focus)


    search_frame = Frame(top, bg="white")
    search_frame.grid(row=0, column=1, sticky="nsew", padx=(50, 10), pady=5)
    search_frame.columnconfigure(0, weight=0)

    # Create dropdown to select search field
    search_field_var = StringVar()
    search_fields = search.get_search_fields()
    search_field_var.set("all")  # Default to search all

    search_field_combo = ttk.Combobox(top,
                                       textvariable=search_field_var,
                                       values=list(search_fields.values()),
                                       width=15,
                                       state="readonly",
                                       font=('Albert Sans', 10))
    search_field_combo.current(0)
    search_field_combo.grid(row=0, column=2, padx=15, pady=15, sticky="nw")
    search_field_combo.bind("<<ComboboxSelected>>", on_field_change)

    # Combobox style
    style = ttk.Style()
    style.configure('TCombobox',
                    background='#F1F3F8',
                    fieldbackground='#F1F3F8',
                    foreground='black')

    # Search entry setup
    search_var = StringVar()
    search_var.trace_add("write", on_input_change)

    search_canvas = Canvas(search_frame, bg="white",width= 400, height=30, bd=0, highlightthickness=0)
    search_canvas.grid(row=0, column=1, pady=5, padx=0,sticky="ew")

    search_bar = Entry(search_canvas, textvariable=search_var, bg="#F1F3F8",
                       font=('Albert Sans', 10, 'normal'), fg="gray",
                       borderwidth=0, highlightthickness=0)

    # Save reference to the Entry widget window in canvas
    search_canvas.search_bar_window = search_canvas.create_window(10, 16, anchor="w", window=search_bar, width=350, height=25)
    search_canvas.radius = 20  # Save radius for redraw
    create_rounded_rectangle(search_canvas, 0, 0, 500, 30, radius=20, fill='#F1F3F8', outline="#E4EBF5", tag="rounded_bg")

    def resize_search_bar(event):
        width = event.width
        search_canvas.delete("rounded_bg")
        create_rounded_rectangle(search_canvas, 0, 0, width, 30, radius=search_canvas.radius,
                                 fill='#F1F3F8', outline="#E4EBF5", tag="rounded_bg")
        search_canvas.coords(search_canvas.search_bar_window, 10, 16)
        search_canvas.itemconfig(search_canvas.search_bar_window, width=width - 20)

    search_canvas.bind("<Configure>", resize_search_bar)

    # Search icon and placeholder text
    icon1 = PhotoImage(file="Images/SearchIcon.png")
    icon_label = Label(search_bar, image=icon1, bg="#F1F3F8", bd=0)
    icon_label.place(x=2, y=3)

    text_image = PhotoImage(file="Images/Search In Here.png")
    text_label = Label(search_bar, image=text_image, bg="#F1F3F8", bd=0)
    text_label.place(x=24, y=6)

    cancel = PhotoImage(file='Images/cancel.png')
    cancel_butt = Button(search_bar, image=cancel, bg="#F1F3F8", bd=0,
                         cursor="hand2", command=delete_entry)

    # Sort button
    sort_canvas = Canvas(top, bg="white",width=30, height=30,borderwidth=0, highlightthickness=0)
    sort_canvas.grid(row=0, column=3, padx=(0, 50), pady=2, sticky="e")

    sort = create_rounded_rectangle(sort_canvas,0, 0, 30, 30,radius=20, fill="white")
    icon2 = PhotoImage(file="Images/Sort.png")
    sort_img = sort_canvas.create_image(15, 15, image=icon2, anchor="center")

    sort_canvas.bind("<Button-1>", sort_clicked)


    def on_sort_hover(event):
        sort_canvas.itemconfig(sort,fill="lightblue")
        
    def on_sort_leave(event):
        sort_canvas.itemconfig(sort,fill="white")

    # Bindings
    search_bar.bind("<FocusIn>", clear_placeholder)
    search_bar.bind("<FocusOut>", restore_placeholder)
    icon_label.bind("<Button-1>", clear_placeholder)
    text_label.bind("<Button-1>", clear_placeholder)
    sort_canvas.bind("<Enter>", on_sort_hover)
    sort_canvas.bind("<Leave>", on_sort_leave)

    top.bind("<Button-1>", remove_focus)

    setup_search_connection()

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
    field_key = "all"
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
    return "all"

def setup_search_connection():
    pass

def sort_clicked(event):
    print("Sort button clicked")
    sort_function(top)
