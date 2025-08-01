import sqlite3

# Connexion à la base de données
conn = sqlite3.connect("db/animaux.db")
cursor = conn.cursor()

# 1. Supprimer la table si elle existe déjà
cursor.execute("DROP TABLE IF EXISTS animaux")

# 2. Recréer la table
cursor.execute("""
CREATE TABLE animaux (
  id INTEGER PRIMARY KEY,
  nom VARCHAR(25),
  espece VARCHAR(25),
  race VARCHAR(25),
  age INTEGER,
  description VARCHAR(500),
  courriel VARCHAR(80),
  adresse VARCHAR(75),
  ville VARCHAR(75),
  cp VARCHAR(7)
)
""")

# 3. Insérer les données
cursor.executescript("""
INSERT INTO animaux VALUES (1, 'Fluffy', 'Mouton', 'Dorper', 2, 'Mouton Dorpor plutôt jeune. Pas pour l''élevage, car provient d''une famille végane.', 'mouton@noteleveur.ca', '47 rang du Nord', 'Victoriaville', 'H3E 3K4');
INSERT INTO animaux VALUES (2, 'Dragon', 'Chien', 'Chihuahua', 5, 'Petit chien docile.', 'steve@hotmail.com', '255 chemin du Loup', 'Drummondville', 'J3R 4I3');
INSERT INTO animaux VALUES (3, 'Perdita', 'Chien', 'Dalmatien', 12, 'Mère de plusieurs portées. Recherche une famille calme pour sa retraite.', 'cruella@disney.com', '34 rue de LaSalle', 'Montréal', 'H3E 4R5');
INSERT INTO animaux VALUES (4, 'Skippy', 'Kangourou', 'Inconnu', 7, 'Ancien acteur d''une série télé.', 'kangourou@animalcrossing.com', '4848 de la chance', 'St-Hilaire', 'J4P 9U4');
INSERT INTO animaux VALUES (5, 'Madame Long Cou', 'Escargot', 'Inconnu', 1, 'Escargot de jardin ayant eu une belle vie.', 'snail@snailmail.com', '33 de la Noix', 'Montréal', 'H3R 3J4');
INSERT INTO animaux VALUES (6, 'Serpent Haut', 'Serpent', 'Boa', 3, 'Serpent boa retrouvé au pavillon SH de l''UQAM.', 'serpent@uqam.ca', 'CP8888 Succ Centre-ville', 'Montréal', 'H3B 3C3');
INSERT INTO animaux VALUES (7, 'Mojo', 'Chien', 'Pug', 8, 'Vieux chien bien calme qui aime les promenades au parc.', 'cedric@hotmail.com', '4744 Marquette', 'Contrecoeur', 'J0L 1C0');
""")

# 4. Commit & close
conn.commit()
conn.close()

print("La table 'animaux' a été recréée avec succès.")