import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

# Получение курса валют
def get_exchange_rate(base_currency, target_currency, api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    return data['conversion_rates'].get(target_currency)

# Сохранение истории конвертаций
def save_history(history):
    with open("history.json", "w") as file:
        json.dump(history, file)

# Загрузка истории конвертаций
def load_history():
    try:
        with open("history.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Проверка корректности ввода
def validate_input(amount):
    try:
        amount = float(amount)
        return amount > 0
    except ValueError:
        return False

# Обработка конвертации
def convert_currency():
    base_currency = base_currency_combobox.get()
    target_currency = target_currency_combobox.get()
    amount = amount_entry.get()

    if not validate_input(amount):
        messagebox.showerror("Ошибка ввода", "Сумма должна быть положительным числом.")
        return

    amount = float(amount)
    api_key = "YOUR_API_KEY"  # Вставьте сюда свой API-ключ
    exchange_rate = get_exchange_rate(base_currency, target_currency, api_key)
    
    if exchange_rate is None:
        messagebox.showerror("Ошибка", f"Не удалось получить курс для {target_currency}.")
        return
    
    converted_amount = amount * exchange_rate
    history.append({
        "base": base_currency,
        "target": target_currency,
        "amount": amount,
        "converted": converted_amount
    })
    
    save_history(history)
    
    # Обновление таблицы истории
    update_history_table()
    result_label.config(text=f"Конвертированная сумма: {converted_amount:.2f} {target_currency}")

# Обновление таблицы истории
def update_history_table():
    for row in history_tree.get_children():
        history_tree.delete(row)
    for record in history:
        history_tree.insert("", "end", values=(record["base"], record["amount"], record["target"], record["converted"]))

# Настройка GUI
root = tk.Tk()
root.title("Currency Converter")

# Выбор валют
base_currency_combobox = ttk.Combobox(root, values=["USD", "EUR", "RUB"], state='readonly')
base_currency_combobox.grid(row=0, column=0)

target_currency_combobox = ttk.Combobox(root, values=["USD", "EUR", "RUB"], state='readonly')
target_currency_combobox.grid(row=0, column=1)

# Поле ввода суммы
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=2)

# Кнопка конвертации
convert_button = tk.Button(root, text="Конвертировать", command=convert_currency)
convert_button.grid(row=0, column=3)

# Результат
result_label = tk.Label(root, text="")
result_label.grid(row=1, columnspan=4)

# Таблица истории
history_tree = ttk.Treeview(root, columns=("Base", "Amount", "Target", "Converted"), show="headings")
history_tree.heading("Base", text="Из валюты")
history_tree.heading("Amount", text="Сумма")
history_tree.heading("Target", text="В валюту")
history_tree.heading("Converted", text="Конвертированная сумма")
history_tree.grid(row=2, columnspan=4)

# Загрузка истории
history = load_history()
update_history_table()

# Запуск GUI
root.mainloop()