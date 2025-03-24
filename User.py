import bcrypt


class User:
    def __init__(self, user_id, nom, prenom, email, mot_de_passe):
        self.user_id = user_id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = mot_de_passe

    @staticmethod
    def register(connection, nom, prenom, email, mot_de_passe):
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
        cursor = connection.cursor()
        query = """
        INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nom, prenom, email, hashed_password))
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        return User(user_id, nom, prenom, email, hashed_password)

    @staticmethod
    def login(connection, email, mot_de_passe):
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM utilisateurs WHERE email = %s"
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data and bcrypt.checkpw(mot_de_passe.encode('utf-8'), user_data['mot_de_passe'].encode('utf-8')):
            return User(user_data['id'], user_data['nom'], user_data['prenom'], user_data['email'], user_data['mot_de_passe'])
        return None