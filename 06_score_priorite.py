import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

# Charger le tableau déjà agrégé par préfecture
df = pd.read_csv("agregation_prefectures.csv")

print("Tableau chargé :", df.shape)
print(df.head())

# Normalisation min-max : ramène chaque indicateur entre 0 et 1
def normalize(colonne):
    return (colonne - colonne.min()) / (colonne.max() - colonne.min())

df["toilettes_norm"] = normalize(df["ratio_toilettes_par_etab"])
df["batiments_norm"] = normalize(df["ratio_batiments_par_etab"])

print("\nColonnes normalisées :")
print(df[["prefecture_nom_bdd", "ratio_toilettes_par_etab", "toilettes_norm", "ratio_batiments_par_etab", "batiments_norm"]])

# Normalisation de l'indicateur bibliothèque (déjà en 0/1, pas besoin de min-max)
df["bibliotheque_norm"] = df["a_bibliotheque"].astype(float)

# Score composite : moyenne des 3 indicateurs normalisés (poids égaux, 1/3 chacun)
df["score_infrastructure"] = (
    (df["toilettes_norm"] + df["batiments_norm"] + df["bibliotheque_norm"]) / 3
).round(4)

# Indice de priorité : l'inverse du score (plus haut = plus prioritaire pour l'investissement)
df["indice_priorite"] = (1 - df["score_infrastructure"]).round(4)

# Trier par priorité décroissante
df = df.sort_values("indice_priorite", ascending=False).reset_index(drop=True)

print("\n=== Classement des préfectures par priorité d'investissement ===")
print(df[["region_nom_bdd", "prefecture_nom_bdd", "score_infrastructure", "indice_priorite"]])

# Sauvegarder le résultat final pour le dashboard
df.to_csv("dashboard_data.csv", index=False)
print("\nFichier sauvegardé : dashboard_data.csv")