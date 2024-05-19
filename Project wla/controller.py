from flask import Flask, render_template
from dal import AccessDao
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)

def get_current_datetime():
    now = datetime.now()
    date_str = now.strftime("%d/%b/%Y")
    datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_str, datetime_str
def generate_plotReferrerUrls(db_config):
    dao = AccessDao(db_config)
    dao.connect()
    
    referrers = dao.fetch_top_referrers()
    data = dao.fetch_unique_visitors_and_hits_per_day()  # Récupérer les données des visiteurs uniques et des hits
    dao.disconnect()

    if not referrers:
        print("Aucune donnée disponible pour le graphe des URL référentes.")
        return None, None

    urls = [referrer[0] for referrer in referrers]
    counts = [referrer[1] for referrer in referrers]

    plt.figure(figsize=(7,3))
    plt.barh(urls, counts, color='skyblue')
    plt.xlabel('Nombre de fois')
    plt.ylabel('URL référente')
    plt.title('Top URL référentes')
    plt.gca().invert_yaxis()  # Inverser l'ordre pour afficher les plus fréquentes en haut
    
    # Ajouter les annotations pour les visiteurs uniques et les hits
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
        print("Aucune donnee disponible pour le graphique.")
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

    plt.figure(figsize=(7, 3))

    # Tracer les visiteurs en bleu
    plt.plot(dates, visitors, marker='o', color='b', label='Visiteurs')

    # Tracer les hits en rouge
    plt.plot(dates, hits, marker='s', color='r', label='Hits')

    plt.xlabel('Date')
    plt.ylabel('Nombre')
    plt.title('Distribution dans le temps')
    plt.xticks(rotation=45)
    plt.legend()  # Ajouter une légende pour distinguer les deux séries
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
        'password': 'ikramBelhaj2003@',
        'database': 'webLog'
    }

    # Récupération des statistiques
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

    # Génération des graphiques
    graph_data, dates = generate_plotVisitorsAndHits(db_config)
    graph_data_time_distribution = generate_plot_time_distribution(db_config)
    graph_url_refences = generate_plotReferrerUrls(db_config)
    if not graph_data or  not graph_data_time_distribution:
        return "Aucune donnée disponible pour le graphique."

    return render_template('graph.html', graph_data=graph_data, dates=dates,
                           graph_data_time_distribution=graph_data_time_distribution,
                           total_requests=total_requests, valid_requests=valid_requests,
                           failed_requests=failed_requests, log_parsing_time=log_parsing_time,
                           unique_visitors_count=unique_visitors_count, 
                           requested_files_count=requested_files_count,
                           referrers_count=referrers_count, not_found_count=not_found_count,
                           static_files_count=static_files_count, log_size=log_size,graph_url_refences=graph_url_refences)


if __name__ == '__main__':
    app.run(debug=True)
