import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200")

# Placeholder text
placeholder_text = "Select an option"

# Function to handle selection
def on_select(event):
    """Change text color to black when an option is selected."""
    if combo.get() != placeholder_text:
        combo.configure(foreground="black")

# Function to handle focus in (remove placeholder)
def on_focus_in(event):
    """Remove placeholder when clicking inside."""
    if combo.get() == placeholder_text:
        combo.set("")  # Clear the text
        combo.configure(foreground="black")  # Set text color to black

# Function to handle focus out (restore placeholder)
def on_focus_out(event):
    """Restore placeholder if no option is selected."""
    if not combo.get():  # If empty, restore placeholder
        combo.set(placeholder_text)
        combo.configure(foreground="gray")

# Create Combobox
combo = ttk.Combobox(root, values=["Option 1", "Option 2", "Option 3"], state="readonly")
combo.pack(pady=20)

# Set placeholder initially
combo.set(placeholder_text)
combo.configure(foreground="gray")  # Placeholder color

# Bind events
combo.bind("<<ComboboxSelected>>", on_select)  # When an option is selected
combo.bind("<FocusIn>", on_focus_in)  # When clicking inside
combo.bind("<FocusOut>", on_focus_out)  # When clicking outside

root.mainloop()
