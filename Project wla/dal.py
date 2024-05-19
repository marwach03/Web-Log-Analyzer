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

    def fetch_total_requests(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return -1  # Valeur par défaut pour indiquer une erreur

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT COUNT(*) AS total_requests
                FROM logs
            '''
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0  # Aucune donnée trouvée
        except Error as e:
            print(f"Erreur lors de la récupération du nombre total de requêtes : {e}")
            return -1  # Valeur par défaut pour indiquer une erreur
        finally:
            cursor.close()

    def fetch_valid_requests(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return -1  # Valeur par défaut pour indiquer une erreur

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT COUNT(*) AS valid_requests
                FROM logs
                WHERE status = 200  
            '''
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0  # Aucune donnée trouvée
        except Error as e:
            print(f"Erreur lors de la récupération du nombre de requêtes valides : {e}")
            return -1  # Valeur par défaut pour indiquer une erreur
        finally:
            cursor.close()

    def fetch_failed_requests(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return -1  # Valeur par défaut pour indiquer une erreur

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT COUNT(*) AS failed_requests
                FROM logs
                WHERE status != 200  -- Remplacez 200 par le code de statut de votre choix pour les requêtes échouées
            '''
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0  # Aucune donnée trouvée
        except Error as e:
            print(f"Erreur lors de la récupération du nombre de requêtes échouées : {e}")
            return -1  # Valeur par défaut pour indiquer une erreur
        finally:
            cursor.close()

    def fetch_log_parsing_time(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return -1  # Valeur par défaut pour indiquer une erreur

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT TIMEDIFF(MAX(date), MIN(date)) AS log_parsing_time
                FROM logs;
            '''
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0  # Aucune donnée trouvée
        except Error as e:
            print(f"Erreur lors de la récupération du temps d'analyse des journaux : {e}")
            return -1  # Valeur par défaut pour indiquer une erreur
        finally:
            cursor.close()

    

