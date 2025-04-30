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

class FormManager:
    _current_form = None
    
    @classmethod
    def show_form(cls, new_form):
        # Close the current form if one exists
        if cls._current_form is not None:
            cls._current_form.destroy()
        
        # Set and show the new form
        cls._current_form = new_form
        cls._current_form.place(x=0, y=0)
    
    @classmethod
    def close_current_form(cls):
        if cls._current_form is not None:
            cls._current_form.destroy()
            cls._current_form = None