import requests
import json
import os
from datetime import datetime

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

def fetch_gaming_news():
    """Versione semplificata per test"""
    
    if not APIFY_TOKEN:
        print("❌ APIFY_TOKEN non trovato! Aggiungi il secret nel repository.")
        print("   Vai su Settings → Secrets and variables → Actions → New repository secret")
        return []
    
    headers = {"Authorization": f"Bearer {APIFY_TOKEN}"}
    
    input_data = {
        "keywords": ["gaming", "videogiochi"],
        "language": "it",
        "maxItems": 3,
        "dateFrom": datetime.now().strftime("%Y-%m-%d")
    }
    
    print(f"🔍 Invio richiesta ad Apify con input: {input_data}")
    
    try:
        # Avvia l'attore
        response = requests.post(
            "https://api.apify.com/v2/acts/fortuitous_pirate~news-archive-scraper/runs",
            headers=headers,
            json=input_data,
            timeout=30
        )
        
        print(f"📡 Status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Errore API: {response.text}")
            return []
        
        run_data = response.json()
        run_id = run_data.get("data", {}).get("id")
        
        if not run_id:
            print("❌ Nessun run_id ottenuto")
            return []
        
        print(f"✅ Run avviato: {run_id}")
        
        # Recupera i risultati
        results = requests.get(
            f"https://api.apify.com/v2/acts/runs/{run_id}/dataset/items",
            headers=headers,
            timeout=30
        )
        
        articles = results.json()
        
        # Salva in JSON
        with open("news_data.json", "w", encoding="utf-8") as f:
            json.dump(articles[:5], f, ensure_ascii=False, indent=2)
        
        print(f"✅ Salvate {len(articles[:5])} notizie in news_data.json")
        return articles[:5]
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    print("🚀 Avvio fetch_news.py...")
    result = fetch_gaming_news()
    print(f"🏁 Fine esecuzione. Trovate {len(result)} notizie.")
