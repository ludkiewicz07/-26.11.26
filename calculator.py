import tkinter as tk
from tkinter import messagebox
import math
import re

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("320x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#951e28") 

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            root,
            textvariable=self.entry_var,
            font=("Arial", 20),
            bd=10,
            insertwidth=2,
            width=14,
            borderwidth=4,
            justify="right",
            bg="#ffffff",       
            fg="#451010", 
        )
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=15, sticky="nsew")

        vcmd = (root.register(self.validate_input), "%P")
        self.entry.config(validate="key", validatecommand=vcmd)

        self.root.bind("<Return>", lambda event: self.calculate())
        self.root.bind("<Escape>", lambda event: self.clear())

        buttons = [
            ("C", 1, 0), ("sqrt", 1, 1), ("<-", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("=", 5, 2, 2),
        ]

        for i in buttons:
            text = i[0]
            row = i[1]
            col = i[2]
            cols_count = i[3] if len(i) > 3 else 1

            action = lambda x=text: self.on_button_click(x)
            b = tk.Button(
                root,
                text=text,
                font=("Arial", 16),
                command=action,
                height=2,
                width=5,
            )
            b.grid(row=row, column=col, columnspan=cols_count, padx=5, pady=5, sticky="nsew")

        for i in range(6):
            root.grid_rowconfigure(i, weight=1)
        for j in range(4):
            root.grid_columnconfigure(j, weight=1)

        self.entry.focus_set()

    def validate_input(self, new_value):
        """Разрешает вводить с клавиатуры только допустимые символы."""
        if new_value == "":
            return True
        return bool(re.match(r"^[0-9+\-*/.]+$", new_value))

    def on_button_click(self, char):
        if char == "C":
            self.clear()
        elif char == "<-":
            self.backspace()
        elif char == "=":
            self.calculate()
        elif char == "sqrt":
            self.calculate_sqrt()
        else:
            self.entry.insert(tk.END, char)

    def clear(self):
        self.entry_var.set("")

    def backspace(self):
        current = self.entry_var.get()
        self.entry_var.set(current[:-1])

    def calculate_sqrt(self):
        """Вычисление квадратного корня с проверкой на отрицательное число."""
        math_expr = self.entry_var.get().strip()
        if math_expr == "":
            return
        try:
            value = float(eval(math_expr))
            if value < 0:
                messagebox.showerror("Ошибка вычисления", "Извлечение квадратного корня из отрицательного числа не поддерживается.")
                return
            result = math.sqrt(value)
            self.entry_var.set(str(int(result)) if result.is_integer() else str(round(result, 8)))
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Операция не поддерживается")
        except Exception:
            messagebox.showerror("Ошибка", "Некорректный ввод")

    def calculate(self):
        """Вычисление арифметического выражения с обработкой ошибок."""
        math_expr = self.entry_var.get().strip()
        if math_expr == "":
            return
        try:
            if not re.match(r"^[0-9+\-*/.]+$", math_expr):
                raise ValueError("Недопустимые символы")

            result = eval(math_expr)
            if isinstance(result, float):
                result = int(result) if result.is_integer() else round(result, 8)
            self.entry_var.set(str(result))

        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Операция не поддерживается")
        except SyntaxError:
            messagebox.showerror("Ошибка", "Синтаксическая ошибка")
        except Exception:
            messagebox.showerror("Ошибка", "Некорректный ввод")


root = tk.Tk()
app = CalculatorApp(root)
root.mainloop()