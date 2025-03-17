import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
import bcrypt
import re
import os
import subprocess

print("Module de connexion:", os.getcwd())

# Fonction pour valider le mot de passe selon les critères
def validate_password(password):
    # Vérifie la longueur du mot de passe
    if len(password) < 10:
        return False

    # Vérifie si le mot de passe contient au moins une majuscule, une minuscule, un chiffre et un caractère spécial
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[@$!%*?&]', password):
        return False

    return True

# Fonction pour vérifier les identifiants lors de la connexion
def verify_login(email, password):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Parfait1313",
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

# Fonction d'inscription avec validation et hachage du mot de passe
def register_user(nom, prenom, email, mot_de_passe):
    # Valider le mot de passe
    if not validate_password(mot_de_passe):
        messagebox.showerror("Erreur", "Le mot de passe ne respecte pas les critères de sécurité.")
        return

    try:
        # Connexion à la base de données
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Parfait1313",
            database="boom_budget",
        )
        cursor = db.cursor()

        # Vérifier si l'email existe déjà
        cursor.execute("SELECT id FROM utilisateurs WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Erreur", "L'email est déjà utilisé. Veuillez en choisir un autre.")
            cursor.close()
            db.close()
            return

        # Hacher le mot de passe
        hashed_password = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())

        # Inscrire l'utilisateur dans la base de données
        cursor.execute("INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)",
                    (nom, prenom, email, hashed_password))
        db.commit()
        cursor.close()
        db.close()

        messagebox.showinfo("Succès", "Utilisateur inscrit avec succès.")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Erreur", "Impossible d'inscrire l'utilisateur.")

# Fonction de gestion de la connexion
def on_login():
    email = entry1.get()  # Utiliser l'email pour se connecter
    password = entry2.get()

    if verify_login(email, password):
        messagebox.showinfo("Succès", "Connexion réussie !")
        # Fermer la fenêtre de connexion
        app.destroy()
        # Lancer l'application principale (par exemple)
        backend_path = "login.py"
        try:
            subprocess.run(["python", backend_path])
        except Exception:
            messagebox.showerror("Erreur", f"Fichier introuvable : {backend_path}")
    else:
        messagebox.showerror("Erreur", "Email ou mot de passe incorrect")

# Fonction de gestion de l'inscription
def on_register():
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    email = entry_email.get()
    mot_de_passe = entry_mdp.get()

    if not nom or not prenom or not email or not mot_de_passe:
        messagebox.showerror("Erreur", "Tous les champs sont requis.")
        return

    # Appeler la fonction d'inscription
    register_user(nom, prenom, email, mot_de_passe)

# Initialiser l'application
app = ctk.CTk()
app.geometry("400x500")
app.title("Fenêtre d'inscription / Connexion")

# Configurer l'apparence et le thème de couleur
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Créer les widgets pour la connexion
frame_connexion = ctk.CTkFrame(master=app)
frame_connexion.pack(pady=20, padx=60, fill="both", expand=True)

label_connexion = ctk.CTkLabel(master=frame_connexion, text="LOGIN", font=("Helvetica", 24))
label_connexion.pack(pady=12, padx=10)

entry1 = ctk.CTkEntry(master=frame_connexion, placeholder_text="Email")
entry1.pack(pady=12, padx=10)

entry2 = ctk.CTkEntry(master=frame_connexion, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button_connexion = ctk.CTkButton(master=frame_connexion, text="Se connecter", command=on_login)
button_connexion.pack(pady=12, padx=10)

# Créer les widgets pour l'inscription
frame_inscription = ctk.CTkFrame(master=app)
frame_inscription.pack(pady=20, padx=60, fill="both", expand=True)

label_inscription = ctk.CTkLabel(master=frame_inscription, text="S'INSCRIRE", font=("Helvetica", 24))
label_inscription.pack(pady=12, padx=10)

entry_nom = ctk.CTkEntry(master=frame_inscription, placeholder_text="Nom")
entry_nom.pack(pady=12, padx=10)

entry_prenom = ctk.CTkEntry(master=frame_inscription, placeholder_text="Prénom")
entry_prenom.pack(pady=12, padx=10)

entry_email = ctk.CTkEntry(master=frame_inscription, placeholder_text="Email")
entry_email.pack(pady=12, padx=10)

entry_mdp = ctk.CTkEntry(master=frame_inscription, placeholder_text="Password", show="*")
entry_mdp.pack(pady=12, padx=10)

button_inscription = ctk.CTkButton(master=frame_inscription, text="S'inscrire", command=on_register)
button_inscription.pack(pady=12, padx=10)

# Lancer l'application
app.mainloop()
