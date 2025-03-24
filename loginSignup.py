import customtkinter as ctk
from tkinter import messagebox
from sessionManager import create_session
from loginSignupFunctions import verify_login, register_user

class LoginSignup(ctk.CTkFrame):  # Make it inherit from CTk (the main window)
    def __init__(self, master):
        super().__init__(master)
        self.master=master
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.create_widgets()
        self.pack(expand=True, fill="both")

    def create_widgets(self):
        """Creates the UI elements and stores them as attributes."""
        self.welcome_label = ctk.CTkLabel(self, text="Bienvenue dans votre banque, en toute simplicité. Boom_Budget",
        font=("Helvetica", 16, "bold"))
        self.welcome_label.pack(pady=10)

        # Login widgets
        self.frame_login = ctk.CTkFrame(self)
        self.frame_login.pack(pady=20, padx=60, fill="both", expand=True)

        self.label_login = ctk.CTkLabel(self.frame_login, text="LOGIN", font=("Helvetica", 24))
        self.label_login.pack(pady=12, padx=10)

        self.entry1 = ctk.CTkEntry(self.frame_login, placeholder_text="Email")
        self.entry1.pack(pady=12, padx=10)

        self.entry2 = ctk.CTkEntry(self.frame_login, placeholder_text="Password", show="*")
        self.entry2.pack(pady=12, padx=10)

        self.button_login = ctk.CTkButton(self.frame_login, text="Login", command=self.on_login)
        self.button_login.pack(pady=12, padx=10)

        # Sign-up widgets
        self.frame_signup = ctk.CTkFrame(self)
        self.frame_signup.pack(pady=20, padx=60, fill="both", expand=True)

        self.label_signup = ctk.CTkLabel(self.frame_signup, text="SIGN UP", font=("Helvetica", 24))
        self.label_signup.pack(pady=12, padx=10)

        self.entry_first_name = ctk.CTkEntry(self.frame_signup, placeholder_text="First Name")
        self.entry_first_name.pack(pady=12, padx=10)

        self.entry_last_name = ctk.CTkEntry(self.frame_signup, placeholder_text="Last Name")
        self.entry_last_name.pack(pady=12, padx=10)

        self.entry_email = ctk.CTkEntry(self.frame_signup, placeholder_text="Email")
        self.entry_email.pack(pady=12, padx=10)

        self.entry_password = ctk.CTkEntry(self.frame_signup, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=12, padx=10)

        self.entry_confirm_password = ctk.CTkEntry(self.frame_signup, placeholder_text="Confirm Password", show="*")
        self.entry_confirm_password.pack(pady=12, padx=10)

        # Checkbox to toggle password visibility
        self.check_var = ctk.BooleanVar()
        self.checkbox = ctk.CTkCheckBox(self.frame_signup, text="Show Password",
                                        variable=self.check_var, command=self.toggle_password)
        self.checkbox.pack(pady=5)

        self.button_signup = ctk.CTkButton(self.frame_signup, text="Sign Up", command=self.on_register)
        self.button_signup.pack(pady=12, padx=10)

    def on_login(self):
        """Handles login logic."""
        email = self.entry1.get()
        password = self.entry2.get()

        if verify_login(email, password):
            create_session(email)
            messagebox.showinfo("Success", "Login successful!")
            self.master.show_banking_app()
        else:
            messagebox.showerror("Error", "Incorrect email or password.")

    def on_register(self):
        """Handles registration logic."""
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        confirm_password = self.entry_confirm_password.get()

        if not first_name or not last_name or not email or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        register_user(first_name, last_name, email, password, confirm_password)

    def toggle_password(self):
        """Toggles password visibility."""
        if self.check_var.get():
            self.entry_password.configure(show="")
            self.entry_confirm_password.configure(show="")
        else:
            self.entry_password.configure(show="*")
            self.entry_confirm_password.configure(show="*")

