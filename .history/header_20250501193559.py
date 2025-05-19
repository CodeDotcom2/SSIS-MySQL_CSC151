from tkinter import *
from misc import remove_focus, create_rounded_rectangle
import search

top = None
x1, y1 = 0, 0

def header(root):
    global search_frame, icon_label, text_label, search_var, cancel, search_bar
    global icon1, text_image, cancel_butt, search_tooltip, tooltip_text, search_help_button
    
    top = Frame(root, bg="white", height=60)
    top.grid(row=0, column=0, sticky="nsew", columnspan=2)
    top.rowconfigure(0, weight=0)
    top.columnconfigure(0, weight=0)
    top.columnconfigure(1, weight=1)
    top.grid_propagate(False)

    text_stud = Label(top, text="Student Information", font=('Albert Sans', 15, 'bold'), bg='white')
    text_stud.grid(row=0, column=0, padx=20)
    text_stud.bind("<Button-1>", remove_focus)

    search_var = StringVar()
    search_var.trace_add("write", on_input_change)

    search_frame = Canvas(top, bg="white", height=40, bd=0, highlightthickness=0)
    search_frame.grid(row=0, column=1, sticky="nsew", padx=(50, 120), pady=5)

    search_bar = Entry(top, textvariable=search_var, bg="#F1F3F8", font=('Albert Sans', 10, 'normal'), 
                      fg="gray", borderwidth=0, highlightthickness=0)
    search_bar.grid(row=0, column=0, padx=0)
    
    icon1 = PhotoImage(file="Images/SearchIcon.png")
    icon_label = Label(search_bar, image=icon1, bg="#F1F3F8", bd=0)
    text_image = PhotoImage(file="Images/Search In Here.png")
    text_label = Label(search_bar, image=text_image, bg="#F1F3F8", bd=0)

    cancel = PhotoImage(file='Images/cancel.png')
    cancel_butt = Button(search_bar, image=cancel, bg="#F1F3F8", bd=0, 
                         cursor="hand2", command=delete_entry)
    
    # Create help button for search syntax
    try:
        help_icon = PhotoImage(file='Images/help.png')
        search_help_button = Button(top, image=help_icon, bd=0, bg="white",
                                   cursor="hand2", command=show_search_help)
        search_help_button.image = help_icon  # Keep a reference to prevent garbage collection
        search_help_button.grid(row=0, column=1, sticky="e", padx=(0, 20))
    except Exception as e:
        print(f"Could not load help icon: {e}")
        # Create text-based help button as fallback
        search_help_button = Button(top, text="?", bd=1, bg="white", fg="#3A7FF6",
                                  font=('Albert Sans', 10, 'bold'), width=2, height=1,
                                  cursor="hand2", command=show_search_help)
        search_help_button.grid(row=0, column=1, sticky="e", padx=(0, 20))
    
    # Create tooltip for search help
    tooltip_text = """
    Search syntax:
    - Just type to search all fields
    - id:12345 to search by ID number
    - name:John to search by name
    - program:Computer to search by program
    - college:Engineering to search by college
    - gender:M to search by gender
    - year:1 or year:1st to search by year level
    """
    search_tooltip = None  # Will be created when hovering over help button
    
    search_help_button.bind("<Enter>", show_tooltip)
    search_help_button.bind("<Leave>", hide_tooltip)
    
    search_frame.bind("<Configure>", on_resize)
    search_bar.bind("<FocusIn>", clear_placeholder)
    search_bar.bind("<FocusOut>", restore_placeholder)
    icon_label.bind("<Button-1>", clear_placeholder)
    text_label.bind("<Button-1>", clear_placeholder)
    top.bind("<Button-1>", remove_focus)

    # Set up the search as soon as header is initialized
    setup_search_connection()


def show_tooltip(event):
    global search_tooltip, tooltip_text
    x, y, _, _ = event.widget.bbox("insert")
    x += event.widget.winfo_rootx() + 25
    y += event.widget.winfo_rooty() + 25
    
    # Create a toplevel window
    search_tooltip = Toplevel(event.widget)
    search_tooltip.wm_overrideredirect(True)
    search_tooltip.wm_geometry(f"+{x}+{y}")
    
    # Create label inside the toplevel with tooltip text
    label = Label(search_tooltip, text=tooltip_text, justify='left',
                 background="#ffffea", relief="solid", borderwidth=1,
                 font=("Albert Sans", 10, "normal"), padx=5, pady=5)
    label.pack(ipadx=3)


def hide_tooltip(event):
    global search_tooltip
    if search_tooltip:
        search_tooltip.destroy()
        search_tooltip = None


def show_search_help():
    # Create a popup window with search syntax help
    help_window = Toplevel()
    help_window.title("Search Help")
    help_window.geometry("400x300")
    help_window.configure(bg="white")
    
    # Add title
    title = Label(help_window, text="Search Syntax Guide", font=('Albert Sans', 14, 'bold'), 
                 bg="white", pady=10)
    title.pack(fill="x")
    
    # Add description
    description = Label(help_window, text="You can search across all fields or target specific fields using the following syntax:",
                      font=('Albert Sans', 10), bg="white", wraplength=380, justify='left')
    description.pack(fill="x", padx=10, pady=5, anchor="w")
    
    # Add examples frame
    examples_frame = Frame(help_window, bg="white")
    examples_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    examples = [
        ("General Search", "Just type any text to search across all fields"),
        ("ID Number", "id:12345 or idno:12345"),
        ("Name", "name:Smith"),
        ("Program", "program:Computer Science"),
        ("College", "college:Engineering"),
        ("Gender", "gender:F or gender:Female"),
        ("Year Level", "year:1 or year:1st")
    ]
    
    # Add examples as table rows
    for i, (field, syntax) in enumerate(examples):
        bg_color = "#f5f5f5" if i % 2 == 0 else "white"
        
        field_label = Label(examples_frame, text=field, font=('Albert Sans', 10, 'bold'), 
                          bg=bg_color, anchor="w", padx=5, pady=5)
        field_label.grid(row=i, column=0, sticky="nsew")
        
        syntax_label = Label(examples_frame, text=syntax, font=('Albert Sans', 10), 
                           bg=bg_color, anchor="w", padx=5, pady=5)
        syntax_label.grid(row=i, column=1, sticky="nsew")
    
    examples_frame.columnconfigure(0, weight=1)
    examples_frame.columnconfigure(1, weight=2)
    
    # Add close button
    close_button = Button(help_window, text="Close", bg="#3A7FF6", fg="white",
                        font=('Albert Sans', 10), padx=10, pady=5,
                        command=help_window.destroy)
    close_button.pack(pady=10)

def clear_placeholder(event=None):
    if search_var.get() == "":
        icon_label.place_forget()
        text_label.place_forget()
    search_bar.focus_set()

def restore_placeholder(event=None):
    if search_var.get() == "":
        icon_label.place(x=x1 + -7, y=y1 + -3)
        text_label.place(x=x1 + 15, y=y1 + 1)

def on_resize(event):
    global x1, y1
    search_frame.delete("all")
    margin = 6
    radius = 20
    canvas_width = search_frame.winfo_width()
    canvas_height = search_frame.winfo_height()

    x1 = margin
    y1 = margin
    x2 = canvas_width - margin
    y2 = canvas_height - margin

    create_rounded_rectangle(search_frame, x1, y1, x2, y2, radius=radius, fill='#F1F3F8', outline="#E4EBF5")
    search_frame.create_window(x1 + 5, y1 + 3, anchor="nw", window=search_bar, width=x2 - x1 - 10, height=y2 - y1 - 4)

    icon_label.place(x=x1 + -7, y=y1 + -3)
    text_label.place(x=x1 + 15, y=y1 + 1)
    search_var.set("")
    cancel_butt.pack_forget()

def on_input_change(*args):
    if search_var.get():
        cancel_butt.lift()
        cancel_butt.pack(side="right", padx=2)
    else:
        cancel_butt.pack_forget()
    filter_students()

def delete_entry():
    search_var.set("")
    search_bar.focus_set()
    cancel_butt.pack_forget()
    filter_students()

def filter_students():
    # Use the centralized search module to update search text
    search.set_search_text(search_var.get())

def get_search_term():
    return search_var.get()

def setup_search_connection():
    # Nothing needed here as search module handles the communication
    pass