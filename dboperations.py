from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import json
import os
load_dotenv()
dbpassword = os.getenv("pass")

def create_connection():
    '''create connection to database'''
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

def search_transactions_db(connection, user_id, date_from=None, date_to=None, category=None, trans_type=None, order_by_amount=None):
    '''search for transactions based on user'''
    if connection is None:
        messagebox.showerror("Error", "No connection to the database!")
        return []

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM les_transactions WHERE user_id = %s"
    params = [user_id]

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