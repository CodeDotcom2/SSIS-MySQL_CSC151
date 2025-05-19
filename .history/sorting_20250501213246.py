from tkinter import *
from misc import create_rounded_rectangle
from header import top

# Declare global variables
sort_img = None
sort_canvas = None
sort_frame = None

def create_sort_button():
    global sort_img, sort_canvas, sort_frame
    
    # Create canvas
    sort_canvas = Canvas(top, width=30, height=30, highlightthickness=0, bd=0, bg="white")
    sort_canvas.grid(row=0, column=1, padx=(0, 70), pady=(10,0), sticky="ne")
    
    # Create rounded rectangle background
    sort_frame = create_rounded_rectangle(sort_canvas, 0, 0, 30, 30, radius=20, fill="white") 
    
    # Load the image
    sort_img = PhotoImage(file="Images/sort.png")
    sort_canvas.create_image(15, 15, image=sort_img, anchor="center") 

    # Bind events
    sort_canvas.tag_bind(sort_frame, "<Enter>", on_enter)
    sort_canvas.tag_bind(sort_frame, "<Leave>", on_leave)
    sort_canvas.tag_bind(sort_frame, "<Button-1>", sort_clicked)
    
    # Also bind to the canvas itself
    sort_canvas.bind("<Enter>", on_enter)
    sort_canvas.bind("<Leave>", on_leave)
    sort_canvas.bind("<Button-1>", sort_clicked)
    sort_canvas.bind("<ButtonRelease-1>", sort_click_release)

    return sort_canvas

def on_enter(event):
    global sort_frame, sort_canvas
    sort_canvas.itemconfig(sort_frame, fill="#A5CAEC")

def on_leave(event):
    global sort_frame, sort_canvas
    sort_canvas.itemconfig(sort_frame, fill="white")

def sort_clicked(event):
    sort_canvas.itemconfig(sort_frame, fill="light gray")


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
