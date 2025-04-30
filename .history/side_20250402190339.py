from tkinter import *
from misc import create_rounded_rectangle,remove_focus
from addStudent import on_add_button_click
from deleteStudent import delete_stud
from editStudent import edit_stud
from collegeFunction import colleges_func
from programFunction import programs_func

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
            side_bar_canvas.tag_bind(tag, "<ButtonRelease-1>", lambda event: on_release(event, click_func))

def side_buttons():
    side_bar_canvas.delete("all")
    canvas_width, canvas_height = side_bar_canvas.winfo_width(), side_bar_canvas.winfo_height()

    side_frame = create_rounded_rectangle(side_bar_canvas, -200, 0, canvas_width, canvas_height + 50, radius=130, fill="#2363C6")
    side_bar_canvas.tag_bind(side_frame,"<Button-1>",remove_focus)
    button_specs = [
        ("Add Student", "white", "", 160, 35, 35, on_add_button_click),
        ("Delete Student", "#2363C6", "Images/Trash.png", 160, 25, 15, delete_stud),
        ("Edit Student", "#2363C6", "Images/edit.png", 160, 25, 2, edit_stud),
        ("Colleges", "#2363C6", "Images/college.png", 160, 25, 2, colleges_func),
        ("Programs", "#2363C6", "Images/program.png", 160, 25, 2, programs_func)
    ]

    icon_text_spacing, offset_x, prev_y2 = 4, 0, 0
    for text, color, icon_path, width, height, spacing, click_func in button_specs:
        x1 = (canvas_width - width) // 2 + offset_x
        y1 = prev_y2 + spacing if prev_y2 else spacing
        x2, y2 = x1 + width, y1 + height

        button = create_rounded_rectangle(side_bar_canvas, x1, y1, x2, y2, radius=20, fill=color)
        icon = None
        if icon_path:
            icon_img = PhotoImage(file=icon_path)
            icon_x, icon_y = x1 + 8, (y1 + y2) // 2
            icon = side_bar_canvas.create_image(icon_x, icon_y, anchor="w", image=icon_img)
            text_x = icon_x + icon_img.width() + icon_text_spacing
        else:
            text_x = (x1 + x2) // 2
            icon_y = (y1 + y2) // 2
        
        text_item = side_bar_canvas.create_text(text_x, icon_y, text=text, fill="white" if color == "#2363C6" else "#2363C6", font=('Albert Sans', 11 if icon_path else 13, 'bold' if not icon_path else 'normal'), anchor="w" if icon_path else "center")
        prev_y2 = y2

        bind_button_events(button, icon, text_item, click_func)



def side(root):
    global side_bar_canvas
    side_frame = Frame(root, bg="blue")
    side_frame.grid(row=1, column=0, sticky="nsew")
    side_frame.columnconfigure(0, weight=1)
    side_frame.rowconfigure(0,weight=1)  

    side_bar_canvas = Canvas(side_frame, bg="white", width=180, height=105, bd=0, highlightthickness=0)
    side_bar_canvas.grid(row=0, column=0, sticky="nsew")
    

    def on_root_resize(event):
        total_width = root.winfo_width()
        sidebar_width = max(220, min(290, int(total_width * 0.22)))
        root.columnconfigure(0, minsize=sidebar_width)
        side_frame.config(width=sidebar_width)

        canvas_width = side_frame.winfo_width()
        side_bar_canvas.config(width=canvas_width)

    root.bind("<Configure>", on_root_resize)

    def side_bar(event):
        side_buttons()
        side_frame.bind("<Button-1>",remove_focus)

    side_bar_canvas.bind("<Configure>", side_bar)
    
    return side_frame,side_bar_canvas