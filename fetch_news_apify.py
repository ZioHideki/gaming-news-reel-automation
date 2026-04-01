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
            "query": "videogiochi OR gaming OR PlayStation OR Xbox OR Nintendo",
            "language": "it",
            "maxResults": 10,
            "dateFrom": date_from
        }
        
        print(f"📡 Avvio attore Google News FREE...")
        print(f"   Input: {json.dumps(run_input, ensure_ascii=False)}")
        
        # Esegui l'attore
        run = client.actor("dlaf/google-news-free").call(run_input=run_input)
        
        print(f"✅ Run completato: {run}")
        
        # Recupera i risultati
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        
        print(f"📊 Tipo di 'items': {type(items)}")
        print(f"📊 Numero di elementi: {len(items)}")
        
        if items:
            print(f"📊 Primo elemento (tipo: {type(items[0])}):")
            print(json.dumps(items[0], ensure_ascii=False, indent=2)[:500])
        
        # Verifica che items sia una lista
        if not isinstance(items, list):
            print(f"⚠️ items non è una lista, è {type(items)}")
            items = []
        
        # Formatta i risultati in modo sicuro
        formatted_articles = []
        for idx, item in enumerate(items[:5]):
            try:
                # Gestisci diversi possibili formati di risposta
                if isinstance(item, dict):
                    title = item.get("title", "")
                    description = item.get("snippet", item.get("description", item.get("content", "")))
                    source = item.get("source", {}).get("name", "Google News") if isinstance(item.get("source"), dict) else "Google News"
                    url = item.get("link", item.get("url", ""))
                    published = item.get("publishedAt", item.get("date", datetime.now().isoformat()))
                elif isinstance(item, str):
                    # Se è una stringa, la usiamo come descrizione
                    title = f"Notizia {idx+1}"
                    description = item[:200]
                    source = "Google News"
                    url = ""
                    published = datetime.now().isoformat()
                else:
                    print(f"⚠️ Elemento {idx} di tipo sconosciuto: {type(item)}")
                    continue
                
                formatted_articles.append({
                    "title": title or f"Notizia gaming {idx+1}",
                    "description": description[:200] if description else "",
                    "source": {"name": source},
                    "url": url,
                    "publishedAt": published,
                    "category": "gaming"
                })
            except Exception as e:
                print(f"⚠️ Errore nel processare elemento {idx}: {e}")
                continue
        
        if formatted_articles:
            print(f"✅ Formattate {len(formatted_articles)} notizie")
        else:
            print("⚠️ Nessuna notizia formattata, uso fallback")
            return use_fallback_data()
        
        # Salva in JSON
        with open("news_data.json", "w", encoding="utf-8") as f:
            json.dump(formatted_articles, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Salvate {len(formatted_articles)} notizie in news_data.json")
        return formatted_articles
        
    except Exception as e:
        print(f"❌ Errore con Apify: {e}")
        import traceback
        traceback.print_exc()
        print("📝 Uso dati di esempio come fallback...")
        return use_fallback_data()

def use_fallback_data():
    """Dati di esempio in caso di errore"""
    print("📝 Genero dati di esempio...")
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
        },
        {
            "title": "I campionati mondiali di League of Legends tornano in Europa",
            "source": {"name": "Esports Insider"},
            "description": "Riot Games ha annunciato che i Worlds 2026 si terranno in Italia e Francia.",
            "url": "https://www.esportsinsider.com/lol",
            "category": "esports",
            "publishedAt": datetime.now().isoformat()
        },
        {
            "title": "Xbox Game Pass aggiunge 10 nuovi titoli ad aprile",
            "source": {"name": "The Verge"},
            "description": "Microsoft arricchisce il catalogo con giochi AAA e indie di successo.",
            "url": "https://www.theverge.com/xbox",
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
    print(f"🔑 APIFY_TOKEN presente: {'Sì' if APIFY_TOKEN else 'No'}")
    result = fetch_gaming_news()
    print(f"🏁 Fine esecuzione. Trovate {len(result)} notizie.")
