import requests
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com/'
response = requests.get(url)

print(f"Deschidem conexiunea catre {url}...")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"✅ Conexiune reusita! Procesam codul HTML...\n")
    blocuri_citate = soup.find_all("div", class_="quote")
    for index, bloc in enumerate(blocuri_citate[:5],1):
        citat = bloc.find("span", class_="text").text
        autor = bloc.find("small", class_="author").text
        print(f'{index}. "{citat}" - {autor}')

else:
    print(f"❌ Eroare la conectarea! Cod status: {response.status_code}")