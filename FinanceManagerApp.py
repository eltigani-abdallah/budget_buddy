import secrets
import string
import customtkinter as ctk
import pandas as pd
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import dboperations
import User
import lang
import sessionManager




class FinanceManagerApp(ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master)
        self.master=master
        
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.language = "french"
        
        #sessionManager.verify_session()

        self.accounts = {
            "Main Account": 450,
            "Savings Account": 1600,
            "Business Account": 7500,
        }
        self.user_accounts = {}
        self.current_account = "Main Account"
        self.current_user = None
        self.create_widgets()
        self.refresh_overview()
        self.pack(expand=True, fill="both")
    def create_widgets(self):
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill='x', pady=5)

        self.login_button = ctk.CTkButton(top_frame, text=lang.translate(self.language, "login_button"), command=self.show_login_popup)
        self.login_button.pack(side='left', padx=10)

        self.register_button = ctk.CTkButton(top_frame, text=lang.translate(self.language, "register_button"), command=self.show_register_popup)
        self.register_button.pack(side='left', padx=10)

        self.logout_button = ctk.CTkButton(top_frame, text=lang.translate(self.language, "logout_button"), command=self.logout, state='disabled')
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

        self.balance_label = ctk.CTkLabel(self.transactions_tab, text="", font=("Helvetica", 18))
        self.balance_label.pack(pady=10)

        self.reference_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=lang.translate(self.language, "reference_placeholder"))
        self.reference_entry.pack(pady=5)

        self.description_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=lang.translate(self.language, "description_placeholder"))
        self.description_entry.pack(pady=5)

        self.amount_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=lang.translate(self.language, "amount_placeholder"))
        self.amount_entry.pack(pady=5)

        self.category_entry = ctk.CTkComboBox(self.transactions_tab, values=["Bills", "Leisure", "Dining", "Travels", "Other Categories"], text_color="white")
        self.category_entry.pack(pady=5)

        self.action_frame = ctk.CTkFrame(self.transactions_tab)
        self.action_frame.pack(pady=5)

        self.deposit_button = ctk.CTkButton(self.action_frame, text=lang.translate(self.language, "deposit_button"), command=self.deposit)
        self.deposit_button.grid(row=0, column=0, padx=5)

        self.withdraw_button = ctk.CTkButton(self.action_frame, text=lang.translate(self.language, "withdraw_button"), command=self.withdraw)
        self.withdraw_button.grid(row=0, column=1, padx=5)

        self.transfer_button = ctk.CTkButton(self.action_frame, text=lang.translate(self.language, "transfer_button"), command=self.transfer)
        self.transfer_button.grid(row=0, column=2, padx=5)

        self.account_label = ctk.CTkLabel(self.action_frame, text=lang.translate(self.language, "account_label"))
        self.account_label.grid(row=0, column=3, padx=5)
        self.account_menu = ctk.CTkOptionMenu(self.action_frame, values=list(self.accounts.keys()), command=self.switch_account)
        self.account_menu.grid(row=0, column=4, padx=5)
        self.account_menu.set(self.current_account)

        self.search_frame = ctk.CTkFrame(self.transactions_tab)
        self.search_frame.pack(pady=10)

        self.date_label = ctk.CTkLabel(self.search_frame, text=lang.translate(self.language, "date_label"))
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(self.search_frame, width=12, background='lightblue', foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.delete(0, 'end')  # Clear initial date

        self.clear_date_button = ctk.CTkButton(self.search_frame, text="Clear", command=lambda: self.date_entry.delete(0, 'end'))
        self.clear_date_button.grid(row=0, column=2, padx=5, pady=5)

        self.start_date_label = ctk.CTkLabel(self.search_frame, text=lang.translate(self.language, "start_date_label"))
        self.start_date_label.grid(row=1, column=0, padx=5, pady=5)
        self.start_date_entry = DateEntry(self.search_frame, width=12, background='lightblue', foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.start_date_entry.delete(0, 'end')  # Clear initial date

        self.clear_start_date_button = ctk.CTkButton(self.search_frame, text="Clear", command=lambda: self.start_date_entry.delete(0, 'end'))
        self.clear_start_date_button.grid(row=1, column=2, padx=5, pady=5)

        self.end_date_label = ctk.CTkLabel(self.search_frame, text=lang.translate(self.language, "end_date_label"))
        self.end_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.end_date_entry = DateEntry(self.search_frame, width=12, background='lightblue', foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.end_date_entry.delete(0, 'end')  # Clear initial date

        self.clear_end_date_button = ctk.CTkButton(self.search_frame, text="Clear", command=lambda: self.end_date_entry.delete(0, 'end'))
        self.clear_end_date_button.grid(row=2, column=2, padx=5, pady=5)

        self.min_amount_label = ctk.CTkLabel(self.search_frame, text=lang.translate(self.language, "min_amount_label"))
        self.min_amount_label.grid(row=0, column=3, padx=5, pady=5)
        self.min_amount_entry = ctk.CTkEntry(self.search_frame)
        self.min_amount_entry.grid(row=0, column=4, padx=5, pady=5)

        self.max_amount_label = ctk.CTkLabel(self.search_frame, text=lang.translate(self.language, "max_amount_label"))
        self.max_amount_label.grid(row=1, column=3, padx=5, pady=5)
        self.max_amount_entry = ctk.CTkEntry(self.search_frame)
        self.max_amount_entry.grid(row=1, column=4, padx=5, pady=5)

        self.category_label = ctk.CTkLabel(self.search_frame, text=lang.translate(self.language, "category_label"))
        self.category_label.grid(row=2, column=3, padx=5, pady=5)
        self.category_search_entry = ctk.CTkComboBox(self.search_frame, values=["","Bills", "Leisure", "Dining", "Travels", "Other Categories"], text_color="white")
        self.category_search_entry.grid(row=2, column=4, padx=5, pady=5)

        self.type_label = ctk.CTkLabel(self.search_frame, text=lang.translate(self.language, "type_label"))
        self.type_label.grid(row=3, column=0, padx=5, pady=5)
        self.type_entry = ctk.CTkComboBox(self.search_frame, values=["","Withdrawal", "Transfer", "Deposit"], text_color="white")
        self.type_entry.grid(row=3, column=1, padx=5, pady=5)

        self.sort_label = ctk.CTkLabel(self.search_frame, text=lang.translate(self.language, "sort_label"))
        self.sort_label.grid(row=3, column=3, padx=5, pady=5)
        self.sort_entry = ctk.CTkComboBox(self.search_frame, values=["", "ASC", "DESC"], text_color="white")
        self.sort_entry.grid(row=3, column=4, padx=5, pady=5)

        self.search_button = ctk.CTkButton(self.transactions_tab, text=lang.translate(self.language, "search_button"), command=self.search_transactions)
        self.search_button.pack(pady=5)

        # Initialize Treeview
        self.tree = ttk.Treeview(self.transactions_tab, columns=("Date", "Amount", "Category", "Type"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Type", text="Type")
        self.tree.pack(pady=10)

        self.alert_label = ctk.CTkLabel(self.overview_tab, text="", text_color="red")
        self.alert_label.pack(pady=10)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, self.overview_tab)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.export_button = ctk.CTkButton(self.export_tab, text=lang.translate(self.language, "export_button"), command=self.export_to_csv)
        self.export_button.pack(pady=20)

        self.check_alerts_button = ctk.CTkButton(self.notifications_tab, text=lang.translate(self.language, "check_alerts_button"), command=self.check_and_notify_alerts)
        self.check_alerts_button.pack(pady=20)

        self.theme_menu = ctk.CTkOptionMenu(self, values=["dark", "light"], command=self.change_theme)
        self.theme_menu.pack(pady=10)
        self.theme_menu.set("dark")

    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)

    def change_language(self, new_language):
        self.language = new_language
        self.update_translations()

    def update_translations(self):
        translations = lang.lang_dict[self.language]
        self.title(translations["title"])
        self.balance_label.configure(text=translations["balance_label"])
        self.alert_label.configure(text=translations.get("alert_label", ""))
        self.deposit_button.configure(text=translations["deposit_button"])
        self.withdraw_button.configure(text=translations["withdraw_button"])
        self.transfer_button.configure(text=translations["transfer_button"])
        self.search_button.configure(text=translations["search_button"])
        self.export_button.configure(text=translations["export_button"])
        self.check_alerts_button.configure(text=translations["check_alerts_button"])
        self.login_button.configure(text=translations["login_button"])
        self.register_button.configure(text=translations["register_button"])
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
        self.current_account = new_account
        print(f"Switched to account: {self.current_account}")
        self.refresh_overview()

    def deposit(self):
        amount = float(self.amount_entry.get())
        self.accounts[self.current_account] += amount
        self.refresh_overview()

    def withdraw(self):
        amount = float(self.amount_entry.get())
        self.accounts[self.current_account] -= amount
        self.refresh_overview()

    def transfer(self):
        pass

    def search_transactions(self):
        if not self.current_user:
            messagebox.showerror("Error", "Please log in to view transactions.")
            return

        date_from = self.start_date_entry.get() or None
        date_to = self.end_date_entry.get() or None
        category = self.category_search_entry.get() or None
        trans_type = self.type_entry.get() or None
        order_by = self.sort_entry.get() or None

        # Handle single date selection
        single_date = self.date_entry.get()
        if single_date:
            date_from = single_date
            date_to = single_date
            # Display a message or update a label to indicate a single day filter
            self.alert_label.configure(text=lang.translate(self.language, "single_day_filter").format(date=single_date))
        else:
            # Clear the message if not filtering by a single day
            self.alert_label.configure(text="")

        transactions = dboperations.search_transactions_db(dboperations.connection, self.current_user.user_id, date_from, date_to, category, trans_type, order_by)

        # Clear previous entries in Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new transactions into Treeview
        for t in transactions:
            self.tree.insert("", "end", values=(t['date'], t['amount'], t['category'], t['type']))

    def refresh_overview(self):
        pass

    def export_to_csv(self):
        transactions = []
        df = pd.DataFrame(transactions, columns=['ID', 'Reference', 'Description', 'Amount', 'Date', 'Type', 'Category', 'Sender', 'Receiver'])
        df.to_csv('transactions.csv', index=False)
        print("Data exported to transactions.csv")

    def check_and_notify_alerts(self):
        pass

    def show_login_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Login")
        popup.geometry("300x500")

        popup.grab_set()

        email_label = ctk.CTkLabel(popup, text="Email")
        email_label.pack(pady=5)
        email_entry = ctk.CTkEntry(popup)
        email_entry.pack(pady=5)

        password_label = ctk.CTkLabel(popup, text="Password")
        password_label.pack(pady=5)
        password_entry = ctk.CTkEntry(popup, show="*")
        password_entry.pack(pady=5)

        show_password_var = ctk.BooleanVar()
        show_password_checkbox = ctk.CTkCheckBox(popup, text="Show Password", variable=show_password_var, command=lambda: self.toggle_password_visibility(password_entry, show_password_var))
        show_password_checkbox.pack(pady=5)

        login_button = ctk.CTkButton(popup, text="Login", command=lambda: self.login(email_entry.get(), password_entry.get(), popup))
        login_button.pack(pady=10)

    def toggle_password_visibility(self, password_entry, show_password_var):
        if show_password_var.get():
            password_entry.configure(show="")
        else:
            password_entry.configure(show="*")

    def login(self, email, mot_de_passe, popup):
        user = User.login(dboperations.connection, email, mot_de_passe)
        if user:
            self.current_user = user
            self.login_button.configure(state='disabled')
            self.register_button.configure(state='disabled')
            self.logout_button.configure(state='normal')
            popup.destroy()
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def show_register_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Register")
        popup.geometry("300x500")

        popup.grab_set()

        nom_label = ctk.CTkLabel(popup, text="Nom")
        nom_label.pack(pady=5)
        nom_entry = ctk.CTkEntry(popup)
        nom_entry.pack(pady=5)

        prenom_label = ctk.CTkLabel(popup, text="Prénom")
        prenom_label.pack(pady=5)
        prenom_entry = ctk.CTkEntry(popup)
        prenom_entry.pack(pady=5)

        email_label = ctk.CTkLabel(popup, text="Email")
        email_label.pack(pady=5)
        email_entry = ctk.CTkEntry(popup)
        email_entry.pack(pady=5)

        password_label = ctk.CTkLabel(popup, text="Mot de passe")
        password_label.pack(pady=5)
        password_entry = ctk.CTkEntry(popup, show="*")
        password_entry.pack(pady=5)

        confirm_password_label = ctk.CTkLabel(popup, text="Confirmer le mot de passe")
        confirm_password_label.pack(pady=5)
        confirm_password_entry = ctk.CTkEntry(popup, show="*")
        confirm_password_entry.pack(pady=5)

        show_password_var = ctk.BooleanVar()
        show_password_checkbox = ctk.CTkCheckBox(popup, text="Show Password", variable=show_password_var, command=lambda: self.toggle_password_visibility_register(password_entry, confirm_password_entry, show_password_var))
        show_password_checkbox.pack(pady=5)

        register_button = ctk.CTkButton(popup, text="Register", command=lambda: self.register(nom_entry.get(), prenom_entry.get(), email_entry.get(), password_entry.get(), confirm_password_entry.get(), popup))
        register_button.pack(pady=10)

    def toggle_password_visibility_register(self, password_entry, confirm_password_entry, show_password_var):
        if show_password_var.get():
            password_entry.configure(show="")
            confirm_password_entry.configure(show="")
        else:
            password_entry.configure(show="*")
            confirm_password_entry.configure(show="*")

    def register(self, nom, prenom, email, mot_de_passe, confirm_mot_de_passe, popup):
        if mot_de_passe != confirm_mot_de_passe:
            messagebox.showerror("Error", "Passwords do not match")
            return

        user = User.register(dboperations.connection, nom, prenom, email, mot_de_passe)
        if user:
            self.current_user = user
            self.login_button.configure(state='disabled')
            self.register_button.configure(state='disabled')
            self.logout_button.configure(state='normal')
            popup.destroy()
        else:
            messagebox.showerror("Error", "Registration failed")

    def show_logout_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Confirmation")
        popup.geometry("300x500")

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
        self.current_user = None
        self.login_button.configure(state='normal')
        self.register_button.configure(state='normal')
        self.logout_button.configure(state='disabled')
        self.destroy()

    def logout(self):
        self.show_logout_popup()

    def generate_unique_account_number(self):
        while True:
            account_number = ''.join(secrets.choice(string.digits) for _ in range(10))
            if account_number not in self.user_accounts:
                return account_number

    def create_new_account(self, user_data):
        new_account_number = self.generate_unique_account_number()
        self.user_accounts[new_account_number] = user_data
        print(f"New account created with number: {new_account_number}")


# app=FinanceManagerApp()
# app.protocol("WM_DELETE_WINDOW", sessionManager.on_close)
# #app.mainloop()