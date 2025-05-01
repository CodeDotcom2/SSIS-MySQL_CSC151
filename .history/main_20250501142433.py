from tkinter import *
from tkinter import ttk
from header import header
from side import side
from body import body
from database import create_database, create_tables,initialize_database,create_default_na_programs

def main():
    create_database()
    create_tables()
    initialize_database()
    create_default_na_programs()
    root = Tk()
    root.title(" ")
    root.geometry("1200x700")
    root.minsize(900, 600)
    
    root.columnconfigure(0, weight=1, minsize=220)  # Sidebar
    root.columnconfigure(1, weight=5)  # Main content
    root.rowconfigure(0, weight=0, minsize=60)  # Header
    root.rowconfigure(1, weight=1)  # Body
    
    style = ttk.Style()
    style.configure('Custom.TCombobox', 
                    fieldbackground='white', 
                    background='white',
                    selectbackground='#A5CAEC')
    
    header(root)
    body_frame = body(root)
    side(root,body_frame)
    
    root.mainloop()

if __name__ == "__main__":
    main()