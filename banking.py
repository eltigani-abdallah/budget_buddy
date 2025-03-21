import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from tkcalendar import Calendar, DateEntry
import secrets
import string

class FinanceManagerApp(ctk.CTk):
    """
    Financial management application using CustomTkinter for the user interface.

    Attributes:
        language (str): Current language of the user interface.
        translations (dict): Dictionary containing translations for each supported language.
        accounts (dict): Dictionary containing account balances.
        user_accounts (dict): Dictionary to store user accounts.
        current_account (str): Currently selected account.
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
        self.translations = {
            "french": {
                "title": "Finance Manager",
                "balance_label": "Total Balance:",
                "alert_label": "Warning: You are overdrawn!",
                "deposit_button": "Deposit",
                "withdraw_button": "Withdraw",
                "transfer_button": "Transfer",
                "search_button": "Search",
                "export_button": "Export to CSV",
                "check_alerts_button": "Check Alerts",
                "date_label": "Date (YYYY-MM-DD):",
                "category_label": "Category:",
                "type_label": "Type:",
                "start_date_label": "Start Date (YYYY-MM-DD):",
                "end_date_label": "End Date (YYYY-MM-DD):",
                "min_amount_label": "Min Amount:",
                "max_amount_label": "Max Amount:",
                "sort_label": "Sort by Amount:",
                "reference_placeholder": "Reference",
                "description_placeholder": "Description",
                "amount_placeholder": "Amount",
                "category_placeholder": "Category",
                "logout_button": "Logout",
                "account_label": "Bank Account:"
            },
            "english": {
                "title": "Finance Manager",
                "balance_label": "Total Balance:",
                "alert_label": "Warning: You are overdrawn!",
                "deposit_button": "Deposit",
                "withdraw_button": "Withdraw",
                "transfer_button": "Transfer",
                "search_button": "Search",
                "export_button": "Export to CSV",
                "check_alerts_button": "Check Alerts",
                "date_label": "Date (YYYY-MM-DD):",
                "category_label": "Category:",
                "type_label": "Type:",
                "start_date_label": "Start Date (YYYY-MM-DD):",
                "end_date_label": "End Date (YYYY-MM-DD):",
                "min_amount_label": "Min Amount:",
                "max_amount_label": "Max Amount:",
                "sort_label": "Sort by Amount:",
                "reference_placeholder": "Reference",
                "description_placeholder": "Description",
                "amount_placeholder": "Amount",
                "category_placeholder": "Category",
                "logout_button": "Logout",
                "account_label": "Bank Account:"
            },
            "russian": {
                "title": "Financial Manager",
                "balance_label": "Total Balance:",
                "alert_label": "Warning: You are overdrawn!",
                "deposit_button": "Deposit",
                "withdraw_button": "Withdraw",
                "transfer_button": "Transfer",
                "search_button": "Search",
                "export_button": "Export to CSV",
                "check_alerts_button": "Check Alerts",
                "date_label": "Date (YYYY-MM-DD):",
                "category_label": "Category:",
                "type_label": "Type:",
                "start_date_label": "Start Date (YYYY-MM-DD):",
                "end_date_label": "End Date (YYYY-MM-DD):",
                "min_amount_label": "Min Amount:",
                "max_amount_label": "Max Amount:",
                "sort_label": "Sort by Amount:",
                "reference_placeholder": "Reference",
                "description_placeholder": "Description",
                "amount_placeholder": "Amount",
                "category_placeholder": "Category",
                "logout_button": "Logout",
                "account_label": "Bank Account:"
            },
            "korean": {
                "title": "Finance Manager",
                "balance_label": "Total Balance:",
                "alert_label": "Warning: You are overdrawn!",
                "deposit_button": "Deposit",
                "withdraw_button": "Withdraw",
                "transfer_button": "Transfer",
                "search_button": "Search",
                "export_button": "Export to CSV",
                "check_alerts_button": "Check Alerts",
                "date_label": "Date (YYYY-MM-DD):",
                "category_label": "Category:",
                "type_label": "Type:",
                "start_date_label": "Start Date (YYYY-MM-DD):",
                "end_date_label": "End Date (YYYY-MM-DD):",
                "min_amount_label": "Min Amount:",
                "max_amount_label": "Max Amount:",
                "sort_label": "Sort by Amount:",
                "reference_placeholder": "Reference",
                "description_placeholder": "Description",
                "amount_placeholder": "Amount",
                "category_placeholder": "Category",
                "logout_button": "Logout",
                "account_label": "Bank Account:"
            }
        }

        self.title("Finance Manager")
        self.geometry("1000x700")

        self.accounts = {
            "Main Account": 450,
            "Savings Account": 1600,
            "Business Account": 7500,
        }
        self.user_accounts = {}
        self.current_account = "Main Account"
        self.create_widgets()
        self.refresh_overview()

    def create_widgets(self):
        """
        Creates and configures the user interface widgets.
        """
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill='x', pady=5)

        self.logout_button = ctk.CTkButton(top_frame, text=self.translations[self.language]["logout_button"], command=self.logout)
        self.logout_button.pack(side='left', padx=10)

        self.language_menu = ctk.CTkOptionMenu(top_frame, values=["french", "english", "russian", "korean"], command=self.change_language)
        self.language_menu.pack(side='right', padx=10)
        self.language_menu.set(self.language)

        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(pady=20, fill='both', expand=True)

        self.transactions_tab = self.notebook.add("Transactions")
        self.overview_tab = self.notebook.add("Overview")
        self.export_tab = self.notebook.add("Export")
        self.notifications_tab = self.notebook.add("Notifications")

        custom_font = ctk.CTkFont(family="KalniaGlaze-VariableFont_wdth,wght", size=24)

        self.balance_label = ctk.CTkLabel(self.transactions_tab, text="", font=("Helvetica", 18))
        self.balance_label.pack(pady=10)

        self.reference_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=self.translations[self.language]["reference_placeholder"])
        self.reference_entry.pack(pady=5)

        self.description_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=self.translations[self.language]["description_placeholder"])
        self.description_entry.pack(pady=5)

        self.amount_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=self.translations[self.language]["amount_placeholder"])
        self.amount_entry.pack(pady=5)

        self.category_entry = ctk.CTkComboBox(self.transactions_tab, values=["Bills", "Leisure", "Dining", "Travels", "Other Categories"], text_color="white")
        self.category_entry.pack(pady=5)

        self.action_frame = ctk.CTkFrame(self.transactions_tab)
        self.action_frame.pack(pady=5)

        self.deposit_button = ctk.CTkButton(self.action_frame, text=self.translations[self.language]["deposit_button"], command=self.deposit)
        self.deposit_button.grid(row=0, column=0, padx=5)

        self.withdraw_button = ctk.CTkButton(self.action_frame, text=self.translations[self.language]["withdraw_button"], command=self.withdraw)
        self.withdraw_button.grid(row=0, column=1, padx=5)

        self.transfer_button = ctk.CTkButton(self.action_frame, text=self.translations[self.language]["transfer_button"], command=self.transfer)
        self.transfer_button.grid(row=0, column=2, padx=5)

        self.account_label = ctk.CTkLabel(self.action_frame, text=self.translations[self.language]["account_label"])
        self.account_label.grid(row=0, column=3, padx=5)
        self.account_menu = ctk.CTkOptionMenu(self.action_frame, values=list(self.accounts.keys()), command=self.switch_account)
        self.account_menu.grid(row=0, column=4, padx=5)
        self.account_menu.set(self.current_account)

        self.search_frame = ctk.CTkFrame(self.transactions_tab)
        self.search_frame.pack(pady=10)

        self.date_label = ctk.CTkLabel(self.search_frame, text=self.translations[self.language]["date_label"])
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(self.search_frame, width=12, background='lightblue', foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        self.start_date_label = ctk.CTkLabel(self.search_frame, text=self.translations[self.language]["start_date_label"])
        self.start_date_label.grid(row=1, column=0, padx=5, pady=5)
        self.start_date_entry = DateEntry(self.search_frame, width=12, background='lightblue', foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.end_date_label = ctk.CTkLabel(self.search_frame, text=self.translations[self.language]["end_date_label"])
        self.end_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.end_date_entry = DateEntry(self.search_frame, width=12, background='lightblue', foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.min_amount_label = ctk.CTkLabel(self.search_frame, text=self.translations[self.language]["min_amount_label"])
        self.min_amount_label.grid(row=0, column=2, padx=5, pady=5)
        self.min_amount_entry = ctk.CTkEntry(self.search_frame)
        self.min_amount_entry.grid(row=0, column=3, padx=5, pady=5)

        self.max_amount_label = ctk.CTkLabel(self.search_frame, text=self.translations[self.language]["max_amount_label"])
        self.max_amount_label.grid(row=1, column=2, padx=5, pady=5)
        self.max_amount_entry = ctk.CTkEntry(self.search_frame)
        self.max_amount_entry.grid(row=1, column=3, padx=5, pady=5)

        self.category_label = ctk.CTkLabel(self.search_frame, text=self.translations[self.language]["category_label"])
        self.category_label.grid(row=2, column=2, padx=5, pady=5)
        self.category_search_entry = ctk.CTkComboBox(self.search_frame, values=["Bills", "Leisure", "Dining", "Travels", "Other Categories"], text_color="white")
        self.category_search_entry.grid(row=2, column=3, padx=5, pady=5)

        self.type_label = ctk.CTkLabel(self.search_frame, text=self.translations[self.language]["type_label"])
        self.type_label.grid(row=3, column=0, padx=5, pady=5)
        self.type_entry = ctk.CTkComboBox(self.search_frame, values=["Withdrawal", "Transfer", "Deposit"], text_color="white")
        self.type_entry.grid(row=3, column=1, padx=5, pady=5)

        self.sort_label = ctk.CTkLabel(self.search_frame, text=self.translations[self.language]["sort_label"])
        self.sort_label.grid(row=3, column=2, padx=5, pady=5)
        self.sort_entry = ctk.CTkComboBox(self.search_frame, values=["", "ASC", "DESC"], text_color="white")
        self.sort_entry.grid(row=3, column=3, padx=5, pady=5)

        self.search_button = ctk.CTkButton(self.transactions_tab, text=self.translations[self.language]["search_button"], command=self.search_transactions)
        self.search_button.pack(pady=5)

        self.transactions_listbox = ctk.CTkTextbox(self.transactions_tab, width=760, height=200)
        self.transactions_listbox.pack(pady=10)

        self.alert_label = ctk.CTkLabel(self.overview_tab, text="", text_color="red")
        self.alert_label.pack(pady=10)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, self.overview_tab)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.export_button = ctk.CTkButton(self.export_tab, text=self.translations[self.language]["export_button"], command=self.export_to_csv)
        self.export_button.pack(pady=20)

        self.check_alerts_button = ctk.CTkButton(self.notifications_tab, text=self.translations[self.language]["check_alerts_button"], command=self.check_and_notify_alerts)
        self.check_alerts_button.pack(pady=20)

        self.theme_menu = ctk.CTkOptionMenu(self, values=["dark", "light"], command=self.change_theme)
        self.theme_menu.pack(pady=10)
        self.theme_menu.set("dark")

    def change_theme(self, theme):
        """
        Changes the theme of the application.

        Args:
            theme (str): The theme to apply ("dark" or "light").
        """
        ctk.set_appearance_mode(theme)

    def change_language(self, new_language):
        """
        Changes the language of the user interface.

        Args:
            new_language (str): The new language to apply.
        """
        self.language = new_language
        self.update_translations()

    def update_translations(self):
        """
        Updates the translations of the user interface based on the current language.
        """
        translations = self.translations[self.language]
        self.title(translations["title"])
        self.balance_label.configure(text=translations["balance_label"])
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

    def switch_account(self, new_account):
        """
        Switches the currently selected account.

        Args:
            new_account (str): The new account to select.
        """
        self.current_account = new_account
        print(f"Switched to account: {self.current_account}")
        self.refresh_overview()

    def deposit(self):
        """
        Adds an amount to the current account balance.
        """
        amount = float(self.amount_entry.get())
        self.accounts[self.current_account] += amount
        self.refresh_overview()

    def withdraw(self):
        """
        Subtracts an amount from the current account balance.
        """
        amount = float(self.amount_entry.get())
        self.accounts[self.current_account] -= amount
        self.refresh_overview()

    def transfer(self):
        """
        Transfers an amount between accounts (to be implemented).
        """
        pass

    def search_transactions(self):
        """
        Searches for transactions based on specified criteria (to be implemented).
        """
        pass

    def refresh_transactions(self, filter_criteria=None):
        """
        Refreshes the list of transactions (to be implemented).

        Args:
            filter_criteria (dict, optional): Filtering criteria for transactions.
        """
        pass

    def refresh_overview(self):
        """
        Refreshes the display of the current account balance.
        """
        self.balance_label.configure(text=f"{self.translations[self.language]['balance_label']} {self.accounts[self.current_account]:.2f} €")

    def export_to_csv(self):
        """
        Exports transactions to a CSV file.
        """
        transactions = []
        df = pd.DataFrame(transactions, columns=['ID', 'Reference', 'Description', 'Amount', 'Date', 'Type', 'Category', 'Sender', 'Receiver'])
        df.to_csv('transactions.csv', index=False)
        print("Data exported to transactions.csv")

    def check_and_notify_alerts(self):
        """
        Checks and notifies alerts (to be implemented).
        """
        pass

    def show_logout_popup(self):
        """
        Displays a logout confirmation popup.
        """
        popup = ctk.CTkToplevel(self)
        popup.title("Confirmation")
        popup.geometry("300x200")

        popup.grab_set()

        message_label = ctk.CTkLabel(popup, text="Are you leaving?", font=("Helvetica", 16, "bold"))
        message_label.pack(pady=10)

        sub_message_label = ctk.CTkLabel(popup, text="Have a nice day and see you soon", font=("Helvetica", 12))
        sub_message_label.pack(pady=5)

        logout_button = ctk.CTkButton(popup, text="Logout", command=self.confirm_logout)
        logout_button.pack(pady=10)

        stay_button = ctk.CTkButton(popup, text="Stay on the application", command=popup.destroy)
        stay_button.pack(pady=5)

    def confirm_logout(self):
        """
        Confirms logout and closes the application.
        """
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
        print(f"New account created with number: {new_account_number}")

if __name__ == "__main__":
    app = FinanceManagerApp()
    app.mainloop()
