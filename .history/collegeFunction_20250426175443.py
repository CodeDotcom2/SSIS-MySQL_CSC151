from form import toggle_form_visibility


college_frame = None
side_bar = None

def set_form_frame(frame, side_bar_canvas):
    global college_frame, side_bar
    college_frame = frame
    side_bar = side_bar_canvas


def colleges_func(event=None):
    toggle_form_visibility(college_frame, side_bar)

    print("COLLEGES")