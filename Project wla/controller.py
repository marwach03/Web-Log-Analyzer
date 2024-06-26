import matplotlib
matplotlib.use('Agg')  # Utiliser le backend non interactif
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dal import UserDao, AccessDao, SSHLogDAO  # Assuming dal.py contains the AccessDao class for database access
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = 'OOZIE09'  # Vous pouvez utiliser os.urandom(24) pour générer une clé aléatoire

# Configuration de la base de données
db_config = {
    'user': 'root',
    'password': 'Ghitatagmouti2003',
    'database': 'webLog'
}

user_dao = UserDao(db_config)

def get_current_datetime():
    now = datetime.now()
    date_str = now.strftime("%d/%b/%Y")
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_str, datetime_str
def generate_plot_requested_files(db_config):
    dao = AccessDao(db_config)
    dao.connect()
    
    data = dao.fetch_requested_files()
    dao.disconnect()

    if not data:
        print("Aucune donnée disponible pour le graphique.")
        return None, None

    requests = [entry['request'] for entry in data]
    hits = [entry['hits'] for entry in data]
    visitors = [entry['visitors'] for entry in data]

    fig, ax1 = plt.subplots(figsize=(10, 7))

    # Largeur des barres
    bar_width = 0.35

    # Positions des barres pour les visiteurs et les hits
    bar_positions_visitors = np.arange(len(requests))
    bar_positions_hits = bar_positions_visitors + bar_width

    # Barres pour les visiteurs
    ax1.bar(bar_positions_visitors, visitors, bar_width, color='b', label='Visitors')
    ax1.set_xlabel('Requested Files (URLs)')
    ax1.set_ylabel('Visitors', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.set_xticks(bar_positions_visitors + bar_width / 2)
    ax1.set_xticklabels(requests, rotation=90)

    # Création d'un deuxième axe y partageant le même axe x
    ax2 = ax1.twinx()
    ax2.bar(bar_positions_hits, hits, bar_width, color='r', label='Hits')
    ax2.set_ylabel('Hits', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # Ajout de la légende
    fig.legend(loc='upper left')

    plt.title('Top Requested Files (URLs) Sorted by Hits and Visitors')

    # Ajustement automatique des marges
    fig.tight_layout()

    # Sauvegarde du graphique dans un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data, requests

def generate_plot_http_status_codes_by_category(db_config):
    dao = AccessDao(db_config)
    dao.connect()
    
    data = dao.fetch_http_status_codes_by_category()
    dao.disconnect()

    if not data:
        print("Aucune donnée disponible pour le graphique des codes de statut HTTP.")
        return None, None

    categories = [entry['category'] for entry in data]
    hits = [entry['hits'] for entry in data]
    visitors = [entry['visitors'] for entry in data]

    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Largeur des barres
    bar_width = 0.35

    # Positions des barres pour les hits
    bar_positions_hits = np.arange(len(categories))

    # Barres pour les hits (en rouge)
    ax1.bar(bar_positions_hits, hits, bar_width, color='r', label='Hits')
    ax1.set_xlabel('Catégorie de code de statut HTTP')
    ax1.set_ylabel('Nombre de hits', color='r')
    ax1.tick_params(axis='y', labelcolor='r')

    # Création d'un deuxième axe y pour les visiteurs
    ax2 = ax1.twinx()
    ax2.bar(bar_positions_hits + bar_width, visitors, bar_width, color='b', label='Visitors')
    ax2.set_ylabel('Nombre de visiteurs', color='b')
    ax2.tick_params(axis='y', labelcolor='b')

    # Ajout de la légende
    fig.legend(loc='upper right')

    plt.title('Répartition des codes de statut HTTP par catégorie')

    # Ajout des graduations en bas
    plt.xticks(bar_positions_hits + bar_width / 2, categories)

    # Ajustement automatique des marges
    fig.tight_layout()

    # Sauvegarde du graphique dans un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data, categories



def generate_plot_static_requests(db_config):
    dao = AccessDao(db_config)
    dao.connect()
    
    data = dao.fetch_top_static_requests()
    dao.disconnect()

    if not data:
        print("Aucune donnée disponible pour le graphique.")
        return None, None

    requests = [entry['request'] for entry in data]
    hits = [entry['hits'] for entry in data]
    visitors = [entry['visitors'] for entry in data]

    fig, ax1 = plt.subplots(figsize=(10, 7))

    # Largeur des barres
    bar_width = 0.35

    # Positions des barres pour les visiteurs et les hits
    bar_positions_visitors = np.arange(len(requests))
    bar_positions_hits = bar_positions_visitors + bar_width

    # Barres pour les visiteurs
    ax1.bar(bar_positions_visitors, visitors, bar_width, color='b', label='Visitors')
    ax1.set_xlabel('Request')
    ax1.set_ylabel('Visitors', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.set_xticks(bar_positions_visitors + bar_width / 2)
    ax1.set_xticklabels(requests, rotation=90)

    # Création d'un deuxième axe y partageant le même axe x
    ax2 = ax1.twinx()
    ax2.bar(bar_positions_hits, hits, bar_width, color='r', label='Hits')
    ax2.set_ylabel('Hits', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # Ajout de la légende
    fig.legend(loc='upper left')

    plt.title('Top Static Requests Sorted by Hits and Visitors')

    # Ajustement automatique des marges
    fig.tight_layout()

    # Sauvegarde du graphique dans un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data, requests

def generate_plotReferrerUrls(db_config):
    dao = AccessDao(db_config)
    dao.connect()
    
    referrers = dao.fetch_top_referrers()
    data = dao.fetch_unique_visitors_and_hits_per_day()
    dao.disconnect()

    if not referrers:
        print("Aucune donnée disponible pour le graphe des URL référentes.")
        return None, None

    urls = [referrer[0] for referrer in referrers]
    counts = [referrer[1] for referrer in referrers]

    plt.figure(figsize=(10, 5))
    plt.barh(urls, counts, color='skyblue')
    plt.xlabel('Nombre de fois')
    plt.ylabel('URL référente')
    plt.title('Top URL référentes')
    plt.gca().invert_yaxis()

    for entry, url in zip(data, urls):
        unique_visitors = entry['unique_visitors']
        total_hits = entry['total_hits']
        plt.text(total_hits, url, f"Visitors: {unique_visitors}\nHits: {total_hits}", va='center')

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data, urls

def generate_plotVisitorsAndHits(db_config):
    dao = AccessDao(db_config)
    dao.connect()
    
    data = dao.fetch_unique_visitors_and_hits_per_day()
    dao.disconnect()

    if not data:
        print("Aucune donnée disponible pour le graphique des visiteurs et hits.")
        return None, None

    dates = [entry['log_date'] for entry in data]
    unique_visitors = [entry['unique_visitors'] for entry in data]
    total_hits = [entry['total_hits'] for entry in data]

    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(dates, unique_visitors, marker='o', color='b', label='Unique Visitors')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Unique Visitors', color='b')

    ax2 = ax1.twinx()
    ax2.plot(dates, total_hits, marker='s', color='r', label='Total Hits')
    ax2.set_ylabel('Total Hits', color='r')
    ax2.tick_params('y', colors='r')

    plt.title('Unique Visitors and Total Hits Per Day')
    fig.tight_layout()
    fig.autofmt_xdate(rotation=45)
    fig.legend(loc='upper left')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data, dates

def generate_plotBrowsers(db_config):
    dao = AccessDao(db_config)
    dao.connect()
    
    data = dao.fetch_browsers_and_stats()
    dao.disconnect()

    if not data:
        print("Aucune donnée disponible pour le graphique des navigateurs.")
        return None, None

    user_agents = [entry['user_agent'] for entry in data]
    total_hits = [entry['total_hits'] for entry in data]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.barh(user_agents, total_hits, color='c')
    ax.set_xlabel('Total Hits')
    ax.set_ylabel('User Agent')
    ax.set_title('Total Hits by Browser/User Agent')
    fig.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data, user_agents

def generate_plot_time_distribution(db_config):
    dao = AccessDao(db_config)
    dao.connect()
    
    data = dao.fetch_time_distribution()
    dao.disconnect()

    if not data:
        print("Aucune donnée disponible pour le graphique de distribution dans le temps.")
        return None

    dates = [entry[0] for entry in data]
    visitors = [entry[1] for entry in data]
    hits = [entry[2] for entry in data]

    plt.figure(figsize=(10, 5))

    plt.plot(dates, visitors, marker='o', color='b', label='Visiteurs')
    plt.plot(dates, hits, marker='s', color='r', label='Hits')

    plt.xlabel('Date')
    plt.ylabel('Nombre')
    plt.title('Distribution dans le temps')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data

def generate_plot_not_found_urls(db_config):
    dao = AccessDao(db_config)
    dao.connect()
    not_found_data = dao.fetch_not_found_data()
    dao.disconnect()
    if not not_found_data:
        print("Aucune donnée disponible pour les URLs non trouvées.")
        return None, None

    urls = [entry['url'] for entry in not_found_data]
    hits = [entry['hits'] for entry in not_found_data]

    plt.figure(figsize=(8, 6))
    plt.bar(urls, hits, color='blue')
    plt.xlabel('URLs')
    plt.ylabel('Nombre de Hits')
    plt.title('Top URLs Non Trouvées')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data_not_found = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data_not_found

def generate_plot_operating_systems(db_config):
    dao = AccessDao(db_config)
    dao.connect()
    
    data = dao.fetch_operating_systems_stats()
    dao.disconnect()

    if not data:
        print("Aucune donnée disponible pour le graphique des systèmes d'exploitation.")
        return None, None

    operating_systems = [entry['operating_system'] for entry in data]
    hits = [entry['hits'] for entry in data]
    visitors = [entry['visitors'] for entry in data]

    fig, ax1 = plt.subplots(figsize=(10, 7))

    ax1.bar(operating_systems, visitors, color='b', label='Visitors')
    ax1.set_xlabel('Operating System')
    ax1.set_ylabel('Visitors', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.set_xticklabels(operating_systems, rotation=90)

    ax2 = ax1.twinx()
    ax2.bar(operating_systems, hits, color='r', label='Hits')
    ax2.set_ylabel('Hits', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    plt.title('Hits et Visitors par Système d\'Exploitation')
    fig.tight_layout()
    fig.legend(loc='upper left')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data, operating_systems

def generate_plot_failed_login_attempts(db_config):
    ssh_log_dao = SSHLogDAO(db_config)
    results = ssh_log_dao.get_failed_login_attempts_by_date()

    if not results:
        print("Aucune donnée disponible pour le graphique des tentatives de connexion échouées.")
        return None

    dates = [result[0] for result in results]
    failed_attempts = [result[1] for result in results]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, failed_attempts, marker='o', color='r')
    plt.xlabel('Date')
    plt.ylabel('Nombre de tentatives échouées')
    plt.title('Tentatives de connexion échouées par date')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data
######################3
def generate_plot_failed_login_attempts_per_Hour(db_config):
    ssh_log_dao = SSHLogDAO(db_config)
    results = ssh_log_dao.get_failed_login_attempts_by_Hour()

    if not results:
        print("Aucune donnée disponible pour le graphique des tentatives de connexion échouées.")
        return None

    # Extraction des dates et des tentatives échouées à partir des résultats
    dates = [result[0] for result in results]
    failed_attempts = [result[1] for result in results]

    # Tracé des données
    plt.figure(figsize=(10, 5))
    plt.plot(dates, failed_attempts, marker='o', color='r')
    plt.xlabel('Heure')
    plt.ylabel('Nombre de tentatives échouées')
    plt.title('Tentatives de connexion échouées par Heure')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Conversion du graphique en format base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data
def generate_plot_failed_login_attempts_per_Mounth(db_config):
    ssh_log_dao = SSHLogDAO(db_config)
    results = ssh_log_dao.get_failed_login_attempts_by_Mounth()

    if not results:
        print("Aucune donnée disponible pour le graphique des tentatives de connexion échouées.")
        return None

    # Extraction des dates et des tentatives échouées à partir des résultats
    dates = [result[0] for result in results]
    failed_attempts = [result[1] for result in results]

    # Tracé des données
    plt.figure(figsize=(10, 5))
    plt.plot(dates, failed_attempts, marker='o', color='r')
    plt.xlabel('Mois')
    plt.ylabel('Nombre de tentatives échouées')
    plt.title('Tentatives de connexion échouées par Mois')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Conversion du graphique en format base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data


def generate_plot_ip_exceeding_connections(db_config):
    ssh_log_dao = SSHLogDAO(db_config)
    ssh_log_dao.connect()
    
    results = ssh_log_dao.get_ips_exceeding_max_connections()
    
    if not results:
        print("Aucune donnée disponible pour le graphique des IPs dépassant le nombre maximum de connexions.")
        return None

    ips = []
    connection_attempts = []

    for result in results:
        if 'ip' in result and 'connection_attempts' in result:
            ips.append(result['ip'])
            connection_attempts.append(int(result['connection_attempts']))
        else:
            print("Clés ou valeurs manquantes dans les résultats.")
            return None

    # Tracé du graphique
    plt.figure(figsize=(10, 5))
    plt.bar(ips, connection_attempts, color='b')
    plt.xlabel('IP')
    plt.ylabel('Nombre de tentatives de connexion')
    plt.title('IPs dépassant 350 tentatives de connexion')
    plt.xticks(rotation=90)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data

def generate_plot_failed_login_attempts_by_ip(db_config):
    ssh_log_dao = SSHLogDAO(db_config)
    results = ssh_log_dao.get_failed_login_attempts_by_ip()

    if not results:
        print("Aucune donnée disponible pour le graphique des tentatives de connexion échouées par IP.")
        return None

    # Dictionnaire pour stocker les groupes d'adresses IP
    ip_groups = {}
    for ip, attempts in results:
        ip_first_part = ip.split('.')[0]  # Première partie de l'adresse IP
        if ip_first_part not in ip_groups:
            ip_groups[ip_first_part] = attempts  # Crée un nouveau groupe avec la première tentative
        else:
            ip_groups[ip_first_part] += attempts  # Ajoute le nombre de tentatives au groupe existant

    # Sélectionner seulement la moitié des adresses IP disponibles
    selected_ips = dict(list(ip_groups.items())[:len(ip_groups) // 2])

    ip_addresses = list(selected_ips.keys())  # Liste des premières parties des adresses IP
    failed_attempts = list(selected_ips.values())  # Liste du nombre total de tentatives échouées pour chaque groupe

    plt.figure(figsize=(10, 5))
    plt.bar(ip_addresses, failed_attempts, color='r')
    plt.xlabel('Adresse IP (1ère partie)')
    plt.ylabel('Nombre de tentatives échouées')
    plt.title('Tentatives de connexion échouées par groupe d\'adresse IP')
    plt.xticks(rotation=90)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data


@app.route('/')
def index():
    db_config = {
        'user': 'root',
        'password': 'Ghitatagmouti2003',
        'database': 'webLog'
    }

    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    dao = AccessDao(db_config)
    dao.connect()
    total_requests = dao.fetch_total_requests()
    valid_requests = dao.fetch_valid_requests()
    failed_requests = dao.fetch_failed_requests()
    log_parsing_time = dao.fetch_log_parsing_time()
    unique_visitors_count = dao.fetch_unique_visitors_count()
    requested_files_count = dao.fetch_requested_files_count()
    referrers_count = dao.fetch_referrers_count()
    not_found_count = dao.fetch_not_found_count()
    static_files_count = dao.fetch_static_files_count()
    log_size = dao.fetch_log_size()
    dao.disconnect()

    graph_data, dates = generate_plotVisitorsAndHits(db_config)
    graph_data_time_distribution = generate_plot_time_distribution(db_config)
    graph_url_refences, urls = generate_plotReferrerUrls(db_config)
    graph_data_static_requests, requests = generate_plot_static_requests(db_config)
    graph_data_not_found = generate_plot_not_found_urls(db_config)
    requested_files_graph_data, requested_files = generate_plot_requested_files(db_config)
    graph_data_operating_systems, operating_systems = generate_plot_operating_systems(db_config)
    graph_data_http_status_codes_by_category, status_codes_by_category = generate_plot_http_status_codes_by_category(db_config)
    graph_data_failed_login_attempts = generate_plot_failed_login_attempts(db_config)
    graph_data_failed_login_attempts_perHour = generate_plot_failed_login_attempts_per_Hour(db_config)
    graph_data_failed_login_attempts_perMounth = generate_plot_failed_login_attempts_per_Mounth(db_config)
    graph_data_ip_exceeding_connections=generate_plot_ip_exceeding_connections(db_config)
    graph_data_failed_login_attemptsIP = generate_plot_failed_login_attempts_by_ip(db_config)
    
    if not graph_data or not graph_data_time_distribution or not graph_data_static_requests or not graph_url_refences or not graph_data_http_status_codes_by_category or not graph_data_ip_exceeding_connections or not graph_data_failed_login_attemptsIP:
        return "Aucune donnée disponible pour le graphique."

    return render_template('graph.html', graph_data=graph_data, dates=dates,
                           graph_data_static_requests=graph_data_static_requests,
                           requests=requests, graph_data_time_distribution=graph_data_time_distribution,
                           graph_url_refences=graph_url_refences, urls=urls,graph_data_not_found=graph_data_not_found,
                           total_requests=total_requests, valid_requests=valid_requests,
                           failed_requests=failed_requests, log_parsing_time=log_parsing_time,
                           graph_data_http_status_codes_by_category=graph_data_http_status_codes_by_category,
                           status_codes_by_category=status_codes_by_category,
                           graph_data_failed_login_attempts=graph_data_failed_login_attempts,
                           graph_data_failed_login_attempts_perHour = graph_data_failed_login_attempts_perHour,
                           graph_data_failed_login_attemptsIP=graph_data_failed_login_attemptsIP,
                           graph_data_failed_login_attempts_perMounth = graph_data_failed_login_attempts_perMounth,
                           unique_visitors_count=unique_visitors_count, 
                           requested_files_count=requested_files_count,
                            graph_data_ip_exceeding_connections=graph_data_ip_exceeding_connections,
                           referrers_count=referrers_count, not_found_count=not_found_count,
                           static_files_count=static_files_count, log_size=log_size,
                            requested_files_graph_data=requested_files_graph_data,
                            requested_files = requested_files, graph_data_operating_systems=graph_data_operating_systems, 
                            operating_systems=operating_systems)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = user_dao.get_user_by_email(email)
        if user and user[2] == password:  # Assurez-vous que le mot de passe est vérifié correctement
            session['logged_in'] = True
            session['email'] = email
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html')

    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if user_dao.get_user_by_email(email):
            flash('Email already exists, please choose another one.')
        else:
            user_dao.insert_user(email, password)
            flash('Registration successful, you can now log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)