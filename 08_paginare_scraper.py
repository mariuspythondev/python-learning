import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('citate_fiverr.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS citate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    citat TEXT NOT NULL,
    autor TEXT NOT NULL)
""")
for numar_pagina in range(1, 4):
    url = f"https://quotes.toscrape.com/page/{numar_pagina}/"
    print(f"Scriem pagina {numar_pagina}: {url}...")

    raspuns = requests.get(url)
    if raspuns.status_code == 200:
        soup = BeautifulSoup(raspuns.text, 'html.parser')
        blocuri_citate = soup.find_all("div", class_="quote")

        for bloc in blocuri_citate:
            citat = bloc.find("span", class_="text").text
            autor = bloc.find("small", class_="author").text

            cursor.execute("INSERT INTO citate (citat, autor) VALUES (?, ?)", (citat, autor))
    else:
        print(f"Eroare la pagina {numar_pagina}")
conn.commit()
conn.close()
print("Toate datele de pe cele 3 pagini au fost extrase si salvate in SQLite!")