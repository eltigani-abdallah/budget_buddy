import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# Function to establish a connection to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
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

    listbox.delete(0, tk.END)
    for t in transactions:
        listbox.insert(tk.END, f"{t['date']} - {t['amount']}€ - {t['category']} - {t['type']}")

# Function to display a graph of all transactions
def show_graph():
    transactions = search_transactions(connection)
    plot_transactions(transactions)

# Establish database connection
connection = create_connection()

# Tkinter Interface
root = tk.Tk()
root.title("Transaction Search")
root.geometry("600x500")

tk.Label(root, text="Date from (YYYY-MM-DD):").pack()
entry_date_from = tk.Entry(root)
entry_date_from.pack()

tk.Label(root, text="Date to (YYYY-MM-DD):").pack()
entry_date_to = tk.Entry(root)
entry_date_to.pack()

category_var = tk.StringVar()
tk.Label(root, text="Category:").pack()
category_menu = ttk.Combobox(root, textvariable=category_var, values=["", "loisir", "repas", "pot-de-vin"])
category_menu.pack()

type_var = tk.StringVar()
tk.Label(root, text="Transaction Type:").pack()
type_menu = ttk.Combobox(root, textvariable=type_var, values=["", "withdrawal", "payment"])
type_menu.pack()

order_var = tk.StringVar()
tk.Label(root, text="Sort by amount:").pack()
order_menu = ttk.Combobox(root, textvariable=order_var, values=["", "asc", "desc"])
order_menu.pack()

search_button = tk.Button(root, text="Search Transactions", command=search_and_display)
search_button.pack()

graph_button = tk.Button(root, text="Show Graph", command=show_graph)
graph_button.pack()

listbox = tk.Listbox(root, width=80, height=10)
listbox.pack()

root.mainloop()

# Close the database connection when the application exits
if connection and connection.is_connected():
    connection.close()