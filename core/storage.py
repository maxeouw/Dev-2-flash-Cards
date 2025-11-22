"""
class StorageManager
"""

import sqlite3

#Création/Ouverture db
db = sqlite3.connect('storage.db')

#Pour créer les requetes
cursor = db.cursor()

#Création table
cursor.execute('''
CREATE TABLE IF NOT EXISTS categorie(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS carte(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    reponse TEXT NOT NULL,
    categorie_id INTEGER,
    FOREIGN KEY(categorie_id) REFERENCES categorie(id)

)
''')

cursor.execute('''INSERT INTO categorie (nom) VALUES ('Science')''')

db.commit()

db.close()