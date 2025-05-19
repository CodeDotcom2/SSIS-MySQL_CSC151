from tkinter import *
from programForm import view_programs_form

def programs_func(event=None,body_frame=None):
    if body_frame is None:
        return
    form_frame3 = view_programs_form(body_frame, body_frame=body_frame)
    form_frame3.place(x=0, y=0) 
