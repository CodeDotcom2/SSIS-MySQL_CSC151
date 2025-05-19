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

    def toggle_visibility():
        nonlocal is_visible
        if is_visible:
            sort_canvas.place_forget()
            is_visible = False
            if sort_button and sort_button_canvas:
                sort_button_canvas.itemconfig(sort_button, fill="white")
        else:
            sort_canvas.place(relx=0.95, rely=0.0, anchor="ne")
            is_visible = True
            if sort_button and sort_button_canvas:
                sort_button_canvas.itemconfig(sort_button, fill="#A5CAEC")

    def apply_sort(field, direction):
        # Implement your sorting logic here
        print(f"Sorting by {field} in {direction} order")
        toggle_visibility()

    # Check if sort panel already exists
    if sort_canvas and sort_canvas.winfo_exists():
        toggle_visibility()
        return
        
    # Create main sort container
    sort_canvas = Canvas(body_frame, bg="#F0F0F0", width=250, height=350, highlightthickness=0, borderwidth=0)
    sort_canvas.place(relx=0.95, rely=0.0, anchor="ne")
    is_visible = True
    
    if sort_button and sort_button_canvas:
        sort_button_canvas.itemconfig(sort_button, fill="#A5CAEC")
    
    # Create rounded background
    create_rounded_rectangle(sort_canvas, 0, 0, 250, 350, radius=20, fill="white", outline="#E4EBF5", width=2)
    sort_canvas.create_text(250/2, 30, text="Sort Students By", font=("Albert Sans", 15, "bold"), fill="#333333")
    
    # Create separator line
    sort_canvas.create_line(20, 60, 230, 60, fill="#E4EBF5", width=2)
    
    # Create frame for sort options
    sort_frame = Frame(sort_canvas, bg="white", bd=0, highlightthickness=0)
    sort_canvas.create_window(250/2, 200, window=sort_frame, width=230, height=250)
    
    # Sort options
    sort_options = [
        ("ID Number", "id_number"),
        ("Name", "last_name"),
    ]
    sort_direction = StringVar(value="ascending")
    sort_field = StringVar(value="id_number")
    
    # Configure style
    style = ttk.Style()
    style.configure("Sort.TRadiobutton", 
                  background="white", 
                  font=("Albert Sans", 12),
                  padding=8)
    
    # Add sort option radio buttons
    for i, (text, value) in enumerate(sort_options):
        rb = ttk.Radiobutton(
            sort_frame, 
            text=text, 
            value=value,
            variable=sort_field,
            style="Sort.TRadiobutton"
        )
        rb.grid(row=i, column=0, sticky=W, pady=5, padx=20)

    # Direction selection
    direction_frame = Frame(sort_frame, bg="white")
    direction_frame.grid(row=len(sort_options), column=0, sticky=W, pady=(10, 5), padx=20)
    
    direction_label = Label(direction_frame, text="Direction:", font=("Albert Sans", 14), 
                         bg="white", fg="#333333")
    direction_label.pack(side=LEFT, padx=(0, 10))
    
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

    # Button container
    button_frame = Frame(sort_frame, bg="white")
    button_frame.grid(row=len(sort_options)+2, column=0, sticky=E, pady=(20, 10), padx=20)
    
    # Apply button
    apply_button = Button(
        button_frame,
        text="Apply",
        font=("Albert Sans", 12),
        bg="#3A7FF6",
        fg="white",
        padx=15,
        pady=5,
        relief="flat",
        cursor="hand2",
        activebackground="#2A6FD6",
        activeforeground="white",
        command=lambda: apply_sort(sort_field.get(), sort_direction.get())
    )
    apply_button.pack(side=RIGHT, padx=5)
    
    # Cancel button
    cancel_button = Button(
        button_frame,
        text="Cancel",
        font=("Albert Sans", 12),
        bg="#f0f0f0",
        fg="black",
        padx=15,
        pady=5,
        relief="flat",
        cursor="hand2",
        activebackground="#e0e0e0",
        activeforeground="black",
        command=toggle_visibility
    )
    cancel_button.pack(side=RIGHT, padx=5)

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
    
    # TODO: Implement actual sorting logic here
    # This would connect to your database query or modify how data is displayed
    
    # Hide the canvas
    toggle_visibility()
    
    # TODO: Refresh the student table with the sorted data
    # This would call a function in your body.py to refresh the display
    from body import refresh_students

def set_sort_button_reference(button_obj, button_canvas):
    """
    Set the reference to the sort button from header.py
    """
    global sort_button, sort_button_canvas
    sort_button = button_obj
    sort_button_canvas = button_canvas