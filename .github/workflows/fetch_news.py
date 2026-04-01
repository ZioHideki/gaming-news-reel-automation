import requests
import json
import os
from datetime import datetime

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

def fetch_gaming_news():
    """Chiamata API ad Apify per raccogliere notizie gaming"""
    
    # Avvia l'attore News Archive Scraper via API
    headers = {"Authorization": f"Bearer {APIFY_TOKEN}"}
    
    input_data = {
        "keywords": ["gaming", "videogiochi"],
        "language": "it",
        "maxItems": 5,
        "dateFrom": datetime.now().strftime("%Y-%m-%d")
    }
    
    response = requests.post(
        "https://api.apify.com/v2/acts/fortuitous_pirate~news-archive-scraper/runs",
        headers=headers,
        json=input_data
    )
    
    run_id = response.json()["data"]["id"]
    
    # Recupera i risultati
    results = requests.get(
        f"https://api.apify.com/v2/acts/runs/{run_id}/dataset/items",
        headers=headers
    )
    
    articles = results.json()
    
    # Salva in file JSON per il passaggio successivo
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(articles[:5], f, ensure_ascii=False, indent=2)
    
    print(f"✅ Raccolte {len(articles[:5])} notizie")
    return articles[:5]

if __name__ == "__main__":
    fetch_gaming_news()
