import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.scrapers.ebay_scraper import scrape_ebay
from src.scrapers.amazon_scraper import scrape_amazon
from src.notifications.discord_bot import send_discord_notification
import asyncio
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Price Scraper", layout="wide")

st.title("🛒 Intelligenter Preis-Scraper")
st.write("Finde die günstigsten Preise auf eBay, Amazon und Vinted")

# Eingabe
product_name = st.text_input("Produktname eingeben:", placeholder="z.B. iPhone 15")
discord_webhook = st.text_input("Discord Webhook URL (optional):", placeholder="https://discord.com/api/webhooks/...")

if st.button("Preise suchen") and product_name:
    with st.spinner("Durchsuche Shops..."):
        # Alle Scraper parallel ausführen
        ebay_results = scrape_ebay(product_name)
        amazon_results = scrape_amazon(product_name)
        # vinted_results = scrape_vinted(product_name)
        
        all_results = ebay_results + amazon_results  # + vinted_results
        
        if all_results:
            # Preis parsing und Sortierung
            for product in all_results:
                try:
                    # Preis bereinigen (einfache Implementierung)
                    price_text = product['price'].replace('€', '').replace(',', '.').split()[0]
                    product['price_clean'] = float(price_text)
                except:
                    product['price_clean'] = float('inf')
            
            # Nach Preis sortieren
            sorted_results = sorted(all_results, key=lambda x: x['price_clean'])
            cheapest = sorted_results[0]
            
            # Ergebnisse anzeigen
            st.success(f"Günstigstes Produkt gefunden: {cheapest['price']}")
            
            # Discord Notification
            if discord_webhook:
                asyncio.run(send_discord_notification(discord_webhook, cheapest))
                st.info("Discord Notification gesendet!")
            
            # Tabelle anzeigen
            df = pd.DataFrame(sorted_results)
            st.dataframe(df[['title', 'price', 'platform', 'link']])
            
            # Als CSV speichern
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Ergebnisse als CSV herunterladen",
                csv,
                f"preise_{product_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                "text/csv"
            )
        else:
            st.error("Keine Produkte gefunden")
