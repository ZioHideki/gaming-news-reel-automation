import json

# Opzione 1: Usare Rendervid (open-source, supporta cloud rendering)[citation:3][citation:7]
# Opzione 2: Usare Replicate (ha modelli video gratuiti)
# Opzione 3: Usare Pippit AI (free tier, interfaccia web)[citation:8]

def create_video_from_news():
    # Leggi le notizie raccolte
    with open("news_data.json", "r", encoding="utf-8") as f:
        news = json.load(f)
    
    # Costruisci script per il video
    script = "🎮 NOTIZIE GAMING DI OGGI 🎮\n\n"
    for i, article in enumerate(news[:3], 1):
        title = article.get("title", "Notizia senza titolo")
        script += f"{i}. {title}\n"
    
    script += "\n📱 Seguimi per altre notizie!"
    
    print("Script generato:")
    print(script)
    
    # Qui puoi chiamare un'API di generazione video cloud
    # Esempio con Rendervid (vedi documentazione)
    print("✅ Video generato (simulazione)")
    print("💡 Per la generazione video effettiva, usa Rendervid o Replicate")

if __name__ == "__main__":
    create_video_from_news()
