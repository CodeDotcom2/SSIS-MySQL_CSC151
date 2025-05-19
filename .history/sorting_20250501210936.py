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
    sort_canvas = Canvas(top, width=30, height=30, highlightthickness=0, bd=0, bg="red")
    sort_canvas.grid(row=0, column=1, padx=(0, 70), pady=0, sticky="e")
    
    # Create rounded rectangle background
    sort_frame = create_rounded_rectangle(sort_canvas, 0, -20, 30, 30, radius=20, fill="white") 
    
    # Load the image
    sort_img = PhotoImage(file="Images/sort.png")
    sort_canvas.create_image(15, 10, image=sort_img, anchor="center") 

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
    global sort_frame, sort_canvas
    sort_canvas.itemconfig(sort_frame, fill="#A5CAEC")

def on_leave(event):
    global sort_frame, sort_canvas
    sort_canvas.itemconfig(sort_frame, fill="white")

def sort_clicked(event):

    print("Sort button clicked")
