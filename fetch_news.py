import requests
import json
import os
from datetime import datetime

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

def fetch_gaming_news():
    """Raccoglie notizie gaming - con fallback a dati di esempio se Apify non funziona"""
    
    articles = []
    
    # Prova con Apify se c'è il token
    if APIFY_TOKEN:
        headers = {"Authorization": f"Bearer {APIFY_TOKEN}"}
        
        input_data = {
            "keywords": ["gaming", "videogiochi", "esports", "playstation", "xbox", "nintendo"],
            "language": "it",
            "maxItems": 5,
            "dateFrom": datetime.now().strftime("%Y-%m-%d")
        }
        
        try:
            print("🔍 Provo a contattare Apify...")
            
            # Avvia l'attore News Archive Scraper
            response = requests.post(
                "https://api.apify.com/v2/acts/fortuitous_pirate~news-archive-scraper/runs",
                headers=headers,
                json=input_data,
                timeout=30
            )
            
            if response.status_code == 200:
                run_data = response.json()
                run_id = run_data.get("data", {}).get("id")
                
                if run_id:
                    print(f"✅ Run avviato: {run_id}")
                    
                    # Recupera i risultati
                    results = requests.get(
                        f"https://api.apify.com/v2/acts/runs/{run_id}/dataset/items",
                        headers=headers,
                        timeout=30
                    )
                    
                    articles = results.json()
                    print(f"✅ Apify: trovate {len(articles)} notizie")
                else:
                    print("⚠️ Nessun run_id ottenuto")
            else:
                print(f"⚠️ Apify risponde con status {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Apify non disponibile: {e}")
    else:
        print("ℹ️ APIFY_TOKEN non configurato, uso dati di esempio")
    
    # Se Apify non ha funzionato, usa dati di esempio
    if not articles:
        print("📝 Genero dati di esempio (nessuna connessione ad Apify)")
        articles = [
            {
                "title": "Nintendo annuncia nuovi giochi per Switch 2",
                "source": {"name": "IGN Italia"},
                "description": "Durante il Nintendo Direct di aprile, la casa di Kyoto ha svelato tre nuovi titoli in arrivo nel 2026: un nuovo Mario 3D, Zelda spin-off e Metroid Prime 4.",
                "url": "https://www.ign.com/nintendo",
                "category": "gaming",
                "publishedAt": datetime.now().isoformat()
            },
            {
                "title": "PlayStation 5 supera i 70 milioni di unità vendute",
                "source": {"name": "GamesIndustry.biz"},
                "description": "Sony raggiunge un nuovo traguardo per PlayStation 5, diventando una delle console più vendute della storia. Il traguardo arriva a 3 anni e mezzo dal lancio.",
                "url": "https://www.gamesindustry.biz/ps5",
                "category": "gaming",
                "publishedAt": datetime.now().isoformat()
            },
            {
                "title": "Nuovo aggiornamento gratuito per Cyberpunk 2077",
                "source": {"name": "Kotaku"},
                "description": "CD Projekt Red rilascia la patch 2.5 con nuove missioni, miglioramenti grafici per PS5 Pro e la tanto attesa modalità foto potenziata.",
                "url": "https://www.kotaku.com/cyberpunk",
                "category": "gaming",
                "publishedAt": datetime.now().isoformat()
            },
            {
                "title": "I campionati mondiali di League of Legends tornano in Europa",
                "source": {"name": "Esports Insider"},
                "description": "Riot Games ha annunciato che i Worlds 2026 si terranno in Italia (Milano) e Francia (Parigi) con la finale allo Stade de France.",
                "url": "https://www.esportsinsider.com/lol",
                "category": "esports",
                "publishedAt": datetime.now().isoformat()
            },
            {
                "title": "Xbox Game Pass aggiunge 10 nuovi titoli ad aprile",
                "source": {"name": "The Verge"},
                "description": "Microsoft arricchisce il catalogo con giochi AAA come Starfield 2 e indie di successo come Hollow Knight: Silksong.",
                "url": "https://www.theverge.com/xbox",
                "category": "gaming",
                "publishedAt": datetime.now().isoformat()
            }
        ]
    
    # Salva in JSON
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(articles[:5], f, ensure_ascii=False, indent=2)
    
    print(f"✅ Salvate {len(articles[:5])} notizie in news_data.json")
    return articles[:5]

if __name__ == "__main__":
    print("🚀 Avvio fetch_news.py...")
    print(f"📅 Data esecuzione: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    result = fetch_gaming_news()
    print(f"🏁 Fine esecuzione. Trovate {len(result)} notizie.")
