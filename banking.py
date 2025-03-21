import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from tkcalendar import Calendar, DateEntry
import secrets
import string

class FinanceManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.language = "français"
        self.translations = {
            "français": {
                "title": "Gestionnaire de Finances",
                "balance_label": "Solde total :",
                "alert_label": "Attention : Vous êtes à découvert !",
                "deposit_button": "Dépôt",
                "withdraw_button": "Retrait",
                "transfer_button": "Transfert",
                "search_button": "Rechercher",
                "export_button": "Exporter vers CSV",
                "check_alerts_button": "Vérifier les Alertes",
                "date_label": "Date (YYYY-MM-DD):",
                "category_label": "Catégorie:",
                "type_label": "Type:",
                "start_date_label": "Date de début (YYYY-MM-DD):",
                "end_date_label": "Date de fin (YYYY-MM-DD):",
                "min_amount_label": "Montant min:",
                "max_amount_label": "Montant max:",
                "sort_label": "Trier par montant:",
                "reference_placeholder": "Référence",
                "description_placeholder": "Description",
                "amount_placeholder": "Montant",
                "category_placeholder": "Catégorie",
                "logout_button": "Déconnexion",
                "account_label": "Compte bancaire :"
            },
            "anglais": {
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
            "russe": {
                "title": "Финансовый Менеджер",
                "balance_label": "Общий баланс:",
                "alert_label": "Внимание: Вы в минусе!",
                "deposit_button": "Депозит",
                "withdraw_button": "Снятие",
                "transfer_button": "Перевод",
                "search_button": "Поиск",
                "export_button": "Экспорт в CSV",
                "check_alerts_button": "Проверить оповещения",
                "date_label": "Дата (ГГГГ-ММ-ДД):",
                "category_label": "Категория:",
                "type_label": "Тип:",
                "start_date_label": "Дата начала (ГГГГ-ММ-ДД):",
                "end_date_label": "Дата окончания (ГГГГ-ММ-ДД):",
                "min_amount_label": "Мин. сумма:",
                "max_amount_label": "Макс. сумма:",
                "sort_label": "Сортировать по сумме:",
                "reference_placeholder": "Ссылка",
                "description_placeholder": "Описание",
                "amount_placeholder": "Сумма",
                "category_placeholder": "Категория",
                "logout_button": "Выход",
                "account_label": "Банковский счет:"
            },
            "coréen": {
                "title": "재무 관리자",
                "balance_label": "총 잔액:",
                "alert_label": "경고: 당신은 마이너스입니다!",
                "deposit_button": "입금",
                "withdraw_button": "출금",
                "transfer_button": "이체",
                "search_button": "검색",
                "export_button": "CSV로 내보내기",
                "check_alerts_button": "알림 확인",
                "date_label": "날짜 (YYYY-MM-DD):",
                "category_label": "카테고리:",
                "type_label": "유형:",
                "start_date_label": "시작 날짜 (YYYY-MM-DD):",
                "end_date_label": "종료 날짜 (YYYY-MM-DD):",
                "min_amount_label": "최소 금액:",
                "max_amount_label": "최대 금액:",
                "sort_label": "금액별 정렬:",
                "reference_placeholder": "참조",
                "description_placeholder": "설명",
                "amount_placeholder": "금액",
                "category_placeholder": "카테고리",
                "logout_button": "로그아웃",
                "account_label": "은행 계좌:"
            }
        }

        self.title("Gestionnaire de Finances")
        self.geometry("1000x700")

        # Utiliser un dictionnaire pour stocker les soldes des comptes
        self.accounts = {
            "Compte Principal": 450,
            "Compte Épargne": 1600,
            "Compte Entreprise": 7500,
        }
        self.user_accounts = {}  # Dictionnaire pour stocker les comptes utilisateurs
        self.current_account = "Compte Principal"
        self.create_widgets()
        self.refresh_overview()

    def create_widgets(self):
        # Créez un conteneur pour les boutons de déconnexion et de langue
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill='x', pady=5)

        # Ajoutez le bouton de déconnexion à gauche dans le conteneur
        self.logout_button = ctk.CTkButton(top_frame, text=self.translations[self.language]["logout_button"], command=self.logout)
        self.logout_button.pack(side='left', padx=10)

        # Ajoutez le menu de langue à droite dans le conteneur
        self.language_menu = ctk.CTkOptionMenu(top_frame, values=["français", "anglais", "russe", "coréen"], command=self.change_language)
        self.language_menu.pack(side='right', padx=10)
        self.language_menu.set(self.language)

        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(pady=20, fill='both', expand=True)

        self.transactions_tab = self.notebook.add("Transactions")
        self.overview_tab = self.notebook.add("Vue d'ensemble")
        self.export_tab = self.notebook.add("Exportation")
        self.notifications_tab = self.notebook.add("Notifications")

        custom_font = ctk.CTkFont(family="KalniaGlaze-VariableFont_wdth,wght", size=24)

        # Ajoutez le reste de vos widgets ici...

        # Exemple : Ajout du label de solde
        self.balance_label = ctk.CTkLabel(self.transactions_tab, text="", font=("Helvetica", 18))
        self.balance_label.pack(pady=10)

        self.reference_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=self.translations[self.language]["reference_placeholder"])
        self.reference_entry.pack(pady=5)

        self.description_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=self.translations[self.language]["description_placeholder"])
        self.description_entry.pack(pady=5)

        self.amount_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=self.translations[self.language]["amount_placeholder"])
        self.amount_entry.pack(pady=5)

        # Use CTkComboBox for category selection
        self.category_entry = ctk.CTkComboBox(self.transactions_tab, values=["Bills", "Leisure", "Dining", "Travels", "Other Categories"], text_color="white")
        self.category_entry.pack(pady=5)

        # Container for deposit, withdraw, transfer buttons and account switcher
        self.action_frame = ctk.CTkFrame(self.transactions_tab)
        self.action_frame.pack(pady=5)

        self.deposit_button = ctk.CTkButton(self.action_frame, text=self.translations[self.language]["deposit_button"], command=self.deposit)
        self.deposit_button.grid(row=0, column=0, padx=5)

        self.withdraw_button = ctk.CTkButton(self.action_frame, text=self.translations[self.language]["withdraw_button"], command=self.withdraw)
        self.withdraw_button.grid(row=0, column=1, padx=5)

        self.transfer_button = ctk.CTkButton(self.action_frame, text=self.translations[self.language]["transfer_button"], command=self.transfer)
        self.transfer_button.grid(row=0, column=2, padx=5)

        # Add the account switcher next to the transfer button
        self.account_label = ctk.CTkLabel(self.action_frame, text=self.translations[self.language]["account_label"])
        self.account_label.grid(row=0, column=3, padx=5)
        self.account_menu = ctk.CTkOptionMenu(self.action_frame, values=list(self.accounts.keys()), command=self.switch_account)
        self.account_menu.grid(row=0, column=4, padx=5)
        self.account_menu.set(self.current_account)

        self.search_frame = ctk.CTkFrame(self.transactions_tab)
        self.search_frame.pack(pady=10)

        # Dates column with Calendar
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

        # Amounts column
        self.min_amount_label = ctk.CTkLabel(self.search_frame, text=self.translations[self.language]["min_amount_label"])
        self.min_amount_label.grid(row=0, column=2, padx=5, pady=5)
        self.min_amount_entry = ctk.CTkEntry(self.search_frame)
        self.min_amount_entry.grid(row=0, column=3, padx=5, pady=5)

        self.max_amount_label = ctk.CTkLabel(self.search_frame, text=self.translations[self.language]["max_amount_label"])
        self.max_amount_label.grid(row=1, column=2, padx=5, pady=5)
        self.max_amount_entry = ctk.CTkEntry(self.search_frame)
        self.max_amount_entry.grid(row=1, column=3, padx=5, pady=5)

        # Other fields
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
        ctk.set_appearance_mode(theme)

    def change_language(self, new_language):
        self.language = new_language
        self.update_translations()

    def update_translations(self):
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
        self.current_account = new_account
        print(f"Switched to account: {self.current_account}")
        # Ajoutez ici la logique pour mettre à jour l'affichage en fonction du compte sélectionné
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
        pass

    def refresh_transactions(self, filter_criteria=None):
        pass

    def refresh_overview(self):
        self.balance_label.configure(text=f"{self.translations[self.language]['balance_label']} {self.accounts[self.current_account]:.2f} €")

    def export_to_csv(self):
        transactions = []  # La liste des transactions sera remplie par votre collègue
        df = pd.DataFrame(transactions, columns=['ID', 'Référence', 'Description', 'Montant', 'Date', 'Type', 'Catégorie', 'Expéditeur', 'Bénéficiare'])
        df.to_csv('transactions.csv', index=False)
        print("Données exportées vers transactions.csv")

    def check_and_notify_alerts(self):
        pass

    def show_logout_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Confirmation")
        popup.geometry("300x200")

        # Rendre la fenêtre modale
        popup.grab_set()

        message_label = ctk.CTkLabel(popup, text="Vous partez ?", font=("Helvetica", 16, "bold"))
        message_label.pack(pady=10)

        sub_message_label = ctk.CTkLabel(popup, text="Bonne journée et à bientôt", font=("Helvetica", 12))
        sub_message_label.pack(pady=5)

        logout_button = ctk.CTkButton(popup, text="Se déconnecter", command=self.confirm_logout)
        logout_button.pack(pady=10)

        stay_button = ctk.CTkButton(popup, text="Rester sur l'application", command=popup.destroy)
        stay_button.pack(pady=5)

    def confirm_logout(self):
        self.destroy()  # Ferme la fenêtre actuelle
        # Vous pouvez ajouter ici le code pour ouvrir une nouvelle fenêtre de connexion si nécessaire

    def logout(self):
        self.show_logout_popup()

    def generate_unique_account_number(self):
        """Génère un numéro de compte unique."""
        while True:
            account_number = ''.join(secrets.choice(string.digits) for _ in range(10))
            if account_number not in self.user_accounts:
                return account_number

    def create_new_account(self, user_data):
        """Crée un nouveau compte pour l'utilisateur avec un numéro de compte aléatoire."""
        new_account_number = self.generate_unique_account_number()
        self.user_accounts[new_account_number] = user_data
        print(f"Nouveau compte créé avec le numéro : {new_account_number}")

if __name__ == "__main__":
    app = FinanceManagerApp()
    app.mainloop()
