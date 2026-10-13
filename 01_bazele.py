# 1. Variabile simple (String, Int, Bool)
developer = 'mariuspythondev'
ore_studiu_zilnic = 3
este_disciplinat = True

print(f'=== Profil developer: {developer} ===')
print(f'Ore alocate pe zi: {ore_studiu_zilnic}')
print(f'Status disciplina: {este_disciplinat}\n')

# 2. Liste (Colectăm mai multe elemente ordonate)
tehnologii = ['Python', 'VSCode', 'Git', 'SQLite', 'BeautifulSoup']
print('Tehnologii de invatat:')
for tech in tehnologii:
    print(f' - {tech}')

# 3. Dicționare (Cum salvăm un element extras dintr-un site)
# Un dicționar păstrează datele ca o pereche 'cheie': 'valoare'
proiect_demo = {
    'titlu': 'Scraper Imobiliar',
    'status': 'In lucru',
    'target_platform': 'Fiverr',
    'pagini_procesate': 15
}

print(f'\n === Detalii proiect ===')
print(f'Titlu proiect: {proiect_demo["titlu"]}')
print(f"Platforma de livrare: {proiect_demo['target_platform']}")