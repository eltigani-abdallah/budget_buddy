import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import json
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def on_close():
    logout()
    print("shutting down...")
    app.quit()
    exit()

session_file="./assets/session.json"
with open(session_file, "r") as file:
    session_data=json.load(file)

user_email= session_data.get("email")

if not user_email:
    print("invalid session.")
    exit()

dbpassword= os.getenv("PASS")
try:
    db=mysql.connector.connect(
        host="localhost",
        user="root",
        password=dbpassword,
        database="boom_budget"
    )
    mycursor=db.cursor()
    mycursor.execute("SELECT id FROM utilisateurs WHERE email = %s",(user_email,))
    user=mycursor.fetchone()
    mycursor.close()
    db.close()
    if not user:
        print("invalid login")
        exit()
    print(f"welcome {user_email}, you are logged in")
except Exception as e:
    print(f"database error {e}")
    exit()

def logout():
    if os.path.exists("./assets/session.json"):
        os.remove("./assets/session.json")
    print("you have been logged out")
    exit()


def load_lang(langs):
    with open (langs,"r", encoding="utf-8") as file:
        return json.load(file)
    
lang_dict=load_lang("./assets/lang.json")

def translate(lang, key):
    return lang_dict.get(lang,{}).get(key,f"[{key} not found]")

class FinanceManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.language = "français"

        self.title("Gestionnaire de Finances")
        self.geometry("1000x700")

        self.balance = 0  # Initial balance
        self.create_widgets()
        self.refresh_overview()

    

    def create_widgets(self):
        self.language_menu = ctk.CTkOptionMenu(self, values=["français", "anglais", "russe", "coréen"], command=self.change_language)
        self.language_menu.pack(anchor="ne", pady=10, padx=10)
        self.language_menu.set(self.language)

        self.notebook = ctk.CTkTabview(self)
        self.notebook.pack(pady=20, fill='both', expand=True)

        self.transactions_tab = self.notebook.add("Transactions")
        self.overview_tab = self.notebook.add("Vue d'ensemble")
        self.export_tab = self.notebook.add("Exportation")
        self.notifications_tab = self.notebook.add("Notifications")

        custom_font = ctk.CTkFont(family="KalniaGlaze-VariableFont_wdth,wght", size=24)

        self.bank_name_label = ctk.CTkLabel(self.transactions_tab, text="Boom_Budget", font=custom_font)
        self.bank_name_label.pack(pady=10)

        self.reference_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=translate(self.language,"reference_placeholder"))
        self.reference_entry.pack(pady=5)

        self.description_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=translate(self.language,"description_placeholder"))
        self.description_entry.pack(pady=5)

        self.amount_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=translate(self.language,"amount_placeholder"))
        self.amount_entry.pack(pady=5)

        self.category_entry = ctk.CTkEntry(self.transactions_tab, placeholder_text=translate(self.language,"category_placeholder"))
        self.category_entry.pack(pady=5)

        self.deposit_button = ctk.CTkButton(self.transactions_tab, text=translate(self.language,"deposit_button"), command=self.deposit)
        self.deposit_button.pack(pady=5)

        self.withdraw_button = ctk.CTkButton(self.transactions_tab, text=translate(self.language,"withdraw_button"), command=self.withdraw)
        self.withdraw_button.pack(pady=5)

        self.transfer_button = ctk.CTkButton(self.transactions_tab, text=translate(self.language,"transfer_button"), command=self.transfer)
        self.transfer_button.pack(pady=5)

        self.search_frame = ctk.CTkFrame(self.transactions_tab)
        self.search_frame.pack(pady=10)

        # Dates column
        self.date_label = ctk.CTkLabel(self.search_frame, text=translate(self.language,"date_label"))
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ctk.CTkEntry(self.search_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        self.start_date_label = ctk.CTkLabel(self.search_frame, text=translate(self.language,"start_date_label"))
        self.start_date_label.grid(row=1, column=0, padx=5, pady=5)
        self.start_date_entry = ctk.CTkEntry(self.search_frame)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        self.end_date_label = ctk.CTkLabel(self.search_frame, text=translate(self.language,"end_date_label"))
        self.end_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.end_date_entry = ctk.CTkEntry(self.search_frame)
        self.end_date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Amounts column
        self.min_amount_label = ctk.CTkLabel(self.search_frame, text=translate(self.language,"min_amount_label"))
        self.min_amount_label.grid(row=0, column=2, padx=5, pady=5)
        self.min_amount_entry = ctk.CTkEntry(self.search_frame)
        self.min_amount_entry.grid(row=0, column=3, padx=5, pady=5)

        self.max_amount_label = ctk.CTkLabel(self.search_frame, text=translate(self.language,"max_amount_label"))
        self.max_amount_label.grid(row=1, column=2, padx=5, pady=5)
        self.max_amount_entry = ctk.CTkEntry(self.search_frame)
        self.max_amount_entry.grid(row=1, column=3, padx=5, pady=5)

        # Other fields
        self.category_label = ctk.CTkLabel(self.search_frame, text=translate(self.language,"category_label"))
        self.category_label.grid(row=2, column=2, padx=5, pady=5)
        self.category_search_entry = ctk.CTkEntry(self.search_frame)
        self.category_search_entry.grid(row=2, column=3, padx=5, pady=5)

        self.type_label = ctk.CTkLabel(self.search_frame, text=translate(self.language,"type_label"))
        self.type_label.grid(row=3, column=0, padx=5, pady=5)
        self.type_entry = ctk.CTkEntry(self.search_frame)
        self.type_entry.grid(row=3, column=1, padx=5, pady=5)

        self.sort_label = ctk.CTkLabel(self.search_frame, text=translate(self.language,"sort_label"))
        self.sort_label.grid(row=3, column=2, padx=5, pady=5)
        self.sort_entry = ctk.CTkComboBox(self.search_frame, values=["", "ASC", "DESC"])
        self.sort_entry.grid(row=3, column=3, padx=5, pady=5)

        self.search_button = ctk.CTkButton(self.transactions_tab, text=translate(self.language,"search_button"), command=self.search_transactions)
        self.search_button.pack(pady=5)

        self.transactions_listbox = ctk.CTkTextbox(self.transactions_tab, width=760, height=200)
        self.transactions_listbox.pack(pady=10)

        self.balance_label = ctk.CTkLabel(self.overview_tab, text="", font=("Helvetica", 18))
        self.balance_label.pack(pady=10)

        self.alert_label = ctk.CTkLabel(self.overview_tab, text="", text_color="red")
        self.alert_label.pack(pady=10)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, self.overview_tab)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.export_button = ctk.CTkButton(self.export_tab, text=translate(self.language,"export_button"), command=self.export_to_csv)
        self.export_button.pack(pady=20)

        self.check_alerts_button = ctk.CTkButton(self.notifications_tab, text=translate(self.language,"check_alerts_button"), command=self.check_and_notify_alerts)
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
        translations = lang_dict[self.language]
        self.title(translations["title"])
        self.balance_label.configure(text=translations["balance_label"])
        self.alert_label.configure(text=translations.get("alert_label", ""))
        self.deposit_button.configure(text=translations["deposit_button"])
        self.withdraw_button.configure(text=translations["withdraw_button"])
        self.transfer_button.configure(text=translations["transfer_button"])
        self.search_button.configure(text=translations["search_button"])
        self.export_button.configure(text=translations["export_button"])
        self.check_alerts_button.configure(text=translations["check_alerts_button"])
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
        self.category_entry.configure(placeholder_text=translations["category_placeholder"])

    def deposit(self):
        pass

    def withdraw(self):
        pass

    def transfer(self):
        pass

    def search_transactions(self):
        pass

    def refresh_transactions(self, filter_criteria=None):
        pass

    def refresh_overview(self):
        self.balance += 800  # Add 300 euros to the balance
        self.balance_label.configure(text=f"{translate(self.language,'balance_label')} {self.balance:.2f} €")

    def export_to_csv(self):
        transactions = []  # La liste des transactions sera remplie par votre collègue
        df = pd.DataFrame(transactions, columns=['ID', 'Référence', 'Description', 'Montant', 'Date', 'Type', 'Catégorie', 'Expéditeur''Bénéficiare'])
        df.to_csv('transactions.csv', index=False)
        print("Données exportées vers transactions.csv")

    def check_and_notify_alerts(self):
        pass


if __name__ == "__main__":
    app = FinanceManagerApp()
    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()
