from tkinter import *
from tkinter import ttk,messagebox
from misc import create_rounded_rectangle,FormManager
from database import save_college


#college 
def college_form(root, body_frame=None):
    if body_frame is None:
        from body import body
        body_frame = body(root)
    
    form_frame2 = Canvas(body_frame, bg="white", width=350, height=250, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(form_frame2, -800, 0, 350, 250, radius=130, fill='lightgray')

    manage_text = Label(root, text="Manage Colleges", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    form_frame2.create_window(160, 30, window=manage_text)


        # Add College Button
    add_canvas = Canvas(root, width=180, height=45, bg="lightgray", highlightthickness=0)
    form_frame2.create_window(165, 90, window=add_canvas)

    add = create_rounded_rectangle(add_canvas, 5, 5, 180, 45, radius=20, fill='white')
    add_college = add_canvas.create_text(92, 25, text="Add College", fill="black", font=("Arial", 15, "bold"))


        # View Colleges Button
    view_canvas = Canvas(root, width=180, height=45, bg="lightgray", highlightthickness=0)
    form_frame2.create_window(165, 140, window=view_canvas)

    view = create_rounded_rectangle(view_canvas, 5, 5, 180, 45, radius=20, fill='white')
    view_college = view_canvas.create_text(92, 25, text="View Colleges", fill="black", font=("Arial", 15, "bold"))
    
    def on_view_college_click(event):
        form_frame2.destroy()
        view_form = view_colleges_form(root, body_frame)
        view_form.place(x=0, y=0)
    
    view_canvas.tag_bind(view, "<Button-1>", on_view_college_click)
    view_canvas.tag_bind(view_college, "<Button-1>", on_view_college_click)
    
        # Close Button
    close_canvas = Canvas(root, width=100, height=45, bg="lightgray", highlightthickness=0)
    form_frame2.create_window(165, 210, window=close_canvas)

    close = create_rounded_rectangle(close_canvas, 5, 5, 100, 45, radius=20, fill='#AA4141')
    close_college = close_canvas.create_text(50, 24, text="Close", fill="white", font=("Arial", 15, "bold"))

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

    def on_add_college_click(event):
        form_frame2.destroy()
        new_form = add_college_form(root, body_frame)
        new_form.place(x=0, y=0)

    add_canvas.tag_bind(add, "<Button-1>", on_add_college_click)
    add_canvas.tag_bind(add_college, "<Button-1>", on_add_college_click)
    
    FormManager.show_form(form_frame2)
    return form_frame2

def view_colleges_form(root, body_frame=None):
    from database import get_all_colleges, delete_college
    global back_icon
    
    if body_frame is None:
        from body import body
        body_frame = body(root)
    
    form_frame = Canvas(body_frame, bg="white", width=600, height=400, bd=0, highlightthickness=0)
    form = create_rounded_rectangle(form_frame, -300, 0, 600, 400, radius=130, fill='lightgray')
    
    # Header
    title_text = Label(root, text="View Colleges", font=("Arial", 25, "bold"), bg="lightgray", fg="#2363C6")
    form_frame.create_window(300, 30, window=title_text)
    
    
    # Create treeview for college list
    style = ttk.Style()
    style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white", font=("Arial", 12))
    style.map('Treeview', background=[('selected', '#2363C6')])
    
    # Create frame for treeview
    tree_frame = Frame(root, bg="lightgray")
    form_frame.create_window(300, 200, window=tree_frame, width=550, height=250)
    
    # Scrollbar
    scroll_y = Scrollbar(tree_frame, orient="vertical")
    scroll_y.pack(side=RIGHT, fill=Y)
    
    # Create Treeview
    columns = ("ID", "College Code", "College Name", "Num. of Programs", "Num. of Students")
    college_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scroll_y.set, selectmode="browse")
    
    # Configure columns
    college_tree.heading("ID", text="ID")
    college_tree.heading("College Code", text="College Code")
    college_tree.heading("College Name", text="College Name")
    college_tree.heading("Num. of Programs", text="Num. of Programs")
    college_tree.heading("Num. of Students", text="Num. of Students")

    # Hide the ID column (we'll use it for reference but don't need to display it)
    college_tree.column("ID", width=0, stretch=NO)
    college_tree.column("College Code", width=100, anchor=W)
    college_tree.column("College Name", width=250, anchor=CENTER)
    college_tree.column("Num. of Programs", width=100, anchor=CENTER)
    college_tree.column("Num. of Students", width=100, anchor=CENTER)

    
    scroll_y.config(command=college_tree.yview)
    college_tree.pack(fill=BOTH, expand=1)
    
    # Load data
    def load_colleges():
        for item in college_tree.get_children():
            college_tree.delete(item)
        
        # Get colleges from database
        colleges = get_all_colleges()
        for college in colleges:
            # Insert with ID as first column (hidden)
            college_tree.insert("", END, values=(
                college['id'], 
                college['code'], 
                college['name'],
                0, 
                0  
            ))
    
    load_colleges()
    
    button_frame = Frame(root, bg="lightgray")
    form_frame.create_window(300, 350, window=button_frame)
    

    
   
    # Add Button  
    def add_selected():
        new_form = add_college_form(root, body_frame)
        new_form.place(x=0, y=0)
    
    add_btn = Button(button_frame,text="Add", command=add_selected,bg="#2363C6", fg="white")
    add_btn.pack(side=LEFT,padx=10)
    
    # Edit button
    def edit_selected():
        selected_item = college_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a college to edit")
            return
        
        item_values = college_tree.item(selected_item[0], "values")
        college_id = item_values[0]  # Now correctly getting the ID
        college_code = item_values[1]
        college_name = item_values[2]
        
        form_frame.destroy()
        edit_form = add_college_form(root, body_frame, edit_mode=True, college_id=college_id, 
                                  college_name=college_name, college_code=college_code)
        edit_form.place(x=0, y=0)
    
    edit_btn = Button(button_frame, text="Edit", command=edit_selected, bg="#2363C6", fg="white", 
                     font=("Arial", 12), padx=20, pady=5, border=0)
    edit_btn.pack(side=LEFT, padx=10)
    
    # Delete button
    def delete_selected():
        selected_item = college_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a college to delete")
            return
        
        item_values = college_tree.item(selected_item[0], "values")
        college_id = item_values[0]
        college_name = item_values[2]
        
        confirm = messagebox.askyesno("Confirm Delete", 
            f"Are you sure you want to delete {college_name}?\n\n"
            "This will also delete ALL programs in this college and set "
            "affected students' program to N/A.")
        
        if confirm:
            success, message = delete_college(college_id)
            if success:
                messagebox.showinfo("Success", message)
                load_colleges()  
                from body import refresh_students
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
            back_canvas2.config(cursor="", bg="white")
            
    def go_back(event):
        form_frame2.destroy()
        if edit_mode:
            view_form = view_colleges_form(root, body_frame)
            view_form.place(x=0, y=0)
        else:
            college_form_canvas = college_form(root, body_frame)
            college_form_canvas.place(x=0, y=0)

    back_canvas2.bind("<Button-1>", go_back)
    back_canvas2.bind("<Motion>", on_hover)
    back_canvas2.bind("<Leave>", lambda event: back_canvas2.config(cursor=""))

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