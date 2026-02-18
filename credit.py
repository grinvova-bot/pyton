import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class CreditCard:
    def __init__(self, name, number, balance, limit):
        self.name = name
        self.number = number
        self.balance = balance
        self.limit = limit

class Deposit:
    def __init__(self, name, account_number, balance, interest_rate):
        self.name = name
        self.account_number = account_number
        self.balance = balance
        self.interest_rate = interest_rate

class FinanceManager:
    def __init__(self):
        self.credit_cards = []
        self.deposits = []

    def add_credit_card(self, name, number, balance, limit):
        card = CreditCard(name, number, balance, limit)
        self.credit_cards.append(card)
        messagebox.showinfo("Success", f"Credit card {name} added successfully.")

    def add_deposit(self, name, account_number, balance, interest_rate):
        deposit = Deposit(name, account_number, balance, interest_rate)
        self.deposits.append(deposit)
        messagebox.showinfo("Success", f"Deposit {name} added successfully.")

    def view_credit_cards(self):
        if not self.credit_cards:
            messagebox.showinfo("Info", "No credit cards found.")
            return
        info = "\n".join([f"Name: {card.name}, Number: {card.number}, Balance: {card.balance}, Limit: {card.limit}" for card in self.credit_cards])
        messagebox.showinfo("Credit Cards", info)

    def view_deposits(self):
        if not self.deposits:
            messagebox.showinfo("Info", "No deposits found.")
            return
        info = "\n".join([f"Name: {deposit.name}, Account Number: {deposit.account_number}, Balance: {deposit.balance}, Interest Rate: {deposit.interest_rate}" for deposit in self.deposits])
        messagebox.showinfo("Deposits", info)

    def update_credit_card(self, number, new_balance, new_limit):
        for card in self.credit_cards:
            if card.number == number:
                card.balance = new_balance
                card.limit = new_limit
                messagebox.showinfo("Success", f"Credit card {card.name} updated successfully.")
                return
        messagebox.showinfo("Info", "Credit card not found.")

    def update_deposit(self, account_number, new_balance, new_interest_rate):
        for deposit in self.deposits:
            if deposit.account_number == account_number:
                deposit.balance = new_balance
                deposit.interest_rate = new_interest_rate
                messagebox.showinfo("Success", f"Deposit {deposit.name} updated successfully.")
                return
        messagebox.showinfo("Info", "Deposit not found.")

class FinanceApp:
    def __init__(self, root):
        self.manager = FinanceManager()
        self.root = root
        self.root.title("Finance Manager")

        self.create_widgets()
        self.update_summary_table()

    def create_widgets(self):
        # Main Menu
        self.main_menu = ttk.Frame(self.root)
        self.main_menu.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(self.main_menu, text="Finance Manager", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Button(self.main_menu, text="Add Credit Card", command=self.show_add_credit_card).grid(row=1, column=0, pady=5)
        ttk.Button(self.main_menu, text="View Credit Cards", command=self.manager.view_credit_cards).grid(row=1, column=1, pady=5)
        ttk.Button(self.main_menu, text="Update Credit Card", command=self.show_update_credit_card).grid(row=1, column=2, pady=5)
        ttk.Button(self.main_menu, text="Add Deposit", command=self.show_add_deposit).grid(row=2, column=0, pady=5)
        ttk.Button(self.main_menu, text="View Deposits", command=self.manager.view_deposits).grid(row=2, column=1, pady=5)
        ttk.Button(self.main_menu, text="Update Deposit", command=self.show_update_deposit).grid(row=2, column=2, pady=5)

        # Add Credit Card Frame
        self.add_credit_card_frame = ttk.Frame(self.root)
        self.create_add_credit_card_widgets()

        # Update Credit Card Frame
        self.update_credit_card_frame = ttk.Frame(self.root)
        self.create_update_credit_card_widgets()

        # Add Deposit Frame
        self.add_deposit_frame = ttk.Frame(self.root)
        self.create_add_deposit_widgets()

        # Update Deposit Frame
        self.update_deposit_frame = ttk.Frame(self.root)
        self.create_update_deposit_widgets()

        # Summary Table
        self.summary_table = ttk.Treeview(self.root, columns=("Type", "Name", "Number", "Balance", "Limit/Rate"), show="headings")
        self.summary_table.heading("Type", text="Type")
        self.summary_table.heading("Name", text="Name")
        self.summary_table.heading("Number", text="Number")
        self.summary_table.heading("Balance", text="Balance")
        self.summary_table.heading("Limit/Rate", text="Limit/Rate")
        self.summary_table.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def create_add_credit_card_widgets(self):
        ttk.Label(self.add_credit_card_frame, text="Name").grid(row=0, column=0, pady=5)
        self.add_credit_card_name_entry = ttk.Entry(self.add_credit_card_frame)
        self.add_credit_card_name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.add_credit_card_frame, text="Number").grid(row=1, column=0, pady=5)
        self.add_credit_card_number_entry = ttk.Entry(self.add_credit_card_frame)
        self.add_credit_card_number_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.add_credit_card_frame, text="Balance").grid(row=2, column=0, pady=5)
        self.add_credit_card_balance_entry = ttk.Entry(self.add_credit_card_frame)
        self.add_credit_card_balance_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.add_credit_card_frame, text="Limit").grid(row=3, column=0, pady=5)
        self.add_credit_card_limit_entry = ttk.Entry(self.add_credit_card_frame)
        self.add_credit_card_limit_entry.grid(row=3, column=1, pady=5)

        ttk.Button(self.add_credit_card_frame, text="Add", command=self.add_credit_card).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(self.add_credit_card_frame, text="Back", command=self.show_main_menu).grid(row=5, column=0, columnspan=2, pady=5)

    def create_update_credit_card_widgets(self):
        ttk.Label(self.update_credit_card_frame, text="Number").grid(row=0, column=0, pady=5)
        self.update_credit_card_number_entry = ttk.Entry(self.update_credit_card_frame)
        self.update_credit_card_number_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.update_credit_card_frame, text="New Balance").grid(row=1, column=0, pady=5)
        self.update_credit_card_balance_entry = ttk.Entry(self.update_credit_card_frame)
        self.update_credit_card_balance_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.update_credit_card_frame, text="New Limit").grid(row=2, column=0, pady=5)
        self.update_credit_card_limit_entry = ttk.Entry(self.update_credit_card_frame)
        self.update_credit_card_limit_entry.grid(row=2, column=1, pady=5)

        ttk.Button(self.update_credit_card_frame, text="Update", command=self.update_credit_card).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(self.update_credit_card_frame, text="Back", command=self.show_main_menu).grid(row=4, column=0, columnspan=2, pady=5)

    def create_add_deposit_widgets(self):
        ttk.Label(self.add_deposit_frame, text="Name").grid(row=0, column=0, pady=5)
        self.add_deposit_name_entry = ttk.Entry(self.add_deposit_frame)
        self.add_deposit_name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.add_deposit_frame, text="Account Number").grid(row=1, column=0, pady=5)
        self.add_deposit_account_number_entry = ttk.Entry(self.add_deposit_frame)
        self.add_deposit_account_number_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.add_deposit_frame, text="Balance").grid(row=2, column=0, pady=5)
        self.add_deposit_balance_entry = ttk.Entry(self.add_deposit_frame)
        self.add_deposit_balance_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.add_deposit_frame, text="Interest Rate").grid(row=3, column=0, pady=5)
        self.add_deposit_interest_rate_entry = ttk.Entry(self.add_deposit_frame)
        self.add_deposit_interest_rate_entry.grid(row=3, column=1, pady=5)

        ttk.Button(self.add_deposit_frame, text="Add", command=self.add_deposit).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(self.add_deposit_frame, text="Back", command=self.show_main_menu).grid(row=5, column=0, columnspan=2, pady=5)

    def create_update_deposit_widgets(self):
        ttk.Label(self.update_deposit_frame, text="Account Number").grid(row=0, column=0, pady=5)
        self.update_deposit_account_number_entry = ttk.Entry(self.update_deposit_frame)
        self.update_deposit_account_number_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.update_deposit_frame, text="New Balance").grid(row=1, column=0, pady=5)
        self.update_deposit_balance_entry = ttk.Entry(self.update_deposit_frame)
        self.update_deposit_balance_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.update_deposit_frame, text="New Interest Rate").grid(row=2, column=0, pady=5)
        self.update_deposit_interest_rate_entry = ttk.Entry(self.update_deposit_frame)
        self.update_deposit_interest_rate_entry.grid(row=2, column=1, pady=5)

        ttk.Button(self.update_deposit_frame, text="Update", command=self.update_deposit).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(self.update_deposit_frame, text="Back", command=self.show_main_menu).grid(row=4, column=0, columnspan=2, pady=5)

    def show_main_menu(self):
        self.main_menu.grid()
        self.add_credit_card_frame.grid_forget()
        self.update_credit_card_frame.grid_forget()
        self.add_deposit_frame.grid_forget()
        self.update_deposit_frame.grid_forget()

    def show_add_credit_card(self):
        self.main_menu.grid_forget()
        self.add_credit_card_frame.grid(row=0, column=0, padx=10, pady=10)

    def show_update_credit_card(self):
        self.main_menu.grid_forget()
        self.update_credit_card_frame.grid(row=0, column=0, padx=10, pady=10)

    def show_add_deposit(self):
        self.main_menu.grid_forget()
        self.add_deposit_frame.grid(row=0, column=0, padx=10, pady=10)

    def show_update_deposit(self):
        self.main_menu.grid_forget()
        self.update_deposit_frame.grid(row=0, column=0, padx=10, pady=10)

    def add_credit_card(self):
        name = self.add_credit_card_name_entry.get()
        number = self.add_credit_card_number_entry.get()
        balance = float(self.add_credit_card_balance_entry.get())
        limit = float(self.add_credit_card_limit_entry.get())
        self.manager.add_credit_card(name, number, balance, limit)
        self.update_summary_table()
        self.show_main_menu()

    def update_credit_card(self):
        number = self.update_credit_card_number_entry.get()
        new_balance = float(self.update_credit_card_balance_entry.get())
        new_limit = float(self.update_credit_card_limit_entry.get())
        self.manager.update_credit_card(number, new_balance, new_limit)
        self.update_summary_table()
        self.show_main_menu()

    def add_deposit(self):
        name = self.add_deposit_name_entry.get()
        account_number = self.add_deposit_account_number_entry.get()
        balance = float(self.add_deposit_balance_entry.get())
        interest_rate = float(self.add_deposit_interest_rate_entry.get())
        self.manager.add_deposit(name, account_number, balance, interest_rate)
        self.update_summary_table()
        self.show_main_menu()

    def update_deposit(self):
        account_number = self.update_deposit_account_number_entry.get()
        new_balance = float(self.update_deposit_balance_entry.get())
        new_interest_rate = float(self.update_deposit_interest_rate_entry.get())
        self.manager.update_deposit(account_number, new_balance, new_interest_rate)
        self.update_summary_table()
        self.show_main_menu()

    def update_summary_table(self):
        # Clear the table
        for item in self.summary_table.get_children():
            self.summary_table.delete(item)

        # Add credit cards
        for card in self.manager.credit_cards:
            self.summary_table.insert("", "end", values=("Credit Card", card.name, card.number, card.balance, card.limit))

        # Add deposits
        for deposit in self.manager.deposits:
            self.summary_table.insert("", "end", values=("Deposit", deposit.name, deposit.account_number, deposit.balance, deposit.interest_rate))

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = FinanceApp(root)
    root.mainloop()

