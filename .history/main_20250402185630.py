from tkinter import *
from header import header
from side import side
from body import body
from misc import set_root

root = Tk()
root.geometry("1100x605")
root.minsize(510, 500)
root.title(" ")
icon = PhotoImage(file="Images/icon.png")
root.iconphoto(True, icon)
root.configure(bg="red")
root.rowconfigure(1, weight=1)
root.columnconfigure(0,minsize=220)
root.columnconfigure(1,weight=1)


set_root(root)

header(root)
side(root)
body(root)
root.mainloop()