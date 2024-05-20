import re
import mysql.connector
from datetime import datetime

# Définir le schéma du fichier journal pour les logs SSH
log_pattern = re.compile(r'(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<host>\w+)\s+(?P<process>sshd\[\d+\]):\s+(?P<message>.+)')

# Mois en chiffres pour conversion de date
months = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
    'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
    'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}

def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

def convert_date(month, day, time):
    year = datetime.now().year
    date_str = f"{year}-{months[month]:02d}-{int(day):02d} {time}"
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

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
        CREATE TABLE IF NOT EXISTS ssh_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATETIME,
            host VARCHAR(255),
            process VARCHAR(255),
            message TEXT,
            ip VARCHAR(15),
            port INT
        )
    ''')

    for idx, log in enumerate(parsed_logs):
        try:
            date = convert_date(log['month'], log['day'], log['time'])
            host = log['host']
            process = log['process']
            message = log['message']
            
            # Extraction de l'IP et du port depuis le message
            ip_port_match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+port\s+(\d+)', message)
            if ip_port_match:
                ip = ip_port_match.group(1)
                port = int(ip_port_match.group(2))
            else:
                ip = None
                port = None

            cursor.execute('''
                INSERT INTO ssh_logs (date, host, process, message, ip, port)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (date, host, process, message, ip, port))

            if (idx + 1) % 100 == 0:
                print(f"{idx + 1} logs insérés...")

        except Exception as e:
            print(f"Erreur lors de l'insertion du log: {log}")
            print(str(e))

    conn.commit()
    cursor.close()
    conn.close()
    print("Chargement terminé.")

if __name__ == "__main__":
    log_file_path = './Project wla/secure_log/var/log/secure-20220313'  # Chemin vers votre fichier de journal
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
