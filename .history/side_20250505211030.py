from tkinter import *
from misc import create_rounded_rectangle,remove_focus,setup_table_deselection
from addStudent import on_add_button_click
from deleteStudent import delete_stud
from editStudent import edit_stud
from collegeFunction import colleges_func
from programFunction import programs_func
from body import student_table

def create_button_hover_effects(button, text, hover_fill='#A5CAEC', hover_text_color='#154BA6', 
                             default_fill='#2363C6',add_fill="white", default_text_color='white', 
                             clicked_fill='#1A4A99', clicked_text_color='white'):
    def on_hover(event):
        side_bar_canvas.itemconfig(button, fill=hover_fill)  
        side_bar_canvas.itemconfig(text, fill=hover_text_color) 
        side_bar_canvas.config(cursor="hand2")
    
    def on_leave(event):
        button_text = side_bar_canvas.itemcget(text, "text")
        side_bar_canvas.itemconfig(button, fill='white' if button_text == "Add Student" else default_fill)
        side_bar_canvas.itemconfig(text, fill='#2363C6' if button_text == "Add Student" else default_text_color)
        side_bar_canvas.config(cursor="")
    
    def on_click(event):
        side_bar_canvas.itemconfig(button, fill=clicked_fill)
        side_bar_canvas.itemconfig(text, fill=clicked_text_color)

    def on_release(event, click_func):
        button_text = side_bar_canvas.itemcget(text, "text")
        side_bar_canvas.itemconfig(button, fill=add_fill if button_text == "Add Student" else hover_fill)
        side_bar_canvas.itemconfig(text, fill= "#2363C6" if button_text == "Add Student" else hover_text_color) 
        click_func(event)  
    
    return on_hover, on_leave, on_click, on_release

def bind_button_events(button, icon, text, click_func):
    on_hover, on_leave, on_click, on_release = create_button_hover_effects(button, text)
    
    for tag in [button, text, icon]:
        if tag:
            side_bar_canvas.tag_bind(tag, "<Enter>", on_hover)
            side_bar_canvas.tag_bind(tag, "<Leave>", on_leave)
            side_bar_canvas.tag_bind(tag, "<Button-1>", on_click)  
            side_bar_canvas.tag_bind(tag, "<ButtonRelease-1>", lambda event, func=click_func: on_release(event, func))

def side_buttons(body_frame):
    global side_bar_canvas, side_frame
    global add_button, add_text, edit_button, edit_text, delete_button, delete_text, colleges_button, colleges_text, programs_button, programs_text
    global edit_icon_img, delete_icon_img, colleges_icon_img, programs_icon_img, delete_icon, edit_icon, colleges_icon, programs_icon
    global icon_images
    
    icon_images = []

    side_bar_canvas.delete("all")
    canvas_width = side_bar_canvas.winfo_width()
    canvas_height = side_bar_canvas.winfo_height()

    side_frame = create_rounded_rectangle(side_bar_canvas, -200, 0, canvas_width, canvas_height + 50, radius=130, fill="#2363C6")
    side_bar_canvas.tag_bind(side_frame,"<Button-1>",remove_focus)
    
    add_width, add_height = 160, 35
    edit_width, edit_height = 160, 25
    delete_width, delete_height = 160, 25
    colleges_width, colleges_height = 160, 25
    programs_width, programs_height = 160, 25

    add_to_edit_spacing = 15
    edit_to_delete_spacing = 2
    delete_to_colleges_spacing = 2
    colleges_to_programs_spacing = 2

    offset_x = 0  
    icon_text_spacing = 4  

    # Add Student Button 
    add_x1 = (canvas_width - add_width) // 2
    add_y1 = 35
    add_x2 = add_x1 + add_width
    add_y2 = add_y1 + add_height

    add_button = create_rounded_rectangle(side_bar_canvas, add_x1, add_y1, add_x2, add_y2, radius=20, fill="white")
    add_text = side_bar_canvas.create_text((add_x1 + add_x2) // 2, (add_y1 + add_y2) // 2,
                                           text="Add Student", fill="#2363C6", font=('Albert Sans', 13, 'bold'))

    # Delete Student Button
    delete_x1 = ((canvas_width - delete_width) // 2) + offset_x
    delete_y1 = add_y2 + add_to_edit_spacing 
    delete_x2 = delete_x1 + delete_width
    delete_y2 = delete_y1 + delete_height

    delete_button = create_rounded_rectangle(side_bar_canvas, delete_x1, delete_y1, delete_x2, delete_y2, radius=20, fill="#2363C6")

    delete_icon_img = PhotoImage(file="Images/Trash.png")
    icon_images.append(delete_icon_img)
    delete_icon_x = delete_x1 + 8  
    delete_icon_y = (delete_y1 + delete_y2) // 2
    delete_icon = side_bar_canvas.create_image(delete_icon_x, delete_icon_y, anchor="w", image=delete_icon_img)

    delete_text_x = delete_icon_x + delete_icon_img.width() + icon_text_spacing
    delete_text = side_bar_canvas.create_text(delete_text_x, delete_icon_y, text="Delete Student", fill="white",
                                              font=('Albert Sans', 11, 'normal'), anchor="w")

    # Edit Student Button
    edit_x1 = ((canvas_width - edit_width) // 2) + offset_x
    edit_y1 = delete_y2 + edit_to_delete_spacing  
    edit_x2 = edit_x1 + edit_width
    edit_y2 = edit_y1 + edit_height

    edit_button = create_rounded_rectangle(side_bar_canvas, edit_x1, edit_y1, edit_x2, edit_y2, radius=20, fill="#2363C6")

    edit_icon_img = PhotoImage(file="Images/edit.png")
    icon_images.append(edit_icon_img)
    edit_icon_x = edit_x1 + 10  # Left inside button
    edit_icon_y = (edit_y1 + edit_y2) // 2
    edit_icon = side_bar_canvas.create_image(edit_icon_x, edit_icon_y, anchor="w", image=edit_icon_img)

    edit_text_x = edit_icon_x + edit_icon_img.width() + icon_text_spacing
    edit_text = side_bar_canvas.create_text(edit_text_x, edit_icon_y, text="Edit Student", fill="white",
                                            font=('Albert Sans', 11, 'normal'), anchor="w")

    # Colleges Button
    colleges_x1 = ((canvas_width - colleges_width) // 2) + offset_x
    colleges_y1 = edit_y2 + delete_to_colleges_spacing
    colleges_x2 = colleges_x1 + colleges_width
    colleges_y2 = colleges_y1 + colleges_height

    colleges_button = create_rounded_rectangle(side_bar_canvas, colleges_x1, colleges_y1, colleges_x2, colleges_y2, radius=20, fill="#2363C6")

    colleges_icon_img = PhotoImage(file="Images/college.png") 
    icon_images.append(colleges_icon_img)
    colleges_icon_x = colleges_x1 + 8
    colleges_icon_y = (colleges_y1 + colleges_y2) // 2
    colleges_icon = side_bar_canvas.create_image(colleges_icon_x, colleges_icon_y, anchor="w", image=colleges_icon_img)

    colleges_text_x = colleges_icon_x + colleges_icon_img.width() + icon_text_spacing
    colleges_text = side_bar_canvas.create_text(colleges_text_x, colleges_icon_y, text="Colleges", fill="white",
                                                font=('Albert Sans', 11, 'normal'), anchor="w")

    # Programs Button
    programs_x1 = ((canvas_width - programs_width) // 2) + offset_x
    programs_y1 = colleges_y2 + colleges_to_programs_spacing
    programs_x2 = programs_x1 + programs_width
    programs_y2 = programs_y1 + programs_height

    programs_button = create_rounded_rectangle(side_bar_canvas, programs_x1, programs_y1, programs_x2, programs_y2, radius=20, fill="#2363C6")

    programs_icon_img = PhotoImage(file="Images/program.png")  
    icon_images.append(programs_icon_img)
    programs_icon_x = programs_x1 + 10
    programs_icon_y = (programs_y1 + programs_y2) // 2
    programs_icon = side_bar_canvas.create_image(programs_icon_x, programs_icon_y, anchor="w", image=programs_icon_img)

    programs_text_x = programs_icon_x + programs_icon_img.width() + icon_text_spacing
    programs_text = side_bar_canvas.create_text(programs_text_x, programs_icon_y, text="Programs", fill="white",
                                                font=('Albert Sans', 11, 'normal'), anchor="w")
    
    # Add button hover and click effects
    side_bar_canvas.tag_bind(add_button, "<Enter>", lambda event: on_add_hover(event, add_button, add_text))
    side_bar_canvas.tag_bind(add_text, "<Enter>", lambda event: on_add_hover(event, add_button, add_text))
    
    side_bar_canvas.tag_bind(add_button, "<Leave>", lambda event: on_add_leave(event, add_button, add_text))
    side_bar_canvas.tag_bind(add_text, "<Leave>", lambda event: on_add_leave(event, add_button, add_text))
    
    side_bar_canvas.tag_bind(add_button, "<Button-1>", lambda event: on_add_button_click(event, body_frame=body_frame))
    side_bar_canvas.tag_bind(add_text, "<Button-1>", lambda event: on_add_button_click(event, body_frame=body_frame))
    
    # Bind other buttons using common function
    bind_button_and_elements(delete_button, delete_icon, delete_text, delete_stud)
    bind_button_and_elements(edit_button, edit_icon, edit_text, lambda event: edit_stud(event, body_frame=body_frame))
    bind_button_and_elements(colleges_button, colleges_icon, colleges_text, lambda event: colleges_func(event, body_frame=body_frame))
    bind_button_and_elements(programs_button, programs_icon, programs_text, lambda event: programs_func(event, body_frame=body_frame))

def on_add_hover(event, button, text):
    side_bar_canvas.itemconfig(button, fill="#A5CAEC")
    side_bar_canvas.itemconfig(text, fill="#154BA6")
    side_bar_canvas.config(cursor="hand2")

def on_add_leave(event, button, text):
    side_bar_canvas.itemconfig(button, fill="white")
    side_bar_canvas.itemconfig(text, fill="#2363C6")
    side_bar_canvas.config(cursor="")

def bind_button_and_elements(button, icon, text, click_func):
    side_bar_canvas.tag_bind(button, "<Enter>", lambda event: on_hover_button(event, button, text))
    side_bar_canvas.tag_bind(icon, "<Enter>", lambda event: on_hover_button(event, button, text))
    side_bar_canvas.tag_bind(text, "<Enter>", lambda event: on_hover_button(event, button, text))
    
    side_bar_canvas.tag_bind(button, "<Leave>", lambda event: on_leave_button(event, button, text))
    side_bar_canvas.tag_bind(icon, "<Leave>", lambda event: on_leave_button(event, button, text))
    side_bar_canvas.tag_bind(text, "<Leave>", lambda event: on_leave_button(event, button, text))
    
    side_bar_canvas.tag_bind(button, "<Button-1>", lambda event: on_click_button(event, button, text))
    side_bar_canvas.tag_bind(icon, "<Button-1>", lambda event: on_click_button(event, button, text))
    side_bar_canvas.tag_bind(text, "<Button-1>", lambda event: on_click_button(event, button, text))
    
    side_bar_canvas.tag_bind(button, "<ButtonRelease-1>", lambda event: on_release_button(event, button, text, click_func))
    side_bar_canvas.tag_bind(icon, "<ButtonRelease-1>", lambda event: on_release_button(event, button, text, click_func))
    side_bar_canvas.tag_bind(text, "<ButtonRelease-1>", lambda event: on_release_button(event, button, text, click_func))

def on_hover_button(event, button, text):
    side_bar_canvas.itemconfig(button, fill="#A5CAEC")
    side_bar_canvas.itemconfig(text, fill="#154BA6")
    side_bar_canvas.config(cursor="hand2")

def on_leave_button(event, button, text):
    side_bar_canvas.itemconfig(button, fill="#2363C6")
    side_bar_canvas.itemconfig(text, fill="white")
    side_bar_canvas.config(cursor="")

def on_click_button(event, button, text):
    side_bar_canvas.itemconfig(button, fill="#1A4A99")
    side_bar_canvas.itemconfig(text, fill="white")

def on_release_button(event, button, text, click_func):
    side_bar_canvas.itemconfig(button, fill="#A5CAEC")
    side_bar_canvas.itemconfig(text, fill="#154BA6")
    click_func(event)

def side(root,body_frame):
    global side_bar_canvas
    # Define a fixed maximum width for the sidebar
    SIDEBAR_MAX_WIDTH = 270  # Set your desired maximum width here
    
    side_frame = Frame(root, bg="blue")
    side_frame.grid(row=1, column=0, sticky="nsew")
    side_frame.columnconfigure(0, weight=1)
    side_frame.rowconfigure(0,weight=1)  

    side_bar_canvas = Canvas(side_frame, bg="white", width=SIDEBAR_MAX_WIDTH, height=105, bd=0, highlightthickness=0)
    side_bar_canvas.grid(row=0, column=0, sticky="nsew")
    setup_table_deselection(student_table, side_frame)

    # Force the sidebar to maintain the maximum width
    root.columnconfigure(0, minsize=SIDEBAR_MAX_WIDTH)
    side_frame.config(width=SIDEBAR_MAX_WIDTH)
    
    def on_root_resize(event):
        # Always maintain the maximum width regardless of window size
        root.columnconfigure(0, minsize=SIDEBAR_MAX_WIDTH)
        side_frame.config(width=SIDEBAR_MAX_WIDTH)
        side_bar_canvas.config(width=SIDEBAR_MAX_WIDTH)
        
        # Re-draw the sidebar elements when resized
        side_buttons(body_frame)

    root.bind("<Configure>", on_root_resize)
    
    # Initial draw of the sidebar
    side_bar_canvas.bind("<Configure>", lambda event: side_buttons(body_frame))
    side_frame.bind("<Button-1>", remove_focus)
    
    return side_frame,side_bar_canvas