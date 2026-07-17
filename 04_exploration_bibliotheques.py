import pandas as pd

# Charger le fichier CSV des bibliothèques scolaires
biblio = pd.read_csv("bibliotheques.csv")

# Afficher le nombre de lignes et colonnes
print("Dimensions :", biblio.shape)

# Afficher les noms de toutes les colonnes
print("\nColonnes disponibles :")
print(biblio.columns.tolist())

# Afficher tout le contenu (le fichier est petit)
print("\nContenu complet :")
print(biblio[["region_nom_bdd", "prefecture_nom_bdd", "etablissement_nom"]])