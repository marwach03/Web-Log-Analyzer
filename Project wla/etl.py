import re
import mysql.connector
from datetime import datetime

# Définir le schéma du fichier journal
log_pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<date>[\w:/]+)\s[+\-]\d{4}\] "(?P<method>\w+)\s(?P<url>[^\s]+)\s(?P<protocol>[^\s]+)"\s(?P<status>\d+)\s(?P<size>\d+)\s"(?P<referrer>[^\s]*)"\s"(?P<user_agent>[^"]+)"')

def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

def convert_date(date_str):
    return datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

def extract(file_path):
    print("Extraction des logs depuis le fichier:", file_path)
    with open(file_path, 'r') as file:
        logs = file.readlines()
    print(f"{len(logs)} lignes extraites.")
    return logs

def transform(logs):
    print("Transformation des logs...")
    parsed_logs = [parse_log_line(log) for log in logs]
    valid_logs = [log for log in parsed_logs if log is not None]
    print(f"{len(valid_logs)} logs valides extraits.")
    return valid_logs

def load(parsed_logs, db_config):
    print("Chargement des logs dans la base de données...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Créer la table si elle n'existe pas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ip VARCHAR(15),
            date DATETIME,
            method VARCHAR(10),
            url TEXT,
            protocol VARCHAR(10),
            status INT,
            size INT,
            referrer TEXT,
            user_agent TEXT
        )
    ''')

    for idx, log in enumerate(parsed_logs):
        # Assurez-vous que les données ne dépassent pas les longueurs de colonne et convertissez la date
        try:
            ip = log['ip'][:15]
            date = convert_date(log['date'])
            method = log['method'][:10]
            url = log['url']
            protocol = log['protocol'][:10]
            status = int(log['status'])
            size = int(log['size'])
            referrer = log['referrer']
            user_agent = log['user_agent']

            cursor.execute('''
                INSERT INTO logs (ip, date, method, url, protocol, status, size, referrer, user_agent)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (ip, date, method, url, protocol, status, size, referrer, user_agent))

            if (idx + 1) % 1000 == 0:
                print(f"{idx + 1} logs insérés...")

        except Exception as e:
            print(f"Erreur lors de l'insertion du log: {log}")
            print(str(e))

    conn.commit()
    cursor.close()
    conn.close()
    print("Chargement terminé.")

if __name__ == "__main__":
    log_file_path = './apache/var/log/httpd/access_log'  # Chemin vers votre fichier de journal
    db_config = {
        'user': 'root',
        'password': 'marwachaoui2003@',
        'database': 'webLog'
    }

    # ETL Process
    logs = extract(log_file_path)
    parsed_logs = transform(logs)
    load(parsed_logs, db_config)

    print('Les journaux transformés ont été enregistrés dans la base de données.')
