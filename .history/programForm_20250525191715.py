from tkinter import *
from tkinter import ttk,messagebox
from misc import create_rounded_rectangle,FormManager,bind_button_effects,on_select,remove_focus
from body import refresh_students

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
            program_form_canvas = view_programs_form(root, body_frame)  
            program_form_canvas.place(x=0, y=0)

    back_canvas3.bind("<Button-1>", go_back)
    back_canvas3.bind("<Motion>", on_hover)
    back_canvas3.bind("<Leave>", lambda event: back_canvas3.config(cursor="",bg="light gray"))

    style = ttk.Style()
    style.configure("Gray.TCombobox", 
                foreground="gray", 
                font=('Albert Sans', 11),
                relief="flat")
    style.configure("Black.TCombobox", 
                foreground="black", 
                font=('Albert Sans', 11),
                relief="flat")
    
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
    selected_college_display = ""  

    for college in colleges:
        college_display = f"{college['code']} - {college['name']}"
        college_options.append(college_display)
        college_ids[college_display] = college['id']
        
        if edit_mode and college_id and college['id'] == college_id:
            selected_college_display = college_display  # Store the matching display text
            
    
    college_var = StringVar()
    college_dropdown = ttk.Combobox(root, textvariable=college_var, values=college_options, state="readonly",
                                style="Gray.TCombobox", width=30, font=('Arial', 11, 'normal'),postcommand=lambda: college_dropdown.configure(style="Gray.TCombobox"))
    form_frame3.create_window(175, 183, window=college_dropdown)

    # Set the selected college if we're in edit mode
    if edit_mode and selected_college_display:
        college_var.set(selected_college_display)
        for college in colleges:
            if college['id'] == college_id:
                college_dropdown.set(f"{college['code']} - {college['name']}")
                college_dropdown.configure(style="Black.TCombobox")
                break
    else:
        college_dropdown.set("Select College")
        college_dropdown.configure(style="Gray.TCombobox")

    college_dropdown.bind("<<ComboboxSelected>>",on_select)
    
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
        
        if name == "Ex: Bachelor of Science in Information Technology" or name.strip() == "":
            messagebox.showerror("Error", "Please enter a program name")
            return
        if name.upper() == "N/A":
            messagebox.showerror("Error", "Cannot create program with name 'N/A'")
            return
                
        if code == "Ex: BSIT" or code.strip() == "":
            messagebox.showerror("Error", "Please enter a program code")
            return
            
        if selected_college == "Select College" or selected_college.strip() == "":
            messagebox.showerror("Error", "Please select a college")
            return
        
        selected_college_id = college_ids.get(selected_college)
        if not selected_college_id:
            messagebox.showerror("Error", "Invalid college selection")
            return
            
        if edit_mode:
            success, message = update_program(program_id, name, code, selected_college_id)
            if success:
                messagebox.showinfo("Success", message)
                go_back(None)
                refresh_students()  
            else:
                messagebox.showerror("Error", message)
        else:
            success, message = save_program(name, code, selected_college_id)
            if success:
                messagebox.showinfo("Success", message)
                add_name.delete(0, END)
                add_name.insert(0, "Ex: Bachelor of Science in Information Technology")
                add_name.config(fg="gray", justify="center")
                
                program_code_entry.delete(0, END)
                program_code_entry.insert(0, "Ex: BSIT")
                program_code_entry.config(fg="gray", justify="center")
                
                college_var.set("Select College") 
                college_dropdown.configure(style="Gray.TCombobox")

                college_dropdown.update_idletasks()
                form_frame3.update_idletasks()

                root.focus_set()
                
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
    from database import get_all_programs, delete_program, get_all_colleges
    global back_icon, sort_order, sort_button_text, original_colors,icon1,cancel,text_image
    
    if body_frame is None:
        from body import body
        body_frame = body(root)
    
    sort_order = "ascending"
    
    form_frame = Canvas(body_frame, bg="white", width=700, height=450, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(form_frame, -300, 0, 700, 450, radius=130, fill='lightgray')
    
    # Header
    title_text = Label(root, text="Programs", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    form_frame.create_window(350, 30, window=title_text)
    
    # Search functionality
    program_var = StringVar()
    college_var = StringVar()
    
    def program_search(*args):
        if program_var.get():
            cancel_butt.place(x=260, y=4)
        else:
            cancel_butt.place_forget()
        program_filter()
        
    def clear_placeholder(event=None):
        if program_var.get() == "":
            icon4.place_forget()
            icon5.place_forget()
        program_search_bar.focus_set()
    
    def restore_placeholder(event=None):
        if program_var.get() == "":
            icon4.place(x=2, y=3)
            icon5.place(x=25, y=7)
            
    def program_filter(*args):
        search_term = program_var.get().lower()
        selected_college = college_var.get()
        
        # Get programs from database
        programs = get_all_programs()
        
        # Clear existing data
        program_table.delete(*program_table.get_children())
        original_colors.clear()
        
        # Filter programs
        filtered_programs = []
        for program in programs:
            # Skip if college filter is set and doesn't match
            if selected_college != "All Colleges" and program['college_code'] != selected_college:
                continue
                
            # Skip if search term doesn't match
            if search_term and (search_term not in program['code'].lower() and 
                               search_term not in program['name'].lower()):
                continue
                
            filtered_programs.append((
                program['code'],
                program['name'],
                program['college_code']
            ))
        
        # Sort based on current order
        if sort_order == "ascending":
            filtered_programs.sort(key=lambda x: x[0])  # Sort by program code
        else:
            filtered_programs.sort(key=lambda x: x[0], reverse=True)
        
        for program in filtered_programs:
            row_id = program_table.insert("", "end", values=program, tags=("normal",))
            original_colors[row_id] = "normal"
    
    def clear_search(event=None):
        program_var.set("")
        program_filter()
        cancel_butt.place_forget()
        
    def toggle_sort_order():
        global sort_order, sort_button_text
        if sort_order == "ascending":
            sort_order = "descending"
            sort_button_text.config(text="Descending")
        else:
            sort_order = "ascending"
            sort_button_text.config(text="Ascending")
        program_filter()
    
    # Search bar
    search_canvas = Canvas(root, width=300, height=33, bg="lightgray", highlightthickness=0)
    form_frame.create_window(162, 75, window=search_canvas)
    
    program_search_bar = Entry(root, textvariable=program_var, bg="white", font=('Albert Sans', 12, 'normal'), 
                             fg="gray", borderwidth=0, highlightthickness=0)
    form_frame.create_window(22, 65, window=program_search_bar, anchor="nw", width=284, height=25)
    
    
    icon1 = PhotoImage(file="Images/SearchIcon.png")
    icon4 = Label(program_search_bar, image=icon1, bg="white", bd=0)
    icon4.place(x=2, y=3)
    
    cancel = PhotoImage(file='Images/cancel.png')
    cancel_butt = Button(program_search_bar, image=cancel, bg="white", activebackground="white", 
                        bd=0, cursor="hand2", command=clear_search)
    
    text_image = PhotoImage(file="Images/Search In Here.png")
    icon5 = Label(program_search_bar, image=text_image, bg="white", bd=0)
    icon5.place(x=25, y=7)
    
    search = create_rounded_rectangle(search_canvas, 5, 3, 300, 33, radius=20, fill='white')
    
    program_var.trace_add("write", program_search)
    program_search_bar.bind("<FocusIn>", clear_placeholder)
    program_search_bar.bind("<FocusOut>", restore_placeholder)
    icon4.bind("<Button-1>", clear_placeholder)
    icon5.bind("<Button-1>", clear_placeholder)
    
    
    # College filter dropdown
    filter_label = Label(root, text="Filter by College:", font=("Arial", 12, "bold"), 
                        bg="lightgray", fg="black")
    form_frame.create_window(385, 77, window=filter_label)
    
    # Get colleges for dropdown
    colleges = get_all_colleges()
    college_list = ["All Colleges"] + [college['code'] for college in colleges]
    college_var.set(college_list[0])
    
    college_dropdown = ttk.Combobox(root, textvariable=college_var, values=college_list, 
                                   state="readonly", width=14, font=("Arial", 11))
    form_frame.create_window(520, 77, window=college_dropdown)
    college_var.trace("w", lambda *args: program_filter())
    
    # Create treeview for program list
    style = ttk.Style()
    style.configure("Custom.Treeview", background="white", foreground="black", 
                   rowheight=25, fieldbackground="white", font=("Arial", 10))
    style.configure("Custom.Treeview.Heading", background="white", foreground="black", 
                   font=("Arial", 10, "bold"), relief="flat")
    style.map("Custom.Treeview", background=[("selected", "#2E5EB5")])
    
    # Create frame for treeview
    table_frame = Frame(root)
    columns = ("#1", "#2", "#3", "#4")
    program_table = ttk.Treeview(table_frame, style="Custom.Treeview", columns=columns, 
                               show="headings", height=7)
    
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=program_table.yview)
    program_table.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side="right", fill="y")
    program_table.pack(side="left", fill="both", expand=True)
    
    program_table.heading("#1", text="Program Code")
    program_table.heading("#2", text="Program Name")
    program_table.heading("#3", text="College Code")
    program_table.heading("#4", text="Num. of Students")
    
    program_table.column("#1", width=120, anchor="w")
    program_table.column("#2", width=280, anchor="w")
    program_table.column("#3", width=120, anchor="center")
    program_table.column("#4", width=130, anchor="center")
    
    program_table.tag_configure("hover", background="#C5D5F0")
    
    def disable_column_drag(event):
        region = program_table.identify_region(event.x, event.y)
        if region == "separator" or region == "heading":
            return "break"
    
    program_table.bind('<Button-1>', disable_column_drag, add='+')
    program_table.bind('<B1-Motion>', disable_column_drag, add='+')
    
    form_frame.create_window(350, 210, window=table_frame)
    
    original_colors = {}
    
    # Hover effects
    hovered_row = None
    
    def on_hover(event):
        nonlocal hovered_row
        row_id = program_table.identify_row(event.y)
        
        if hovered_row and (hovered_row != row_id or not row_id):
            if hovered_row in original_colors:
                program_table.item(hovered_row, tags=(original_colors[hovered_row],))
            hovered_row = None
        
        if row_id and row_id != hovered_row:
            hovered_row = row_id
            if row_id in original_colors:
                program_table.item(row_id, tags=("hover",))
    
    def on_leave(event):
        nonlocal hovered_row
        if hovered_row and hovered_row in original_colors:
            program_table.item(hovered_row, tags=(original_colors[hovered_row],))
        hovered_row = None
    
    program_table.bind("<Motion>", on_hover)
    program_table.bind("<Leave>", on_leave)
    
    # Buttons
    # Add Button
    add_canvas = Canvas(root, width=100, height=30, bg="lightgray", highlightthickness=0)
    form_frame.create_window(57, 340, window=add_canvas)
    
    add = create_rounded_rectangle(add_canvas, 5, 5, 100, 30, radius=20, fill='#2363C6')
    adding_text = add_canvas.create_text(50, 17, text="Add", fill="white", font=("Arial", 12, "bold"))
    
    # Edit Button
    edit_canvas = Canvas(root, width=100, height=30, bg="lightgray", highlightthickness=0)
    form_frame.create_window(157, 340, window=edit_canvas)
    
    edit_button = create_rounded_rectangle(edit_canvas, 5, 5, 100, 30, radius=20, fill='#2363C6')
    edit_text = edit_canvas.create_text(50, 17, text="Edit", fill="white", font=("Arial", 12, "bold"))
    
    # Delete Button
    delete_canvas = Canvas(root, width=100, height=30, bg="lightgray", highlightthickness=0)
    form_frame.create_window(257, 340, window=delete_canvas)
    
    delete = create_rounded_rectangle(delete_canvas, 5, 5, 100, 30, radius=20, fill='#AA4141')
    delete_text = delete_canvas.create_text(50, 17, text="Delete", fill="white", font=("Arial", 12, "bold"))
    
    # Close Button
    close_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
    form_frame.create_window(350, 400, window=close_canvas)
    
    close = create_rounded_rectangle(close_canvas, 5, 5, 100, 45, radius=20, fill='#AA4141')
    close_college = close_canvas.create_text(50, 24, text="Close", fill="white", font=("Arial", 15, "bold"))
    
    # Sort Button
    name_sort_bg = Canvas(root, bg="lightgray", width=80, height=22, bd=0, highlightthickness=0)
    form_frame.create_window(635, 77, window=name_sort_bg)
    
    sort_button = create_rounded_rectangle(name_sort_bg, 0, 0, 80, 22, radius=20, fill="#2363C6")
    
    sort_button_text = Label(root, text="Ascending", font=("Albert Sans", 8, "bold"), 
                           bg="#2363C6", fg="white")
    form_frame.create_window(635, 77, window=sort_button_text)
    
    name_sort_bg.bind("<Button-1>", lambda e: toggle_sort_order())
    sort_button_text.bind("<Button-1>", lambda e: toggle_sort_order())
    
    def name_sort_hover(event):
        name_sort_bg.itemconfig(sort_button, fill="#1E56A0")
        sort_button_text.config(bg="#1E56A0")
    
    def name_sort_leave(event):
        name_sort_bg.itemconfig(sort_button, fill="#2363C6")
        sort_button_text.config(bg="#2363C6")
    
    name_sort_bg.bind("<Enter>", name_sort_hover)
    name_sort_bg.bind("<Leave>", name_sort_leave)
    sort_button_text.bind("<Enter>", name_sort_hover)
    sort_button_text.bind("<Leave>", name_sort_leave)
    
    # Button commands
    def add_selected():
        form_frame.destroy()
        new_form = add_program_form(root, body_frame)
        new_form.place(x=0, y=0)
    
    def edit_selected():
        selected_item = program_table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a program to edit")
            return
        
        # Configure styles for editing
        style = ttk.Style()
        style.configure("Black.TCombobox", foreground="black", relief="flat")
        style.configure("Black.TEntry", foreground="black")
        
        item_values = program_table.item(selected_item[0], "values")
        program_code = item_values[0]
        program_name = item_values[1]
        
        # Get the program ID from database
        programs = get_all_programs()
        program = next((p for p in programs if p['code'] == program_code and p['name'] == program_name), None)
        
        if program:
            form_frame.destroy()
            edit_form = add_program_form(root, body_frame, edit_mode=True, 
                                    program_id=program['id'], 
                                    program_name=program['name'], 
                                    program_code=program['code'],
                                    college_id=program['college_id'])
            
            # Force black text for all fields in edit mode
            for widget in edit_form.winfo_children():
                if isinstance(widget, ttk.Combobox):
                    widget.configure(style="Black.TCombobox")
                elif isinstance(widget, Entry):
                    widget.configure(foreground="black")
            
            edit_form.place(x=0, y=0)
    
    def delete_selected():
        selected_item = program_table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a program to delete")
            return
        
        item_values = program_table.item(selected_item[0], "values")
        program_code = item_values[0]
        program_name = item_values[1]
        
        # Get the program ID from database
        programs = get_all_programs()
        program = next((p for p in programs if p['code'] == program_code and p['name'] == program_name), None)
        
        if program:
            confirm = messagebox.askyesno("Confirm Delete", 
                f"Are you sure you want to delete {program_name}?")
            
            if confirm:
                success, message = delete_program(program['id'])
                if success:
                    messagebox.showinfo("Success", message)
                    program_filter()
                    from body import refresh_students
                    refresh_students()
                else:
                    messagebox.showerror("Error", message)
    
    def close_form():
        form_frame.destroy()
    
    # Bind button effects
    bind_button_effects(add_canvas, add, adding_text,
                default_color="#2363C6", hover_color="#1E56A0", click_color="#1B4883",
                default_text_color="white", hover_text_color="white",
                command=add_selected)
    
    bind_button_effects(edit_canvas, edit_button, edit_text,
                default_color="#2363C6", hover_color="#1E56A0", click_color="#1B4883",
                default_text_color="white", hover_text_color="white",
                command=edit_selected)
    
    bind_button_effects(delete_canvas, delete, delete_text,
                default_color="#AA4141", hover_color="#C75050", click_color="#B22929",
                default_text_color="white", hover_text_color="white",
                command=delete_selected)
    
    bind_button_effects(close_canvas, close, close_college,
                default_color="#AA4141", hover_color="#C75050", click_color="#B22929",
                default_text_color="white", hover_text_color="white",
                command=close_form)
    
    # Initial data load
    program_filter()
    
    FormManager.show_form(form_frame)
    return form_frame