from tkinter import *
from misc import create_rounded_rectangle

def set_form_frame(parent):
    # Clear any existing widgets in the parent frame
    for widget in parent.winfo_children():
        widget.destroy()

    # Create the college frame
    college_frame = Canvas(parent, bg="white", width=350, height=480, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(college_frame, -300, 0, 350, 480, radius=130, fill='lightgray')
    college_frame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nw")

    # Title
    title_label = Label(parent, text="College Form", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    college_frame.create_window(160, 30, window=title_label)

def colleges_func(parent):
    set_form_frame(parent)
    print("COLLEGES")