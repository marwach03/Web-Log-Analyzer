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


    def fetch_unique_visitors_count(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return -1  # Valeur par défaut pour indiquer une erreur

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT COUNT(DISTINCT ip) AS unique_visitors_count
                FROM logs
            '''
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0  # Aucune donnée trouvée
        except Error as e:
            print(f"Erreur lors de la récupération du nombre de visiteurs uniques : {e}")
            return -1  # Valeur par défaut pour indiquer une erreur
        finally:
            cursor.close()

    def fetch_requested_files_count(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return -1  # Valeur par défaut pour indiquer une erreur

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT COUNT(DISTINCT url) AS requested_files_count
                FROM logs
            '''
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0  # Aucune donnée trouvée
        except Error as e:
            print(f"Erreur lors de la récupération du nombre de fichiers demandés : {e}")
            return -1  # Valeur par défaut pour indiquer une erreur
        finally:
            cursor.close()

    
    def fetch_referrers_count(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return -1  # Valeur par défaut pour indiquer une erreur

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT COUNT(DISTINCT referrer) AS referrers_count
                FROM logs
                WHERE referrer IS NOT NULL
            '''
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0  # Aucune donnée trouvée
        except Error as e:
            print(f"Erreur lors de la récupération du nombre de référents : {e}")
            return -1  # Valeur par défaut pour indiquer une erreur
        finally:
            cursor.close()

    def fetch_not_found_count(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return -1  # Valeur par défaut pour indiquer une erreur

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT COUNT(*) AS not_found_count
                FROM logs
                WHERE status = 404
            '''
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0  # Aucune donnée trouvée
        except Error as e:
            print(f"Erreur lors de la récupération du nombre de demandes 'Not Found' : {e}")
            return -1  # Valeur par défaut pour indiquer une erreur
        finally:
            cursor.close()
    def fetch_static_files_count(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return -1  # Valeur par défaut pour indiquer une erreur

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT COUNT(*) AS static_files_count
                FROM logs
                WHERE url LIKE '%.css' OR url LIKE '%.js' OR url LIKE '%.jpg' OR url LIKE '%.png' OR url LIKE '%.gif'
            '''
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0  # Aucune donnée trouvée
        except Error as e:
            print(f"Erreur lors de la récupération du nombre de fichiers statiques : {e}")
            return -1  # Valeur par défaut pour indiquer une erreur
        finally:
            cursor.close()
    def fetch_log_size(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return -1  # Valeur par défaut pour indiquer une erreur

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT SUM(size) AS total_log_size
                FROM logs
            '''
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                total_size_bytes = result[0]
                total_size_mb = total_size_bytes / (1024 * 1024)  # Convertir en MiB
                return total_size_mb
            else:
                return 0, 0  # Aucune donnée trouvée
        except Error as e:
            print(f"Erreur lors de la récupération de la taille totale des logs : {e}")
            return -1, -1  # Valeur par défaut pour indiquer une erreur
        finally:
            cursor.close()

    def fetch_browsers_and_stats(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = '''
                SELECT 
                    user_agent,
                    COUNT(*) AS total_hits,
                    COUNT(DISTINCT ip) AS unique_visitors
                FROM 
                    logs
                GROUP BY 
                    user_agent
                ORDER BY 
                    total_hits DESC
            '''
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Erreur lors de la récupération des statistiques des navigateurs : {e}")
            return []
        finally:
            cursor.close()

    
    def fetch_time_distribution(self):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return []

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT 
                    date,
                    COUNT(*) AS hits,
                    COUNT(DISTINCT ip) AS visitors
                FROM 
                    logs
                GROUP BY 
                    date
                ORDER BY 
                    date

            '''
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Erreur lors de la récupération de la distribution dans le temps : {e}")
            return []
        finally:
            cursor.close()
    def fetch_top_referrers(self, limit=10):
        if not self.connection:
            print("Pas de connexion à la base de données")
            return []

        try:
            cursor = self.connection.cursor()
            query = '''
                SELECT 
                l.referrer, 
                COUNT(*) AS referrer_count,
                COUNT(DISTINCT l.ip) AS unique_visitors,
                COUNT(*) AS total_hits
                FROM 
                    logs l
                WHERE 
                    l.referrer IS NOT NULL
                GROUP BY 
                    l.referrer
                ORDER BY 
                referrer_count DESC
                LIMIT %s
            '''
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Erreur lors de la récupération des URL référentes : {e}")
            return []
        finally:
            cursor.close()


    


