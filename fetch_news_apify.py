import json
import os
from datetime import datetime, timedelta
from apify_client import ApifyClient

# Ottieni il token dai secrets di GitHub
APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

def fetch_gaming_news():
    """Raccoglie notizie gaming degli ultimi 7 giorni usando Google News FREE"""
    
    if not APIFY_TOKEN:
        print("❌ APIFY_TOKEN non configurato!")
        print("   Vai su Settings → Secrets and variables → Actions → New repository secret")
        return []
    
    # Calcola data di 7 giorni fa
    date_from = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    print(f"🔍 Cerco notizie gaming dal {date_from} ad oggi...")
    
    try:
        # Inizializza il client Apify
        client = ApifyClient(APIFY_TOKEN)
        
        # Configurazione per Google News FREE
        run_input = {
            "query": "videogiochi OR gaming OR PlayStation OR Xbox OR Nintendo OR \"PC gaming\" OR esports OR \"video games\"",
            "language": "it",
            "maxResults": 20,
            "dateFrom": date_from
        }
        
        print(f"📡 Avvio attore Google News FREE...")
        
        # Esegui l'attore
        run = client.actor("dlaf/google-news-free").call(run_input=run_input)
        
        # Recupera i risultati
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        
        print(f"✅ Trovate {len(items)} notizie da Google News")
        
        # Formatta i risultati in modo consistente
        formatted_articles = []
        for item in items[:5]:  # Prendi solo le prime 5
            formatted_articles.append({
                "title": item.get("title", ""),
                "description": item.get("snippet", item.get("description", "")),
                "source": {"name": item.get("source", {}).get("name", "Google News")},
                "url": item.get("link", item.get("url", "")),
                "publishedAt": item.get("publishedAt", datetime.now().isoformat()),
                "category": "gaming"
            })
        
        # Salva in JSON
        with open("news_data.json", "w", encoding="utf-8") as f:
            json.dump(formatted_articles, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Salvate {len(formatted_articles)} notizie in news_data.json")
        return formatted_articles
        
    except Exception as e:
        print(f"❌ Errore con Apify: {e}")
        print("📝 Uso dati di esempio come fallback...")
        return use_fallback_data()

def use_fallback_data():
    """Dati di esempio in caso di errore"""
    articles = [
        {
            "title": "Nintendo annuncia nuovi giochi per Switch 2",
            "source": {"name": "IGN Italia"},
            "description": "Durante il Nintendo Direct di aprile, la casa di Kyoto ha svelato tre nuovi titoli in arrivo nel 2026.",
            "url": "https://www.ign.com/nintendo",
            "category": "gaming",
            "publishedAt": datetime.now().isoformat()
        },
        {
            "title": "PlayStation 5 supera i 70 milioni di unità vendute",
            "source": {"name": "GamesIndustry.biz"},
            "description": "Sony raggiunge un nuovo traguardo per PlayStation 5, diventando una delle console più vendute della storia.",
            "url": "https://www.gamesindustry.biz/ps5",
            "category": "gaming",
            "publishedAt": datetime.now().isoformat()
        },
        {
            "title": "Nuovo aggiornamento gratuito per Cyberpunk 2077",
            "source": {"name": "Kotaku"},
            "description": "CD Projekt Red rilascia la patch 2.5 con nuove missioni e miglioramenti grafici.",
            "url": "https://www.kotaku.com/cyberpunk",
            "category": "gaming",
            "publishedAt": datetime.now().isoformat()
        }
    ]
    
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Salvate {len(articles)} notizie di esempio in news_data.json")
    return articles

if __name__ == "__main__":
    print("🚀 Avvio fetch_news_apify.py...")
    print(f"📅 Data esecuzione: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    result = fetch_gaming_news()
    print(f"🏁 Fine esecuzione. Trovate {len(result)} notizie.")
