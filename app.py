
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Analiza aukcji Troostwijk", layout="wide")

st.title("📦 Analizator aukcji - Troostwijk (MVP)")
st.markdown("Wklej link do aukcji z [troostwijkauctions.com](https://www.troostwijkauctions.com)")

url = st.text_input("Link do aukcji")

def parse_troostwijk(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.find("h1").get_text(strip=True)
        location = soup.find("div", class_="auction-location").get_text(strip=True) if soup.find("div", class_="auction-location") else "-"
        img = soup.find("img", class_="swiper-lazy")["src"] if soup.find("img", class_="swiper-lazy") else ""
        return {
            "Tytuł": title,
            "Lokalizacja": location,
            "Zdjęcie": img,
            "Link": url
        }
    except Exception as e:
        return {"Tytuł": "Błąd: " + str(e), "Lokalizacja": "-", "Zdjęcie": "", "Link": url}

if url:
    data = parse_troostwijk(url)
    st.subheader("📄 Wyniki analizy")
    st.write(f"**Tytuł:** {data['Tytuł']}")
    st.write(f"**Lokalizacja:** {data['Lokalizacja']}")
    st.image(data["Zdjęcie"], width=300)
    st.write(f"[Przejdź do aukcji]({data['Link']})")
