import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

def calculate():
    try:
        L = float(entry_L.get())
        D = float(entry_D.get())
        Dmax = float(entry_Dmax.get())
        Dmin = float(entry_Dmin.get())
        m = float(entry_m.get())
        M = float(entry_M.get())
        IT = float(entry_IT.get())
        C_мат = float(entry_C_mat.get())
        C_уд = float(entry_C_ud.get())

        kIT = 1 + IT / 100
        kM = 1.3 if combo_material.get() == "Плохая" else 1
        kK = 1
        включенные_функции = []
        if check_keyway.get():
            kK = 1.1
            включенные_функции.append("Шпоночный паз")
        if check_gear.get():
            kK = 1.6
            включенные_функции.append("Зубчатая поверхность")
        if not включенные_функции:
            включенные_функции.append("Нет конструктивных элементов")
            
        kZ = 1.2 if combo_blank.get() == "Штамповка" else 1
        включенные_функции.append("Заготовка: " + combo_blank.get())
        включенные_функции.append("Обрабатываемость: " + combo_material.get())

        # Расчет стоимости
        cost = kM * kK * kZ * ((M - m) * C_мат + m * C_уд)

        result_text = f"Стоимость обработки: {cost:.2f} руб."
        functions_text = "; ".join(включенные_функции)

        result_label.config(text=f"{result_text}\nВключенные функции: {functions_text}")

        # Сохранение результата в CSV-файл
        save_to_csv(result_text, functions_text)
    
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения!")

def save_to_csv(result, functions):
    file_exists = os.path.isfile("data.csv")
    with open("data.csv", mode="a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Результат", "Включенные функции"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({"Результат": result, "Включенные функции": functions})

# Создание окна
root = tk.Tk()
root.title("Расчет стоимости обработки детали")
root.geometry("400x550")

frame_inputs = ttk.LabelFrame(root, text="Входные данные")
frame_inputs.pack(padx=10, pady=10, fill="both", expand=True)

labels = ["Длина детали (L), мм:", "Средний диаметр (D), мм:", 
          "Макс. диаметр (Dmax), мм:", "Мин. диаметр (Dmin), мм:", 
          "Масса детали (m), кг:", "Масса заготовки (M), кг:", 
          "Доля точных поверхностей IT, %:", 
          "Стоимость материала, руб/кг:", "Удельные затраты труда, руб/кг:"]
entries = []

for lbl in labels:
    frame = ttk.Frame(frame_inputs)
    frame.pack(fill="x", padx=5, pady=2)
    label = ttk.Label(frame, text=lbl, width=30)
    label.pack(side="left")
    entry = ttk.Entry(frame)
    entry.pack(side="right", fill="x", expand=True)
    entries.append(entry)

entry_L, entry_D, entry_Dmax, entry_Dmin, entry_m, entry_M, entry_IT, entry_C_mat, entry_C_ud = entries

# Выбор параметров
frame_options = ttk.LabelFrame(root, text="Выбор параметров")
frame_options.pack(padx=10, pady=10, fill="both", expand=True)

ttk.Label(frame_options, text="Обрабатываемость:").pack(anchor="w", padx=5)
combo_material = ttk.Combobox(frame_options, values=["Нормальная", "Плохая"])
combo_material.pack(fill="x", padx=5)
combo_material.current(0)

ttk.Label(frame_options, text="Заготовка:").pack(anchor="w", padx=5)
combo_blank = ttk.Combobox(frame_options, values=["Прокат", "Штамповка"])
combo_blank.pack(fill="x", padx=5)
combo_blank.current(0)

frame_check = ttk.Frame(frame_options)
frame_check.pack(pady=5, fill="x")

check_keyway = tk.BooleanVar()
check_gear = tk.BooleanVar()
ttk.Checkbutton(frame_check, text="Шпоночный паз", variable=check_keyway).pack(side="left", padx=5)
ttk.Checkbutton(frame_check, text="Зубчатая поверхность", variable=check_gear).pack(side="right", padx=5)

btn_calc = ttk.Button(root, text="Рассчитать", command=calculate)
btn_calc.pack(pady=10, padx=20, fill="x")

result_label = ttk.Label(root, text="Результат: -", font=("Arial", 12, "bold"), justify="center")
result_label.pack(pady=10)

root.mainloop()