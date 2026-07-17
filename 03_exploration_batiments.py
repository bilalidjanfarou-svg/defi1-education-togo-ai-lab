import pandas as pd

# Charger le fichier CSV des bâtiments scolaires
batiments = pd.read_csv("batiments.csv")

# Afficher le nombre de lignes et colonnes
print("Dimensions :", batiments.shape)

# Afficher les noms de toutes les colonnes
print("\nColonnes disponibles :")
print(batiments.columns.tolist())

# Compter les fonctions des bâtiments (salle de classe, bureau, etc.)
print("\nFonctions des bâtiments :")
print(batiments["batiment_fonction"].value_counts())