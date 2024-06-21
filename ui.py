# ui.py
import tkinter as tk
from tkinter import messagebox
from handlers import validate_and_save, submit_health_assessment
from validators import validate_input, validate_integer_input, allow_string, on_validate_float_input, validate_float_with_max_digits, allow_string_and_numbers

class UI:
    class BMICalculator:
        def calculate_bmi(self, weight_str, height_str):
            if not weight_str or not height_str:
                raise ValueError("Please enter both weight and height.")

            try:
                weight = float(weight_str)
                height = float(height_str) / 100

                if height == 0:
                    raise ValueError("Height cannot be zero.")

                bmi = weight / (height ** 2)
                bmi_rounded = round(bmi, 2)

                bmi_category = ""
                if bmi < 18.5:
                    bmi_category = "Underweight"
                    color = "blue"
                elif 18.5 <= bmi < 24.9:
                    bmi_category = "Normal weight"
                    color = "green"
                elif 25 <= bmi < 29.9:
                    bmi_category = "Overweight"
                    color = "orange"
                else:
                    bmi_category = "Obesity"
                    color = "red"

                return bmi_rounded, color, bmi_category
            except ValueError as e:
                raise ValueError("Please enter valid numbers for weight and height.") from e    

    def highlight_error(self, widget, duration=1000):
        widget.config(bg="pink")
        self.root.after(duration, lambda: widget.config(bg="white"))

    def on_validate_integer_input(self, text, action):
        if action == "1":
            return self.validate_integer_input_2(text)
        else:
            return True
            
    def allow_string(input_text):
                return input_text.replace(" ", "").isalpha() or input_text == ""

    def allow_string_and_special_chars(input_text):
        return all(char.isalnum() or char in "!@#$%^&*()_+-=[]{}|;:',.<>/?`~" for char in input_text) or input_text == ""

    def validate_integer_input_2(self, text):
        if text.isdigit() and len(text) <= 6:
            return True
        elif text == "":
            return True
        else:
            return False    

    def __init__(self, root):
        self.root = root
        self.entry_widgets = []
        self.vcmd_float = (self.root.register(on_validate_float_input), "%P")
        self.bmi_calculator = self.BMICalculator()  # Create an instance of the nested BMICalculator class
        self.setup_ui()
        
    def setup_ui(self):
        self.display_area = tk.Frame(self.root, bg="#c59aed")
        self.display_area.place(relwidth=1, relheight=1)

        self.update_display1()  # Initialize with the first display

        button1 = tk.Button(self.root, text="Patient Details", width=20, bg="#9b51e0", fg="black", command=self.update_display1)
        button2 = tk.Button(self.root, text="Health Assessment", width=20, bg="#9b51e0", fg="black", command=self.update_display2)
        button3 = tk.Button(self.root, text="Finances", width=20, bg="#9b51e0", fg="black", command=self.update_display3)
        button4 = tk.Button(self.root, text="Claims", width=20, bg="#9b51e0", fg="black", command=self.update_display4)

        button1.pack(anchor=tk.NW, padx=10, pady=0)
        button2.place(relx=0.22, rely=0.00, anchor=tk.NE)
        button3.place(relx=0.32, rely=0.00, anchor=tk.NE)
        button4.place(relx=0.42, rely=0.00, anchor=tk.NE)

    def update_display1(self):
        try:
            self.entry_widgets = []
            for widget in self.display_area.winfo_children():
                widget.destroy()

            def focus_next_widget(event):
                event.widget.tk_focusNext().focus()
                return "break"

            def highlight_error(widget, duration=1000):
                widget.config(bg="pink")
                self.root.after(duration, lambda: widget.config(bg="white"))

            string_labels = ["Name", "Surname", "Main member", "Medical aid", "Gender", "Race", "Emergency name 1", "Emergency name 2", "church name", "religious leader"]
            for i, label_text in enumerate(string_labels):
                label = tk.Label(self.display_area, text=label_text + ":", bg="#c59aed", font=("Helvetica", 14))
                label.place(relx=0.2, rely=i * 0.09 + 0.07, anchor='e')
                text_box = tk.Text(self.display_area, height=1, width=25, font=("Helvetica", 16))
                text_box.place(relx=0.2, rely=i * 0.09 + 0.07, anchor='w')
                self.entry_widgets.append(text_box)
                text_box.bind("<KeyRelease>", lambda event, widget=text_box: validate_input(event, widget, self.allow_string, 20, highlight_error))

            labels = ["ID Number", "Medical aid number", "Address", "Tel 1", "Tel 2", "Email(optional)", "Dependant code", "Emergency number 1", "Emergency number 2", "church tel"]
            for i, label_text in enumerate(labels):
                label = tk.Label(self.display_area, text=label_text + ":", bg="#c59aed", font=("Helvetica", 14))
                label.place(relx=0.63, rely=i * 0.09 + 0.07, anchor='e')
                text_box = tk.Text(self.display_area, height=1, width=20, font=("Helvetica", 16))
                text_box.place(relx=0.63, rely=i * 0.09 + 0.07, anchor='w')
                text_box.bind("<Tab>", focus_next_widget)
                self.entry_widgets.append(text_box)

                if label_text == "ID Number":
                    text_box.bind("<KeyRelease>", lambda event, widget=text_box: validate_input(event, widget, validate_integer_input, 13, highlight_error))
                elif label_text in ["Medical aid number", "Tel 1", "Tel 2", "Emergency number 1", "Emergency number 2", "church tel"]:
                    text_box.bind("<KeyRelease>", lambda event, widget=text_box: validate_input(event, widget, validate_integer_input, 10, highlight_error))
                elif label_text == "Address":
                    text_box.bind("<KeyRelease>", lambda event, widget=text_box: validate_input(event, widget, self.allow_string_and_numbers, 30, highlight_error))
                elif label_text == "Email(optional)":
                    text_box.bind("<KeyRelease>", lambda event, widget=text_box: validate_input(event, widget, self.allow_string_and_special_chars, 30, highlight_error))
                elif label_text == "Dependant code":
                    text_box.bind("<KeyRelease>", lambda event, widget=text_box: validate_input(event, widget, self.validate_integer_input_2, 6, highlight_error))

            save_button = tk.Button(self.display_area, text="Save", command=lambda: validate_and_save(self.entry_widgets), font=("Helvetica", 18), bg="#9b51e0")
            save_button.place(relx=0.9, rely=0.9, anchor='center')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the program: {e}")
            
    def update_display2(self):
        try:
            self.entry_widgets = []
            for widget in self.display_area.winfo_children():
                widget.destroy()

            # Create 4 frames in a 2x2 grid
            frame1 = tk.Frame(self.display_area, bg="#ad71e5", bd=2, relief="groove")
            frame2 = tk.Frame(self.display_area, bg="#ad71e5", bd=2, relief="groove")
            frame3 = tk.Frame(self.display_area, bg="#ad71e5", bd=2, relief="groove")
            frame4 = tk.Frame(self.display_area, bg="#ad71e5", bd=2, relief="groove")

            frame1.place(relx=0.05, rely=0.05, relwidth=0.43, relheight=0.43)
            frame2.place(relx=0.5, rely=0.05, relwidth=0.43, relheight=0.43)
            frame3.place(relx=0.05, rely=0.5, relwidth=0.43, relheight=0.43)
            frame4.place(relx=0.5, rely=0.5, relwidth=0.43, relheight=0.43)

            def focus_next_widget(event):
                event.widget.tk_focusNext().focus()
                return "break"

            bp_labels = [("Systolic:", 12), ("Diastolic:", 12), ("Pulse:", 12)]
            for i, (label_text, font_size) in enumerate(bp_labels):
                label = tk.Label(frame1, text=label_text, bg="#ad71e5", font=("Helvetica", font_size))
                label.place(relx=0.3, rely=i * 0.2 + 0.2, anchor='e')
                entry = tk.Entry(frame1, font=("Helvetica", 16))
                entry.place(relx=0.4, rely=i * 0.2 + 0.2, anchor='w')
                entry.config(validate="key", validatecommand=(self.root.register(validate_float_with_max_digits), "%P"))
                self.entry_widgets.append(entry)

            vitalSigns_labels = [("Glucose:", 12), ("Cholesterol:", 12), ("Saturation:", 12)]
            for i, (label_text, font_size) in enumerate(vitalSigns_labels):
                label = tk.Label(frame2, text=label_text, bg="#ad71e5", font=("Helvetica", font_size))
                label.place(relx=0.3, rely=i * 0.2 + 0.2, anchor='e')
                entry = tk.Entry(frame2, font=("Helvetica", 16))
                entry.place(relx=0.4, rely=i * 0.2 + 0.2, anchor='w')
                entry.config(validate="key", validatecommand=(self.root.register(validate_float_with_max_digits), "%P"))
                self.entry_widgets.append(entry)

            lg_labels = [("HDL:", 12), ("LDL:", 12), ("Total cholesterol:", 12)]
            for i, (label_text, font_size) in enumerate(lg_labels):
                label = tk.Label(frame3, text=label_text, bg="#ad71e5", font=("Helvetica", font_size))
                label.place(relx=0.3, rely=i * 0.2 + 0.2, anchor='e')
                entry = tk.Entry(frame3, font=("Helvetica", 16))
                entry.place(relx=0.4, rely=i * 0.2 + 0.2, anchor='w')
                entry.config(validate="key", validatecommand=(self.root.register(validate_float_with_max_digits), "%P"))
                self.entry_widgets.append(entry)

            labels = ["Weight (kg)", "Height (cm)"]
            for i, label_text in enumerate(labels):
                label = tk.Label(frame4, text=label_text + ":", bg="#ad71e5", font=("Helvetica", 14))
                label.place(relx=0.35, rely=i * 0.2 + 0.2, anchor='e')
                entry = tk.Entry(frame4, font=("Helvetica", 16))
                entry.place(relx=0.4, rely=i * 0.2 + 0.2, anchor='w')
                self.entry_widgets.append(entry)
                entry.bind("<Tab>", focus_next_widget)

            bmi_label = tk.Label(frame4, text="BMI:", bg="#ad71e5", font=("Helvetica", 14))
            bmi_label.place(relx=0.35, rely=0.61, anchor='e')
            bmi_result = tk.Label(frame4, text="", bg="#ad71e5", font=("Helvetica", 14))
            bmi_result.place(relx=0.4, rely=0.61, anchor='w')
            self.entry_widgets.append(bmi_result)

            def calculate_bmi():
                weight_str = self.entry_widgets[9].get()
                height_str = self.entry_widgets[10].get()
                
                try:
                    bmi_rounded, color, bmi_category = self.bmi_calculator.calculate_bmi(weight_str, height_str)
                    self.entry_widgets[11].config(text=f"{bmi_rounded:.2f}", fg=color)
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            calculate_button = tk.Button(frame4, text="Calculate BMI", command=calculate_bmi, font=("Helvetica", 18), bg="#9b51e0")
            calculate_button.place(relx=0.4, rely=0.80, anchor='center')

            save_button = tk.Button(self.display_area, text="Save", command=lambda: validate_and_save(self.entry_widgets), font=("Helvetica", 18), bg="#9b51e0")
            save_button.place(relx=0.8, rely=0.84, anchor='center')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the program: {e}")

    def update_display3(self):
        try:
            self.entry_widgets = []
            for widget in self.display_area.winfo_children():
                widget.destroy()

            labels = ["Income", "Expenses", "Savings", "Investments"]
            for i, label_text in enumerate(labels):
                label = tk.Label(self.display_area, text=label_text + ":", bg="#c59aed", font=("Helvetica", 14))
                label.place(relx=0.2, rely=i * 0.1 + 0.05, anchor='e')
                entry = tk.Entry(self.display_area, font=("Helvetica", 16))
                entry.place(relx=0.3, rely=i * 0.1 + 0.05, anchor='w')
                self.entry_widgets.append(entry)

            submit_button = tk.Button(self.display_area, text="Submit", command=lambda: submit_health_assessment(self.entry_widgets), font=("Helvetica", 18), bg="#9b51e0")
            submit_button.place(relx=0.3, rely=0.5, anchor='center')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the program: {e}")

    def update_display4(self):
        try:
            self.entry_widgets = []
            for widget in self.display_area.winfo_children():
                widget.destroy()

            labels = ["Claim Number", "Claim Date", "Amount", "Description"]
            for i, label_text in enumerate(labels):
                label = tk.Label(self.display_area, text=label_text + ":", bg="#c59aed", font=("Helvetica", 14))
                label.place(relx=0.2, rely=i * 0.1 + 0.05, anchor='e')
                entry = tk.Entry(self.display_area, font=("Helvetica", 16))
                entry.place(relx=0.3, rely=i * 0.1 + 0.05, anchor='w')
                self.entry_widgets.append(entry)

            submit_button = tk.Button(self.display_area, text="Submit Claim", command=lambda: submit_health_assessment(self.entry_widgets), font=("Helvetica", 18), bg="#9b51e0")
            submit_button.place(relx=0.3, rely=0.5, anchor='center')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the program: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Program")
    root.geometry("1400x1000")
    root.configure(bg="light green")
    app = UI(root)
    root.mainloop()
