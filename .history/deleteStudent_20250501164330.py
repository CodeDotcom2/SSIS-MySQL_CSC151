from tkinter import *
from tkinter import messagebox
from database import delete_student
from body import refresh_students, get_selected_student_data

def delete_stud(event=None):
    student_data = get_selected_student_data()
    
    if not student_data:
        messagebox.showerror("Error", "No student selected. Please select a student to delete.")
        return
    
    student_name = f"{student_data['first_name']} {student_data['last_name']}"
    confirm = messagebox.askyesno(
        "Confirm Deletion",
        f"Are you sure you want to delete {student_name}?\n\nThis action cannot be undone.",
        icon="warning"
    )
    
    if confirm:
        success, message = delete_student(student_data['id'])
        
        if success:
            messagebox.showinfo("Success", message)
            refresh_students()
        else:
            messagebox.showerror("Error", message)