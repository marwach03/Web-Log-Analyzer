import mysql.connector
from mysql.connector import Error

class AccessDao:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            print("Connexion a la base de donnees reussie")
        except Error as e:
            print(f"Erreur de connexion à la base de donnees: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Deconnexion de la base de donnees reussie")
    
    
    def fetch_unique_visitors_and_hits_per_day(self):
        if not self.connection:
            print("Pas de connexion a la base de donnees")
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = '''
                SELECT 
                    DATE(date) AS log_date, 
                    COUNT(DISTINCT ip) AS unique_visitors,
                    COUNT(*) AS total_hits
                FROM 
                    logs
                GROUP BY 
                    log_date
                ORDER BY 
                    log_date
            '''
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Erreur lors de la recuperation des visiteurs uniques et des hits par jour: {e}")
            return []
        finally:
            cursor.close()

    


