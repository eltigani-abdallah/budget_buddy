import mysql.connector 
from mysql.connector import Error
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()

dbpassword = os.getenv("pass")

# Function to establish a connection to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password= dbpassword,
            database="boom_budget"
        )
        if connection.is_connected():
            print("Connected to the database successfully!")
            return connection
    except Error as e:
        print(f"Error while connecting to the database: {e}")
        return None

# Function to search for transactions based on provided criteria
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

# Function to plot transactions on a bar chart
def plot_transactions(transactions):
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

# Function to search transactions based on user input and display them
def search_and_display():
    date_from = entry_date_from.get() or None
    date_to = entry_date_to.get() or None
    category = category_var.get() or None
    trans_type = type_var.get() or None
    order_by = order_var.get() or None

    # Convert date strings to datetime.date objects
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Error", "Invalid 'Date from' format. Use YYYY-MM-DD.")
            return
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Error", "Invalid 'Date to' format. Use YYYY-MM-DD.")
            return

    transactions = search_transactions(connection, date_from, date_to, category, trans_type, order_by)

    # Clear previous entries in Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Insert new transactions into Treeview
    for t in transactions:
        tree.insert("", "end", values=(t['date'], t['amount'], t['category'], t['type']))

# Function to display a graph of all transactions
def show_graph():
    transactions = search_transactions(connection)
    plot_transactions(transactions)

# Establish database connection
connection = create_connection()

# Tkinter Interface
root = tk.Tk()
root.title("Transaction Search")
root.geometry("800x600")

# Filter Panel
filter_frame = tk.Frame(root)
filter_frame.pack(pady=50)  

tk.Label(filter_frame, text="Date from (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)  
entry_date_from = tk.Entry(filter_frame)
entry_date_from.grid(row=0, column=1, padx=10, pady=10)

tk.Label(filter_frame, text="Date to (YYYY-MM-DD):").grid(row=0, column=2, padx=10, pady=10)
entry_date_to = tk.Entry(filter_frame)
entry_date_to.grid(row=0, column=3, padx=10, pady=10)

category_var = tk.StringVar()
tk.Label(filter_frame, text="Category:").grid(row=1, column=0, padx=10, pady=10)
category_menu = ttk.Combobox(filter_frame, textvariable=category_var, values=["", "Expense Categories","Entertainment & Leisure","Shopping","Food & Dining","bribe","Other Categories"])
category_menu.grid(row=1, column=1, padx=10, pady=10)

type_var = tk.StringVar()
tk.Label(filter_frame, text="Transaction Type:").grid(row=1, column=2, padx=10, pady=10)
type_menu = ttk.Combobox(filter_frame, textvariable=type_var, values=["", "withdrawal", "Transfer", "Deposit"])
type_menu.grid(row=1, column=3, padx=10, pady=10)

order_var = tk.StringVar()
tk.Label(filter_frame, text="Sort by amount:").grid(row=2, column=0, padx=10, pady=10)
order_menu = ttk.Combobox(filter_frame, textvariable=order_var, values=["", "asc", "desc"])
order_menu.grid(row=2, column=1, padx=10, pady=10)

search_button = tk.Button(filter_frame, text="Search Transactions", command=search_and_display)
search_button.grid(row=2, column=2, padx=10, pady=10)

graph_button = tk.Button(filter_frame, text="Show Graph", command=show_graph)
graph_button.grid(row=2, column=3, padx=10, pady=10)



# Treeview for displaying transactions
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

tree = ttk.Treeview(tree_frame, columns=("Date", "Amount", "Category", "Type"), show="headings", selectmode="extended")
tree.heading("Date", text="Date")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.heading("Type", text="Type")

tree.column("Date", width=100)
tree.column("Amount", width=100)
tree.column("Category", width=100)
tree.column("Type", width=100)

tree.pack(side=tk.LEFT)

# Scrollbar for Treeview
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Start the main event loop
root.mainloop()

# Close the database connection when the application exits
if connection and connection.is_connected():
    connection.close()