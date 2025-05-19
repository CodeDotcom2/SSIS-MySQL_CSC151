from tkinter import *
from tkinter import ttk
from misc import create_rounded_rectangle
from header import top

# Declare global variables
sort_img = None
sort_canvas = None
sort_frame = None
sorting_window = None  # For the popup window

def create_sort_button():
    global sort_img, sort_canvas, sort_frame
    
    # Create canvas
    sort_canvas = Canvas(top, width=30, height=30, highlightthickness=0, bd=0, bg="white")
    sort_canvas.grid(row=0, column=1, padx=(0, 70), pady=(10, 0), sticky="ne")
    
    # Create rounded rectangle background
    sort_frame = create_rounded_rectangle(sort_canvas, 0, 0, 30, 30, radius=20, fill="white") 
    
    # Load the image (make sure the path is correct)
    try:
        sort_img = PhotoImage(file="Images/sort.png")
        sort_canvas.create_image(15, 15, image=sort_img, anchor="center")
    except:
        # Fallback if image fails to load
        sort_canvas.create_text(15, 15, text="Sort", font=("Arial", 8), fill="black")

    # Bind events
    sort_canvas.tag_bind(sort_frame, "<Enter>", on_enter)
    sort_canvas.tag_bind(sort_frame, "<Leave>", on_leave)
    sort_canvas.tag_bind(sort_frame, "<Button-1>", sort_clicked)
    
    # Also bind to the canvas itself
    sort_canvas.bind("<Enter>", on_enter)
    sort_canvas.bind("<Leave>", on_leave)
    sort_canvas.bind("<Button-1>", sort_clicked)
    sort_canvas.bind("<ButtonRelease-1>", sort_click_release)

    return sort_canvas

def on_enter(event):
    sort_canvas.itemconfig(sort_frame, fill="#f0f0f0")  # Light gray hover color
    sort_canvas.config(cursor="hand2")

def on_leave(event):
    sort_canvas.itemconfig(sort_frame, fill="white")
    sort_canvas.config(cursor="")

def sort_clicked(event):
    sort_canvas.itemconfig(sort_frame, fill="#d0d0d0")  # Slightly darker when clicked

def sort_click_release(event):
    global sorting_window
    
    # Reset button color
    sort_canvas.itemconfig(sort_frame, fill="#f0f0f0")
    
    # Create the sorting options popup
    create_sorting_window()

def create_sorting_window():
    global sorting_window
    
    # Remove existing window if it exists
    if sorting_window:
        sorting_window.destroy()
    
    # Create new window
    sorting_window = Canvas(top, width=120, height=150, bg="white", highlightthickness=0, bd=0)
    sorting_window.grid(row=0, column=1, padx=(0, 70), pady=(50, 0), sticky="ne")
    
    # Create rounded rectangle background
    sorting_frame = create_rounded_rectangle(sorting_window, 0, 0, 120, 150, radius=20, fill="#f5f5f5")
    
    # Sort by label
    sort_by = Label(sorting_window, text="Sort By:", font=("Arial", 10, "bold"), bg="#f5f5f5", fg="#2363C6")
    sorting_window.create_window(60, 20, window=sort_by)

    # Name sort option
    name_sort_bg = Canvas(sorting_window, width=100, height=30, bg="#f5f5f5", highlightthickness=0, bd=0)
    sorting_window.create_window(60, 60, window=name_sort_bg)
    
    name_button = create_rounded_rectangle(name_sort_bg, 0, 0, 100, 30, radius=15, fill="#2363C6")
    name_text = Label(name_sort_bg, text="Name", font=("Arial", 10, "bold"), bg="#2363C6", fg="white")
    name_text.place(relx=0.5, rely=0.5, anchor=CENTER)

    # ID sort option
    id_sort_bg = Canvas(sorting_window, width=100, height=30, bg="#f5f5f5", highlightthickness=0, bd=0)
    sorting_window.create_window(60, 110, window=id_sort_bg)
    
    id_button = create_rounded_rectangle(id_sort_bg, 0, 0, 100, 30, radius=15, fill="#2363C6")
    id_text = Label(id_sort_bg, text="ID", font=("Arial", 10, "bold"), bg="#2363C6", fg="white")
    id_text.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Bind click events to close the window when clicking outside
    sorting_window.bind("<Button-1>", lambda e: sorting_window.destroy())
    name_sort_bg.bind("<Button-1>", lambda e: None)  # Prevent propagation
    id_sort_bg.bind("<Button-1>", lambda e: None)  # Prevent propagation

