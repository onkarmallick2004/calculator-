import tkinter as tk
import math

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

BACKGROUND_COLOR = "#1E1E2C"
DISPLAY_COLOR = "#2E2E3D"
DIGIT_COLOR = "#4A4A5E"
OPERATOR_COLOR = "#3A3A4D"
SPECIAL_COLOR = "#FFAB73"
LABEL_COLOR = "#FFFFFF"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x750")
        self.window.resizable(0, 0)
        self.window.title("Calculator")
        self.window.configure(bg=BACKGROUND_COLOR)

        self.total_expression = ""
        self.current_expression = ""

        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 6):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_scientific_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<BackSpace>", lambda event: self.backspace())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_percentage_button()
        self.create_backspace_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=DISPLAY_COLOR,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=DISPLAY_COLOR,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=DISPLAY_COLOR)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=DIGIT_COLOR, fg=LABEL_COLOR,
                               font=DIGITS_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OPERATOR_COLOR, fg=LABEL_COLOR,
                               font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=SPECIAL_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=SPECIAL_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=SPECIAL_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    def create_backspace_button(self):
        button = tk.Button(self.buttons_frame, text="⌫", bg=SPECIAL_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.backspace)
        button.grid(row=0, column=0, sticky=tk.NSEW)

    def percentage(self):
        self.current_expression = str(eval(f"{self.current_expression}/100"))
        self.update_label()

    def create_percentage_button(self):
        button = tk.Button(self.buttons_frame, text="%", bg=SPECIAL_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.percentage)
        button.grid(row=4, column=0, sticky=tk.NSEW)

    def create_scientific_buttons(self):
        functions = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "ln": math.log, "log": math.log10
        }
        i = 1
        for func, operation in functions.items():
            button = tk.Button(self.buttons_frame, text=func, bg=OPERATOR_COLOR, fg=LABEL_COLOR,
                               font=DEFAULT_FONT_STYLE, borderwidth=0,
                               command=lambda x=operation: self.apply_function(x, func))
            button.grid(row=5, column=i, sticky=tk.NSEW)
            i += 1

    def apply_function(self, operation, func_name):
        try:
            value = float(self.current_expression)
            if func_name in ["sin", "cos", "tan"]:
                value = math.radians(value)  # Convert degrees to radians
            self.current_expression = str(operation(value))
        except ValueError:
            self.current_expression = "Error"
        self.update_label()

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=SPECIAL_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window, bg=BACKGROUND_COLOR)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()

