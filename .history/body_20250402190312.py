from tkinter import *
from tkinter import ttk
from misc import remove_focus

def body(root):
    body_frame = Frame(root, bg="white")
    body_frame.grid(row=1, column=1, sticky="nsew")
    body_frame.columnconfigure(0, weight=1)
    body_frame.rowconfigure(0, weight=1)
    
    table_frame = Frame(body_frame, bg="white")
    table_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)
    

    columns = ("ID No.", "Name", "Gender", "Year Level", "College", "Program")
    
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
    style = ttk.Style()
    style.configure("Treeview", font=('Albert Sans', 12), rowheight=40, padding=(5, 5))
    style.configure("Treeview.Heading", font=('Albert Sans', 15, 'bold'), anchor="w", padding=(1, 8), foreground="#9F9EA1")
    
    for col in columns:
        tree.heading(col, text=col, anchor="w")
        tree.column(col, anchor="w", width=100 if col in ["ID No.", "Year Level", "Gender", "College"] else 250)
    
    # Set column widths - using proportional weights
    tree.column("ID No.", width=80, minwidth=80)
    tree.column("Name", width=200, minwidth=150)
    tree.column("Gender", width=100, minwidth=80)
    tree.column("Year Level", width=100, minwidth=80)
    tree.column("College", width=150, minwidth=120)
    tree.column("College", width=150, minwidth=120)

    
    # Create scrollbars
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # Grid the treeview and scrollbars to fill the frame
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    


    return body_frame