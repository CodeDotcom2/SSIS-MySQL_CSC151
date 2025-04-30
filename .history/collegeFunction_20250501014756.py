from tkinter import *
from collegeForm import college_form

def colleges_func(event=None,body_frame=None):
    if body_frame is None:
        return
    form_frame2 = college_form(body_frame, body_frame=body_frame)
    form_frame2.place(x=0, y=0) 
