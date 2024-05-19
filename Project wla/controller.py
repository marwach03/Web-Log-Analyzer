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

# Fonction pour générer le graphique et renvoyer les données pour l'afficher dans le modèle HTML
def generate_plotVisitorsAndHits(db_config):
    dao = AccessDao(db_config)
    dao.connect()
    
    data = dao.fetch_unique_visitors_and_hits_per_day()
    dao.disconnect()

    if not data:
        print("Aucune donnée disponible pour le graphique.")
        return None, None

    dates = [entry['log_date'] for entry in data]
    unique_visitors = [entry['unique_visitors'] for entry in data]
    total_hits = [entry['total_hits'] for entry in data]

    # Création de la figure et des axes
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Plot pour les visiteurs uniques
    ax1.plot(dates, unique_visitors, marker='o', color='b', label='Unique Visitors')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Unique Visitors', color='b')

    # Créer un deuxième axe pour les hits totaux
    ax2 = ax1.twinx()
    ax2.plot(dates, total_hits, marker='s', color='r', label='Total Hits')
    ax2.set_ylabel('Total Hits', color='r')
    ax2.tick_params('y', colors='r')

    # Configuration du titre et de la légende
    plt.title('Unique Visitors and Total Hits Per Day')
    fig.tight_layout()
    fig.autofmt_xdate(rotation=45)
    fig.legend(loc='upper left')

    # Convertir le graphique en base64 pour l'afficher dans le modèle HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data = base64.b64encode(buffer.read()).decode()
    plt.close()

    return graph_data, dates



# Route pour afficher le graphique
@app.route('/')
def index():
    today, last_updated = get_current_datetime()
    db_config = {
        'user': 'root',
        'password': 'Ghitatagmouti2003',
        'database': 'webLog'
    }

    graph_data, dates = generate_plotVisitorsAndHits(db_config)
    if not graph_data:
        return "Aucune donnée disponible pour le graphique."

    return render_template('graph.html',today=today, graph_data=graph_data, dates=dates)
    

if __name__ == '__main__':
    app.run(debug=True)
