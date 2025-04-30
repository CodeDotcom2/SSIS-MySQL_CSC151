from tkinter import *
from form import toggle_form_visibility
from mySQL import add_student

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


def submit_form():
    id_no = id_no.get()
    last_name = last_name.get()
    first_name = first_name.get()
    gender = gender_dropdown.get()
    year_level = year_dropdown.get()
    college_id = college_dropdown.get()  # Make sure this is the actual ID
    program_id = program_dropdown.get()  # Same here

    add_student(id_no, last_name, first_name, gender, year_level, college_id, program_id)
