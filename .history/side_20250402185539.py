from tkinter import *
from misc import create_rounded_rectangle

def side_buttons():
    add_frame = create_rounded_rectangle(side_bar_canvas,20,5,5,20,20,fill="red")


def side(root):
    global side_bar_canvas
    side_frame = Frame(root, bg="blue")
    side_frame.grid(row=1, column=0, sticky="nsew")
    side_frame.columnconfigure(0, weight=1)
    side_frame.rowconfigure(0,weight=1)  

    side_bar_canvas = Canvas(side_frame, bg="white", width=180, height=105, bd=0, highlightthickness=0)
    side_bar_canvas.grid(row=0, column=0, sticky="nsew")
    
    add_frame = create_rounded_rectangle(side_bar_canvas,5,5,5,5,20,fill="red")

    def on_root_resize(event):
        total_width = root.winfo_width()
        sidebar_width = max(220, min(290, int(total_width * 0.22)))
        root.columnconfigure(0, minsize=sidebar_width)
        side_frame.config(width=sidebar_width)

        canvas_width = side_frame.winfo_width()
        side_bar_canvas.config(width=canvas_width)

    root.bind("<Configure>", on_root_resize)

    def side_bar(event):
        from misc import create_rounded_rectangle
        canvas_width = side_bar_canvas.winfo_width()
        canvas_height = side_bar_canvas.winfo_height()
        

        side_bar_canvas.delete("all")
        #side_frame = create_rounded_rectangle(side_bar_canvas, -200, 0, canvas_width, canvas_height + 50, radius=130, fill="#2363C6")

    side_bar_canvas.bind("<Configure>", side_bar)

    return side_frame