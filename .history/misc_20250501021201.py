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
            
class TableManager:
    def __init__(self):
        self.current_hover = None
        self._hover_tag = "hover_effect"
    
    def configure_table(self, table, parent_frame):
        """Enhanced table configuration with hover and click-deselect"""
        # Clear existing tags to prevent duplicates
        table.tag_configure(self._hover_tag, background='#e6f0ff')
        
        # Bind hover events
        table.bind("<Motion>", lambda e: self._on_hover(e, table))
        table.bind("<Leave>", lambda e: self._on_leave(table))
        
        # Bind click events for deselection
        parent_frame.bind("<Button-1>", 
                        lambda e: self._on_frame_click(e, table), 
                        add='+')
        parent_frame.config(takefocus=1)
        parent_frame.focus_set()
    
    def _on_hover(self, event, table):
        item = table.identify_row(event.y)
        if item != self.current_hover:
            # Remove previous hover
            if self.current_hover:
                table.item(self.current_hover, tags=())
            
            # Apply new hover if not selected
            if item and item not in table.selection():
                table.item(item, tags=(self._hover_tag,))
                self.current_hover = item
    
    def _on_leave(self, table):
        if self.current_hover:
            table.item(self.current_hover, tags=())
            self.current_hover = None
    
    def _on_frame_click(self, event, table):
        # Only deselect if clicking on empty space
        if not table.identify_row(event.y):
            table.selection_remove(table.selection())
def setup_table_deselection(table_widget, parent_frame):
    def on_frame_click(event):
        if not table_widget.identify_row(event.y):
            table_widget.selection_remove(table_widget.selection())
    
    parent_frame.bind("<Button-1>", on_frame_click)
    parent_frame.config(takefocus=1)
    parent_frame.focus_set()