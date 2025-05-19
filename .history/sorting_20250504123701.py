from tkinter import *
from misc import create_rounded_rectangle
from body import body_frame

sort_window = None

def sort_clicked(root):
    global sort_window, body_frame
    
    # Get reference to body_frame if not already available
    if body_frame is None:
        from body import body
        body_frame = body(root)
    
    # Remove existing window if it exists
    if sort_window:
        sort_window.destroy()
    
    # Create new sorting window in body area
    sort_window = Canvas(body_frame, width=350, height=200, bg="white", highlightthickness=0, bd=0)
    sort_window.place(x=800, y=70)  # Position similar to student form
    
    # Rounded rectangle background
    sorting_frame = create_rounded_rectangle(sort_window, 0, 0, 350, 200, radius=20, fill="lightgray")
    
    # Title
    title_label = Label(sort_window, text="Sort By", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    sort_window.create_window(175, 30, window=title_label)

    # Name sort option
    name_sort_bg = Canvas(sort_window, width=300, height=40, bg="lightgray", highlightthickness=0, bd=0)
    sort_window.create_window(175, 90, window=name_sort_bg)
    
    name_button = create_rounded_rectangle(name_sort_bg, 0, 0, 300, 40, radius=15, fill="#2363C6")
    name_text = Label(name_sort_bg, text="Name", font=("Arial", 15, "bold"), bg="#2363C6", fg="white")
    name_text.place(relx=0.5, rely=0.5, anchor=CENTER)

    # ID sort option
    id_sort_bg = Canvas(sort_window, width=300, height=40, bg="lightgray", highlightthickness=0, bd=0)
    sort_window.create_window(175, 150, window=id_sort_bg)
    
    id_button = create_rounded_rectangle(id_sort_bg, 0, 0, 300, 40, radius=15, fill="#2363C6")
    id_text = Label(id_sort_bg, text="ID", font=("Arial", 15, "bold"), bg="#2363C6", fg="white")
    id_text.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Bind click events
    def close_window(e):
        sort_window.destroy()
    
    def sort_by_name(e):
        print("Sorting by name")
        sort_window.destroy()
    
    def sort_by_id(e):
        print("Sorting by ID")
        sort_window.destroy()

    sort_window.bind("<Button-1>", close_window)
    name_sort_bg.bind("<Button-1>", sort_by_name)
    name_text.bind("<Button-1>", sort_by_name)
    id_sort_bg.bind("<Button-1>", sort_by_id)
    id_text.bind("<Button-1>", sort_by_id)

    # Hover effects
    def name_hover(e):
        name_sort_bg.itemconfig(name_button, fill="#1A4A99")
        name_sort_bg.config(cursor="hand2")
    
    def name_leave(e):
        name_sort_bg.itemconfig(name_button, fill="#2363C6")
        name_sort_bg.config(cursor="")
    
    def id_hover(e):
        id_sort_bg.itemconfig(id_button, fill="#1A4A99")
        id_sort_bg.config(cursor="hand2")
    
    def id_leave(e):
        id_sort_bg.itemconfig(id_button, fill="#2363C6")
        id_sort_bg.config(cursor="")

    name_sort_bg.bind("<Enter>", name_hover)
    name_sort_bg.bind("<Leave>", name_leave)
    name_text.bind("<Enter>", name_hover)
    name_text.bind("<Leave>", name_leave)

    id_sort_bg.bind("<Enter>", id_hover)
    id_sort_bg.bind("<Leave>", id_leave)
    id_text.bind("<Enter>", id_hover)
    id_text.bind("<Leave>", id_leave)