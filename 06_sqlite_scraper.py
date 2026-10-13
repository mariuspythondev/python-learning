import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('citate_fiverr.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE citate (id INTEGER PRIMARY KEY AUTOINCREMENT, citat TEXT, autor TEXT)")

url = 'https://quotes.toscrape.com/'
response = requests.get(url)
print(f"Deschidem conexiunea catre {url}...")
if response.status_code == 200:
    print(f"✅ Conexiune reusita! Procesam codul HTML...\n")
    soup = BeautifulSoup(response.text, 'html.parser')
    blocuri_citate = soup.find_all("div", class_="quote")
    for index, bloc in enumerate(blocuri_citate[:5], 1):
        citat = bloc.find('span', class_="text").text
        autor = bloc.find('small', class_="author").text
        cursor.execute("INSERT INTO citate (citat, autor) VALUES (?, ?)", (citat, autor))

else:
    print(f"❌ Eroare la conectarea! Cod status: {response.status_code}")

conn.commit()
conn.close()
