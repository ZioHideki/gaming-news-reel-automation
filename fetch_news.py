import requests
import json
import os
import time
from datetime import datetime

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")

def fetch_gaming_news():
    """Raccoglie notizie gaming con attesa del completamento"""
    
    articles = []
    
    if APIFY_TOKEN:
        headers = {"Authorization": f"Bearer {APIFY_TOKEN}"}
        
        input_data = {
            "keywords": ["gaming", "videogiochi", "esports", "playstation", "xbox", "nintendo"],
            "language": "it",
            "maxItems": 5,
            "dateFrom": datetime.now().strftime("%Y-%m-%d")
        }
        
        try:
            print("🔍 Avvio run su Apify...")
            
            # 1. Avvia l'attore
            response = requests.post(
                "https://api.apify.com/v2/acts/fortuitous_pirate~news-archive-scraper/runs",
                headers=headers,
                json=input_data,
                timeout=30
            )
            
            print(f"📡 Status code: {response.status_code}")
            
            if response.status_code == 201:
                run_data = response.json()
                run_id = run_data.get("data", {}).get("id")
                
                if run_id:
                    print(f"✅ Run avviato con ID: {run_id}")
                    
                    # 2. Attendi il completamento
                    print("⏳ Attendiamo il completamento del run...")
                    max_attempts = 30  # massimo 30 tentativi
                    attempt = 0
                    run_status = "RUNNING"
                    
                    while run_status not in ["SUCCEEDED", "FAILED", "ABORTED"] and attempt < max_attempts:
                        time.sleep(5)  # aspetta 5 secondi
                        attempt += 1
                        
                        status_response = requests.get(
                            f"https://api.apify.com/v2/acts/runs/{run_id}",
                            headers=headers,
                            timeout=30
                        )
                        
                        if status_response.status_code == 200:
                            run_status = status_response.json().get("data", {}).get("status", "RUNNING")
                            print(f"   Tentativo {attempt}: stato = {run_status}")
                        else:
                            print(f"   ⚠️ Impossibile ottenere stato: {status_response.status_code}")
                            break
                    
                    # 3. Recupera i risultati se completato con successo
                    if run_status == "SUCCEEDED":
                        print("✅ Run completato! Recupero i risultati...")
                        results_response = requests.get(
                            f"https://api.apify.com/v2/acts/runs/{run_id}/dataset/items",
                            headers=headers,
                            timeout=30
                        )
                        
                        if results_response.status_code == 200:
                            articles = results_response.json()
                            print(f"✅ Apify: trovate {len(articles)} notizie")
                        else:
                            print(f"⚠️ Errore nel recupero risultati: {results_response.status_code}")
                    else:
                        print(f"⚠️ Run non completato con successo. Stato finale: {run_status}")
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
        print("📝 Genero dati di esempio (nessuna notizia da Apify)")
        articles = [
            {
                "title": "Nintendo annuncia nuovi giochi per Switch 2",
                "source": {"name": "IGN Italia"},
                "description": "Durante il Nintendo Direct di aprile, la casa di Kyoto ha svelato tre nuovi titoli in arrivo nel 2026: un nuovo Mario 3D, Zelda spin-off e Metroid Prime 4.",
                "url": "https://www.ign.com/nintendo",
                "category": "gaming"
            },
            {
                "title": "PlayStation 5 supera i 70 milioni di unità vendute",
                "source": {"name": "GamesIndustry.biz"},
                "description": "Sony raggiunge un nuovo traguardo per PlayStation 5, diventando una delle console più vendute della storia.",
                "url": "https://www.gamesindustry.biz/ps5",
                "category": "gaming"
            },
            {
                "title": "Nuovo aggiornamento gratuito per Cyberpunk 2077",
                "source": {"name": "Kotaku"},
                "description": "CD Projekt Red rilascia la patch 2.5 con nuove missioni, miglioramenti grafici per PS5 Pro e la tanto attesa modalità foto potenziata.",
                "url": "https://www.kotaku.com/cyberpunk",
                "category": "gaming"
            },
            {
                "title": "I campionati mondiali di League of Legends tornano in Europa",
                "source": {"name": "Esports Insider"},
                "description": "Riot Games ha annunciato che i Worlds 2026 si terranno in Italia (Milano) e Francia (Parigi).",
                "url": "https://www.esportsinsider.com/lol",
                "category": "esports"
            },
            {
                "title": "Xbox Game Pass aggiunge 10 nuovi titoli ad aprile",
                "source": {"name": "The Verge"},
                "description": "Microsoft arricchisce il catalogo con giochi AAA e indie di successo.",
                "url": "https://www.theverge.com/xbox",
                "category": "gaming"
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
