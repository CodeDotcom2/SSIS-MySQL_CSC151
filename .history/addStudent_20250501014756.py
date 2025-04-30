from tkinter import *
from studentForm import create_form

def on_add_button_click(event=None, body_frame=None):
    if body_frame is None:
        return
    form_canvas = create_form(body_frame, body_frame=body_frame)
    form_canvas.place(x=0, y=0)