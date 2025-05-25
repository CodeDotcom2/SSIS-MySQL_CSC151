from tkinter import *
from tkinter import ttk,messagebox
from misc import create_rounded_rectangle,FormManager,bind_button_effects,set_root
from database import save_college
import re

#college 

def view_colleges_form(root, body_frame=None):
    from database import get_all_colleges, delete_college
    global back_icon, sort_order, sort_button_text, original_colors,icon1,cancel,text_image
    
    if body_frame is None:
        from body import body
        body_frame = body(root)
    
    sort_order = "ascending"
    
    form_frame = Canvas(body_frame, bg="white", width=720, height=450, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(form_frame, -300, 0, 720, 450, radius=130, fill='lightgray')
    
    # Header
    title_text = Label(root, text="Colleges", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    form_frame.create_window(360, 30, window=title_text)
    
    # Search functionality
    colleges_var = StringVar()
    def clear_placeholder(event=None):
        if colleges_var.get() == "":
            icon2.place_forget()
            icon3.place_forget()
        college_search_bar.focus_set()
    
    def restore_placeholder(event=None):
        if colleges_var.get() == "":
            icon2.place(x=2, y=3)
            icon3.place(x=25, y=7)
        
    def college_search(*args):
        if colleges_var.get():
            cancel_butt.place(x=260, y=4)
        else:
            cancel_butt.place_forget()
        college_filter()
            
    def college_filter(*args):
        search_term = colleges_var.get().lower()
        
        colleges = get_all_colleges()
        
        filtered_colleges = [
            college for college in colleges 
            if search_term in college['code'].lower() or search_term in college['name'].lower()
        ]
        
        college_table.delete(*college_table.get_children())
        original_colors.clear()
        
        if sort_order == "ascending":
            filtered_colleges.sort(key=lambda x: x['code'])
        else:
            filtered_colleges.sort(key=lambda x: x['code'], reverse=True)
        
        for college in filtered_colleges:
            row_id = college_table.insert("", "end", values=(
                college['code'],
                college['name'],
                0,  
                0   
            ), tags=("normal",))
            original_colors[row_id] = "normal"
    
    def clear_search(event=None):
        colleges_var.set("")
        college_filter()
        cancel_butt.place_forget()
        
    def toggle_sort_order():
        global sort_order, sort_button_text
        if sort_order == "ascending":
            sort_order = "descending"
            sort_button_text.config(text="Descending")
        else:
            sort_order = "ascending"
            sort_button_text.config(text="Ascending")
        college_filter()
    
    # Search bar
    search_canvas = Canvas(root, width=300, height=33, bg="lightgray", highlightthickness=0)
    form_frame.create_window(162, 75, window=search_canvas)
    
    college_search_bar = Entry(root, textvariable=colleges_var, bg="white", font=('Albert Sans', 12, 'normal'), 
                             fg="gray", borderwidth=0, highlightthickness=0)
    form_frame.create_window(22, 65, window=college_search_bar, anchor="nw", width=284, height=25)
    
    icon1 = PhotoImage(file="Images/SearchIcon.png")
    icon2 = Label(college_search_bar, image=icon1, bg="white", bd=0)
    icon2.place(x=2, y=3)
    
    cancel = PhotoImage(file='Images/cancel.png')
    cancel_butt = Button(college_search_bar, image=cancel, bg="white", activebackground="white", 
                        bd=0, cursor="hand2", command=clear_search)
    
    text_image = PhotoImage(file="Images/Search In Here.png")
    icon3 = Label(college_search_bar, image=text_image, bg="white", bd=0)
    icon3.place(x=25, y=7)
    
    search = create_rounded_rectangle(search_canvas, 5, 3, 300, 33, radius=20, fill='white')
    
    colleges_var.trace_add("write", college_search)
    
    college_search_bar.bind("<FocusIn>", clear_placeholder)
    college_search_bar.bind("<FocusOut>", restore_placeholder)
    icon2.bind("<Button-1>", clear_placeholder)
    icon3.bind("<Button-1>", clear_placeholder)
    
    # Create treeview for college list
    style = ttk.Style()
    style.configure("Custom.Treeview", background="white", foreground="black", 
                   rowheight=25, fieldbackground="white", font=("Arial", 10))
    style.configure("Custom.Treeview.Heading", background="white", foreground="black", 
                   font=("Arial", 10, "bold"), relief="flat")
    style.map("Custom.Treeview", background=[("selected", "#2E5EB5")])
    
    # Create frame for treeview
    table_frame = Frame(root)
    columns = ("#1", "#2", "#3", "#4")
    college_table = ttk.Treeview(table_frame, style="Custom.Treeview", columns=columns, 
                               show="headings", height=7)
    
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=college_table.yview)
    college_table.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side="right", fill="y")
    college_table.pack(side="left", fill="both", expand=True)
    
    college_table.heading("#1", text="College Code")
    college_table.heading("#2", text="College Name")
    college_table.heading("#3", text="Num. of Programs")
    college_table.heading("#4", text="Num. of Students")
    
    college_table.column("#1", width=100, anchor="w")
    college_table.column("#2", width=325, anchor="w")
    college_table.column("#3", width=125, anchor="center")
    college_table.column("#4", width=118, anchor="center")
    
    college_table.tag_configure("hover", background="#C5D5F0")
    
    def disable_column_drag(event):
        region = college_table.identify_region(event.x, event.y)
        if region == "separator" or region == "heading":
            return "break"
    
    college_table.bind('<Button-1>', disable_column_drag, add='+')
    college_table.bind('<B1-Motion>', disable_column_drag, add='+')
    
    form_frame.create_window(360, 210, window=table_frame)
    
    original_colors = {}
    
    # Hover effects
    hovered_row = None
    
    def on_hover(event):
        nonlocal hovered_row
        row_id = college_table.identify_row(event.y)
        
        if hovered_row and (hovered_row != row_id or not row_id):
            if hovered_row in original_colors:
                college_table.item(hovered_row, tags=(original_colors[hovered_row],))
            hovered_row = None
        
        if row_id and row_id != hovered_row:
            hovered_row = row_id
            if row_id in original_colors:
                college_table.item(row_id, tags=("hover",))
    
    def on_leave(event):
        nonlocal hovered_row
        if hovered_row and hovered_row in original_colors:
            college_table.item(hovered_row, tags=(original_colors[hovered_row],))
        hovered_row = None
    
    college_table.bind("<Motion>", on_hover)
    college_table.bind("<Leave>", on_leave)
    
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
        new_form = add_college_form(root, body_frame)
        new_form.place(x=0, y=0)
    
    def edit_selected():
        selected_item = college_table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a college to edit")
            return
        
        item_values = college_table.item(selected_item[0], "values")
        college_code = item_values[0]
        college_name = item_values[1]
        
        # Get the college ID from database
        colleges = get_all_colleges()
        college = next((c for c in colleges if c['code'] == college_code and c['name'] == college_name), None)
        
        if college:
            form_frame.destroy()
            edit_form = add_college_form(root, body_frame, edit_mode=True, 
                                       college_id=college['id'], 
                                       college_name=college['name'], 
                                       college_code=college['code'])
            edit_form.place(x=0, y=0)
    
    def delete_selected():
        selected_item = college_table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a college to delete")
            return
        
        item_values = college_table.item(selected_item[0], "values")
        college_code = item_values[0]
        college_name = item_values[1]
        
        # Get the college ID from database
        colleges = get_all_colleges()
        college = next((c for c in colleges if c['code'] == college_code and c['name'] == college_name), None)
        
        if college:
            confirm = messagebox.askyesno("Confirm Delete", 
                f"Are you sure you want to delete {college_name}?\n\n"
                "This will also delete ALL programs in this college and set "
                "affected students' program to N/A.")
            
            if confirm:
                success, message = delete_college(college['id'])
                if success:
                    messagebox.showinfo("Success", message)
                    college_filter()
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
    
    college_filter()
    
    FormManager.show_form(form_frame)
    return form_frame   

def add_college_form(root, body_frame=None, edit_mode=False, college_id=None, college_name=None, college_code=None):
    from database import save_college, update_college
    global back_icon
    
    if body_frame is None:
        from body import body
        body_frame = body(root)

    form_frame2 = Canvas(body_frame, bg="white", width=350, height=250, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(form_frame2, -300, 0, 350, 250, radius=130, fill='lightgray')

    # Set the title based on mode (Add or Edit)
    title_text = "Edit College" if edit_mode else "Add College"
    manage_text = Label(root, text=title_text, font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    form_frame2.create_window(175, 30, window=manage_text)

    back_icon = PhotoImage(file="Images/back.png")

    back_canvas2 = Canvas(root, width=30, height=30, bg="lightgray", highlightthickness=0)
    image_id = back_canvas2.create_image(15, 15, image=back_icon, anchor="center")

    form_frame2.create_window(20, 25, window=back_canvas2)
    
    def on_hover(event):
        overlapping = back_canvas2.find_overlapping(event.x, event.y, event.x, event.y)
        if image_id in overlapping:
            back_canvas2.config(cursor="hand2", bg="lightgray")  
        else:
            back_canvas2.config(cursor="", bg="lightgray")
            
    def go_back(event):
        form_frame2.destroy()
        if edit_mode:
            view_form = view_colleges_form(root, body_frame)
            view_form.place(x=0, y=0)
        else:
            college_form_canvas = view_colleges_form(root, body_frame)
            college_form_canvas.place(x=0, y=0)

    back_canvas2.bind("<Button-1>", go_back)
    back_canvas2.bind("<Motion>", on_hover)
    back_canvas2.bind("<Leave>", lambda event: back_canvas2.config(cursor="",bg="lightgray"))

    style = ttk.Style()
    style.configure("Custom.TCombobox", foreground="") 
    style.configure("Custom.TCombobox", relief="flat", foreground="gray")
    
    # Add College
    title = Label(root, text="College Information", bg="lightgray", font=("Arial", 15, "bold"))
    form_frame2.create_window(130, 70, window=title)

    name_label = Label(root, text="College Name", bg="lightgray", font=("Arial", 10, "bold"))
    form_frame2.create_window(175, 117, window=name_label)

    add_name = Entry(root, font=('Albert Sans', 12, 'normal'), width=30, fg="gray", justify="center")
    form_frame2.create_window(175, 97, window=add_name)
    
    if edit_mode and college_name:
        add_name.delete(0, END)
        add_name.insert(0, college_name)
        add_name.config(fg="black", justify="left")
    else:
        add_name.insert(0, "Ex: College of Computer Studies")
        add_name.bind("<FocusIn>", lambda event: add_name.get() == "Ex: College of Computer Studies" and 
                     (add_name.delete(0, END), add_name.config(fg="black", justify="left")))
        add_name.bind("<FocusOut>", lambda event: add_name.get() == "" and 
                     (add_name.insert(0, "Ex: College of Computer Studies"), add_name.config(fg="gray", justify="center")))

    course_text = Label(root, text="College Code", bg="lightgray", fg="gray", font=("Arial", 10))
    form_frame2.create_window(175, 160, window=course_text)
    
    college_code_entry = Entry(root, font=('Albert Sans', 12, 'normal'), width=30, fg="gray", justify="center")
    form_frame2.create_window(175, 140, window=college_code_entry)
    
    if edit_mode and college_code:
        college_code_entry.delete(0, END)
        college_code_entry.insert(0, college_code)
        college_code_entry.config(fg="black", justify="left")
    else:
        college_code_entry.insert(0, "Ex: CCS")
        college_code_entry.bind("<FocusIn>", lambda event: college_code_entry.get() == "Ex: CCS" and 
                              (college_code_entry.delete(0, END), college_code_entry.config(fg="black", justify="left")))
        college_code_entry.bind("<FocusOut>", lambda event: college_code_entry.get() == "" and 
                              (college_code_entry.insert(0, "Ex: CCS"), college_code_entry.config(fg="gray", justify="center")))

    # Button text changes based on mode
    button_text = "Update" if edit_mode else "Save"
    save_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
    form_frame2.create_window(120, 210, window=save_canvas)
    save_button = create_rounded_rectangle(save_canvas, 5, 5, 100, 45, radius=20, fill='#2363C6')
    save_text = save_canvas.create_text(50, 24, text=button_text, fill="white", font=("Arial", 15, "bold"))

    close_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
    form_frame2.create_window(225, 210, window=close_canvas)

    close = create_rounded_rectangle(close_canvas, 5, 5, 100, 45, radius=20, fill='#AA4141')
    close_college = close_canvas.create_text(50, 24, text="Close", fill="white", font=("Arial", 15, "bold"))        

    def submit_form():
        from body import refresh_students
        college_name = add_name.get()
        code = college_code_entry.get()
        
        # Basic validation
        if college_name == "Ex: College of Computer Studies" or college_name.strip() == "":
            messagebox.showerror("Error", "Please enter a college name")
            return
            
        if code == "Ex: CCS" or code.strip() == "":
            messagebox.showerror("Error", "Please enter a college code")
            return
        
        if any(char.isdigit() for char in college_name):
            messagebox.showerror("Error", "Last name should not contain numbers")
            return
        
        if any(char.isdigit() for char in code):
            messagebox.showerror("Error", "First name should not contain numbers")
            return
        if not re.fullmatch(r"[A-Za-z\s\-\(\)]+", college_name) or not re.fullmatch(r"[A-Za-z\s\-\(\)]+", code):
            messagebox.showerror("Input Error", "College name must contain only letters, dashes, and parentheses (no numbers allowed).")
            return
        # Save to database or update existing record
        if edit_mode:
            success, message = update_college(college_id, college_name, code)
            if success:
                messagebox.showinfo("Success", message)
                go_back(None) 
                refresh_students()  
            else:
                messagebox.showerror("Error", message)
        else:
            # Original save logic for new college
            success, message = save_college(college_name, code)
            if success:
                messagebox.showinfo("Success", message)
                # Clear the form
                add_name.delete(0, END)
                add_name.insert(0, "Ex: College of Computer Studies")
                add_name.config(fg="gray", justify="center")
                
                college_code_entry.delete(0, END)
                college_code_entry.insert(0, "Ex: CCS")
                college_code_entry.config(fg="gray", justify="center")
                
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
        form_frame2.destroy()

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
    FormManager.show_form(form_frame2)
    return form_frame2