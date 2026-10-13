fiver_gig = {
    'titlu_serviciu': 'Python Automation & Scraping',
    'pret_usd': 25,
    'completat': True,
}

clienti = ['Ion', 'Mihai', 'Andreea',]
print(f'=== Serviciu Fiver ===')
print(f'Titlu serviciului: {fiver_gig["titlu_serviciu"]}')
print(f'Pretul serviciului: {fiver_gig["pret_usd"]} USD')
for client in clienti:
    print(f' - {client}')


