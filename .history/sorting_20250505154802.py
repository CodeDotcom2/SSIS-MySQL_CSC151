from tkinter import *
from misc import create_rounded_rectangle

sort_window = None

def sort_function(root):
    if body_frame is None:
        from body import body
        body_frame = body(root)
    form_frame = Canvas(body_frame, bg="white", width=350, height=480, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(form_frame, -800, 0, 350, 480, radius=130, fill='lightgray')
    
    print("Sorting function called")