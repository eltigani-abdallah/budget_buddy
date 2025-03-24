'''this file will contain all functions relating to graph creation
    will also contain functions necessary to use graph searching'''

import matplotlib.pyplot as plt
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
dbpassword = os.getenv("pass")





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
    
connection = create_connection()


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


#function to display pie chart of transactions
def show_pie_chart():
    date_from = entry_date_from.get() or None
    date_to = entry_date_to.get() or None
    category = category_var.get() or None
    trans_type = type_var.get() or None
    order_by = order_var.get() or None

    transactions = search_transactions(connection,date_from,date_to,trans_type, order_by, category)


    
    if not transactions:
        messagebox.showinfo("Chart", "No data to display.")
        return
    
    category_totals=defaultdict(float)
    for t in transactions:
        category_totals[t['category']] += float(t['amount'])

    categories=list(category_totals.keys())
    amounts=list(category_totals.values())

    max_value=max(amounts)
    max_index=amounts.index(max_value)
    explode=[0.2 if i==max_index else 0 for i in range(len(amounts))]
    plt.pie(amounts, labels=categories, explode=explode, shadow=True, autopct="%1.1f%%")
    plt.show()
