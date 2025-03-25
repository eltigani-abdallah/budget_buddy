import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from tkcalendar import Calendar, DateEntry
import secrets
import string
import os
import json
from datetime import datetime
from collections import defaultdict
import accounts

def on_close():
    save_data(app)
    logout()
    print("shutting down...")
    app.quit()
    exit()

def logout():
    if os.path.exists("./assets/session.json"):
        os.remove("./assets/session.json")
    print("you have been logged out")
    exit()

def load_lang(langs):
    with open(langs, "r", encoding="utf-8") as file:
        return json.load(file)

def load_data():
    if os.path.exists("./assets/data.json"):
        with open("./assets/data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return (
                data.get("transactions", []),
                data.get("beneficiaries", {}),
                data.get("current_user_email", ""),
                data.get("accounts", {})
            )
    return [], {}, "", {}

def save_data(app):
    data = {
        "transactions": app.transactions,
        "beneficiaries": app.beneficiaries,
        "current_user_email": app.current_user_email,
        "accounts": app.accounts
    }
    with open("./assets/data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

lang_dict = load_lang("./assets/lang.json")

def translate(lang, key):
    return lang_dict.get(lang, {}).get(key, f"[{key} not found]")

class FinanceManagerApp(ctk.CTk):
    """
    Financial management application using CustomTkinter for the user interface.

    Attributes:
        language (str): Current language of the user interface.
        translations (dict): Dictionary containing translations for each supported language.
        accounts (dict): Dictionary containing account balances.
        user_accounts (dict): Dictionary to store user accounts.
        current_account (str): Currently selected account.
        beneficiaries (dict): Dictionary to store beneficiary information.
    """

    def __init__(self):
        """
        Initializes the FinanceManagerApp application.
        Configures the user interface, accounts, and translations.
        """
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.language = "french"

        self.title("Finance Manager")
        self.geometry("1000x700")

        self.transactions, self.beneficiaries, self.current_user_email, self.accounts = load_data()
        # If no accounts are loaded, initialize with default accounts
        if not self.accounts:
            self.accounts = {
                "Main Account": 450,
                "Savings Account": 1600,
                "Business Account": 7500,
            }
        self.current_account = "Main Account"
        self.create_widgets()
        self.refresh_overview()
        self.update_email_label()  # Update the email label

    def create_widgets(self):
        """
        Creates and configures the user interface widgets.
        """
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill='x', pady=5)

        self.logout_button = ctk.CTkButton(top_frame, text=translate(self.language, "logout_button"), command=self.logout)
        self.logout_button.pack(side='left', padx=10)

        # Add a label to display the user's email address
        self.email_label = ctk.CTkLabel(top_frame, text=f"Email: {self.current_user_email}")
        self.email_label.pack(side='right', padx=10)

        self.language_menu = ctk.CTkOptionMenu(top_frame, values=["french", "english", "russian", "korean"], command=self.change_language)
        self.language_menu.pack(side='right', padx=10)
        self.language_menu.set(self.language)

        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(pady=20, fill='both', expand=True)

        self.transactions_tab = self.notebook.add("Transactions")
        self.overview_tab = self.notebook.add("Overview")
        self.export_tab = self.notebook.add("Export")
        self.notifications_tab = self.notebook.add("Notifications")
        self.beneficiaries_tab = self.notebook.add("Beneficiaries")
        self.history_tab = self.notebook.add("History")

        custom_font = ctk.CTkFont(family="KalniaGlaze-VariableFont_wdth,wght", size=24)

        self.balance_label = ctk.CTkLabel(self.transactions_tab, text="", font=("Helvetica", 18))
        self.balance_label.pack(pady=10)

        self.reference_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=translate(self.language, "reference_placeholder"))
        self.reference_entry.pack(pady=5)

        self.description_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=translate(self.language, "description_placeholder"))
        self.description_entry.pack(pady=5)

        self.amount_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=translate(self.language, "amount_placeholder"))
        self.amount_entry.pack(pady=5)

        self.category_entry = ctk.CTkComboBox(self.transactions_tab, values=["", "Bills", "Leisure", "Dining", "Travels", "Other Categories"], text_color="white")
        self.category_entry.pack(pady=5)

        self.action_frame = ctk.CTkFrame(self.transactions_tab)
        self.action_frame.pack(pady=5)

        # Move the bank account above the beneficiary
        self.account_label = ctk.CTkLabel(self.action_frame, text=translate(self.language, "account_label"))
        self.account_label.grid(row=0, column=3, padx=5, pady=5)
        self.account_entry = ctk.CTkComboBox(self.action_frame, values=list(self.accounts.keys()), command=self.switch_account)
        self.account_entry.grid(row=0, column=4, padx=5, pady=5)
        self.account_entry.set(self.current_account)

        self.beneficiary_label = ctk.CTkLabel(self.action_frame, text=translate(self.language, "beneficiary_label"))
        self.beneficiary_label.grid(row=1, column=3, padx=5, pady=5)
        self.beneficiary_entry = ctk.CTkEntry(self.action_frame, placeholder_text=translate(self.language, "beneficiary_label"))
        self.beneficiary_entry.grid(row=1, column=4, padx=5, pady=5)

        self.deposit_button = ctk.CTkButton(self.action_frame, text=translate(self.language, "deposit_button"), command=self.deposit)
        self.deposit_button.grid(row=2, column=0, padx=5, pady=5)

        self.withdraw_button = ctk.CTkButton(self.action_frame, text=translate(self.language, "withdraw_button"), command=self.withdraw)
        self.withdraw_button.grid(row=2, column=1, padx=5, pady=5)

        self.transfer_button = ctk.CTkButton(self.action_frame, text=translate(self.language, "transfer_button"), command=self.transfer)
        self.transfer_button.grid(row=2, column=2, padx=5, pady=5)

        # Add a field to specify amounts for each destination account
        self.multi_transfer_frame = ctk.CTkFrame(self.transactions_tab)
        self.multi_transfer_frame.pack(pady=5)

        self.multi_transfer_label = ctk.CTkLabel(self.multi_transfer_frame, text="Amounts to transfer:")
        self.multi_transfer_label.pack()

        self.multi_transfer_entries = {}
        for account in self.accounts.keys():
            if account != self.current_account:
                label = ctk.CTkLabel(self.multi_transfer_frame, text=f"to {account}:")
                label.pack(side='left', padx=10)  # Add spacing
                entry = ctk.CTkEntry(self.multi_transfer_frame)
                entry.pack(side='left', padx=10)  # Add spacing
                self.multi_transfer_entries[account] = entry

        self.multi_transfer_button = ctk.CTkButton(self.action_frame, text="Perform Multiple Transfers", command=self.multi_transfer)
        self.multi_transfer_button.grid(row=2, column=3, padx=5, pady=5, columnspan=2)

        self.search_frame = ctk.CTkFrame(self.transactions_tab)
        self.search_frame.pack(pady=10)

        self.date_label = ctk.CTkLabel(self.search_frame, text=translate(self.language, "date_label"))
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(self.search_frame, width=12, background='lightblue', foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.delete(0, 'end')  # Clear initial date

        self.clear_date_button = ctk.CTkButton(self.search_frame, text="Clear", command=lambda: self.date_entry.delete(0, 'end'))
        self.clear_date_button.grid(row=0, column=2, padx=5, pady=5)

        self.start_date_label = ctk.CTkLabel(self.search_frame, text=translate(self.language, "start_date_label"))
        self.start_date_label.grid(row=1, column=0, padx=5, pady=5)
        self.start_date_entry = DateEntry(self.search_frame, width=12, background='lightblue', foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.start_date_entry.delete(0, 'end')  # Clear initial date

        self.clear_end_date_button = ctk.CTkButton(self.search_frame, text="Clear", command=lambda: self.end_date_entry.delete(0, 'end'))
        self.clear_end_date_button.grid(row=2, column=2, padx=5, pady=5)

        self.end_date_label = ctk.CTkLabel(self.search_frame, text=translate(self.language, "end_date_label"))
        self.end_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.end_date_entry = DateEntry(self.search_frame, width=12, background='lightblue', foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.end_date_entry.delete(0, 'end')  # Clear initial date

        self.clear_start_date_button = ctk.CTkButton(self.search_frame, text="Clear", command=lambda: self.start_date_entry.delete(0, 'end'))
        self.clear_start_date_button.grid(row=1, column=2, padx=5, pady=5)

        self.min_amount_label = ctk.CTkLabel(self.search_frame, text=translate(self.language, "min_amount_label"))
        self.min_amount_label.grid(row=0, column=3, padx=5, pady=5)
        self.min_amount_entry = ctk.CTkEntry(self.search_frame)
        self.min_amount_entry.grid(row=0, column=4, padx=5, pady=5)

        self.max_amount_label = ctk.CTkLabel(self.search_frame, text=translate(self.language, "max_amount_label"))
        self.max_amount_label.grid(row=1, column=3, padx=5, pady=5)
        self.max_amount_entry = ctk.CTkEntry(self.search_frame)
        self.max_amount_entry.grid(row=1, column=4, padx=5, pady=5)

        self.category_label = ctk.CTkLabel(self.search_frame, text=translate(self.language, "category_label"))
        self.category_label.grid(row=2, column=3, padx=5, pady=5)
        self.category_search_entry = ctk.CTkComboBox(self.search_frame, values=["", "Bills", "Leisure", "Dining", "Travels", "Other Categories"], text_color="white")
        self.category_search_entry.grid(row=2, column=4, padx=5, pady=5)

        self.type_label = ctk.CTkLabel(self.search_frame, text=translate(self.language, "type_label"))
        self.type_label.grid(row=3, column=0, padx=5, pady=5)
        self.type_entry = ctk.CTkComboBox(self.search_frame, values=["", "Withdrawal", "Transfer", "Deposit"], text_color="white")
        self.type_entry.grid(row=3, column=1, padx=5, pady=5)

        self.sort_label = ctk.CTkLabel(self.search_frame, text=translate(self.language, "sort_label"))
        self.sort_label.grid(row=3, column=3, padx=5, pady=5)
        self.sort_entry = ctk.CTkComboBox(self.search_frame, values=["", "ASC", "DESC"], text_color="white")
        self.sort_entry.grid(row=3, column=4, padx=5, pady=5)

        self.search_button = ctk.CTkButton(self.transactions_tab, text=translate(self.language, "search_button"), command=self.search_transactions)
        self.search_button.pack(pady=5)

        self.transactions_listbox = ctk.CTkTextbox(self.transactions_tab, width=760, height=200)
        self.transactions_listbox.pack(pady=10)

        self.alert_label = ctk.CTkLabel(self.overview_tab, text="", text_color="red")
        self.alert_label.pack(pady=10)

        # Button to display the pie chart
        self.show_chart_button = ctk.CTkButton(self.overview_tab, text="Show Pie Chart", command=self.show_pie_chart)
        self.show_chart_button.pack(pady=10)

        # Frame to contain the chart
        self.chart_frame = ctk.CTkFrame(self.overview_tab, width=600, height=600)
        self.chart_frame.pack(pady=10)

        self.export_button = ctk.CTkButton(self.export_tab, text=translate(self.language, "export_button"), command=self.export_to_csv)
        self.export_button.pack(pady=20)

        self.check_alerts_button = ctk.CTkButton(self.notifications_tab, text=translate(self.language, "check_alerts_button"), command=self.check_and_notify_alerts)
        self.check_alerts_button.pack(pady=20)

        self.add_beneficiary_label = ctk.CTkLabel(self.beneficiaries_tab, text=translate(self.language, "add_beneficiary_label"))
        self.add_beneficiary_label.pack(pady=25)

        self.beneficiary_email_entry = ctk.CTkEntry(self.beneficiaries_tab, placeholder_text=translate(self.language, "beneficiary_label"))
        self.beneficiary_email_entry.pack(pady=5)

        self.add_beneficiary_button = ctk.CTkButton(self.beneficiaries_tab, text=translate(self.language, "add_beneficiary_button"), command=self.add_beneficiary)
        self.add_beneficiary_button.pack(pady=5)

        self.beneficiary_listbox = ctk.CTkTextbox(self.beneficiaries_tab, width=760, height=200)
        self.beneficiary_listbox.pack(pady=10)

        self.history_listbox = ctk.CTkTextbox(self.history_tab, width=760, height=400)
        self.history_listbox.pack(pady=10)

        self.refresh_history_button = ctk.CTkButton(self.history_tab, text="Refresh History", command=self.display_history)
        self.refresh_history_button.pack(pady=5)

        self.theme_menu = ctk.CTkOptionMenu(self, values=["dark", "light"], command=self.change_theme)
        self.theme_menu.pack(pady=10)
        self.theme_menu.set("dark")

    def clear_date(self):
        """
        Clears the date in the date field.
        """
        self.date_entry.set_date(None)

    def clear_start_date(self):
        """
        Clears the start date in the start date field.
        """
        self.start_date_entry.set_date(None)

    def clear_end_date(self):
        """
        Clears the end date in the end date field.
        """
        self.end_date_entry.set_date(None)

    def update_email_label(self):
        """
        Updates the email label with the user's current email address.
        """
        self.email_label.configure(text=f"Email: {self.current_user_email}")

    def show_pie_chart(self):
        """
        Displays a pie chart of transaction categories based on the user's spending.
        """
        # Filter transactions by the current user's email
        user_transactions = [t for t in self.transactions if t['user_email'] == self.current_user_email]

        # Calculate totals by category
        category_totals = defaultdict(float)
        for transaction in user_transactions:
            if transaction['type'] in ['Withdrawal', 'Transfer']:  # Only consider expenses
                if transaction['category'] in ["Bills", "Leisure", "Dining", "Travels", "Other Categories"]:
                    category_totals[transaction['category']] += float(transaction['amount'])

        # Create the pie chart
        categories = list(category_totals.keys())
        amounts = list(category_totals.values())
        if not amounts:
            print("No transactions available to display for the current user.")
            return

        max_value = max(amounts)
        max_index = amounts.index(max_value)
        explode = [0.1 if i == max_index else 0 for i in range(len(amounts))]

        fig, ax = plt.subplots(figsize=(8, 8))  # Increase the figure size
        ax.pie(amounts, labels=categories, explode=explode, shadow=True, autopct="%1.1f%%")

        # Clear previous content of the frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Embed the chart in the interface
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def change_theme(self, theme):
        """
        Changes the application theme.

        Args:
            theme (str): The theme to apply ("dark" or "light").
        """
        ctk.set_appearance_mode(theme)

    def change_language(self, new_language):
        """
        Changes the user interface language.

        Args:
            new_language (str): The new language to apply.
        """
        self.language = new_language
        self.update_translations()

    def update_translations(self):
        """
        Updates the user interface translations based on the current language.
        """
        translations = lang_dict[self.language]
        self.title(translations["title"])
        self.balance_label.configure(text=translations["balance_label"] + " " + f"{self.accounts[self.current_account]:.2f} €")
        self.alert_label.configure(text=translations.get("alert_label", ""))
        self.deposit_button.configure(text=translations["deposit_button"])
        self.withdraw_button.configure(text=translations["withdraw_button"])
        self.transfer_button.configure(text=translations["transfer_button"])
        self.search_button.configure(text=translations["search_button"])
        self.export_button.configure(text=translations["export_button"])
        self.check_alerts_button.configure(text=translations["check_alerts_button"])
        self.logout_button.configure(text=translations["logout_button"])
        self.date_label.configure(text=translations["date_label"])
        self.category_label.configure(text=translations["category_label"])
        self.type_label.configure(text=translations["type_label"])
        self.start_date_label.configure(text=translations["start_date_label"])
        self.end_date_label.configure(text=translations["end_date_label"])
        self.min_amount_label.configure(text=translations["min_amount_label"])
        self.max_amount_label.configure(text=translations["max_amount_label"])
        self.sort_label.configure(text=translations["sort_label"])
        self.reference_entry.configure(placeholder_text=translations["reference_placeholder"])
        self.description_entry.configure(placeholder_text=translations["description_placeholder"])
        self.amount_entry.configure(placeholder_text=translations["amount_placeholder"])
        self.account_label.configure(text=translations["account_label"])
        self.beneficiary_label.configure(text=translations["beneficiary_label"])
        self.add_beneficiary_label.configure(text=translations["add_beneficiary_label"])
        self.beneficiary_email_entry.configure(placeholder_text=translations["beneficiary_label"])
        self.add_beneficiary_button.configure(text=translations["add_beneficiary_button"])

    def switch_account(self, new_account):
        """
        Changes the currently selected account.

        Args:
            new_account (str): The new account to select.
        """
        self.current_account = new_account
        print(f"Switching to account {self.current_account}")
        self.refresh_overview()

    def select_beneficiary(self, beneficiary_email):
        """
        Selects a beneficiary for transfer.

        Args:
            beneficiary_email (str): The email of the beneficiary to select.
        """
        self.selected_beneficiary = beneficiary_email
        print(f"Beneficiary selected {self.selected_beneficiary}")

    def deposit(self):
        """
        Adds an amount to the current account balance.
        """
        amount = float(self.amount_entry.get())
        self.accounts[self.current_account] += amount
        self.transactions.append({
            "type": "Deposit",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": self.description_entry.get(),
            "category": self.category_entry.get(),
            "from_account": self.current_account,
            "to_account": self.current_account,
            "user_email": self.current_user_email  # Use the current user's email
        })
        self.refresh_overview()
        self.display_history()  # Update history after a deposit
        self.check_and_notify_alerts()  # Check alerts after a deposit

    def withdraw(self):
        """
        Subtracts an amount from the current account balance.
        """
        amount = float(self.amount_entry.get())
        self.accounts[self.current_account] -= amount
        self.transactions.append({
            "type": "Withdrawal",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": self.description_entry.get(),
            "category": self.category_entry.get(),
            "from_account": self.current_account,
            "to_account": self.current_account,
            "user_email": self.current_user_email  # Use the current user's email
        })
        self.refresh_overview()
        self.display_history()  # Update history after a withdrawal
        self.check_and_notify_alerts()  # Check alerts after a withdrawal

    def transfer(self):
        """
        Transfers an amount between accounts or to a beneficiary.
        """
        amount = float(self.amount_entry.get())
        target_account = self.account_entry.get()
        if target_account != self.current_account:
            self.accounts[self.current_account] -= amount
            self.accounts[target_account] += amount
            self.transactions.append({
                "type": "Transfer",
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "description": self.description_entry.get(),
                "category": self.category_entry.get(),
                "from_account": self.current_account,
                "to_account": target_account,
                "user_email": self.current_user_email  # Use the current user's email
            })
        elif self.beneficiary_entry.get():
            self.accounts[self.current_account] -= amount
            self.transactions.append({
                "type": "Transfer",
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "description": self.description_entry.get(),
                "category": self.category_entry.get(),
                "from_account": self.current_account,
                "to_beneficiary": self.beneficiary_entry.get(),
                "user_email": self.current_user_email  # Use the current user's email
            })
        self.refresh_overview()
        self.display_history()  # Update history after a transfer
        self.check_and_notify_alerts()  # Check alerts after a transfer

    def multi_transfer(self):
        """
        Performs multiple transfers between the user's accounts.
        """
        total_amount = 0
        transfers = []

        for account, entry in self.multi_transfer_entries.items():
            amount = float(entry.get())
            if amount > 0:
                transfers.append((account, amount))
                total_amount += amount

        if total_amount > self.accounts[self.current_account]:
            print("Insufficient balance to perform all transfers.")
            return

        for account, amount in transfers:
            self.accounts[self.current_account] -= amount
            self.accounts[account] += amount
            self.transactions.append({
                "type": "Transfer",
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "description": "Multiple Transfer",
                "category": "Internal Transfer",
                "from_account": self.current_account,
                "to_account": account,
                "user_email": self.current_user_email
            })

        self.refresh_overview()
        self.display_history()  # Update history after multiple transfers
        self.check_and_notify_alerts()  # Check alerts after multiple transfers

    def add_beneficiary(self):
        """
        Adds a new beneficiary using their email address.
        """
        email = self.beneficiary_email_entry.get()
        if email not in self.beneficiaries:
            self.beneficiaries[email] = {"name": "Unknown", "email": email}
            self.beneficiary_listbox.insert(ctk.END, f"Beneficiary added {email}\n")
            print(f"Beneficiary added {email}")

    def search_transactions(self):
        """
        Searches for transactions based on specified criteria.
        """
        date = self.date_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        min_amount = self.min_amount_entry.get()
        max_amount = self.max_amount_entry.get()
        category = self.category_search_entry.get()
        transaction_type = self.type_entry.get()
        sort_order = self.sort_entry.get()

        filtered_transactions = self.transactions

        if date:
            filtered_transactions = [t for t in filtered_transactions if t["date"] == date]
        if start_date:
            filtered_transactions = [t for t in filtered_transactions if t["date"] >= start_date]
        if end_date:
            filtered_transactions = [t for t in filtered_transactions if t["date"] <= end_date]
        if min_amount:
            filtered_transactions = [t for t in filtered_transactions if float(t["amount"]) >= float(min_amount)]
        if max_amount:
            filtered_transactions = [t for t in filtered_transactions if float(t["amount"]) <= float(max_amount)]
        if category:
            filtered_transactions = [t for t in filtered_transactions if t["category"] == category]
        if transaction_type:
            filtered_transactions = [t for t in filtered_transactions if t["type"] == transaction_type]
        if sort_order:
            filtered_transactions = sorted(filtered_transactions, key=lambda x: x["date"], reverse=(sort_order == "DESC"))

        self.display_transactions(filtered_transactions)

    def display_transactions(self, transactions):
        """
        Displays the list of transactions in the transactions listbox.

        Args:
            transactions (list): List of transactions to display.
        """
        self.transactions_listbox.delete("1.0", ctk.END)
        for transaction in transactions:
            account_info = f"From: {transaction.get('from_account', 'N/A')} To: {transaction.get('to_account', 'N/A') if 'to_account' in transaction else transaction.get('to_beneficiary', 'N/A')}"
            self.transactions_listbox.insert(ctk.END, f"{transaction['date']} - {transaction['description']} - {transaction['amount']} € - {account_info} - {transaction['category']} - {transaction['type']} - {transaction.get('user_email', '')}\n")

    def display_history(self):
        """
        Displays the complete transaction history in the text area.
        """
        self.history_listbox.delete("1.0", ctk.END)  # Clear current content
        for transaction in self.transactions:
            account_info = f"From: {transaction.get('from_account', 'N/A')} To: {transaction.get('to_account', 'N/A') if 'to_account' in transaction else transaction.get('to_beneficiary', 'N/A')}"
            self.history_listbox.insert(ctk.END, f"{transaction['date']} - {transaction['description']} - {transaction['amount']} € - {account_info} - {transaction['category']} - {transaction['type']} - {transaction.get('user_email', '')}\n")

    def refresh_overview(self):
        """
        Refreshes the display of the current account balance.
        """
        self.balance_label.configure(text=f"{translate(self.language, 'balance_label')} {self.accounts[self.current_account]:.2f} €")

    def export_to_csv(self):
        """
        Exports transactions to a CSV file.
        """
        df = pd.DataFrame(self.transactions, columns=['type', 'amount', 'date', 'description', 'category', 'from_account', 'to_account', 'to_beneficiary', 'user_email'])
        df.to_csv('transactions.csv', index=False)
        print("Data exported to transactions.csv")

    def check_and_notify_alerts(self):
        """
        Checks accounts for overdrafts and displays an alert if necessary.
        """
        for account, balance in self.accounts.items():
            if balance < 0:
                self.show_alert_popup(account, balance)

    def show_alert_popup(self, account, balance):
        """
        Displays an alert popup to inform the user that an account is overdrawn.

        Args:
            account (str): The name of the overdrawn account.
            balance (float): The negative balance of the account.
        """
        alert_popup = ctk.CTkToplevel(self)
        alert_popup.title("Alert")
        alert_popup.geometry("300x150")

        alert_popup.grab_set()

        message_label = ctk.CTkLabel(alert_popup, text=f"Alert: {account} is overdrawn!", font=("Helvetica", 14, "bold"))
        message_label.pack(pady=10)

        balance_label = ctk.CTkLabel(alert_popup, text=f"Balance: {balance:.2f} €", font=("Helvetica", 12))
        balance_label.pack(pady=5)

        ok_button = ctk.CTkButton(alert_popup, text="OK", command=alert_popup.destroy)
        ok_button.pack(pady=10)

    def show_logout_popup(self):
        """
        Displays a logout confirmation popup.
        """
        popup = ctk.CTkToplevel(self)
        popup.title("Confirmation")
        popup.geometry("300x200")

        popup.grab_set()

        message_label = ctk.CTkLabel(popup, text="Leaving already?", font=("Helvetica", 16, "bold"))
        message_label.pack(pady=10)

        sub_message_label = ctk.CTkLabel(popup, text="Have a great day and see you soon", font=("Helvetica", 12))
        sub_message_label.pack(pady=5)

        logout_button = ctk.CTkButton(popup, text="Logout", command=self.confirm_logout)
        logout_button.pack(pady=10)

        stay_button = ctk.CTkButton(popup, text="Stay on the app", command=popup.destroy)
        stay_button.pack(pady=5)

    def confirm_logout(self):
        """
        Confirms logout and closes the application.
        """
        on_close()
        self.destroy()

    def logout(self):
        """
        Displays the logout confirmation popup.
        """
        self.show_logout_popup()

    def generate_unique_account_number(self):
        """
        Generates a unique account number.

        Returns:
            str: Unique account number.
        """
        while True:
            account_number = ''.join(secrets.choice(string.digits) for _ in range(10))
            if account_number not in self.user_accounts:
                return account_number

    def create_new_account(self, user_data):
        """
        Creates a new account for the user with a random account number.

        Args:
            user_data (dict): User data for the new account.
        """
        new_account_number = self.generate_unique_account_number()
        self.user_accounts[new_account_number] = user_data
        print(f"New account created with number {new_account_number}")

if __name__ == "__main__":
    app = FinanceManagerApp()
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()