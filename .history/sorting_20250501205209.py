from tkinter import *
from misc import create_rounded_rectangle
from header import top

# Declare the sort_img variable at module level
sort_img = None

def sort():
    global sort_img  # Use a properly named global variable
    
    sort_canvas = Canvas(top, width=40, height=40, highlightthickness=0, bd=0, bg="white")
    sort_canvas.grid(row=0, column=1, padx=(0, 70), pady=0, sticky="e")
    sort_frame = create_rounded_rectangle(sort_canvas, 4, 7, 35, 35, radius=20, fill="white") 
    
    # Load the image and store it in the global variable
    sort_img = PhotoImage(file="Images/sort.png")
    sort_canvas.create_image(20, 16, image=sort_img, anchor="center") 


    sort_canvas.tag_bind(sort_frame, "<Button-1>", lambda event: sort_clicked(event))

    return sort_canvas

def sort_clicked(event):
    print("Sort button clicked")

def sort_func(event, body_frame):
    # Implement the sorting functionality here
    pass