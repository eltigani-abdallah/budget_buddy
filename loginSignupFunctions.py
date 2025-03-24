import os
import re
from tkinter import messagebox
import bcrypt
from dotenv import load_dotenv
import mysql.connector


load_dotenv()

dbpassword = os.getenv("pass")

print("Login Module:", os.getcwd())

# Function to validate password based on security criteria
def validate_password(password):
    if len(password) < 10:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[@$!%*?_&]', password): 
        return False
    return True


def verify_login(email, password):
    '''
    Function to verify login credentials
    '''
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password= dbpassword,
            database="boom_budget",
        )
        cursor = db.cursor()
        cursor.execute("SELECT mot_de_passe FROM utilisateurs WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


# Function for user registration with password validation and hashing
def register_user(first_name, last_name, email, password, confirm_password):
    if not validate_password(password):
        messagebox.showerror("Error", "The password does not meet security requirements.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=dbpassword,
            database="boom_budget",
        )
        cursor = db.cursor()
        cursor.execute("SELECT id FROM utilisateurs WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "This email is already in use. Please choose another one.")
            cursor.close()
            db.close()
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)",
                    (first_name, last_name, email, hashed_password))
        db.commit()
        cursor.close()
        db.close()

        messagebox.showinfo("Success", "User successfully registered.")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", "Unable to register the user.")
