from tkinter import *
from misc import create_rounded_rectangle, main_root

def set_form_frame(root):
    """Create and configure the college form"""
    # Clear the main area
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 0 and int(widget.grid_info()["column"]) > 0:
            widget.grid_forget()
    
    # Create a frame for the college form
    college_frame = Frame(root, bg="white")
    college_frame.grid(row=1, column=1, sticky="nsew")
    
    # Create the canvas for the form
    college_canvas = Canvas(college_frame, bg="white", width=350, height=480, bd=0, highlightthickness=0)
    college_canvas.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Create the rounded rectangle background
    form = create_rounded_rectangle(college_canvas, -300, 0, 350, 480, radius=130, fill='lightgray')
    
    # Title
    title_label = Label(college_frame, text="College Form", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    college_canvas.create_window(160, 30, window=title_label)
    
    # Add form elements
    college_name_label = Label(college_frame, text="College Name:", bg="lightgray", font=("Arial", 12))
    college_canvas.create_window(100, 80, window=college_name_label, anchor="w")
    college_name_entry = Entry(college_frame, width=25)
    college_canvas.create_window(250, 80, window=college_name_entry)
    
    # Add a location field
    location_label = Label(college_frame, text="Location:", bg="lightgray", font=("Arial", 12))
    college_canvas.create_window(100, 120, window=location_label, anchor="w")
    location_entry = Entry(college_frame, width=25)
    college_canvas.create_window(250, 120, window=location_entry)
    
    # Add an established year field
    established_label = Label(college_frame, text="Established Year:", bg="lightgray", font=("Arial", 12))
    college_canvas.create_window(100, 160, window=established_label, anchor="w")
    established_entry = Entry(college_frame, width=25)
    college_canvas.create_window(250, 160, window=established_entry)
    
    # Add a website field
    website_label = Label(college_frame, text="Website:", bg="lightgray", font=("Arial", 12))
    college_canvas.create_window(100, 200, window=website_label, anchor="w")
    website_entry = Entry(college_frame, width=25)
    college_canvas.create_window(250, 200, window=website_entry)
    
    # Add buttons
    save_button = Button(college_frame, text="Save", bg="#2363C6", fg="white", font=("Arial", 12, "bold"), 
                         padx=20, pady=5, relief=FLAT)
    college_canvas.create_window(140, 300, window=save_button)
    
    cancel_button = Button(college_frame, text="Cancel", bg="#A5CAEC", fg="#154BA6", font=("Arial", 12, "bold"), 
                          padx=20, pady=5, relief=FLAT)
    college_canvas.create_window(240, 300, window=cancel_button)

def colleges_func(event=None):
    """Handle the colleges button click event"""
    # Call the set_form_frame function with main_root
    set_form_frame(main_root)
    
    print("COLLEGES form displayed")