from tkinter import *
from header import header
from sorting import sort
from side import side 
from body import body
from misc import set_root
from form import create_form
from addStudent import set_form_frame as add_set_form_frame
from editStudent import set_form_frame as edit_set_form_frame
from collegeFunction import set_form_frame as college_set_form_frame

root = Tk()
root.geometry("1100x605")
root.minsize(510, 500)
root.title(" ")
icon = PhotoImage(file="Images/icon.png")
root.iconphoto(True, icon)
root.configure(bg="red")
root.rowconfigure(1, weight=1)
root.columnconfigure(0, minsize=220)
root.columnconfigure(1, weight=1)

set_root(root)

header(root)
side_frame, side_bar_canvas = side(root)
body_frame = body(root)
sort()
form_frame = create_form(root, body_frame)
form_frame.grid_remove() 


add_set_form_frame(form_frame, side_bar_canvas)
edit_set_form_frame(form_frame, side_bar_canvas)
college_set_form_frame(form_frame, side_bar_canvas)


root.mainloop()