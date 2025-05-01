from tkinter import *
from tkinter import ttk,messagebox
from misc import create_rounded_rectangle,FormManager
from body import refresh_students

def program_form(root, body_frame=None):
    if body_frame is None:
        from body import body
        body_frame = body(root)


    form_frame3 = Canvas(body_frame, bg="white", width=350, height=250, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(form_frame3, -800, 0, 350, 250, radius=130, fill='lightgray')

    manage_text = Label(root, text="Manage Programs", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    form_frame3.create_window(160, 30, window=manage_text)


        # Add College Button
    add_canvas = Canvas(root, width=180, height=45, bg="lightgray", highlightthickness=0)
    form_frame3.create_window(165, 90, window=add_canvas)

    add = create_rounded_rectangle(add_canvas, 5, 5, 180, 45, radius=20, fill='white')
    add_program = add_canvas.create_text(92, 25, text="Add Program", fill="black", font=("Arial", 15, "bold"))

    def on_add_program_click(event):
        form_frame3.destroy()
        new_form = add_program_form(root, body_frame)
        new_form.place(x=0, y=0)

    add_canvas.tag_bind(add, "<Button-1>", on_add_program_click)
    add_canvas.tag_bind(add_program, "<Button-1>", on_add_program_click)

        # View Colleges Button
    view_canvas = Canvas(root, width=180, height=45, bg="lightgray", highlightthickness=0)
    form_frame3.create_window(165, 140, window=view_canvas)

    view = create_rounded_rectangle(view_canvas, 5, 5, 180, 45, radius=20, fill='white')
    view_college = view_canvas.create_text(92, 25, text="View Programs", fill="black", font=("Arial", 15, "bold"))
    def on_view_program_click(event):
        form_frame3.destroy()
        new_form = view_programs_form(root, body_frame)
        new_form.place(x=0, y=0)
    
    view_canvas.tag_bind(view, "<Button-1>", on_view_program_click)
    view_canvas.tag_bind(view_college, "<Button-1>", on_view_program_click) 

        # Close Button
    close_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
    form_frame3.create_window(165, 210, window=close_canvas)

    close = create_rounded_rectangle(close_canvas, 5, 5, 100, 45, radius=20, fill='#AA4141')
    close_college = close_canvas.create_text(50, 24, text="Close", fill="white", font=("Arial", 15, "bold"))

    def close_form():
        form_frame3.destroy()

    def close_hover(event):
        close_canvas.itemconfig(close, fill="#d32f2f")
        close_canvas.config(cursor="hand2")
    
    def close_leave(event):
        close_canvas.itemconfig(close, fill="#AA4141")
        close_canvas.config(cursor="")

    close_canvas.tag_bind(close, "<Enter>", close_hover)
    close_canvas.tag_bind(close_college, "<Enter>", close_hover)
    close_canvas.tag_bind(close, "<Leave>", close_leave)
    close_canvas.tag_bind(close_college, "<Leave>", close_leave)
    close_canvas.tag_bind(close, "<Button-1>", lambda event: close_form())
    close_canvas.tag_bind(close_college, "<Button-1>", lambda event: close_form())
    
    FormManager.show_form(form_frame3)
    return form_frame3

def add_program_form(root, body_frame=None, edit_mode=False, program_id=None, program_name=None, program_code=None, college_id=None):
    from database import get_all_colleges, update_program, save_program
    global back_icon
    
    if body_frame is None:
        from body import body
        body_frame = body(root)

    form_frame3 = Canvas(body_frame, bg="white", width=350, height=350, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(form_frame3, -300, 0, 350, 350, radius=130, fill='lightgray')

    # Set the title based on mode (Add or Edit)
    title_text = "Edit Program" if edit_mode else "Add Program"
    manage_text = Label(root, text=title_text, font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    form_frame3.create_window(175, 30, window=manage_text)

    back_icon = PhotoImage(file="Images/back.png")

    back_canvas3 = Canvas(root, width=30, height=30, bg="lightgray", highlightthickness=0)
    image_id = back_canvas3.create_image(15, 15, image=back_icon, anchor="center")

    form_frame3.create_window(20, 25, window=back_canvas3)

    def on_hover(event):
        overlapping = back_canvas3.find_overlapping(event.x, event.y, event.x, event.y)
        if image_id in overlapping:
            back_canvas3.config(cursor="hand2")  
        else:
            back_canvas3.config(cursor="")
            
    def go_back(event):
        form_frame3.destroy()
        if edit_mode:
            view_form = view_programs_form(root, body_frame)
            view_form.place(x=0, y=0)
        else:
            program_form_canvas = program_form(root, body_frame)  
            program_form_canvas.place(x=0, y=0)

    back_canvas3.bind("<Button-1>", go_back)
    back_canvas3.bind("<Motion>", on_hover)
    back_canvas3.bind("<Leave>", lambda event: back_canvas3.config(cursor=""))

    style = ttk.Style()
    style.configure("Custom.TCombobox", foreground="") 
    style.configure("Custom.TCombobox", relief="flat", foreground="gray")
    
    # Add Program Form
    title = Label(root, text="Program Information", bg="lightgray", font=("Arial", 15, "bold"))
    form_frame3.create_window(130, 70, window=title)

    # Program Name
    name_label = Label(root, text="Program Name", bg="lightgray", font=("Arial", 10, "bold"))
    form_frame3.create_window(175, 117, window=name_label)

    add_name = Entry(root, font=('Albert Sans', 12, 'normal'), width=30, fg="gray", justify="center")
    form_frame3.create_window(175, 97, window=add_name)
    
    if edit_mode and program_name:
        add_name.delete(0, END)
        add_name.insert(0, program_name)
        add_name.config(fg="black", justify="left")
    else:
        add_name.insert(0, "Ex: Bachelor of Science in Information Technology")
        add_name.bind("<FocusIn>", lambda event: add_name.get() == "Ex: Bachelor of Science in Information Technology" and (add_name.delete(0, END), add_name.config(fg="black",justify="left")))
        add_name.bind("<FocusOut>", lambda event: add_name.get() == "" and (add_name.insert(0, "Ex: Bachelor of Science in Information Technology"), add_name.config(fg="gray",justify="center")))

    # Program Code
    code_label = Label(root, text="Program Code", bg="lightgray", font=("Arial", 10, "bold"))
    form_frame3.create_window(175, 160, window=code_label)
    
    program_code_entry = Entry(root, font=('Albert Sans', 12, 'normal'), width=30, fg="gray", justify="center")
    form_frame3.create_window(175, 140, window=program_code_entry)
    
    if edit_mode and program_code:
        program_code_entry.delete(0, END)
        program_code_entry.insert(0, program_code)
        program_code_entry.config(fg="black", justify="left")
    else:
        program_code_entry.insert(0, "Ex: BSIT")
        program_code_entry.bind("<FocusIn>", lambda event: program_code_entry.get() == "Ex: BSIT" and (program_code_entry.delete(0, END), program_code_entry.config(fg="black",justify="left")))
        program_code_entry.bind("<FocusOut>", lambda event: program_code_entry.get() == "" and (program_code_entry.insert(0, "Ex: BSIT"), program_code_entry.config(fg="gray",justify="center")))

    # College Selection
    college_label = Label(root, text="Select College", bg="lightgray", font=("Arial", 10, "bold"))
    form_frame3.create_window(175, 203, window=college_label)
    
    # Get all colleges for dropdown
    colleges = get_all_colleges()
    college_options = []
    college_ids = {}
    selected_index = 0
    
    for i, college in enumerate(colleges):
        college_name = f"{college['code']} - {college['name']}"
        college_options.append(college_name)
        college_ids[college_name] = college['id']
        
        if edit_mode and college_id and college['id'] == college_id:
            selected_index = i
    
    college_var = StringVar()
    college_dropdown = ttk.Combobox(root, textvariable=college_var, values=college_options, 
                                   style="Custom.TCombobox", width=30, font=('Arial', 11, 'normal'))
    form_frame3.create_window(175, 183, window=college_dropdown)
    
    if edit_mode and selected_index < len(college_options):
        college_dropdown.current(selected_index)
    else:
        college_dropdown.set("Select College")

    # Button text changes based on mode
    button_text = "Update" if edit_mode else "Save"
    save_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
    form_frame3.create_window(120, 300, window=save_canvas)
    save_button = create_rounded_rectangle(save_canvas, 5, 5, 100, 45, radius=20, fill='#2363C6')
    save_text = save_canvas.create_text(50, 24, text=button_text, fill="white", font=("Arial", 15, "bold"))

    # Close Button
    close_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
    form_frame3.create_window(225, 300, window=close_canvas)
    close = create_rounded_rectangle(close_canvas, 5, 5, 100, 45, radius=20, fill='#AA4141')
    close_college = close_canvas.create_text(50, 24, text="Close", fill="white", font=("Arial", 15, "bold"))
    
    def submit_form():
        from body import refresh_students
        name = add_name.get()
        code = program_code_entry.get()
        selected_college = college_var.get()
        
        # Basic validation
        if name == "Ex: Bachelor of Science in Information Technology" or name.strip() == "":
            messagebox.showerror("Error", "Please enter a program name")
            return
            
        if code == "Ex: BSIT" or code.strip() == "":
            messagebox.showerror("Error", "Please enter a program code")
            return
            
        if selected_college == "Select College" or selected_college.strip() == "":
            messagebox.showerror("Error", "Please select a college")
            return
        
        # Get college_id from selected college
        selected_college_id = college_ids.get(selected_college)
        if not selected_college_id:
            messagebox.showerror("Error", "Invalid college selection")
            return
            
        # Save to database or update existing record
        if edit_mode:
            success, message = update_program(program_id, name, code, selected_college_id)
            if success:
                messagebox.showinfo("Success", message)
                go_back(None)
                refresh_students()  # Refresh student list if needed
            else:
                messagebox.showerror("Error", message)
        else:
            # Original save logic for new program
            success, message = save_program(name, code, selected_college_id)
            if success:
                messagebox.showinfo("Success", message)
                # Clear the form
                add_name.delete(0, END)
                add_name.insert(0, "Ex: Bachelor of Science in Information Technology")
                add_name.config(fg="gray", justify="center")
                
                program_code_entry.delete(0, END)
                program_code_entry.insert(0, "Ex: BSIT")
                program_code_entry.config(fg="gray", justify="center")
                
                college_dropdown.set("Select College")
            else:
                messagebox.showerror("Error", message)
    
    def save_hover(event):
        save_canvas.itemconfig(save_button, fill="#1A4A99")
        save_canvas.config(cursor="hand2")
    
    def save_leave(event):
        save_canvas.itemconfig(save_button, fill="#2363C6")
        save_canvas.config(cursor="")

    save_canvas.tag_bind(save_button, "<Enter>", save_hover)
    save_canvas.tag_bind(save_text, "<Enter>", save_hover)
    save_canvas.tag_bind(save_button, "<Leave>", save_leave)
    save_canvas.tag_bind(save_text, "<Leave>", save_leave)
    save_canvas.tag_bind(save_button, "<Button-1>", lambda event: submit_form())
    save_canvas.tag_bind(save_text, "<Button-1>", lambda event: submit_form())

    def close_form():
        form_frame3.destroy()

    def close_hover(event):
        close_canvas.itemconfig(close, fill="#d32f2f")
        close_canvas.config(cursor="hand2")
    
    def close_leave(event):
        close_canvas.itemconfig(close, fill="#AA4141")
        close_canvas.config(cursor="")

    close_canvas.tag_bind(close, "<Enter>", close_hover)
    close_canvas.tag_bind(close_college, "<Enter>", close_hover)
    close_canvas.tag_bind(close, "<Leave>", close_leave)
    close_canvas.tag_bind(close_college, "<Leave>", close_leave)
    close_canvas.tag_bind(close, "<Button-1>", lambda event: close_form())
    close_canvas.tag_bind(close_college, "<Button-1>", lambda event: close_form())

    FormManager.show_form(form_frame3)
    return form_frame3

def view_programs_form(root, body_frame=None):
    from database import get_all_programs, delete_program
    global back_icon
    
    if body_frame is None:
        from body import body
        body_frame = body(root)
    
    form_frame = Canvas(body_frame, bg="white", width=600, height=400, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(form_frame, -300, 0, 600, 400, radius=130, fill='lightgray')
    
    # Header
    title_text = Label(root, text="View Programs", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    form_frame.create_window(300, 30, window=title_text)
    
    # Back button
    back_icon = PhotoImage(file="Images/back.png")
    back_canvas = Canvas(root, width=30, height=30, bg="lightgray", highlightthickness=0)
    image_id = back_canvas.create_image(15, 15, image=back_icon, anchor="center")
    form_frame.create_window(20, 25, window=back_canvas)
    
    def go_back(event):
        form_frame.destroy()
        program_form_canvas = program_form(root, body_frame)
        program_form_canvas.place(x=0, y=0)
    
    back_canvas.bind("<Button-1>", go_back)
    
    # Create treeview for program list
    style = ttk.Style()
    style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white", font=("Arial", 12))
    style.map('Treeview', background=[('selected', '#2363C6')])
    
    # Create frame for treeview
    tree_frame = Frame(root, bg="lightgray")
    form_frame.create_window(300, 200, window=tree_frame, width=550, height=250)
    
    # Scrollbar
    scroll_y = Scrollbar(tree_frame, orient="vertical")
    scroll_y.pack(side=RIGHT, fill=Y)
    
    # Create Treeview with ID as a hidden column
    columns = ("ID", "Program Code", "Program Name", "College", "College ID")
    program_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scroll_y.set, selectmode="browse")
    
    # Configure columns
    program_tree.heading("ID", text="ID")
    program_tree.heading("Program Code", text="Program Code")
    program_tree.heading("Program Name", text="Program Name")
    program_tree.heading("College", text="College")
    program_tree.heading("College ID", text="College ID")

    # Hide ID and College ID columns
    program_tree.column("ID", width=0, stretch=NO)
    program_tree.column("Program Code", width=100, anchor=W)
    program_tree.column("Program Name", width=250, anchor=CENTER)
    program_tree.column("College", width=200, anchor=CENTER)
    program_tree.column("College ID", width=0, stretch=NO)
    
    scroll_y.config(command=program_tree.yview)
    program_tree.pack(fill=BOTH, expand=1)
    
    # Load data
    def load_programs():
        for item in program_tree.get_children():
            program_tree.delete(item)
        
        # Get programs from database
        programs = get_all_programs()
        for program in programs:
            program_tree.insert("", END, values=(
                program['id'],
                program['code'], 
                program['name'], 
                f"{program['college_code']} - {program['college_name']}",
                program['college_id']
            ))
    
    load_programs()
    
    button_frame = Frame(root, bg="lightgray")
    form_frame.create_window(300, 350, window=button_frame)
    
    # Edit button
    def edit_selected():
        selected_item = program_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a program to edit")
            return
        
        # Get values from the selected item
        item_values = program_tree.item(selected_item[0], "values")
        program_id = item_values[0]
        program_code = item_values[1]
        program_name = item_values[2]
        college_id = item_values[4]
        
        form_frame.destroy()
        edit_form = add_program_form(root, body_frame, edit_mode=True, program_id=program_id,
                                  program_name=program_name, program_code=program_code, college_id=college_id)
        edit_form.place(x=0, y=0)
    
    edit_btn = Button(button_frame, text="Edit", command=edit_selected, bg="#2363C6", fg="white", 
                     font=("Arial", 12), padx=20, pady=5, border=0)
    edit_btn.pack(side=LEFT, padx=10)
    
    # Delete button
    def delete_selected():
        selected_item = program_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a program to delete")
            return
        
        item_values = program_tree.item(selected_item[0], "values")
        program_id = item_values[0]
        program_name = item_values[2]
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{program_name}'?\n"
            "All enrolled students will be moved to an 'N/A' program."
        )
        
        if confirm:
            success, message = delete_program(program_id)
            if success:
                messagebox.showinfo("Success", message)
                load_programs()  # Refresh the list
                refresh_students()  
            else:
                messagebox.showerror("Error", message)

    delete_btn = Button(button_frame, text="Delete", command=delete_selected, bg="#AA4141", fg="white", 
                       font=("Arial", 12), padx=20, pady=5, border=0)
    delete_btn.pack(side=LEFT, padx=10)
    
    # Close button
    def close_form():
        form_frame.destroy()
    close_btn = Button(button_frame, text="Close", command=close_form, bg="#555555", fg="white", 
                      font=("Arial", 12), padx=20, pady=5, border=0)
    close_btn.pack(side=LEFT, padx=10)
    FormManager.show_form(form_frame)
    return form_frame