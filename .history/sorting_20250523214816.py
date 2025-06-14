from tkinter import *
from tkinter import ttk
from misc import create_rounded_rectangle

# Global variables
sort_canvas = None
sort_frame = None
is_visible = False
sort_button = None  # Reference to the sort button in header
sort_button_canvas = None  # Reference to the canvas containing the sort button

def sort_function(body_frame):
    from header import header
    global sort_canvas, sort_frame, is_visible, sort_button, sort_button_canvas

    if sort_canvas and sort_canvas.winfo_exists():
        if is_visible:
            sort_canvas.place_forget()
            is_visible = False
            if sort_button and sort_button_canvas:
                sort_button_canvas.itemconfig(sort_button, fill="white")
            return
        else:
            sort_canvas.place(relx=0.95, rely=0.0, anchor="ne")
            is_visible = True
            if sort_button and sort_button_canvas:
                sort_button_canvas.itemconfig(sort_button, fill="#A5CAEC")
            return
        
    # Create main container
    sort_canvas = Canvas(body_frame, bg="white", width=250, height=265, highlightthickness=0, borderwidth=0)
    sort_canvas.place(relx=0.95, rely=0.0, anchor="ne")
    is_visible = True
    
    if sort_button and sort_button_canvas:
        sort_button_canvas.itemconfig(sort_button, fill="#A5CAEC")
    
    # Create background
    create_rounded_rectangle(sort_canvas, 0, 0, 250, 265, radius=30, fill="#E8E8E8", outline="lightgray", width=2)
    sort_canvas.create_text(250/2, 30, text="Sort Students By", font=("Albert Sans", 15, "bold"), fill="#333333")

    # Create main content frame moved higher (y=140)
    sort_frame = Frame(sort_canvas, bg="#E8E8E8", bd=0, highlightthickness=0)
    sort_canvas.create_window(250/2, 140, window=sort_frame, width=230, height=180)  # Reduced height to 180

    sort_options = [
        ("ID Number", "id_number"),
        ("Name", "last_name"),
    ]
    sort_direction = StringVar(value="ascending")
    sort_field = StringVar(value="id_number")
    
    style = ttk.Style()
    style.configure("Sort.TRadiobutton", 
                  background="#E8E8E8", 
                  font=("Albert Sans", 12),
                  padding=8)
    
    # Sort options
    for i, (text, value) in enumerate(sort_options):
        rb = ttk.Radiobutton(
            sort_frame, 
            text=text, 
            value=value,
            variable=sort_field,
            style="Sort.TRadiobutton"
        )
        rb.grid(row=i, column=0, sticky=W, pady=0, padx=0)

    # Direction selection
    direction_label = Label(sort_frame, text="Direction:", font=("Albert Sans", 14), 
                         bg="#E8E8E8", fg="#333333")
    direction_label.grid(row=len(sort_options), column=0, sticky=W, pady=(5, 0), padx=0)
    
    direction_frame = Frame(sort_frame, bg="#E8E8E8")
    direction_frame.grid(row=len(sort_options)+1, column=0, sticky=W, pady=0, padx=0)
    
    asc_rb = ttk.Radiobutton(
        direction_frame, 
        text="Ascending", 
        value="ascending",
        variable=sort_direction,
        style="Sort.TRadiobutton"
    )
    asc_rb.pack(side=LEFT, padx=(0, 10))

    desc_rb = ttk.Radiobutton(
        direction_frame, 
        text="Descending", 
        value="descending",
        variable=sort_direction,
        style="Sort.TRadiobutton"
    )
    desc_rb.pack(side=LEFT)

    # Create button canvas positioned higher with 15px from bottom
    button_canvas = Canvas(sort_canvas, bg="#E8E8E8", width=230, height=50, highlightthickness=0)
    sort_canvas.create_window(250/2, 270 - 40, window=button_canvas)  # 50/2 + 15 = 40 from bottom

    # Button dimensions and positions
    button_width = 100  # Both buttons will now use the same width
    button_height = 40
    gap = 10
    total_width = (button_width * 2) + gap
    start_x = (230 - total_width) / 2

    # Create rounded rectangle buttons (now both using the same width)
    apply_bg = create_rounded_rectangle(button_canvas, 
                                      start_x, 5, 
                                      start_x + button_width, 45, 
                                      radius=20, fill="#3A7FF6")
    
    cancel_bg = create_rounded_rectangle(button_canvas, 
                                       start_x + button_width + gap, 5, 
                                       start_x + (button_width * 2) + gap, 45, 
                                       radius=20, fill="#AA4141")

    # Add centered button text
    apply = button_canvas.create_text(start_x + button_width/2, 25, 
                            text="Apply", font=("Albert Sans", 12,"bold"), fill="white")
    cancel = button_canvas.create_text(start_x + button_width + gap + button_width/2, 25, 
                            text="Cancel", font=("Albert Sans", 12,"bold"), fill="white")

    # Add button click functionality
    button_canvas.tag_bind(apply_bg, "<Button-1>", lambda e: apply_sort(sort_field.get(), sort_direction.get()))
    button_canvas.tag_bind(apply, "<Button-1>", lambda e: apply_sort(sort_field.get(), sort_direction.get()))
    button_canvas.tag_bind(cancel_bg, "<Button-1>", lambda e: toggle_visibility())
    button_canvas.tag_bind(cancel, "<Button-1>", lambda e: toggle_visibility())
    

    # Add hover effects
    button_canvas.tag_bind(apply_bg, "<Enter>", lambda e: button_canvas.itemconfig(apply_bg, fill="#1A4A99"))
    button_canvas.tag_bind(apply, "<Enter>", lambda e: button_canvas.itemconfig(apply_bg, fill="#1A4A99"))
    button_canvas.tag_bind(apply_bg, "<Leave>", lambda e: button_canvas.itemconfig(apply_bg, fill="#2363C6"))
    
    button_canvas.tag_bind(cancel_bg, "<Enter>", lambda e: button_canvas.itemconfig(cancel_bg, fill="#d32f2f"))
    button_canvas.tag_bind(cancel_bg, "<Leave>", lambda e: button_canvas.itemconfig(cancel_bg, fill="#AA4141"))
    button_canvas.tag_bind(cancel, "<Enter>", lambda e: button_canvas.itemconfig(cancel_bg, fill="#d32f2f"))


    # Separator line
    sort_canvas.create_line(25, 60, 225, 60, fill="#E4EBF5", width=2)

def toggle_visibility():
    """
    Toggle the visibility of the sorting canvas
    """
    global sort_canvas, is_visible, sort_button, sort_button_canvas
    if sort_canvas:
        if is_visible:
            sort_canvas.place_forget()
            is_visible = False
            # Reset sort button color when form is closed
            if sort_button and sort_button_canvas:
                sort_button_canvas.itemconfig(sort_button, fill="white")
        else:
            sort_canvas.place(relx=0.95, rely=0.0, anchor="ne")
            is_visible = True
            # Change sort button color when form is active
            if sort_button and sort_button_canvas:
                sort_button_canvas.itemconfig(sort_button, fill="#A5CAEC")

def apply_sort(field, direction):
    """
    Apply the sorting options and hide the canvas
    """
    print(f"Sorting by {field} in {direction} order")
    
    from body import refresh_students
    refresh_students(sort_field=field, sort_direction=direction)
    # Hide the canvas
    toggle_visibility()


def set_sort_button_reference(button_obj, button_canvas):
    """
    Set the reference to the sort button from header.py
    """
    global sort_button, sort_button_canvas
    sort_button = button_obj
    sort_button_canvas = button_canvas