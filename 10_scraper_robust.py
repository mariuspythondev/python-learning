import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com/"

try:
    print(f"Incercam conectarea la {url}...")
    # Setăm și un timeout de 5 secunde (dacă site-ul nu răspunde în 5 secunde, renunță singur)
    response = requests.get(url,timeout=5)

    # Verificam codul HTTP
    response.raise_for_status() # Aruncă o eroare dacă statusul nu este 200 (ex: 404, 500)

    print("Conexiune stabila si securizata!")

    # Aici poti pune logica ta de BeautifulSoup pe  care o stii deja
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f'Titlul paginii extrase: {soup.title.text}')

except requests.exceptions.RequestException as e:
    print(f" A aparut o eroare de retea: {e}")
    