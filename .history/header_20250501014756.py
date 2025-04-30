from tkinter import *
from misc import remove_focus,create_rounded_rectangle

top = None

def header(root):
    global search_frame,icon_label,text_label, search_var,cancel,search_bar
    global icon1,text_image,cancel_butt
    top = Frame(root,bg="white",height=60)
    top.grid(row=0, column=0, sticky="nsew",columnspan=2)
    top.rowconfigure(0, weight=0)
    top.columnconfigure(0, weight=0)
    top.columnconfigure(1, weight=1)
    top.grid_propagate(False)

    text_stud = Label(top, text="Student Information", font=('Albert Sans', 15, 'bold'), bg='white')
    text_stud.grid(row=0, column=0, padx=20)
    text_stud.bind("<Button-1>",remove_focus)

    search_var = StringVar()
    search_var.trace_add("write", on_input_change)

    search_frame = Canvas(top, bg="white", height=40, bd=0, highlightthickness=0)
    search_frame.grid(row=0, column=1, sticky="nsew", padx=(50, 120), pady=5)

    search_bar = Entry(top, textvariable=search_var, bg="#F1F3F8", font=('Albert Sans', 10, 'normal'), fg="gray", borderwidth=0, highlightthickness=0)
    search_bar.grid(row=0,column=0,padx=0)
    icon1 = PhotoImage(file="Images/SearchIcon.png")
    icon_label = Label(search_bar, image=icon1, bg="#F1F3F8", bd=0)
    text_image = PhotoImage(file="Images/Search In Here.png")
    text_label = Label(search_bar, image=text_image, bg="#F1F3F8", bd=0)

    cancel = PhotoImage(file='Images/cancel.png')
    cancel_butt = Button(search_bar,image=cancel,bg="#F1F3F8", bd=0,cursor="hand2",command=delete_entry)
    

    search_frame.bind("<Configure>", on_resize)
    search_bar.bind("<FocusIn>", clear_placeholder)
    search_bar.bind("<FocusOut>", restore_placeholder)
    icon_label.bind("<Button-1>",clear_placeholder)
    text_label.bind("<Button-1>",clear_placeholder)
    top.bind("<Button-1>",remove_focus)


def clear_placeholder(event=None):
    if search_var.get() == "":
        icon_label.place_forget()
        text_label.place_forget()
    search_bar.focus_set()
def restore_placeholder(event=None):
    if search_var.get() == "":
        icon_label.place(x=x1 + -7, y=y1 + -3)
        text_label.place(x=x1 + 15, y=y1 + 1)
def on_resize(event):
    global x1,y1
    search_frame.delete("all")
    margin = 6
    radius = 20
    canvas_width = search_frame.winfo_width()
    canvas_height = search_frame.winfo_height()

    x1 = margin
    y1 = margin
    x2 = canvas_width - margin
    y2 = canvas_height - margin

    create_rounded_rectangle(search_frame, x1, y1, x2, y2, radius=radius, fill='#F1F3F8', outline="#E4EBF5")
    
    search_frame.create_window(x1 + 5, y1 + 3, anchor="nw", window=search_bar, width=x2 - x1 - 10, height=y2 - y1 - 4)

    icon_label.place(x=x1 + -7, y=y1 + -3)
    text_label.place(x=x1 + 15, y=y1 + 1)
    search_var.set("")
    cancel_butt.pack_forget()

def on_input_change(*args):
    if search_var.get():
        cancel_butt.lift()
        cancel_butt.pack(side="right", padx=2)
    else:
        cancel_butt.pack_forget()
    filter_students()

def delete_entry():
    search_var.set("")
    search_bar.focus_set()
    cancel_butt.pack_forget()

def filter_students():
    try:
        from body import refresh_students
        refresh_students()
    except ImportError:
        pass  
def get_search_term():
    return search_var.get()

def setup_search_connection():
    try:
        from body import set_search_function
        set_search_function(get_search_term)
        search_var.trace_add("write", lambda *args: filter_students())
    except ImportError:
        pass  # Handle first-time import