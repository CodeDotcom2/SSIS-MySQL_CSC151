from tkinter import *
from tkinter import messagebox
from studentForm import create_form
from body import get_selected_student_data

def edit_stud(event=None, body_frame=None):
    if body_frame is None:
        return
    
    # Get the selected student data
    student_data = get_selected_student_data()
    
    if not student_data:
        messagebox.showwarning("No Selection", "Please select a student to edit")
        return
    
    # Create the form in edit mode with the selected student data
    form_frame = create_form(body_frame, body_frame=body_frame, mode="edit", student_data=student_data)
    form_frame.text_elements['title'].config(text="Edit Student")
    form_frame.place(x=0, y=0)