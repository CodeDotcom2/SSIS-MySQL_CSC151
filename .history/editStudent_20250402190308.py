from tkinter import *
from form import toggle_form_visibility,update_form_text

form_frame = None
side_bar = None

def set_form_frame(frame, side_bar_canvas):
    global form_frame, side_bar
    form_frame = frame
    side_bar = side_bar_canvas

def edit_stud(event=None):
    global form_frame, side_bar
    toggle_form_visibility(form_frame, side_bar)

    update_form_text(form_frame,'title',"Edit Student")
    submit_canvas = form_frame.text_elements['submit_canvas']
    submit_text = form_frame.text_elements['submit_text']
    submit_canvas.itemconfig(submit_text, text="Update")

    

    print("Editing student")