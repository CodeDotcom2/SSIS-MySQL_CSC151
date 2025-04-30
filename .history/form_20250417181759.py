from tkinter import *
from tkinter import ttk
from misc import create_rounded_rectangle


def create_form(root, body_frame=None):
    if body_frame is None:
        from body import body
        body_frame = body(root)
    
    form_frame = Canvas(body_frame, bg="white", width=350, height=480, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(form_frame, -300, 0, 350, 480, radius=130, fill='lightgray')

    text_elements = {}
    
    # Title
    title_label = Label(root, text="Student Form", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    form_frame.create_window(160, 30, window=title_label)
    text_elements['title'] = title_label
    
    # Student's Full Name label
    name_label = Label(root, text="Student's Full Name ", bg="lightgray", font=("Arial", 15, "bold"))
    form_frame.create_window(112, 85, window=name_label)
    text_elements['name_label'] = name_label
    
    # Last Name
    last_name = Entry(root, font=("Albert Sans", 12, "normal"), width=14)
    form_frame.create_window(80, 110, window=last_name)
    text_elements['last_name'] = last_name
    
    last_text = Label(root, text="Last Name ", bg="lightgray", fg="gray", font=("Arial", 10))
    form_frame.create_window(80, 132, window=last_text)
    text_elements['last_text'] = last_text
    
    # First Name
    first_name = Entry(root, font=("Albert Sans", 12, "normal"), width=20)
    form_frame.create_window(245, 110, window=first_name)
    text_elements['first_name'] = first_name
    
    first_text = Label(root, text="First Name ", bg="lightgray", fg="gray", font=("Arial", 10))
    form_frame.create_window(245, 132, window=first_text)
    text_elements['first_text'] = first_text
    
    # Gender
    gender = Label(root, text="Gender", font=('Arial', 15, 'bold'), bg='light gray')
    form_frame.create_window(50, 155, window=gender)
    text_elements['gender'] = gender
    
    gender_dropdown = ttk.Combobox(root, style="Custom.TCombobox", values=["Male", "Female", "Others"], 
                                  state="readonly", width=14, font=(('Arial', 11, 'normal')))
    form_frame.create_window(80, 180, window=gender_dropdown)
    text_elements['gender_dropdown'] = gender_dropdown
    
    # ID
    id_label = Label(root, text="ID No.", font=('Arial', 15, 'bold'), bg='light gray')
    form_frame.create_window(44, 210, window=id_label)
    text_elements['id_label'] = id_label
    
    id_no = Entry(root, font=('Albert Sans', 12, 'normal'), width=14, fg="gray", justify="center")
    form_frame.create_window(80, 233, window=id_no)
    id_no.insert(0, "Ex: 1234-5678")
    id_no.bind("<FocusIn>", lambda event: id_no.get() == "Ex: 1234-5678" and (id_no.delete(0, END), id_no.config(fg="black", justify="left")))
    id_no.bind("<FocusOut>", lambda event: id_no.get() == "" and (id_no.insert(0, "Ex: 1234-5678"), id_no.config(fg="gray", justify="center")))
    text_elements['id_no'] = id_no
    
    # Year Level
    year = Label(root, text="Year Level", font=('Arial', 15, 'bold'), bg='light gray')
    form_frame.create_window(210, 210, window=year)
    text_elements['year'] = year
    
    year_dropdown = ttk.Combobox(root, style="Custom.TCombobox", values=["1st", "2nd", "3rd", "4th", "5+"], 
                               state="readonly", width=14, font=('Arial', 11, 'normal'))
    form_frame.create_window(230, 233, window=year_dropdown)
    text_elements['year_dropdown'] = year_dropdown
    
    # College
    college = Label(root, text="College", font=('Arial', 15, 'bold'), bg='light gray')
    form_frame.create_window(50, 263, window=college)
    text_elements['college'] = college
    
    college_dropdown = ttk.Combobox(root, style="Custom.TCombobox", values="CCS""COE", state="readonly", width=37, font=('Arial', 11, 'normal'))
    form_frame.create_window(175, 287, window=college_dropdown)
    college_dropdown.set("Select") 
    #college_dropdown.bind("<<ComboboxSelected>>", on_select)
    
    # Submit button
    submit_canvas = Canvas(root, width=100, height=45, bg="light gray", highlightthickness=0)
    form_frame.create_window(120, 400, window=submit_canvas)
    submit = create_rounded_rectangle(submit_canvas, 5, 5, 100, 45, radius=20, fill='#2363C6')
    submit_text = submit_canvas.create_text(50, 24, text="Submit", fill="white", font=("Arial", 15, "bold"))
    text_elements['submit_text'] = submit_text
    text_elements['submit_canvas'] = submit_canvas
    
    # Close button
    close_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
    form_frame.create_window(225, 400, window=close_canvas)
    close = create_rounded_rectangle(close_canvas, 5, 5, 100, 45, radius=20, fill='#AA4141')
    close_text = close_canvas.create_text(50, 24, text="Close", fill="white", font=("Arial", 15, "bold"))
    text_elements['close_text'] = close_text
    text_elements['close_canvas'] = close_canvas
    

    form_frame.text_elements = text_elements
    
    return form_frame

def toggle_form_visibility(form_frame, side_bar=None):
    if form_frame is None:
        print("Error: form_frame is None")
        return False
        
    if form_frame.winfo_viewable():
        form_frame.grid_remove()
        if side_bar:
            side_bar.configure(bg="white")
        return False
    else:
        form_frame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nw")
        if side_bar:
            side_bar.configure(bg="lightgray")
        return True
    
def update_form_text(form_frame, element_name, new_text):

    if not hasattr(form_frame, 'text_elements'):
        print("Error: Form frame doesn't have text elements dictionary")
        return False
    
    if element_name not in form_frame.text_elements:
        print(f"Error: Element '{element_name}' not found in form")
        return False
    
    element = form_frame.text_elements[element_name]
    

    if isinstance(element, Label):
        element.config(text=new_text)
    elif isinstance(element, Entry):
        element.delete(0, END)
        element.insert(0, new_text)
    elif isinstance(element, ttk.Combobox):
        element.set(new_text)
    elif isinstance(element, int): 
        parent_canvas = form_frame.text_elements.get(element_name + '_canvas')
        if parent_canvas and isinstance(parent_canvas, Canvas):
            parent_canvas.itemconfig(element, text=new_text)
    
    return True