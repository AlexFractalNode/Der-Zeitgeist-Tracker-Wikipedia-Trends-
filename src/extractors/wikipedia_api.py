import requests
import pandas as pd
from datetime import datetime, timedelta

def get_wikipedia_data(article, days=30, language="de.wikipedia.org"):
    """Holt die Wikipedia-Aufrufzahlen und gibt ein Pandas DataFrame zurück."""
    print(f"📡 Lade Daten für: {article}...")
    
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    start_str = start_date.strftime('%Y%m%d')
    end_str = end_date.strftime('%Y%m%d')

    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{language}/all-access/all-agents/{article}/daily/{start_str}/{end_str}"

    # WICHTIG: Passe die E-Mail hier an!
    headers = {
        "User-Agent": "ZeitgeistBot_StudentProject/1.0 (lewiv59587@amiralty.com)"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Fehler: API antwortet mit Status {response.status_code}")
        return None

    data = response.json()
    df = pd.DataFrame(data['items'])
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H')
    df = df[['timestamp', 'views']]
    df.columns = ['Datum', 'Aufrufe']
    df.set_index('Datum', inplace=True)

    return df
