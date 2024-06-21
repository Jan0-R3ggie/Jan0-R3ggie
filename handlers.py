from tkinter import messagebox
import tkinter as tk
from database import save_to_database
from validators import validate_integer_input

def validate_and_save(entry_widgets):
    for widget in entry_widgets:
        input_text = widget.get("1.0", "end-1c")
        if not validate_integer_input(input_text):
            messagebox.showwarning("Warning", "The input should be 10 digits long.")
            return
    save_to_database()

def submit_health_assessment(frame1, frame2, frame3, frame4):
    health_info = {}

    for frame in [frame1, frame2, frame3, frame4]:
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Entry) and widget.get().strip() != "":
                # Assuming the label is in the row above the Entry widget
                label_text = widget.master.winfo_children()[widget.grid_info()["row"] - 1].cget("text")
                value = widget.get()

                if not value.strip():
                    messagebox.showwarning("Warning", f"The field '{label_text}' is empty!")
                    return

                health_info[label_text] = value

    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to submit the information?")     
    if confirmed:
        messagebox.showinfo("Success", "Health assessment submitted successfully!")
        # Code to handle submission, e.g., save to a database or send to an API
        print("Information submitted:", health_info)
    else:
        messagebox.showinfo("Cancelled", "Submission cancelled.")
