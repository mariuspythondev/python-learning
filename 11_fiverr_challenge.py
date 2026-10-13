import csv
import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect("final_client.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE complete_quotes (
id INTEGER PRIMARY KEY AUTOINCRETMENT, quote TEXT, author TEXT
)
"""
)
        

url = "https://quotes.toscrape.com/"

try:
    print(f"Open conection to {url}...")
    response = requests.get(url, timeout=5)

    response.raise_for_status()

    for number_page in range(1,4):
        url = f"https://quotes.toscrape.com/page/{number_page}/"
        print(f"Citim pagina {number_page}:{url}...")

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')
            block_quotes = soup.find_all('div', class_='quote')

            for block in block_quotes:
                quote = block.find("span",class_="text").text
                author = block.find("small",class_="author").text

                cursor.execute(
                    "INSERT INTO complete_quotes (quote, author) VALUES (?, ?)" (quote, author)
                )
                conn.commit()
            cursor.execute("SELECT quote FROM complete_quotes WHERE author = ?", ("Albert Einstein",))
            resultat = cursor.fetchall()
            print("=== Citate filtrate: Albert Einstein ===")
            for res in resultat:
                print(f"- {res[0]}")
            with open('final_raport_fiver.csv', 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Quote', 'Author'])
                writer.writerows(resultat)

            print('🚀 Pipeline-ul complet a rulat cu succes!')

        else:
            print(f"Eroare la conectare! Cod status:{response.status_code}")



except requests.exceptions.RequestException as e:
    print("A network error occurred {e}")

conn.close()
