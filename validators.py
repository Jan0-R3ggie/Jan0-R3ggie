# validators.py
def validate_input(event, widget, validation_function, max_length=None):
    input_text = widget.get("1.0", "end-1c")

    if max_length is not None and len(input_text) > max_length:
        widget.delete("end-2c", "end-1c")
        widget.master.highlight_error(widget)  # Call highlight_error

    if not validation_function(input_text):
        widget.delete("end-2c", "end-1c")
        widget.master.highlight_error(widget)  # Call highlight_error

def validate_integer_input(text):
    if text.isdigit():
        return len(text) <= 10
    elif text == "":
        return True
    else:
        return False

def allow_string(input_text):
    return input_text.replace(" ", "").isalpha() or input_text == ""

def validate_integer_input_2(text):
    if text.isdigit() and len(text) <= 3:
        return True
    elif text == "":
        return True
    else:
        return False

def on_validate_float_input(value):
    if value.strip() == "":
        return True

    if value.count(".") > 1:
        return False

    if not value.replace(".", "", 1).isdigit():
        if len(value) == 1 and value[0] == "-":
            return True
        return False

    return True

def on_validate_integer_input(text, action):
    if action == "1":
        return validate_integer_input_2(text)
    else:
        return True
    
def allow_string_and_numbers(input_text):
    return input_text.replace(" ", "").isalnum() or input_text == ""    

def validate_float_with_max_digits(value, max_digits=5, max_decimal_places=2):
    if value.strip() == "":
        return True

    # Remove leading zeros
    value = value.lstrip("0")

    # Handle negative values
    is_negative = value.startswith("-")
    if is_negative:
        value = value[1:]

    # Split the value into integer and decimal parts
    parts = value.split(".")

    # Validate the integer part
    if len(parts[0]) > max_digits - max_decimal_places:
        return False

    # Validate the decimal part
    if len(parts) > 1 and len(parts[1]) > max_decimal_places:
        return False

    return True