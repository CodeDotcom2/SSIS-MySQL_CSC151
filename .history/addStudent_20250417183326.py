from tkinter import *
from form import toggle_form_visibility


form_frame = None
side_bar = None

def set_form_frame(frame, side_bar_canvas):
    global form_frame, side_bar
    form_frame = frame
    side_bar = side_bar_canvas

def on_add_button_click(event=None):
    global form_frame, side_bar
    print("Button Clicked")
    
    if form_frame is None:
        print("Error: form_frame is not initialized")
        return

    toggle_form_visibility(form_frame, side_bar)

