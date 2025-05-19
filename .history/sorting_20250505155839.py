from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from misc import create_rounded_rectangle

# Global variables
sort_window = None
sort_popup = None

def sort_function(body_frame):
    """
    Creates a sorting popup window for student data
    """
    global sort_window, sort_popup
    
    # If there's already a sort window open, close it
    if sort_popup and sort_popup.winfo_exists():
        sort_popup.destroy()
    
    # Get the position for the popup relative to the parent window
    x = body_frame.winfo_rootx() + 100
    y = body_frame.winfo_rooty() + 80
    
    # Create a new toplevel window
    sort_popup = Toplevel()
    sort_popup.title("Sort Students")
    sort_popup.geometry(f"350x480+{x}+{y}")
    sort_popup.configure(bg="white")
    sort_popup.resizable(False, False)
    sort_popup.transient()  # Make it float on top of the main window
    
    # Add a title to the popup
    title_label = Label(sort_popup, text="Sort Students By", font=("Albert Sans", 18, "bold"), 
                        bg="white", fg="black")
    title_label.pack(pady=(20, 30))
    
    # Create a container for the sort options
    options_frame = Frame(sort_popup, bg="white")
    options_frame.pack(fill="both", expand=True, padx=30, pady=10)
    
    # Sort options
    sort_options = [
        ("ID Number", "id_number"),
        ("Name", "last_name"),
        ("Gender", "gender"),
        ("Year Level", "year_level"),
        ("College", "college_code"),
        ("Program", "program_code")
    ]
    
    # Default sort direction
    sort_direction = StringVar(value="ascending")
    
    # Default sort field
    sort_field = StringVar(value="id_number")
    
    # Create radio buttons for each sort option
    for text, value in sort_options:
        rb = ttk.Radiobutton(
            options_frame, 
            text=text, 
            value=value,
            variable=sort_field,
            style="Sort.TRadiobutton"
        )
        rb.pack(anchor="w", pady=8)
    
    # Direction options frame
    direction_frame = Frame(options_frame, bg="white")
    direction_frame.pack(anchor="w", pady=(20, 10))
    
    direction_label = Label(direction_frame, text="Direction:", font=("Albert Sans", 14), 
                           bg="white", fg="black")
    direction_label.pack(side="left")
    
    # Radio buttons for sort direction
    asc_rb = ttk.Radiobutton(
        direction_frame, 
        text="Ascending", 
        value="ascending",
        variable=sort_direction,
        style="Sort.TRadiobutton"
    )
    asc_rb.pack(side="left", padx=(20, 10))
    
    desc_rb = ttk.Radiobutton(
        direction_frame, 
        text="Descending", 
        value="descending",
        variable=sort_direction,
        style="Sort.TRadiobutton"
    )
    desc_rb.pack(side="left")
    
    # Button frame
    button_frame = Frame(sort_popup, bg="white")
    button_frame.pack(fill="x", padx=30, pady=20)
    
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
        command=lambda: apply_sort(sort_field.get(), sort_direction.get(), sort_popup)
    )
    apply_button.pack(side="right", padx=5)
    
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
        command=sort_popup.destroy
    )
    cancel_button.pack(side="right", padx=5)
    
    # Configure the styles for radio buttons
    style = ttk.Style()
    style.configure("Sort.TRadiobutton", 
                    background="white", 
                    font=("Albert Sans", 12))
    
    # Make sure the window is displayed
    sort_popup.focus_set()
    sort_popup.grab_set()  # Make it modal

def apply_sort(field, direction, popup):
    """
    Apply the sorting options and close the popup
    """
    print(f"Sorting by {field} in {direction} order")
    
    # TODO: Implement actual sorting logic here
    # This would connect to your database query or modify how data is displayed
    
    # Close the popup window
    popup.destroy()
    
    # TODO: Refresh the student table with the sorted data
    # This would call a function in your body.py to refresh the display
    from body import refresh_students
    refresh_students()