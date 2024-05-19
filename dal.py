import mysql.connector
from mysql.connector import Error
class AccessDao:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            print("Connexion à la base de données réussie")
        except Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Déconnexion de la base de données réussie")


