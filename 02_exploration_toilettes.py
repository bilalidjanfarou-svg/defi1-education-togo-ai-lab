import pandas as pd

# Charger le fichier CSV des toilettes scolaires
toilettes = pd.read_csv("toilettes.csv")

# Afficher le nombre de lignes et colonnes
print("Dimensions :", toilettes.shape)

# Afficher les noms de toutes les colonnes
print("\nColonnes disponibles :")
print(toilettes.columns.tolist())

# Compter les types de toilettes
print("\nTypes de toilettes :")
print(toilettes["toilette_type"].value_counts())