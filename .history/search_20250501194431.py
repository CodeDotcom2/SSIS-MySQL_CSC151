# search.py - Enhanced search handling for the student information system

# Global variables to store search state
search_text = ""
search_callbacks = []
search_filters = {}

def set_search_text(text):
    """
    Update the global search text, parse it into filters, and notify all registered callbacks
    
    Args:
        text (str): The search text to filter by
    """
    global search_text, search_filters
    search_text = text
    search_filters = parse_search_text(text)
    notify_search_changed()

def get_search_text():
    """
    Get the current search text
    
    Returns:
        str: The current search text
    """
    global search_text
    return search_text

def get_search_filters():
    """
    Get the parsed search filters
    
    Returns:
        dict: Dictionary of search filters
    """
    global search_filters
    return search_filters

def parse_search_text(text):
    """
    Parse the search text into specific filters
    
    Args:
        text (str): The search text to parse
        
    Returns:
        dict: Dictionary of search filters with keys:
              - id_number
              - last_name
              - first_name
              - gender
              - year_level
              - college
              - program
    """
    filters = {}
    if not text:
        return filters
    
    # Split by spaces but keep quoted phrases together
    import shlex
    terms = shlex.split(text)
    
    for term in terms:
        # Check for specific field filters (e.g., "id:1234" or "college:engineering")
        if ':' in term:
            field, value = term.split(':', 1)
            field = field.lower().strip()
            value = value.strip()
            
            if field in ['id', 'idno', 'idnum', 'id_number']:
                # Standardize ID format (add hyphen if missing)
                if '-' not in value and len(value) == 8:
                    value = f"{value[:4]}-{value[4:]}"
                filters['id_number'] = value
            elif field in ['last', 'lastname', 'lname']:
                filters['last_name'] = value
            elif field in ['first', 'firstname', 'fname']:
                filters['first_name'] = value
            elif field in ['gender', 'sex']:
                filters['gender'] = value
            elif field in ['year', 'level', 'yr', 'yearlevel']:
                # Map common year level terms to numbers
                year_mapping = {
                    '1': 1, '1st': 1, 'first': 1,
                    '2': 2, '2nd': 2, 'second': 2,
                    '3': 3, '3rd': 3, 'third': 3,
                    '4': 4, '4th': 4, 'fourth': 4,
                    '5': 5, '5+': 5, 'fifth': 5, '5th': 5
                }
                filters['year_level'] = year_mapping.get(value.lower(), value)
            elif field in ['college', 'col']:
                filters['college'] = value
            elif field in ['program', 'prog']:
                filters['program'] = value
        else:
            # General search - try to match against all fields
            if not filters.get('general'):
                filters['general'] = []
            filters['general'].append(term)
    
    return filters

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