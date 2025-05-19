from tkinter import *
from misc import create_rounded_rectangle
from header import top

# Declare global variables
sort_img = None
sort_canvas = None
sort_frame = None

def create_sort_button():
    global sort_img, sort_canvas, sort_frame
    
    # Create canvas
    sort_canvas = Canvas(top, width=40, height=40, highlightthickness=0, bd=0, bg="white")
    sort_canvas.grid(row=0, column=1, padx=(0, 70), pady=0, sticky="e")
    
    # Create rounded rectangle background
    sort_frame = create_rounded_rectangle(sort_canvas, 4, 2, 35, 32, radius=20, fill="red") 
    
    # Load the image
    sort_img = PhotoImage(file="Images/sort.png")
    sort_canvas.create_image(20, 16, image=sort_img, anchor="center") 

    # Bind events
    sort_canvas.tag_bind(sort_frame, "<Enter>", on_enter)
    sort_canvas.tag_bind(sort_frame, "<Leave>", on_leave)
    sort_canvas.tag_bind(sort_frame, "<Button-1>", sort_clicked)
    
    # Also bind to the canvas itself
    sort_canvas.bind("<Enter>", on_enter)
    sort_canvas.bind("<Leave>", on_leave)
    sort_canvas.bind("<Button-1>", sort_clicked)

    return sort_canvas

def on_enter(event):
    """Change color when mouse enters the button"""
    global sort_frame, sort_canvas
    sort_canvas.itemconfig(sort_frame, fill="#A5CAEC")

def on_leave(event):
    """Revert color when mouse leaves the button"""
    global sort_frame, sort_canvas
    sort_canvas.itemconfig(sort_frame, fill="white")

def sort_clicked(event):
    """Handle button click"""
    print("Sort button clicked")
    # You can add visual feedback here if needed
    # For example, briefly change the color when clicked

def sort_func(body_frame):
    """Implement the sorting functionality here"""
    pass