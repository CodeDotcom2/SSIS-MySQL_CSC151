from tkinter import *
from tkinter import ttk, messagebox
from misc import create_rounded_rectangle,FormManager,on_select
from database import get_all_colleges, get_programs_by_college, save_student, update_student
from body import refresh_students

def create_form(root, body_frame=None, mode="add", student_data=None, refresh_callback=None):
    if body_frame is None:
        from body import body
        body_frame = body(root)
        
    style = ttk.Style()
    style.configure("Custom.TCombobox", foreground="") 
    style.configure("Custom.TCombobox",relief="flat",foreground="gray")
    
    form_frame = Canvas(body_frame, bg="white", width=350, height=480, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(form_frame, -800, 0, 350, 480, radius=130, fill='lightgray')

    text_elements = {}
    
    # Title
    title_text = "Add Student" if mode == "add" else "Edit Student"
    title_label = Label(root, text=title_text, font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
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
    gender_dropdown.set("Select")
    form_frame.create_window(80, 180, window=gender_dropdown)
    text_elements['gender_dropdown'] = gender_dropdown
    gender_dropdown.bind("<<ComboboxSelected>>",on_select)

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
    year_dropdown.bind("<<ComboboxSelected>>",on_select)

    year_dropdown.set("Select")
    
    # College
    college = Label(root, text="College", font=('Arial', 15, 'bold'), bg='light gray')
    form_frame.create_window(50, 263, window=college)
    text_elements['college'] = college
    
    # Get colleges from database
    colleges = get_all_colleges()
    college_names = []
    college_dict = {}
    
    for college in colleges:
        display_text = f"{college['code']} - {college['name']}"
        college_names.append(display_text)
        college_dict[display_text] = college['id']
    
    college_dropdown = ttk.Combobox(root, style="Custom.TCombobox", values=college_names, 
                                    state="readonly", width=37, font=('Arial', 11, 'normal'))
    form_frame.create_window(175, 287, window=college_dropdown)
    college_dropdown.set("Select")
    college_dropdown.bind("<<ComboboxSelecdted>>",on_select)
    text_elements['college_dropdown'] = college_dropdown
    
    # Program
    program = Label(root, text="Program", font=('Arial', 15, 'bold'), bg="light gray")
    form_frame.create_window(58, 317, window=program)

    program_dropdown = ttk.Combobox(root, style="Custom.TCombobox", state="readonly", 
                                    width=37, font=('Arial', 11, 'normal'))
    form_frame.create_window(175, 340, window=program_dropdown)
    program_dropdown.set("Select College First")
    program_dropdown.bind("<<ComboboxSelecdted>>",on_select)
    text_elements['program_dropdown'] = program_dropdown
    
    # Dictionary to store program info
    program_dict = {}
    

    def on_college_select(event):
        selected_college = college_dropdown.get()
        if selected_college != "Select":
            college_id = college_dict[selected_college]
            programs = get_programs_by_college(college_id)
            program_names = []
            program_dict.clear()
            
            for program in programs:
                # Skip programs marked as "N/A"
                if "N/A" in program['name'] or "N/A" in program['code']:
                    continue
                    
                display_text = f"{program['code']} - {program['name']}"
                program_names.append(display_text)
                program_dict[display_text] = program['id']
            
            program_dropdown['values'] = program_names
            if program_names:
                program_dropdown.set("Select Program")
            else:
                program_dropdown.set("No Programs Available")
     
    college_dropdown.bind("<<ComboboxSelected>>", on_college_select)

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

    def close_form():
        form_frame.destroy()
        
    def submit_form():
        # Get all form values
        student_id = student_data.get('id') if mode == "edit" and student_data else None
        last = last_name.get().strip()
        first = first_name.get().strip()
        student_id_no = id_no.get().strip()
        student_gender = gender_dropdown.get()
        student_year = year_dropdown.get()
        selected_program = program_dropdown.get()
        
        # Validate fields
        if not last:
            messagebox.showerror("Error", "Last name is required")
            return
            
        if not first:
            messagebox.showerror("Error", "First name is required")
            return
            
        if student_id_no == "Ex: 1234-5678" or not student_id_no:
            messagebox.showerror("Error", "ID number is required")
            return
            
        if student_gender == "Select":
            messagebox.showerror("Error", "Please select a gender")
            return
            
        if student_year == "Select":
            messagebox.showerror("Error", "Please select a year level")
            return
            
        if college_dropdown.get() == "Select":
            messagebox.showerror("Error", "Please select a college")
            return
            
        if selected_program == "Select Program" or selected_program == "Select College First" or selected_program == "No Programs Available":
            messagebox.showerror("Error", "Please select a program")
            return
            
        # Get program ID from dictionary
        program_id = program_dict.get(selected_program)
        if not program_id:
            messagebox.showerror("Error", "Invalid program selection")
            return
            
        # Save or update student
        success = False
        message = ""
        if mode == "add":
            success, message = save_student(first, last, student_id_no, student_year, student_gender, program_id)
        else:  # Edit mode
            success, message = update_student(student_id, first, last, student_id_no, student_year, student_gender, program_id)
            
        if success:
            messagebox.showinfo("Success", message)
            # Close form and refresh table if callback provided
            if refresh_callback:
                refresh_callback()
            close_form()
            refresh_students()
        else:
            messagebox.showerror("Error", message)
    
    def submit_hover(event):
        submit_canvas.itemconfig(submit, fill="#1A4A99")
        submit_canvas.config(cursor="hand2")
    
    def submit_leave(event):
        submit_canvas.itemconfig(submit, fill="#2363C6")
        submit_canvas.config(cursor="")

    submit_canvas.tag_bind(submit, "<Enter>", submit_hover)
    submit_canvas.tag_bind(submit_text, "<Enter>", submit_hover)
    submit_canvas.tag_bind(submit, "<Leave>", submit_leave)
    submit_canvas.tag_bind(submit_text, "<Leave>", submit_leave)
    submit_canvas.tag_bind(submit, "<Button-1>", lambda event: submit_form())
    submit_canvas.tag_bind(submit_text, "<Button-1>", lambda event: submit_form())

    def close_hover(event):
        close_canvas.itemconfig(close, fill="#d32f2f")
        close_canvas.config(cursor="hand2")
    
    def close_leave(event):
        close_canvas.itemconfig(close, fill="#AA4141")
        close_canvas.config(cursor="")
    
    # Bind events to close button
    close_canvas.tag_bind(close, "<Enter>", close_hover)
    close_canvas.tag_bind(close_text, "<Enter>", close_hover)
    close_canvas.tag_bind(close, "<Leave>", close_leave)
    close_canvas.tag_bind(close_text, "<Leave>", close_leave)
    close_canvas.tag_bind(close, "<Button-1>", lambda event: close_form())
    close_canvas.tag_bind(close_text, "<Button-1>", lambda event: close_form())

    if mode == "edit" and student_data:
        text_elements['id_no'].delete(0, END)
        text_elements['id_no'].config(fg="black", justify="left")
        text_elements['id_no'].insert(0, student_data['id_number'])
        
        text_elements['last_name'].insert(0, student_data['last_name'])
        text_elements['first_name'].insert(0, student_data['first_name'])
        text_elements['gender_dropdown'].set(student_data['gender'])
        
        year_mapping = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5+"}
        year_level = year_mapping.get(student_data['year_level'], "Select")
        text_elements['year_dropdown'].set(year_level)
        
        college_found = False
        for display_text, college_id in college_dict.items():
            if college_id == student_data['college_id']:
                text_elements['college_dropdown'].set(display_text)
                college_found = True
                on_college_select(None)
                break
                
        if college_found:

            form_frame.after(100, lambda: set_program_for_edit(student_data))
        
    def set_program_for_edit(student_data):
        if student_data['program_name'] == 'N/A' or student_data['program_id'] is None:
            # Handle case where program is deleted/NULL
            text_elements['program_dropdown'].set("No Program Assigned")
        else:
            # Normal case where program exists
            program_text = f"{student_data['program_code']} - {student_data['program_name']}"
            if program_text in program_dict:
                text_elements['program_dropdown'].set(program_text)

    form_frame.college_dict = college_dict
    form_frame.program_dict = program_dict
    form_frame.text_elements = text_elements
    
    FormManager.show_form(form_frame)
    return form_frame