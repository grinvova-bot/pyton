import tkinter as tk

def click(button_text):
    if button_text == "=":
        try:
            result = str(eval(entry.get()))
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif button_text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, button_text)

# Создание главного окна
root = tk.Tk()
root.title("Калькулятор")

# Поле ввода
entry = tk.Entry(root, width=20, font=('Arial', 18), borderwidth=2, relief="solid")
entry.grid(row=0, column=0, columnspan=4)

# Кнопки
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', 'C', '=', '+'
]

row_value = 1
col_value = 0

for button_text in buttons:
    tk.Button(root, text=button_text, width=5, height=2, font=('Arial', 18), command=lambda text=button_text: click(text)).grid(row=row_value, column=col_value, sticky="nsew")
    col_value += 1
    if col_value > 3:
        col_value = 0
        row_value += 1

# Настройка сетки
for i in range(4):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
pip install pyinstaller

