from tkinter import *
from tkinter import ttk,font,messagebox
import os,csv,re
import re
from tkinter import messagebox



def populate_form(student_data):
    id_no.delete(0, END)
    id_no.insert(0, student_data[0])

    last_name.delete(0, END)
    last_name.insert(0, student_data[1])

    first_name.delete(0, END)
    first_name.insert(0, student_data[2])

    gender_dropdown.set(student_data[3])
    year_dropdown.set(student_data[4])
    college_dropdown.set(student_data[5])  

    if student_data[5] in college_names:  
        program_dropdown["values"] = college_names[student_data[5]]
    else:
        program_dropdown["values"] = []

    program_dropdown.set(student_data[6]) 

def find_student_in_csv(student_id):

    try:
        with open("students.csv", mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == student_id:
                    return row 
    except FileNotFoundError:
        messagebox.showerror("Error", "CSV file not found.")
    return None

def save_to_csv(update_mode=False, old_id=None):
    global saved_label, students

    file_path = "students.csv"
    headers = ["ID No.", "Last Name", "First Name", "Gender", "Year Level", "College", "Program"]

    student_id = id_no.get()
    last_name_value = last_name.get().title()
    first_name_value = first_name.get().title()
    
    student_data = [
        student_id,
        last_name_value,
        first_name_value,
        gender_dropdown.get(),
        year_dropdown.get(),
        college_dropdown.get(),
        program_dropdown.get()
    ]

    errors = []

    id_pattern = r"^\d{4}-\d{4}$"
    if not re.match(id_pattern, student_id) or any(char.isalpha() for char in student_id):
        errors.append("• ID No. must be in the format XXXX-XXXX (e.g., 2024-1234) and contain only numbers.")

    if any(char.isdigit() for char in last_name_value):
        errors.append("• Last Name must not contain numbers.")
    
    if not all(char.isalpha() or char in [' ', '-'] for char in last_name_value):
        errors.append("• Last Name must contain only letters, spaces, or hyphens.")

    if any(char.isdigit() for char in first_name_value):
        errors.append("• First Name must not contain numbers.")
    
    if not all(char.isalpha() or char in [' ', '-'] for char in first_name_value):
        errors.append("• First Name must contain only letters, spaces, or hyphens.")

    if "" in student_data[:3]:
        errors.append("• All fields (ID No., Last Name, First Name) must be filled out.")

    if gender_dropdown.get() == "Select":
        errors.append("• Please select a Gender.")

    if year_dropdown.get() == "Select":
        errors.append("• Please select a Year Level.")

    if college_dropdown.get() == "Select":
        errors.append("• Please select a College.")

    if program_dropdown.get() == "Select":
        errors.append("• Please select a Program.")

    if errors:
        messagebox.showerror("Form Error", "There are errors in your form:\n\n" + "\n".join(errors))
        return

    file_exists = os.path.exists(file_path)
    updated_rows = []
    existing_student = None

    if file_exists:
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)

            for row in reader:
                if row and row[0] == student_id:
                    existing_student = row
                    continue  
                updated_rows.append(row)

    if existing_student:
        existing_info = f"ID No.: {existing_student[0]}\nName: {existing_student[1]} {existing_student[2]}\nGender: {existing_student[3]}\nYear Level: {existing_student[4]}\nCollege: {existing_student[5]}\nProgram: {existing_student[6]}"
        confirm = messagebox.askyesno(
            "ID Already Exists",
            f"A student with ID No. {student_id} already exists.\n\n{existing_info}\n\nDo you want to override this student?"
        )
        if not confirm:
            return  

    updated_rows.append(student_data)

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(updated_rows)

    students = load_students()
    filter_students()

    id_no.delete(0, "end")
    id_no.insert(0, "Ex: 1234-5678")
    id_no.config(fg="gray", justify="center")

    last_name.delete(0, "end")
    first_name.delete(0, "end")

    gender_dropdown.set("Select")
    gender_dropdown.configure(foreground="gray")
    year_dropdown.set("Select")
    year_dropdown.configure(foreground="gray")

    college_dropdown.set("") 
    college_dropdown.set("Select") 
    college_dropdown.configure(foreground="gray") 
    program_dropdown.set("")
    program_dropdown["state"] = "normal"  
    program_dropdown.delete(0, "end")  
    program_dropdown.insert(0, "Select College First")  
    program_dropdown["state"] = "readonly"  
    program_dropdown.configure(foreground="gray") 

    saved_label = Label(root, bg="lightgray", width=30, text="Saved Successfully!", fg="green", font=("Arial", 10, "bold"))
    frame.create_window(145, 365, window=saved_label)

    bind_reset_events()


def remove_saved_label(event=None):
    global saved_label
    if saved_label is not None:
        saved_label.destroy()
        saved_label = None

def bind_reset_events():
    for widget in [id_no, last_name, first_name, program_dropdown]:
        widget.bind("<Key>", remove_saved_label)
    for dropdown in [gender_dropdown, year_dropdown, college_dropdown]:
        dropdown.bind("<<ComboboxSelected>>", remove_saved_label)

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    points = [
        x1 + radius, y1, x2 - radius, y1,
        x2, y1, x2, y1 + radius, x2, y2 - radius,
        x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

def on_resize(event):
    global x1,y1
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

def on_add_button_click(event):
    item = side_bar_canvas.find_closest(event.x, event.y)[0]
    if item in [add_button, add_text]:  
        side_bar_canvas.itemconfig(add_button, fill='#2E4D8C')
        side_bar_canvas.itemconfig(add_text, fill='#FFFFFF')
    elif item in [edit_button, edit_text, edit_icon]:  
        side_bar_canvas.itemconfig(edit_button, fill='#153E83')
        side_bar_canvas.itemconfig(edit_text, fill='#FFFFFF')
    elif item in [delete_button, delete_text, delete_icon]:  
        side_bar_canvas.itemconfig(delete_button, fill='#153E83')
        side_bar_canvas.itemconfig(delete_text, fill='#FFFFFF')
    
def button_release(event):
    side_bar_canvas.itemconfig(add_button, fill='#D7E3F5')  
    side_bar_canvas.itemconfig(add_text, fill='#154BA6')
    
    if not is_form_visible: 
        
        side_bar_canvas.configure(bg="lightgray")

        toggle_form()
        frame.grid()
    
def on_hover(event):
    side_bar_canvas.itemconfig(add_button, fill='#A5CAEC')  
    side_bar_canvas.itemconfig(add_text, fill='#154BA6') 
    side_bar_canvas.config(cursor="hand2")
def on_leave(event):
    side_bar_canvas.itemconfig(add_button, fill='white')
    side_bar_canvas.itemconfig(add_text, fill='#2363C6')
    side_bar_canvas.config(cursor="")


is_form_visible = False  
rounded_rectangle_id = None
form_widgets = []

#form

def on_select(event):
    event.widget.configure(foreground="black")

    if event.widget == college_dropdown:
        selected_college = college_dropdown.get()
        
        college_code = selected_college.split(" - ")[0]

        program_names = []
        if os.path.exists(PROGRAM_FILE):
            with open(PROGRAM_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3 and row[2] == college_code:  
                        program_names.append(f"{row[0]} - {row[1]}") 

        program_dropdown["values"] = program_names if program_names else ["No programs available"]
        program_dropdown.set("Select")


def toggle_form():
    global program_dropdown,college_names,frame,sorting,is_form_visible,text, round, form_widgets,last_name,first_name,gender_dropdown,id_no,year_dropdown,college_dropdown,submit_canvas

    if is_form_visible:
        restore_content()
    else:
        is_form_visible = True
        frame = Canvas(content_frame, bg="white", width=350, height=480, bd=0, highlightthickness=0)
        frame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nw")
        if sorting:
            sorting.destroy()
            sorting=None
            sort_canvas.itemconfig(sort_frame, fill="white")

        style = ttk.Style()
        style.configure("Custom.TCombobox", foreground="") 
        style.configure("Custom.TCombobox",relief="flat",foreground="gray")

        form_frame = round = create_rounded_rectangle(frame, -300, 0, 350, 480, radius=130,fill='lightgray')
        form_widgets.append(round)
        frame.tag_bind(form_frame,"<Button-1>",remove)

        text = Label(root,text="Student Form", font=("Arial", 25, "bold"), bg="lightgray",fg="#2363C6")
        frame.create_window(160,30,window=text)
        form_widgets.append(text)

        text2 = Label(root, text="Student's Full Name ", bg="lightgray", font=("Arial", 15, "bold"))
        frame.create_window(112,85,window=text2)
        form_widgets.append(text2)
        
        last_name = Entry(root, font=("Albert Sans", 12, "normal"),width=14)
        frame.create_window(80,110,window=last_name)
        form_widgets.append(last_name)

        last_text = Label(root, text="Last Name ", bg="lightgray", fg="gray", font=("Arial", 10))
        frame.create_window(80,132,window=last_text)
        form_widgets.append(last_text)

        first_name = Entry(root, font=("Albert Sans", 12, "normal"),width=20)
        frame.create_window(245,110,window=first_name)
        form_widgets.append(first_name)

        first_text = Label(root, text="First Name ", bg="lightgray", fg="gray", font=("Arial", 10))
        frame.create_window(245,132,window=first_text)
        form_widgets.append(first_text)

        gender = Label(root, text="Gender", font=('Arial', 15, 'bold'), bg='light gray')
        frame.create_window(50,155,window=gender)
        form_widgets.append(gender)

        gender_dropdown = ttk.Combobox(root,style="Custom.TCombobox",values=["Male", "Female", "Others"], state="readonly", width=14,font=(('Arial', 11, 'normal')))
        frame.create_window(80,180,window=gender_dropdown)
        form_widgets.append(gender_dropdown)
        gender_dropdown.set("Select") 
        gender_dropdown.bind("<<ComboboxSelected>>",on_select)

        id = Label(root, text="ID No.", font=('Arial', 15, 'bold'), bg='light gray')
        frame.create_window(44,210,window=id)
        form_widgets.append(id)

        id_no = Entry(root, font=('Albert Sans', 12, 'normal'),width=14, fg="gray",justify="center")
        frame.create_window(80,233,window=id_no)
        form_widgets.append(id_no)
        id_no.insert(0, "Ex: 1234-5678")
        id_no.bind("<FocusIn>", lambda event: id_no.get() == "Ex: 1234-5678" and (id_no.delete(0, END), id_no.config(fg="black",justify="left")))
        id_no.bind("<FocusOut>", lambda event: id_no.get() == "" and (id_no.insert(0, "Ex: 1234-5678"), id_no.config(fg="gray",justify="center")))

        year = Label(root, text="Year Level", font=('Arial', 15, 'bold'), bg='light gray')
        frame.create_window(210,210,window=year)
        form_widgets.append(year)
        
        year_dropdown = ttk.Combobox(root,style="Custom.TCombobox",values=["1st", "2nd", "3rd", "4th","5+"], state="readonly", width=14,font=('Arial', 11, 'normal'))
        frame.create_window(230,233,window=year_dropdown)
        form_widgets.append(year_dropdown)
        year_dropdown.set("Select") 
        year_dropdown.bind("<<ComboboxSelected>>",on_select)

        load_colleges()
        load_programs()

        college = Label(root, text="College", font=('Arial', 15, 'bold'), bg='light gray')
        frame.create_window(50,263,window=college)
        form_widgets.append(college)
        
        college_dropdown = ttk.Combobox(root, style="Custom.TCombobox", values=list(college_names.keys()), state="readonly", width=37, font=('Arial', 11, 'normal'))
        frame.create_window(175, 287, window=college_dropdown)
        form_widgets.append(college_dropdown)
        college_dropdown.set("Select") 
        college_dropdown.bind("<<ComboboxSelected>>", on_select)

        program = Label(root,text="Program",font=('Arial', 15, 'bold'),bg="light gray")
        frame.create_window(58,317,window=program)
        form_widgets.append(program)

        program_dropdown = ttk.Combobox(root,style="Custom.TCombobox", state="readonly", width=37,font=('Arial', 11, 'normal'))
        frame.create_window(175,340,window=program_dropdown)
        form_widgets.append(program_dropdown)
        program_dropdown.set("Select College First") 
        program_dropdown.bind("<<ComboboxSelected>>",on_select)

        
        def submit_click(event):
            submit_canvas.itemconfig(submit, fill='#153E83')
        def submit_release(event):
            submit_canvas.itemconfig(submit, fill='#2363C6')
            save_to_csv()
            
        def submit_hover(event):
            submit_canvas.itemconfig(submit, fill='#154BA6') 
            submit_canvas.config(cursor="hand2")
        def on_submit_leave(event):
            submit_canvas.itemconfig(submit, fill='#2363C6')
            submit_canvas.config(cursor="")


        def close_click(event):
            close_canvas.itemconfig(close, fill='#872D2D')

        def close_release(event):
            close_canvas.itemconfig(close, fill='#AA4141') 
            if 'saved_label' in globals() and saved_label is not None:
                remove_saved_label()
            restore_content()

        def close_hover(event):
            close_canvas.itemconfig(close, fill='#9B3535') 
            close_canvas.config(cursor="hand2")

        def close_leave(event):
            close_canvas.itemconfig(close, fill='#AA4141')
            close_canvas.config(cursor="")


        submit_canvas = Canvas(root, width=100, height=45, bg="light gray", highlightthickness=0)
        frame.create_window(120,400,window=submit_canvas)
        form_widgets.append(submit_canvas)
        submit = create_rounded_rectangle(submit_canvas, 5, 5, 100, 45, radius=20,fill='#2363C6')
        form_widgets.append(submit)
        submit_canvas.create_text(50, 24, text="Submit", fill="white", font=("Arial", 15, "bold"))
        submit_canvas.bind("<Button-1>", submit_click)
        submit_canvas.bind("<ButtonRelease-1>", submit_release)
        submit_canvas.bind("<Enter>", submit_hover)
        submit_canvas.bind("<Leave>", on_submit_leave)
                

        close_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
        frame.create_window(225,400,window=close_canvas)
        form_widgets.append(close_canvas)
        close = create_rounded_rectangle(close_canvas, 5, 5, 100, 45, radius=20, fill='#AA4141')
        form_widgets.append(close)

        close_canvas.create_text(50, 24, text="Close", fill="white", font=("Arial", 15, "bold"))
        close_canvas.bind("<Button-1>", close_click)
        close_canvas.bind("<ButtonRelease-1>", close_release)
        close_canvas.bind("<Enter>", close_hover)
        close_canvas.bind("<Leave>", close_leave)

def delete_stud(event):
    def trigger_once(event):
        on_leave_delete(event)
        root.unbind("<Motion>")

    root.bind("<Motion>", trigger_once)
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a student to delete.")
        return

    student_data = tree.item(selected_item, "values")
    student_id = student_data[0]

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student ID {student_id}?")
    if not confirm:
        return  

    tree.delete(selected_item)

    global students
    students = [s for s in students if s[0] != student_id]

    updated_rows = []
    with open("students.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row and row[0] != student_id:
                updated_rows.append(row)

    with open("students.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(updated_rows)

    restore_content()
    filter_students()

    messagebox.showinfo("Success", f"Student ID {student_id} has been deleted!")

def edit_stud(event):
    global frame, is_form_visible,sorting

    def trigger_once(event):
        on_leave_edit(event)
        root.unbind("<Motion>")
    root.bind("<Motion>",trigger_once)

    selected_item = tree.selection()
    if not selected_item:  
        messagebox.showwarning("Warning", "Please select a student to edit!")
        return

    student_id = tree.item(selected_item, "values")[0]  
    student_data = find_student_in_csv(student_id)

    if student_data:
        if not is_form_visible:
            side_bar_canvas.configure(bg="lightgray")
            toggle_form()


        populate_form(student_data)

        style = ttk.Style()
        style.configure("Custom.TCombobox", foreground="") 
        style.configure("Custom.TCombobox", foreground="black")


        id_no.config(fg="black",justify="left")
        last_name.config(fg="black")
        first_name.config(fg="black")
        text.configure(text="Edit Form")


        submit_canvas.bind("<ButtonRelease-1>", lambda event: update_student(student_id))

    else:
        messagebox.showerror("Error", "Student not found in the CSV file.")

def update_student(old_id):
    file_path = "students.csv"
    
    last_name_value = last_name.get().title()
    first_name_value = first_name.get().title()
    
    new_data = [
        id_no.get(),
        last_name_value,
        first_name_value,
        gender_dropdown.get(),
        year_dropdown.get(),
        college_dropdown.get(),
        program_dropdown.get()
    ]

    errors = []

    id_pattern = r"^\d{4}-\d{4}$"
    if not re.match(id_pattern, id_no.get()) or any(char.isalpha() for char in id_no.get()):
        errors.append("• ID No. must be in the format XXXX-XXXX (e.g., 2024-1234) and contain only numbers.")

    if any(char.isdigit() for char in last_name_value):
        errors.append("• Last Name must not contain numbers.")
        
    if not all(char.isalpha() or char in [' ', '-'] for char in last_name_value):
        errors.append("• Last Name must contain only letters, spaces, or hyphens.")

    if any(char.isdigit() for char in first_name_value):
        errors.append("• First Name must not contain numbers.")
        
    if not all(char.isalpha() or char in [' ', '-'] for char in first_name_value):
        errors.append("• First Name must contain only letters, spaces, or hyphens.")

    if "" in new_data[:3]: 
        errors.append("• All fields (ID No., Last Name, First Name) must be filled out.")

    if gender_dropdown.get() == "Select":
        errors.append("• Please select a Gender.")

    if year_dropdown.get() == "Select":
        errors.append("• Please select a Year Level.")

    if college_dropdown.get() == "Select":
        errors.append("• Please select a College.")

    if program_dropdown.get() == "Select":
        errors.append("• Please select a valid Program.")

    existing_student = None
    try:
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                if row and row[0] == new_data[0] and row[0] != old_id:
                    existing_student = row
                    break
    except FileNotFoundError:
        errors.append("• Student database (CSV file) not found.")

    if errors:
        messagebox.showerror("Form Error", "There are errors in your form:\n\n" + "\n".join(errors))
        return

    if existing_student:
        existing_info = f"ID No.: {existing_student[0]}\nName: {existing_student[1]} {existing_student[2]}\nGender: {existing_student[3]}\nYear Level: {existing_student[4]}\nCollege: {existing_student[5]}\nProgram: {existing_student[6]}"
        confirm = messagebox.askyesno(
            "ID Already Exists",
            f"A student with ID No. {new_data[0]} already exists.\n\n{existing_info}\n\nDo you want to override this student?"
        )
        if not confirm:
            return

    confirm = messagebox.askyesno("Confirm Update", f"Replace data for student ID {old_id}?")
    if not confirm:
        return

    updated_rows = []
    try:
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                if row and row[0] not in (old_id, new_data[0]):  
                    updated_rows.append(row)

        updated_rows.append(new_data)

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(updated_rows)

        messagebox.showinfo("Success", "Student information updated!")

        global students
        students = load_students()  
        filter_students()  

        restore_content()

    except FileNotFoundError:
        messagebox.showerror("Error", "The student database file could not be found.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred while updating the student record:\n\n{str(e)}")

def bind_button_effects(canvas, button_shape, text_id, default_color, hover_color, click_color, default_text_color, hover_text_color, command):

    def on_click(event):
        canvas.itemconfig(button_shape, fill=click_color)
        canvas.itemconfig(text_id, fill=hover_text_color)

    def on_release(event):
        canvas.itemconfig(button_shape, fill=hover_color)
        canvas.itemconfig(text_id, fill=hover_text_color)
        command()

    def on_hover(event):
        canvas.itemconfig(button_shape, fill=hover_color)
        canvas.itemconfig(text_id, fill=hover_text_color)
        canvas.config(cursor="hand2")

    def on_leave(event):
        canvas.itemconfig(button_shape, fill=default_color)
        canvas.itemconfig(text_id, fill=default_text_color)
        canvas.config(cursor="")

    # Bind events
    canvas.bind("<Button-1>", on_click)
    canvas.bind("<ButtonRelease-1>", on_release)
    canvas.bind("<Enter>", on_hover)
    canvas.bind("<Leave>", on_leave)


def colleges_func(event):
    global manage_text,add_college,view_college,add_canvas,view_canvas,add

    if not is_form_visible: 
        toggle_form()
        frame.config(height=250)
        frame.grid()

        for widget in form_widgets:
            if isinstance(widget, int):  
                if frame.type(widget) != "text" and frame.type(widget) != "rectangle":  
                    frame.delete(widget)  
            else: 
                widget.destroy()  
        side_bar_canvas.configure(bg="lightgray")

        colleges_frame = create_rounded_rectangle(frame, -300, 0, 350, 250, radius=130, fill='lightgray')
        form_widgets.append(colleges_frame)

        manage_text = Label(root, text="Manage Colleges", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
        frame.create_window(160, 30, window=manage_text)
        form_widgets.append(manage_text)

        # Add College Button
        add_canvas = Canvas(root, width=180, height=45, bg="lightgray", highlightthickness=0)
        frame.create_window(165, 90, window=add_canvas)
        form_widgets.append(add_canvas)

        add = create_rounded_rectangle(add_canvas, 5, 5, 180, 45, radius=20, fill='white')
        form_widgets.append(add)
        add_college = add_canvas.create_text(92, 25, text="Add College", fill="black", font=("Arial", 15, "bold"))

        # View Colleges Button
        view_canvas = Canvas(root, width=180, height=45, bg="lightgray", highlightthickness=0)
        frame.create_window(165, 140, window=view_canvas)
        form_widgets.append(view_canvas)

        view = create_rounded_rectangle(view_canvas, 5, 5, 180, 45, radius=20, fill='white')
        form_widgets.append(view)
        view_college = view_canvas.create_text(92, 25, text="View Colleges", fill="black", font=("Arial", 15, "bold"))

        # Close Button
        close_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
        frame.create_window(165, 210, window=close_canvas)
        form_widgets.append(close_canvas)

        close = create_rounded_rectangle(close_canvas, 5, 5, 100, 45, radius=20, fill='#AA4141')
        form_widgets.append(close)
        close_college = close_canvas.create_text(50, 24, text="Close", fill="white", font=("Arial", 15, "bold"))


        bind_button_effects(add_canvas, add, add_college, 
                    default_color="white", hover_color="#1E56A0", click_color="#1B4883",
                    default_text_color="black", hover_text_color="white",
                    command=add_college_function)
        
        bind_button_effects(view_canvas, view, view_college, 
                    default_color="white", hover_color="#1E56A0", click_color="#1B4883",
                    default_text_color="black", hover_text_color="white",
                    command=lambda: print("Add clicked")) 
               
        bind_button_effects(close_canvas, close, close_college, 
                    default_color="#AA4141", hover_color="#C75050", click_color="#B22929",
                    default_text_color="white", hover_text_color="white",
                    command=restore_content)        


COLLEGE_FILE = "colleges.csv"
PROGRAM_FILE = "programs.csv"
college_names = {}

def load_colleges():
    global college_names

    if not os.path.exists(COLLEGE_FILE):
        return

    with open(COLLEGE_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                formatted_college = f"{row[0]} - {row[1]}"
                college_names[formatted_college] = []
def load_programs():
    if not os.path.exists(PROGRAM_FILE):
        return
    
    with open(PROGRAM_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                program_entry = f"{row[0]} - {row[1]}"
                college_code = row[2]

                for college in college_names.keys():
                    if college.startswith(college_code): 
                        college_names[college].append(program_entry)
                        break  
def save_college():
    global college_dropdown, college_names

    college_code_value = course_code.get().strip()
    college_name_value = course_name.get().strip()

    if not college_code_value or not college_name_value:
        messagebox.showerror("Input Error", "All fields are required.")
        return

    college_code_value = college_code_value.upper()

    if not re.fullmatch(r"[A-Z]+", college_code_value):
        messagebox.showerror("Input Error", "College code must contain only letters with no spaces.")
        return

    college_name_value = college_name_value.title()

    if not re.fullmatch(r"[A-Za-z\s-]+", college_name_value):
        messagebox.showerror("Input Error", "College name must contain only letters and dashes.")
        return

    if len(college_code_value) > 10:
        messagebox.showerror("Input Error", "College code must not exceed 10 characters.")
        return

    if len(college_name_value) > 100:
        messagebox.showerror("Input Error", "College name must not exceed 100 characters.")
        return

    formatted_college = f"{college_code_value} - {college_name_value}"

    if formatted_college in college_names:
        messagebox.showinfo("Duplicate Entry", "This college already exists.")
        return

    college_names[formatted_college] = []

    try:
        with open(COLLEGE_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([college_code_value, college_name_value])
    except Exception as e:
        messagebox.showerror("File Error", f"An error occurred while saving: {e}")
        return

    if college_dropdown.winfo_exists():
        college_dropdown["values"] = list(college_names.keys())
        college_dropdown.set(formatted_college)  

    saved_label = Label(root, bg="lightgray", width=30, text="Saved Successfully!", fg="green", font=("Arial", 10, "bold"))
    frame.create_window(175, 180, window=saved_label)

    course_name.delete(0, "end")
    course_name.insert(0, "Ex: College of Computer Studies")
    course_name.config(fg="gray", justify="center")

    course_code.delete(0, "end")
    course_code.insert(0, "Ex: CCS")
    course_code.config(fg="gray", justify="center")

def add_college_function(event=None):
    global course_code,course_name

    restore_content()
    side_bar_canvas.itemconfig(add_button, fill='#D7E3F5')  
    side_bar_canvas.itemconfig(add_text, fill='#154BA6')
    if not is_form_visible: 
        toggle_form()
        frame.config(height=250)
        frame.grid()
        for widget in form_widgets:
            if isinstance(widget, int):  
                if frame.type(widget) != "text" and frame.type(widget) != "rectangle":  
                    frame.delete(widget)  
            else: 
                widget.destroy()  
        side_bar_canvas.configure(bg="lightgray")

        colleges_frame = create_rounded_rectangle(frame, -300, 0, 350, 250, radius=130, fill='lightgray')
        form_widgets.append(colleges_frame)
        manage_text = Label(root, text="Add College", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
        frame.create_window(175, 30, window=manage_text)
        form_widgets.append(manage_text)

        
        style = ttk.Style()
        style.configure("Custom.TCombobox", foreground="") 
        style.configure("Custom.TCombobox",relief="flat",foreground="gray")

        course_code_text = Label(root, text="College Information ", bg="lightgray", fg="black", font=("Arial", 15,"bold"))
        frame.create_window(130,70,window=course_code_text)
        form_widgets.append(course_code_text)

        course = Label(root, text="Course Name ", bg="lightgray", fg="gray", font=("Arial", 10))
        frame.create_window(175,117,window=course)
        form_widgets.append(course)

        course_name = Entry(root, font=('Albert Sans', 12, 'normal'),width=30, fg="gray",justify="center")
        frame.create_window(175,97,window=course_name)
        form_widgets.append(course_name)
        course_name.insert(0, "Ex: College of Computer Studies")
        course_name.bind("<FocusIn>", lambda event: course_name.get() == "Ex: College of Computer Studies" and (course_name.delete(0, END), course_name.config(fg="black",justify="left")))
        course_name.bind("<FocusOut>", lambda event: course_name.get() == "" and (course_name.insert(0, "Ex: College of Computer Studies"), course_name.config(fg="gray",justify="center")))
        
        
        course_text = Label(root, text="Course Code ", bg="lightgray", fg="gray", font=("Arial", 10))
        frame.create_window(175,160,window=course_text)
        form_widgets.append(course_text)

        course_code = Entry(root, font=('Albert Sans', 12, 'normal'),width=14, fg="gray",justify="center")
        frame.create_window(175,140,window=course_code)
        form_widgets.append(course_code)
        course_code.insert(0, "Ex: CCS")
        course_code.bind("<FocusIn>", lambda event: course_code.get() == "Ex: CCS" and (course_code.delete(0, END), course_code.config(fg="black",justify="left")))
        course_code.bind("<FocusOut>", lambda event: course_code.get() == "" and (course_code.insert(0, "Ex: CCS"), course_code.config(fg="gray",justify="center")))


        save_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
        frame.create_window(120, 210, window=save_canvas)
        form_widgets.append(save_canvas)

        save_button = create_rounded_rectangle(save_canvas, 5, 5, 100, 45, radius=20, fill='#2363C6')
        form_widgets.append(save_button)
        save_text = save_canvas.create_text(50, 24, text="Save", fill="white", font=("Arial", 15, "bold"))

        close_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
        frame.create_window(225, 210, window=close_canvas)
        form_widgets.append(close_canvas)

        close = create_rounded_rectangle(close_canvas, 5, 5, 100, 45, radius=20, fill='#AA4141')
        form_widgets.append(close)
        close_college = close_canvas.create_text(50, 24, text="Close", fill="white", font=("Arial", 15, "bold"))        

        bind_button_effects(close_canvas, close, close_college, 
                    default_color="#AA4141", hover_color="#C75050", click_color="#B22929",
                    default_text_color="white", hover_text_color="white",
                    command=restore_content)   
        
        bind_button_effects(save_canvas, save_button, save_text, 
                            default_color="#2363C6", hover_color="#2E5EB5", click_color="#1B3A7E",
                            default_text_color="white", hover_text_color="white",
                            command=save_college)


def programs_func(event):
    colleges_func(event)
    manage_text.config(text="Manage Programs")
    add_canvas.itemconfig(add_college, text="Add Programs")
    view_canvas.itemconfig(view_college,text="View Programs")
    bind_button_effects(add_canvas, add, add_college, 
            default_color="white", hover_color="#1E56A0", click_color="#1B4883",
            default_text_color="black", hover_text_color="white",
            command=add_program_function)
    
    


def save_program():
    selected_college = dropdown.get()
    
    if selected_college == "Select College First":
        messagebox.showerror("Error", "Please select a college before saving.")
        return

    program_name_value = course_name.get().strip()
    program_code_value = course_code.get().strip().upper()

    if not program_name_value or program_name_value == "Ex: Bachelor of Science in Computer Science":
        messagebox.showerror("Error", "Please enter a valid program name.")
        return

    if not program_code_value or program_code_value == "Ex: BSCS":
        messagebox.showerror("Error", "Please enter a valid program code.")
        return

    if not re.fullmatch(r"[A-Z0-9\-]+", program_code_value):
        messagebox.showerror("Input Error", "Program code must contain only uppercase letters, numbers, and dashes.")
        return

    program_name_value = ' '.join([word.capitalize() if len(word) > 2 else word.lower() for word in program_name_value.split()])

    if not re.fullmatch(r"[A-Za-z0-9\s-]+", program_name_value):
        messagebox.showerror("Input Error", "Program name must contain only letters, numbers, and dashes.")
        return

    college_code = selected_college.split(" - ")[0]

    existing_programs = set()
    if os.path.exists(PROGRAM_FILE):
        with open(PROGRAM_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3:
                    existing_programs.add((row[0].upper(), row[2]))

    if (program_code_value, college_code) in existing_programs:
        messagebox.showwarning("Duplicate", f"Program '{program_name_value}' already exists under {selected_college}.")
        return

    with open(PROGRAM_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([program_code_value, program_name_value, college_code])

    messagebox.showinfo("Success", f"Program '{program_name_value}' saved under {selected_college}!")

    course_name.delete(0, END)
    course_name.insert(0, "Ex: Bachelor of Science in Computer Science")
    course_name.config(fg="gray", justify="center")

    course_code.delete(0, END)
    course_code.insert(0, "Ex: BSCS")
    course_code.config(fg="gray", justify="center")

def add_program_function(event=None):
    global dropdown,course_code,course_name

    restore_content()
    side_bar_canvas.itemconfig(add_button, fill='#D7E3F5')  
    side_bar_canvas.itemconfig(add_text, fill='#154BA6')
    if not is_form_visible: 
        toggle_form()
        frame.config(height=300)
        frame.grid()
        for widget in form_widgets:
            if isinstance(widget, int):  
                if frame.type(widget) != "text" and frame.type(widget) != "rectangle":  
                    frame.delete(widget)  
            else: 
                widget.destroy()  
        side_bar_canvas.configure(bg="lightgray")

        colleges_frame = create_rounded_rectangle(frame, -300, 0, 350, 300, radius=130, fill='lightgray')
        form_widgets.append(colleges_frame)
        manage_text = Label(root, text="Add Program", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
        frame.create_window(175, 30, window=manage_text)
        form_widgets.append(manage_text)

        
        style = ttk.Style()
        style.configure("Custom.TCombobox", foreground="") 
        style.configure("Custom.TCombobox",relief="flat",foreground="gray")

        course_code_text = Label(root, text="Program Information ", bg="lightgray", fg="black", font=("Arial", 15,"bold"))
        frame.create_window(130,70,window=course_code_text)
        form_widgets.append(course_code_text)


        dropdown = ttk.Combobox(root, style="Custom.TCombobox", values=list(college_names.keys()), state="readonly", width=35, font=('Arial', 11, 'normal'))
        frame.create_window(175, 100, window=dropdown)
        form_widgets.append(dropdown)
        dropdown.set("Select College First") 
        dropdown.bind("<<ComboboxSelected>>", on_select)

        program_name = Label(root, text="Program Name ", bg="lightgray", fg="gray", font=("Arial", 10))
        frame.create_window(175,155,window=program_name)
        form_widgets.append(program_name)

        course_name = Entry(root, font=('Albert Sans', 12, 'normal'),width=30, fg="gray",justify="center")
        frame.create_window(175,135,window=course_name)
        form_widgets.append(course_name)
        course_name.insert(0, "Ex: Bachelor of Science in Computer Science")
        course_name.bind("<FocusIn>", lambda event: course_name.get() == "Ex: Bachelor of Science in Computer Science" and (course_name.delete(0, END), course_name.config(fg="black",justify="left")))
        course_name.bind("<FocusOut>", lambda event: course_name.get() == "" and (course_name.insert(0, "Ex: Bachelor of Science in Computer Science"), course_name.config(fg="gray",justify="center")))

        program_code = Label(root, text="Program Code ", bg="lightgray", fg="gray", font=("Arial", 10))
        frame.create_window(175,200,window=program_code)
        form_widgets.append(program_code)

        course_code = Entry(root, font=('Albert Sans', 12, 'normal'),width=15, fg="gray",justify="center")
        frame.create_window(175,180,window=course_code)
        form_widgets.append(course_code)
        course_code.insert(0, "Ex: BSCS")
        course_code.bind("<FocusIn>", lambda event: course_code.get() == "Ex: BSCS" and (course_code.delete(0, END), course_code.config(fg="black",justify="left")))
        course_code.bind("<FocusOut>", lambda event: course_code.get() == "" and (course_code.insert(0, "Ex: BSCS"), course_code.config(fg="gray",justify="center")))

        save_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
        frame.create_window(120, 260, window=save_canvas)
        form_widgets.append(save_canvas)

        save_button = create_rounded_rectangle(save_canvas, 5, 5, 100, 45, radius=20, fill='#2363C6')
        form_widgets.append(save_button)
        save_text = save_canvas.create_text(50, 24, text="Save", fill="white", font=("Arial", 15, "bold"))

        close_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
        frame.create_window(225, 260, window=close_canvas)
        form_widgets.append(close_canvas)

        close = create_rounded_rectangle(close_canvas, 5, 5, 100, 45, radius=20, fill='#AA4141')
        form_widgets.append(close)
        close_college = close_canvas.create_text(50, 24, text="Close", fill="white", font=("Arial", 15, "bold"))        

        bind_button_effects(close_canvas, close, close_college, 
                    default_color="#AA4141", hover_color="#C75050", click_color="#B22929",
                    default_text_color="white", hover_text_color="white",
                    command=restore_content)   
        
        bind_button_effects(save_canvas, save_button, save_text, 
                            default_color="#2363C6", hover_color="#2E5EB5", click_color="#1B3A7E",
                            default_text_color="white", hover_text_color="white",
                            command=save_program)

def on_sidebar_resize(event):
    global add_button, add_text, edit_button, edit_text, delete_button, delete_text, colleges_button, colleges_text, programs_button, programs_text
    global edit_icon_img, delete_icon_img, colleges_icon_img, programs_icon_img, delete_icon, edit_icon, colleges_icon, programs_icon
    global on_hover_delete, on_leave_delete, on_hover_edit, on_leave_edit, on_hover_colleges, on_leave_colleges, on_hover_programs, on_leave_programs
    
    side_bar_canvas.delete("all")
    canvas_width = side_bar_canvas.winfo_width()
    canvas_height = side_bar_canvas.winfo_height()

    side_frame = create_rounded_rectangle(side_bar_canvas, -200, 0, canvas_width, canvas_height + 50, radius=130, fill="#2363C6")
    side_bar_canvas.tag_bind(side_frame,"<ButtonRelease-1>",remove)
    
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

    # Add Student Button (remains the same)
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
    icon_x = edit_x1 + 10  # Left inside button
    icon_y = (edit_y1 + edit_y2) // 2
    edit_icon = side_bar_canvas.create_image(icon_x, icon_y, anchor="w", image=edit_icon_img)

    text_x = icon_x + edit_icon_img.width() + icon_text_spacing
    edit_text = side_bar_canvas.create_text(text_x, icon_y, text="Edit Student", fill="white",
                                            font=('Albert Sans', 11, 'normal'), anchor="w")

    # Colleges Button
    colleges_x1 = ((canvas_width - colleges_width) // 2) + offset_x
    colleges_y1 = edit_y2 + delete_to_colleges_spacing
    colleges_x2 = colleges_x1 + colleges_width
    colleges_y2 = colleges_y1 + colleges_height

    colleges_button = create_rounded_rectangle(side_bar_canvas, colleges_x1, colleges_y1, colleges_x2, colleges_y2, radius=20, fill="#2363C6")

    colleges_icon_img = PhotoImage(file="Images/college.png") 
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
    programs_icon_x = programs_x1 + 10
    programs_icon_y = (programs_y1 + programs_y2) // 2
    programs_icon = side_bar_canvas.create_image(programs_icon_x, programs_icon_y, anchor="w", image=programs_icon_img)

    programs_text_x = programs_icon_x + programs_icon_img.width() + icon_text_spacing
    programs_text = side_bar_canvas.create_text(programs_text_x, programs_icon_y, text="Programs", fill="white",
                                                font=('Albert Sans', 11, 'normal'), anchor="w")
    
    def create_button_hover_effects(button, text, hover_fill='#A5CAEC', hover_text_color='#154BA6', 
                                 default_fill='#2363C6', default_text_color='white'):
        def on_hover(event):
            side_bar_canvas.itemconfig(button, fill=hover_fill)  
            side_bar_canvas.itemconfig(text, fill=hover_text_color) 
            side_bar_canvas.config(cursor="hand2")
        
        def on_leave(event):
            side_bar_canvas.itemconfig(button, fill=default_fill)
            side_bar_canvas.itemconfig(text, fill=default_text_color)
            side_bar_canvas.config(cursor="")
    
        return on_hover, on_leave

    #add button
    side_bar_canvas.tag_bind(add_button, "<Enter>", on_hover)
    side_bar_canvas.tag_bind(add_button, "<Leave>", on_leave)
    side_bar_canvas.tag_bind(add_button, "<Button-1>", on_add_button_click)
    side_bar_canvas.tag_bind(add_button, "<ButtonRelease-1>", button_release)

    side_bar_canvas.tag_bind(add_text, "<Enter>", on_hover)
    side_bar_canvas.tag_bind(add_text, "<Leave>", on_leave)
    side_bar_canvas.tag_bind(add_text, "<Button-1>", on_add_button_click)
    side_bar_canvas.tag_bind(add_text, "<ButtonRelease-1>", button_release)

    on_hover_delete, on_leave_delete = create_button_hover_effects(delete_button, delete_text)
    on_hover_edit, on_leave_edit = create_button_hover_effects(edit_button, edit_text)
    on_hover_colleges, on_leave_colleges = create_button_hover_effects(colleges_button, colleges_text)
    on_hover_programs, on_leave_programs = create_button_hover_effects(programs_button, programs_text)

    def bind_button_events(button, icon, text, on_hover_func, on_leave_func, click_func):
        # Button events
        side_bar_canvas.tag_bind(button, "<Leave>", on_leave_func)
        side_bar_canvas.tag_bind(button, "<Button-1>", on_add_button_click)
        side_bar_canvas.tag_bind(button, "<ButtonRelease-1>", click_func)

        # Icon events
        side_bar_canvas.tag_bind(icon, "<Enter>", on_hover_func)
        side_bar_canvas.tag_bind(icon, "<ButtonRelease-1>", click_func)

        # Text events
        side_bar_canvas.tag_bind(text, "<Enter>", on_hover_func)
        side_bar_canvas.tag_bind(text, "<Button-1>", on_add_button_click)
        side_bar_canvas.tag_bind(text, "<ButtonRelease-1>", click_func)

    # Apply bindings
    bind_button_events(edit_button, edit_icon, edit_text, on_hover_edit, on_leave_edit, edit_stud)
    bind_button_events(delete_button, delete_icon, delete_text, on_hover_delete, on_leave_delete, delete_stud)
    bind_button_events(colleges_button, colleges_icon, colleges_text, on_hover_colleges, on_leave_colleges, colleges_func)
    bind_button_events(programs_button, programs_icon, programs_text, on_hover_programs, on_leave_programs, programs_func)
    

def delete_entry():
    search_var.set("")
    search_bar.focus_set()
    cancel_butt.pack_forget()

def on_input_change(*args):
    if search_var.get():
        cancel_butt.lift()
        cancel_butt.pack(side="right",padx=2)

def clear_placeholder(event=None):
    if search_var.get() == "":
        icon_label.place_forget()
        text_label.place_forget()
    search_bar.focus_set()

def restore_placeholder(event=None):
    if search_var.get() == "":
        icon_label.place(x=x1 + -7, y=y1 + -3)
        text_label.place(x=x1 + 15, y=y1 + 1)

def remove_focus(event):
    global sorting
    widget = event.widget

    if isinstance(widget, (Entry, Button, ttk.Combobox, ttk.Treeview, Label, Canvas)):
        return

    tree.selection_remove(tree.selection())
    root.focus_set()
    

def toggle_selection(event):
    clicked_item = tree.identify_row(event.y)
    selected_item = tree.selection()

    if clicked_item in selected_item:
        tree.selection_remove(clicked_item)
    else:
        tree.selection_set(clicked_item)


def on_root_resize(event):
    total_width = root.winfo_width()

    sidebar_width = max(220, min(270, int(total_width * 0.25)))

    root.columnconfigure(0, minsize=sidebar_width)

    side.config(width=sidebar_width)

root = Tk()
root.geometry("1100x605")
root.minsize(510, 200)
root.title(" ")
icon = PhotoImage(file="Images/icon.png")
root.iconphoto(True, icon)
root.configure(bg="white")
root.rowconfigure(1, weight=1)
root.columnconfigure(0,minsize=220)
root.columnconfigure(1,weight=1)


#header
header = Frame(root, bg="white",height=50)
header.grid(row=0, column=0, sticky="nsew",columnspan=2)
header.rowconfigure(0, weight=0)
header.columnconfigure(0, weight=0)
header.columnconfigure(1, weight=1)
header.grid_propagate(False)

text_stud = Label(header, text="Student Information", font=('Albert Sans', 15, 'bold'), bg='white')
text_stud.grid(row=0, column=0, padx=20)

def filter_students():
    global students  

    query = search_var.get().strip().lower().replace(",", "").replace("  ", " ")

    tree.delete(*tree.get_children())

    filtered_students = []
    for student in students:
        student_values = [str(value).lower().replace(",", "").strip() for value in student]

        original_name = student[1].lower().replace(",", "").strip()
        reversed_name = " ".join(reversed(student[1].split(","))).strip().lower()

        gender_value = student_values[2]  # Assuming gender is at index 2

        if query == "male" or query == "female":
            if query == gender_value:
                filtered_students.append(student)
        elif any(query in value for i, value in enumerate(student_values) if i != 2) or query in original_name or query in reversed_name:
            filtered_students.append(student)

    for student in filtered_students:
        tree.insert("", "end", values=student)

    return filtered_students

def on_input_change(*args):
    if search_var.get():
        cancel_butt.lift()
        cancel_butt.pack(side="right", padx=2)
    else:
        cancel_butt.pack_forget()
    filter_students()


search_var = StringVar()
search_var.trace_add("write", on_input_change)
search_frame = Canvas(header, bg="white", height=40, bd=0, highlightthickness=0)
search_frame.grid(row=0, column=1, sticky="nsew", padx=(50, 120), pady=5)

search_bar = Entry(header, textvariable=search_var, bg="#F1F3F8", font=('Albert Sans', 10, 'normal'), fg="gray", borderwidth=0, highlightthickness=0)
search_bar.grid(row=0,column=0,padx=0)

icon1 = PhotoImage(file="Images/SearchIcon.png")
icon_label = Label(search_bar, image=icon1, bg="#F1F3F8", bd=0)
text_image = PhotoImage(file="Images/Search In Here.png")
text_label = Label(search_bar, image=text_image, bg="#F1F3F8", bd=0)

cancel = PhotoImage(file='Images/cancel.png')
cancel_butt = Button(search_bar,image=cancel,bg="#F1F3F8", bd=0,cursor="hand2",command=delete_entry)

search_frame.bind("<Configure>", on_resize)
search_bar.bind("<FocusIn>", clear_placeholder)
search_bar.bind("<FocusOut>", restore_placeholder)
icon_label.bind("<Button-1>",clear_placeholder)
text_label.bind("<Button-1>",clear_placeholder)

root.bind("<Button-1>", remove_focus)


# side frame
side = Frame(root,bg="white")
side.grid(row=1,column=0,sticky="nsew")
side.columnconfigure(0, weight=1)
side.rowconfigure(0,weight=1)
# Side Bar
side_bar_canvas = Canvas(side, bg="white", width=180, height=105, bd=0, highlightthickness=0)
side_bar_canvas.grid(row=0, column=0, sticky="nsew")
side_bar_canvas.bind("<Configure>", on_sidebar_resize)


# content
content_frame = Frame(root,bg="white")
content_frame.grid(row=1,column=1,sticky="nsew")
content_frame.grid_rowconfigure(0, weight=1)
content_frame.grid_columnconfigure(0, weight=1)

student_text = Label(content_frame, background="white", text="STUDENTS", font=("AlbertSans", 20, "bold"))
student_text.grid(row=0, column=0, sticky="nw", pady=15, padx=20)


def restore_content(event=None):
    global is_form_visible, form_widgets
    if is_form_visible:
        for widget in form_widgets:
            if isinstance(widget, int):  
                if frame.type(widget) != "text" and frame.type(widget) != "rectangle":  
                    frame.delete(widget)  
            else: 
                widget.destroy()  
        frame.grid_forget()
        form_widgets.clear()
        is_form_visible = False  

    side_bar_canvas.config(bg="white")

def load_students():
    students = []
    if os.path.exists("students.csv"):
        with open("students.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader) 
            for row in reader:
                if len(row) >= 7: 
                    full_name = f"{row[1]}, {row[2]}" 
                    gender = row[3]
                    year_level = row[4]
                    college = row[5].split(" - ")[0] 
                    program = row[6].split(" - ")[0] if " - " in row[6] else row[6]
                    students.append([row[0], full_name, gender, year_level, college, program])
    return students

def display_students():
    global tree, students, scroll_indicator
    students = load_students()

    columns = ("ID No.", "Name", "Gender", "Year Level", "College", "Program")

    if not hasattr(display_students, "initialized"):
        tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=20, selectmode="browse")

        for col in columns:
            tree.heading(col, text=col, anchor="w")
            if col == "ID No.":
                tree.column(col, anchor="w", width=100)
            elif col == "Name":
                tree.column(col, anchor="w", width=250)
            elif col == "Gender":
                tree.column(col, anchor="w", width=80)
            elif col == "Year Level":
                tree.column(col, anchor="w", width=100)
            elif col == "College":
                tree.column(col, anchor="w", width=80)
            elif col == "Program":
                tree.column(col, anchor="w", width=150)

        tree.grid(row=0, column=0, sticky="nsew", pady=(70, 0), padx=(20, 0))

        style = ttk.Style()
        
        style.configure("Treeview", font=('Albert Sans', 12), rowheight=40, padding=(5, 5), highlightthickness=0, borderwidth=0)
        style.configure("Treeview.Heading", font=('Albert Sans', 15, 'bold'), anchor="w", padding=(1, 8), foreground="#9F9EA1", relief="flat", borderwidth=0)
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map("Treeview", background=[('selected', '#2363C6')])

        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=1.0, rely=0.125, relheight=0.855, anchor="ne")

        scroll_indicator = Canvas(content_frame, height=4, bg="light gray", highlightthickness=0)
        scroll_indicator.place_forget()

        def on_tree_scroll(*args):
            first, last = tree.yview()
            if first > 0:
                tree_x = tree.winfo_x()
                tree_y = tree.winfo_y()
                tree_width = tree.winfo_width()
                heading_height = style.lookup("Treeview.Heading", "padding")[1] * 4.5  # distance from heading

                scroll_indicator.place(x=tree_x, y=tree_y + heading_height, 
                                      width=tree_width - 80,  # scroll indicator width
                                      height=4)
                up_arrow.place(relx=0.97, rely=0.9, anchor="ne")
            else:
                scroll_indicator.place_forget()
                up_arrow.place_forget()

        tree.configure(yscrollcommand=lambda *args: (scrollbar.set(*args), on_tree_scroll(*args)))
        
        def update_scroll_indicator_position(*args):
            if scroll_indicator.winfo_ismapped():
                first, last = tree.yview()
                if first > 0:
                    tree_x = tree.winfo_x()
                    tree_y = tree.winfo_y()
                    tree_width = tree.winfo_width()
                    heading_height = style.lookup("Treeview.Heading", "padding")[1] * 2
                    
                    scroll_indicator.place(x=tree_x, y=tree_y + heading_height, 
                                          width=tree_width - 20, 
                                          height=4)
        
        content_frame.bind("<Configure>", update_scroll_indicator_position)
        
        def scroll_to_top():
            tree.yview_moveto(0)

        def scroll_to_bottom():
            tree.yview_moveto(1)

        up_arrow = Button(content_frame, text="▲", command=scroll_to_top, bg="white", fg="black", font=("Arial", 8, "bold"), bd=0)
        down_arrow = Button(content_frame, text="▼", command=scroll_to_bottom, bg="white", fg="black", font=("Arial", 8, "bold"), bd=0)

        down_arrow.place(relx=0.97, rely=0.95, anchor="ne") 

        def disable_column_drag(event):
            region = tree.identify_region(event.x, event.y)
            if region == "separator" or region == "heading":
                return "break"

        tree.bind('<Button-1>', disable_column_drag, add='+')
        tree.bind('<B1-Motion>', disable_column_drag, add='+')

        display_students.initialized = True

    for row in tree.get_children():
        tree.delete(row)
    for student in students:
        tree.insert("", "end", values=student)

    def resize_columns(event=None):
        total_width = tree.winfo_width()
        tree_font = font.Font(font=('Albert Sans', 12))
        max_width = max([tree_font.measure(tree.set(item, "Name")) for item in tree.get_children()], default=200)
        tree.column("Name", width=max_width + 20)

    tree.bind("<Configure>", resize_columns)
    search_var.trace_add("write", lambda *args: filter_students())

    def toggle_selection(event):
        clicked_item = tree.identify_row(event.y)
        selected_item = tree.selection()

        if clicked_item:
            if clicked_item in selected_item:
                tree.after(1, lambda: tree.selection_remove(clicked_item))
            else:
                tree.after(1, lambda: tree.selection_set(clicked_item))
        else:
            tree.after(1, lambda: tree.selection_remove(selected_item))

    tree.bind("<Button-1>", toggle_selection)

def remove(event):
    root.focus_set()

def sort_click(event):
    sort_canvas.itemconfig(sort_frame, fill="light gray")

sort_order = True

def sort_id():
    global tree, sort_order

    sort_order = not sort_order  
    id_reverse = not sort_order  

    def parse_id(id_str):

        try:
            year, number = map(int, id_str.split("-")) 
            return (year, number)
        except ValueError:
            return (float('inf'), float('inf')) 
    displayed_students = []
    for item in tree.get_children():
        displayed_students.append(tree.item(item, "values")) 
    displayed_students.sort(key=lambda x: parse_id(x[0]), reverse=id_reverse)


    for item in tree.get_children():
        tree.delete(item)

    for student in displayed_students:
        tree.insert("", "end", values=student)

    if id_reverse:
        id_text.configure(text="Descending")
    else:
        id_text.configure(text="Ascending")

def sort_name(event=None):
    global tree, sort_order

    sort_order = not sort_order  
    name_reverse = not sort_order  

    displayed_students = []
    for item in tree.get_children():
        displayed_students.append(tree.item(item, "values"))
    displayed_students.sort(key=lambda x: x[1].strip().lower(), reverse=name_reverse)


    for item in tree.get_children():
        tree.delete(item)

    for student in displayed_students:
        tree.insert("", "end", values=student)

    if name_reverse:
        sort_text.configure(text="Descending")
    else:
        sort_text.configure(text="Ascending")

def sort_click_release(event):
    global sorting,sort_text,id_text

    if sorting:
        sorting.destroy() 
        sorting = None


        sort_canvas.itemconfig(sort_frame, fill="white") 
    else:
        if is_form_visible:
            restore_content()
        style = ttk.Style()
        style.configure("Custom.TCombobox", foreground="") 
        style.configure("Custom.TCombobox",relief="flat",foreground="gray")


        def on_click(event):
            widget = event.widget 

            if widget in [sort_text, name_sort_bg]:  
                name_sort_bg.itemconfig(sort_butt, fill='#A5CAEC')
                sort_text.configure(bg="#A5CAEC", fg="#153E83")

            elif widget in [id_text, id_sort_bg]:  
                id_sort_bg.itemconfig(id_butt, fill='#A5CAEC')
                id_text.configure(bg="#A5CAEC", fg="#153E83")
        
        def id_release(event):
            id_sort_bg.itemconfig(id_butt, fill='#153E83')
            id_text.config(bg='#153E83', fg='white')   
            sort_id()
        def name_release(event):
            name_sort_bg.itemconfig(sort_butt, fill='#153E83')
            sort_text.config(bg='#153E83', fg='white')  
            sort_name()

        def name_sort_hover(event):
            name_sort_bg.itemconfig(sort_butt, fill='#153E83')
            sort_text.config(bg='#153E83', fg='white')  
            name_sort_bg.config(cursor="hand2")
            sort_text.configure(cursor="hand2")

        def name_sort_leave(event):
            name_sort_bg.itemconfig(sort_butt, fill='#2363C6') 
            sort_text.config(bg='#2363C6', fg='white') 
            name_sort_bg.config(cursor="")

        def id_sort_hover(event):
            id_sort_bg.itemconfig(id_butt, fill='#153E83')
            id_text.config(bg='#153E83', fg='white')  
            id_sort_bg.config(cursor="hand2")
            id_text.configure(cursor="hand2")

        def id_sort_leave(event):
            id_sort_bg.itemconfig(id_butt, fill='#2363C6') 
            id_text.config(bg='#2363C6', fg='white') 
            name_sort_bg.config(cursor="")

        sorting = Canvas(content_frame, width=100, height=150, bg="white", highlightthickness=0)
        sorting_frame = create_rounded_rectangle(sorting, 0, 0, 100, 150, radius=20, fill="light gray") 
        sorting.grid(row=0, column=0, sticky="ne", padx=(0, 70))

        sorting.tag_bind(sorting_frame, "<Button-1>", remove)


        sort_by = Label(root,text="Sort By:", font=("Arial", 10, "bold"), bg="light gray",fg="#2363C6")
        sorting.create_window(30,15,window=sort_by)

        name_sort = Label(root,text="Name", font=("Arial", 10, "bold"), bg="light gray",fg="black")
        sorting.create_window(25,40,window=name_sort)

        name_sort_bg = Canvas(root,bg="lightgray",width=80,height=22,bd=0,highlightthickness=0)
        sorting.create_window(45,65,window=name_sort_bg)

        sort_butt = create_rounded_rectangle(name_sort_bg, 0, 0, 80, 22, radius=20, fill="#2363C6") 
        sort_text = Label(root,text="Ascending", font=("Albert Sans", 8, "bold"), bg="#2363C6",fg="white")
        sorting.create_window(45,65,window=sort_text)


        name_sort_bg.bind("<Button-1>",on_click)
        name_sort_bg.bind("<ButtonRelease-1>",name_release)
        sort_text.bind("<Button-1>",on_click)
        sort_text.bind("<ButtonRelease-1>",name_release)

        name_sort_bg.bind("<Enter>",name_sort_hover)
        name_sort_bg.bind("<Leave>",name_sort_leave)
        sort_text.bind("<Enter>",name_sort_hover)
        sort_text.bind("<Leave>",name_sort_leave)

        id_sort = Label(root,text="ID No.", font=("Arial", 10, "bold"), bg="light gray",fg="black")
        sorting.create_window(25,90,window=id_sort)

        id_sort_bg = Canvas(root,bg="lightgray",width=80,height=22,bd=0,highlightthickness=0)
        sorting.create_window(45,115,window=id_sort_bg)

        id_butt = create_rounded_rectangle(id_sort_bg, 0, 0, 80, 22, radius=20, fill="#2363C6") 
        id_text = Label(root,text="Ascending", font=("Albert Sans", 8, "bold"), bg="#2363C6",fg="white")
        sorting.create_window(45,115,window=id_text)

        id_sort_bg.bind("<Button-1>",on_click)
        id_sort_bg.bind("<ButtonRelease-1>",id_release)
        id_text.bind("<Button-1>",on_click)
        id_text.bind("<ButtonRelease-1>",id_release)

        id_sort_bg.bind("<Enter>",id_sort_hover)
        id_sort_bg.bind("<Leave>",id_sort_leave)
        id_text.bind("<Enter>",id_sort_hover)
        id_text.bind("<Leave>",id_sort_leave)

sorting = None
sort_canvas = Canvas(header,width=40,height=40,highlightthickness=0,bd=0,bg="white")
sort_canvas.grid(row=0,column=1,padx=(0,70),pady=0,sticky="e")
sort_frame = create_rounded_rectangle(sort_canvas, 4, 7, 35, 35, radius=20, fill="white") 
sort = PhotoImage(file="Images/sort.png")
sort_canvas.create_image(20, 20, image=sort, anchor="center") 

sort_canvas.bind("<Button-1>",sort_click)
sort_canvas.bind("<ButtonRelease-1>",sort_click_release)

display_students()
root.bind("<Configure>",on_root_resize)
root.mainloop()
