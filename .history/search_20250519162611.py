
search_text = ""
search_field = "all"  
search_callbacks = []

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

    global search_text
    search_text = text
    notify_search_changed()

def set_search_field(field):
    global search_field
    if field in SEARCH_FIELDS:
        search_field = field
        notify_search_changed()

def get_search_text():
    global search_text
    return search_text

def get_search_field():
    global search_field
    return search_field

def get_search_fields():
    return SEARCH_FIELDS

def register_search_callback(callback_function):

    if callback_function not in search_callbacks:
        search_callbacks.append(callback_function)

def unregister_search_callback(callback_function):

    if callback_function in search_callbacks:
        search_callbacks.remove(callback_function)

def notify_search_changed():

    global search_text, search_field, search_callbacks
    for callback in search_callbacks:
        try:
            callback(search_text)
        except Exception as e:
            print(f"Error in search callback: {e}")

def get_search_params():

    global search_text, search_field
    return {
        "text": search_text,
        "field": search_field
    }