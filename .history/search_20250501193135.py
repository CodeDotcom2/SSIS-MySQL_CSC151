# search.py - Centralized search handling for the student information system

# Global variables to store search state
search_text = ""
search_callbacks = []

def set_search_text(text):
    """
    Update the global search text and notify all registered callbacks
    
    Args:
        text (str): The search text to filter by
    """
    global search_text
    search_text = text
    notify_search_changed()

def get_search_text():
    """
    Get the current search text
    
    Returns:
        str: The current search text
    """
    global search_text
    return search_text

def register_search_callback(callback_function):
    """
    Register a function to be called when search text changes
    
    Args:
        callback_function (function): A function that will be called with search_text as parameter
    """
    if callback_function not in search_callbacks:
        search_callbacks.append(callback_function)

def unregister_search_callback(callback_function):
    """
    Remove a previously registered callback function
    
    Args:
        callback_function (function): A function previously registered
    """
    if callback_function in search_callbacks:
        search_callbacks.remove(callback_function)

def notify_search_changed():
    """
    Notify all registered callbacks about the search text change
    """
    global search_text, search_callbacks
    for callback in search_callbacks:
        try:
            callback(search_text)
        except Exception as e:
            print(f"Error in search callback: {e}")