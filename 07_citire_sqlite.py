# import sqlite3

# # 1.Ne conectam la aceasi baza de date existenta
# conn = sqlite3.connect('citate_fiverr.db')
# cursor = conn.cursor()

# # 2. Cerem toate inregistrarile din tabel
# cursor.execute("SELECT citat, autor FROM citate")
# rezultate = cursor.fetchall()

# # 3. Parcurgem rezultatele cu o bucla for
# print('=== Citate citite din Baza de Date ===')
# for rand in rezultate:
#     citat = rand[0] # prima coloana
#     autor = rand[1] # a doua coloana
#     print(f"-{citat} spus de {autor}")
# conn.close()



#Exercitiu practic: Citirea datelor din baza de date SQLite si afisarea lor in consola.
import sqlite3
conn = sqlite3.connect('citate_fiverr.db')
cursor = conn.cursor()
cursor.execute("SELECT citat FROM citate WHERE autor = ?", ("Albert Einstein",))
rezultate = cursor.fetchall()
print('=== Citate filtrate: Albert Einstein ===')
for rand in rezultate:
    print(f"- {rand[0]}")

conn.close()