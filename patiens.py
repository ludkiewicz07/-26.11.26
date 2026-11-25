import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import math
import matplotlib.pyplot as plt

FILE = "patients.json"
GENDERS = ["Женский", "Мужской", "Не определён"]

if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        patients = json.load(f)
else:
    patients = []

def save():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(patients, f, ensure_ascii=False, indent=4)

def update():
    table.delete(*table.get_children())
    for i, p in enumerate(patients):
        table.insert("", "end", iid=str(i), values=(
            p["name"], p["age"], p["gender"],
            p["height"], p["weight"], p["bmi"]
        ))

def clear():
    for e in entries:
        e.delete(0, tk.END)
    gender.set("")

def get_data():
    try:
        name = entries[0].get().strip()
        age = int(entries[1].get())
        height = float(entries[2].get().replace(",", "."))
        weight = float(entries[3].get().replace(",", "."))
        sex = gender.get()

        if not name or sex not in GENDERS:
            raise ValueError
        if not (1 <= age <= 120):
            raise ValueError
        if not (1 <= height <= 300 and 1 <= weight <= 700):
            raise ValueError
        if not all(map(math.isfinite, [height, weight])):
            raise ValueError

        bmi = round(weight / (height / 100) ** 2, 2)
        return dict(name=name, age=age, gender=sex,
                    height=height, weight=weight, bmi=bmi)

    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте введённые данные!")
        return None

"""Добавление пациента"""
def add():
    p = get_data()
    if p:
        patients.append(p)
        save()
        update()
        clear()

"""Редактирование пациента"""
def edit():
    if not table.selection():
        messagebox.showwarning("Ошибка", "Выберите пациента!")
        return
    p = get_data()
    if p:
        patients[int(table.selection()[0])] = p
        save()
        update()
        clear()
"""Выбор пациента для редактирования"""
def select(event):
    if table.selection():
        p = patients[int(table.selection()[0])]
        clear()
        for e, key in zip(entries, ["name", "age", "height", "weight"]):
            e.insert(0, str(p[key]))
        gender.set(p["gender"])

"""Графики статистики"""
def statistics():
    if not patients:
        messagebox.showwarning("Ошибка", "Нет данных!")
        return

    fig, ax = plt.subplots(2, 2, figsize=(10, 7))
    sexes = GENDERS

    counts = [sum(p["gender"] == s for p in patients) for s in sexes]
    ax[0, 0].pie(counts, labels=sexes, autopct="%1.1f%%")
    ax[0, 0].set_title("Распределение по полу")

    ages = [p["age"] for p in patients]
    ax[0, 1].hist(ages, bins=min(10, len(set(ages))), edgecolor="black")
    ax[0, 1].set_title("Распределение по возрасту")
    ax[0, 1].set_xlabel("Возраст")

    data = [[p["bmi"] for p in patients if p["gender"] == s]
            for s in sexes]
    labels = [s for s, d in zip(sexes, data) if d]
    data = [d for d in data if d]
    if data:
        ax[1, 0].boxplot(data, tick_labels=labels)
    ax[1, 0].set_title("ИМТ с учётом пола")
    ax[1, 0].set_ylabel("ИМТ")

    for s in sexes:
        group = [p for p in patients if p["gender"] == s]
        ax[1, 1].scatter(
            [p["age"] for p in group],
            [p["bmi"] for p in group], label=s
        )
    ax[1, 1].set_title("ИМТ от возраста")
    ax[1, 1].set_xlabel("Возраст")
    ax[1, 1].set_ylabel("ИМТ")
    ax[1, 1].legend()

    plt.tight_layout()
    plt.show()

root = tk.Tk()
root.title("Учёт пациентов")
root.geometry("950x500")

frame = ttk.Frame(root, padding=10)
frame.pack(side="left", fill="y")

entries = []
for text in ["ФИО", "Возраст", "Рост (см)", "Вес (кг)"]:
    ttk.Label(frame, text=text).pack()
    e = ttk.Entry(frame)
    e.pack(pady=4)
    entries.append(e)

gender = ttk.Combobox(frame, values=GENDERS, state="readonly")
ttk.Label(frame, text="Пол").pack()
gender.pack(pady=5)

for text, command in [
    ("Добавить", add),
    ("Редактировать", edit),
    ("Очистить", clear),
    ("Сводная статистика", statistics)
]:
    ttk.Button(frame, text=text, command=command).pack(fill="x", pady=4)

table = ttk.Treeview(root, columns=(
    "name", "age", "gender", "height", "weight", "bmi"
), show="headings")

for col, title in zip(
    ("name", "age", "gender", "height", "weight", "bmi"),
    ("ФИО", "Возраст", "Пол", "Рост", "Вес", "ИМТ")
):
    table.heading(col, text=title)
    table.column(col, width=110)

table.pack(side="right", fill="both", expand=True, padx=10)
table.bind("<<TreeviewSelect>>", select)

BG_COLOR = "#E3ECF7"
FONT_MAIN = ("Times New Roman", 12)
FONT_BOLD = ("Times New Roman", 12, "bold")

root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use("clam")
style.configure(".", background=BG_COLOR, font=FONT_MAIN)
style.configure("TFrame", background=BG_COLOR)
style.configure("TLabel", background=BG_COLOR, font=FONT_MAIN)
style.configure("TButton", font=FONT_MAIN)
style.configure("TEntry", fieldbackground="#FFFFFF")
style.configure("TCombobox", fieldbackground="#FFFFFF")
style.configure("Treeview", font=FONT_MAIN, rowheight=26, background="#FFFFFF", fieldbackground="#FFFFFF")
style.configure("Treeview.Heading", font=FONT_BOLD)

for e in entries:
    e.configure(font=FONT_MAIN)
gender.configure(font=FONT_MAIN)

update()
root.mainloop()