import pandas as pd

# Charger le fichier CSV des etablissements scolaires
etabs = pd.read_csv("etablissements.csv")

# Affiche de nombre de lignes et colonnes
print("Dimensions :", etabs.shape)

# Affiche  les noms de toutes les colonnes
print("\nColonnes disponibles :")
print(etabs.columns.tolist())

# Compte de nombre d'etablissements par categorie
print("Repartition par categorie :")
print(etabs["etablissement_categorie"].value_counts())

# Nombre de régions et préfectures uniques
print("\nNombre de régions :", etabs["region_nom_bdd"].nunique())
print("Liste des régions :", etabs["region_nom_bdd"].unique())
print("\nNombre de préfectures :", etabs["prefecture_nom_bdd"].nunique())

