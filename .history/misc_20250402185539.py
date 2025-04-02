from tkinter import *
from tkinter import ttk

main_root = None


def set_root(root_window):
    global main_root
    main_root = root_window

def remove_focus(event):
    global main_root
    widget = event.widget

    if isinstance(widget, (Entry, Button, ttk.Combobox, ttk.Treeview)):
        return

    #tree.selection_remove(tree.selection())
    if main_root:    
        main_root.focus_set()

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    points = [
        x1 + radius, y1, x2 - radius, y1,
        x2, y1, x2, y1 + radius, x2, y2 - radius,
        x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)