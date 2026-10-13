import sqlite3
import csv

conn = sqlite3.connect('citate_fiverr.db')
cursor = conn.cursor()

cursor.execute("SELECT citat, autor FROM citate")
rezultate = cursor.fetchall()

with open('citate_export.csv', 'w', newline='', encoding='utf-8') as fisier_csv:
    writer = csv.writer(fisier_csv)
    #Scriem antentul coloanelor
    writer.writerow(['Citat', 'Autor'])
    #Scriem toae datele preuluate din SQLite
    writer.writerows(rezultate)

conn.close()
print("Datele au fost exportate cu succes in fisierul citate_export.csv!")