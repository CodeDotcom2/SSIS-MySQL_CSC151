from tkinter import *
from tkinter import ttk
from header import header
from side import side
from body import body
from database import  create_tables,initialize_database
from misc import set_root

def main():
    create_tables()
    initialize_database()
    root = Tk()
    root.title(" ")
    root.geometry("1200x700")
    root.minsize(900, 600)
    icon = PhotoImage(file="Images/icon.png")
    root.iconphoto(True, icon)
    
    root.columnconfigure(0, weight=1)  
    root.columnconfigure(1, weight=5) 
    root.rowconfigure(0, weight=0)  
    root.rowconfigure(1, weight=1)  
    set_root(root)
    header(root)
    body_frame = body(root)
    side(root,body_frame)
    
    root.mainloop()

if __name__ == "__main__":
    main()