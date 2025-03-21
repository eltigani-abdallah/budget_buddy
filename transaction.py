import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
from dotenv import load_dotenv
from tkcalendar import Calendar

load_dotenv()

dbpassword = os.getenv("pass")

# Function to establish a connection to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=dbpassword,
            database="boom_budget"
        )
        if connection.is_connected():
            print("Connected to the database successfully!")
            return connection
    except Error as e:
        print(f"Error while connecting to the database: {e}")
        return None

# Function to search for transactions based on provided criteria
def show_calendar(entry_field):
    def get_selected_date():
        selected_date = cal.get_date()
        entry_field.delete(0, tk.END)
        entry_field.insert(0, selected_date)
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Select date")
    cal = Calendar(top, selectmode="day", date_pattern='yyyy-mm-dd')
    cal.pack(pady=10)
    
    btn = tk.Button(top, text="ОК", command=get_selected_date)
    btn.pack(pady=5)

# Function to plot transactions on a bar chart
def search_transactions(connection, date_from=None, date_to=None, category=None, trans_type=None, order_by_amount=None):
    if connection is None:
        messagebox.showerror("Error", "No connection to the database!")
        return []
    
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM les_transactions WHERE 1=1"
    params = []

    if date_from:
        query += " AND date >= %s"
        params.append(date_from)
    if date_to:
        query += " AND date <= %s"
        params.append(date_to)
    if category:
        query += " AND category = %s"
        params.append(category)
    if trans_type:
        query += " AND type = %s"
        params.append(trans_type)
    if order_by_amount:
        query += f" ORDER BY amount {order_by_amount.upper()}"

    cursor.execute(query, params)
    transactions = cursor.fetchall()
    cursor.close()
    return transactions

# Function to search transactions based on user input and display them
def search_and_display():
    date_from = entry_date_from.get() or None
    date_to = entry_date_to.get() or None
    category = category_var.get() or None
    trans_type = type_var.get() or None
    order_by = order_var.get() or None
    
    transactions = search_transactions(connection, date_from, date_to, category, trans_type, order_by)
    
    # Clear previous entries in Treeview
    for row in tree.get_children():
        tree.delete(row)

    # insert new transactions into Treeview
    for t in transactions:
        tree.insert("", "end", values=(t['date'], t['amount'], t['category'], t['type']))

# Function to display a graph of filtered transactions
def show_graph():
    date_from = entry_date_from.get() or None
    date_to = entry_date_to.get() or None
    category = category_var.get() or None
    trans_type = type_var.get() or None
    order_by = order_var.get() or None

    transactions = search_transactions(connection, date_from, date_to, category, trans_type, order_by)
    
    if not transactions:
        messagebox.showinfo("Chart", "No data to display.")
        return
    
    dates = [t['date'] for t in transactions]
    amounts = [t['amount'] for t in transactions]

    plt.figure(figsize=(10, 5))
    plt.bar(dates, amounts, color='blue')
    plt.xlabel('Date')
    plt.ylabel('Amount (€)')
    plt.title('Transactions')
    plt.xticks(rotation=45)
    plt.show()


connection = create_connection()


root = tk.Tk()
root.title("Transaction Search")
root.geometry("800x600")


filter_frame = tk.Frame(root)
filter_frame.pack(pady=20)

tk.Label(filter_frame, text="Date from (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
entry_date_from = tk.Entry(filter_frame)
entry_date_from.grid(row=0, column=1, padx=10, pady=10)
entry_date_from.bind("<Button-1>", lambda e: show_calendar(entry_date_from))

tk.Label(filter_frame, text="Date to (YYYY-MM-DD):").grid(row=0, column=2, padx=10, pady=10)
entry_date_to = tk.Entry(filter_frame)
entry_date_to.grid(row=0, column=3, padx=10, pady=10)
entry_date_to.bind("<Button-1>", lambda e: show_calendar(entry_date_to))

category_var = tk.StringVar()
tk.Label(filter_frame, text="Category:").grid(row=1, column=0, padx=10, pady=10)
category_menu = ttk.Combobox(filter_frame, textvariable=category_var, values=["", "Bills", "Leisure", "Dining", "Travels", "Other Categories"])
category_menu.grid(row=1, column=1, padx=10, pady=10)


type_var = tk.StringVar()
tk.Label(filter_frame, text="Transaction Type:").grid(row=1, column=2, padx=10, pady=10)
type_menu = ttk.Combobox(filter_frame, textvariable=type_var, values=["", "Withdrawal", "Transfer", "Deposit"])
type_menu.grid(row=1, column=3, padx=10, pady=10)

order_var = tk.StringVar()
tk.Label(filter_frame, text="Sort by amount:").grid(row=2, column=0, padx=10, pady=10)
order_menu = ttk.Combobox(filter_frame, textvariable=order_var, values=["", "ASC", "DESC"])
order_menu.grid(row=2, column=1, padx=10, pady=10)

search_button = tk.Button(filter_frame, text="Search Transactions", command=search_and_display)
search_button.grid(row=2, column=2, padx=10, pady=10)

graph_button = tk.Button(filter_frame, text="Show Graph", command=show_graph)
graph_button.grid(row=2, column=3, padx=10, pady=10)

tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

tree = ttk.Treeview(tree_frame, columns=("Date", "Amount", "Category", "Type"), show="headings", selectmode="extended")
for col in ("Date", "Amount", "Category", "Type"):
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(side=tk.LEFT)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()
if connection and connection.is_connected():
    connection.close()
