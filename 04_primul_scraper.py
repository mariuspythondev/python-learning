import requests
from bs4 import BeautifulSoup

# 1.Definim URL-ul unei pagini web speciale pentru teste de scraping
url = 'https://quotes.toscrape.com/'

print(f"Deschidem conexiunea catre {url}...")

# 2. Trimitem o cerere HTTP de tip GET catre site
raspuns = requests.get(url)

# Verificam daca site-ul ne-a raspuns cu succes (cod 200 = OK)
if raspuns.status_code == 200:
    print(f"✅ Conexiune reusita!Procesam codul HTML...\n")

    # 3. Parsam continutul HTML cu BeautifulSoup
    soup = BeautifulSoup(raspuns.text, 'html.parser')

    # 4.Cautam toate citatele din pagina (care se afla in tagul 'span' cu clasa 'text')
    citate = soup.find_all("span", class_="text")
    print("=== CITATE EXTRASE ===")
    # Parcurgem primele 5 citate extrase
    for index, citat in enumerate(citate[:5], 1):
        print(f"{index}. {citat.text}")
else:
    print(f"❌ Eroare la conectarea! Cod status: {raspuns.status_code}")