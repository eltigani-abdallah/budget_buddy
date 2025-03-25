import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
import bcrypt
import re 
import os
import subprocess
from dotenv import load_dotenv
import json

load_dotenv()

dbpassword = os.getenv("pass")

print("Login Module:", os.getcwd())

def validate_password(password):
    """
    Validate the password based on security criteria.

    The password must meet the following criteria:
    - At least 10 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character from the set: @$!%*?_&-

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if the password meets all criteria, False otherwise.
    """
    if len(password) < 10:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[@$!%*?_&-]', password):  # Include underscore in the special characters
        return False
    return True

def verify_login(email, password):
    """
    Verify login credentials by checking the email and password against the database.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=dbpassword,
            database="boom_budget",
        )
        ''' 
    Retrieves the password of a user from the database based on their email.

    Parameters:
    email (str): The email address of the user.
    db (object): The database connection object.

    Returns:
    tuple or None: A tuple containing the user's password if the email exists, or None if the email is not found.

    Process:
    1. A cursor is created to execute SQL queries.
    2. A SELECT query is executed to fetch the password for the given email.
    3. The first result (if any) is retrieved using fetchone().
    4. The cursor is closed to free resources.
    5. The database connection is closed to ensure proper resource management.
    
    Note:
    - The query uses parameterized SQL (`%s`) to prevent SQL injection.
    - The returned value is a tuple containing the password or None if no user is found.
    '''
        cursor = db.cursor() 
        cursor.execute("SELECT mot_de_passe FROM utilisateurs WHERE email = %s", (email,)) # select mdp ... lance une requettes SQL, paramètre de substitution utilisé pour éviter les injections SQL
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def register_user(first_name, last_name, email, password, confirm_password):
    """
    Register a new user with password validation and hashing.

    Args:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email of the user.
        password (str): The password of the user.
        confirm_password (str): The confirmed password of the user.

    Returns:
        None
    """
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

def on_login():
    """
    Handle the login process.

    Retrieves the email and password from the input fields, verifies the credentials,
    and proceeds to the next step if the login is successful.

    Returns:
        None
    """
    email = entry1.get()
    password = entry2.get()

    if verify_login(email, password):
        messagebox.showinfo("Success", "Login successful!")
        app.destroy()
        backend_path = "banking.py"

        session_data= {"email": email}
        with open("./assets/session.json", "w") as session_file:
            json.dump(session_data, session_file)

        try:
            subprocess.run(["python", backend_path])
        except Exception:
            messagebox.showerror("Error", f"File not found: {backend_path}")
    else:
        messagebox.showerror("Error", "Incorrect email or password.")

def on_register():
    """
    Handle the registration process.

    Retrieves user details from the input fields and registers the user if all
    validations pass.

    Returns:
        None
    """
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()

    if not first_name or not last_name or not email or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required.")
        return

    register_user(first_name, last_name, email, password, confirm_password)

def toggle_password():
    """
    Toggle the visibility of the password fields.

    Returns:
        None
    """
    if check_var.get():
        entry_password.configure(show="")
        entry_confirm_password.configure(show="")
    else:
        entry_password.configure(show="*")
        entry_confirm_password.configure(show="*")

# Initialize the application
app = ctk.CTk()
app.geometry("400x550")
app.title("Sign Up / Login Window")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# GUI
welcome_label = ctk.CTkLabel(master=app, text="Boom_Budget", font=("Helvetica", 16, "bold"))
welcome_label.pack(pady=10)

# Login widgets
frame_login = ctk.CTkFrame(master=app)
frame_login.pack(pady=20, padx=60, fill="both", expand=True)

label_login = ctk.CTkLabel(master=frame_login, text="LOGIN", font=("Helvetica", 24))
label_login.pack(pady=12, padx=10)

entry1 = ctk.CTkEntry(master=frame_login, placeholder_text="Email")
entry1.pack(pady=12, padx=10)

entry2 = ctk.CTkEntry(master=frame_login, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button_login = ctk.CTkButton(master=frame_login, text="Login", command=on_login)
button_login.pack(pady=12, padx=10)

# Sign-up widgets
frame_signup = ctk.CTkFrame(master=app)
frame_signup.pack(pady=20, padx=60, fill="both", expand=True)

label_signup = ctk.CTkLabel(master=frame_signup, text="SIGN UP", font=("Helvetica", 24))
label_signup.pack(pady=12, padx=10)

entry_first_name = ctk.CTkEntry(master=frame_signup, placeholder_text="First Name")
entry_first_name.pack(pady=12, padx=10)

entry_last_name = ctk.CTkEntry(master=frame_signup, placeholder_text="Last Name")
entry_last_name.pack(pady=12, padx=10)

entry_email = ctk.CTkEntry(master=frame_signup, placeholder_text="Email")
entry_email.pack(pady=12, padx=10)

entry_password = ctk.CTkEntry(master=frame_signup, placeholder_text="Password", show="*")
entry_password.pack(pady=12, padx=10)

entry_confirm_password = ctk.CTkEntry(master=frame_signup, placeholder_text="Confirm Password", show="*")
entry_confirm_password.pack(pady=12, padx=10)

# Checkbox to toggle password visibility
check_var = ctk.BooleanVar()
checkbox = ctk.CTkCheckBox(master=frame_signup, text="Show Password", variable=check_var, command=toggle_password)
checkbox.pack(pady=5)

button_signup = ctk.CTkButton(master=frame_signup, text="Sign Up", command=on_register)
button_signup.pack(pady=12, padx=10)

app.mainloop()
