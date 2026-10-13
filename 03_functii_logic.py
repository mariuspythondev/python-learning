# 1. Definim o funcție care procesează o comandă
def verifica_oferta(titlu, pret):
    print(f"Verificam serviciul: '{titlu}' ...")

    # Structură de decizie if / else
    if pret <= 30:
        return f"✅ Oferta excelenta pentru inceput! Pret: {pret}$"
    elif pret <= 100:
        return f"⚡ Ofertă medie (Proiect mediu). Pret: {pret}$"
    else:
        return f"🚀 Proiect complex / Premium! Pret: {pret}$"


# 2. Testăm funcția cu date diferite
comanda_1 = verifica_oferta("Simple Script Scrapig", 25)
comanda_2 = verifica_oferta("Automation Bot + Database", 75)
comanda_3 = verifica_oferta("Enterprise Web Crawler", 200)

print("\n=== RREZULTATE VERIFICARE ===")
print(comanda_1)
print(comanda_2)
print(comanda_3)