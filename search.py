# search.py - Centralized search handling for the student information system

# Global variables to store search state
search_text = ""
search_field = "all"  # Default to search all fields
search_callbacks = []

# Available search fields
SEARCH_FIELDS = {
    "all": "All Fields",
    "id_number": "ID No.",
    "last_name": "Last Name",
    "first_name": "First Name",
    "gender": "Gender",
    "year_level": "Year Level",
    "college": "College",
    "program": "Program"
}

def set_search_text(text):
    """
    Update the global search text and notify all registered callbacks
    
    Args:
        text (str): The search text to filter by
    """
    global search_text
    search_text = text
    notify_search_changed()

def set_search_field(field):
    """
    Update the search field and notify all registered callbacks
    
    Args:
        field (str): The field to search in (must be one of SEARCH_FIELDS keys)
    """
    global search_field
    if field in SEARCH_FIELDS:
        search_field = field
        notify_search_changed()

def get_search_text():
    """
    Get the current search text
    
    Returns:
        str: The current search text
    """
    global search_text
    return search_text

def get_search_field():
    """
    Get the current search field
    
    Returns:
        str: The current search field
    """
    global search_field
    return search_field

def get_search_fields():
    """
    Get all available search fields
    
    Returns:
        dict: Dictionary of field_key: display_name pairs
    """
    return SEARCH_FIELDS

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
    global search_text, search_field, search_callbacks
    for callback in search_callbacks:
        try:
            callback(search_text)
        except Exception as e:
            print(f"Error in search callback: {e}")

def get_search_params():
    """
    Get the current search parameters as a dictionary
    
    Returns:
        dict: Dictionary with search_text and search_field
    """
    global search_text, search_field
    return {
        "text": search_text,
        "field": search_field
    }