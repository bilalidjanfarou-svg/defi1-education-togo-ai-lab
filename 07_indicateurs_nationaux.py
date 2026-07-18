import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

indic = pd.read_csv("indicateurs_nationaux.csv")

print("Dimensions :", indic.shape)
print("\nColonnes :", indic.columns.tolist())

# Voir les indicateurs disponibles et leurs dernières valeurs
print("\nDerniers chiffres disponibles par indicateur (niveau=Total, secteur=Total) :")
recent = indic[(indic["niveau"] == "Total") & (indic["secteur"] == "Total")]
recent = recent.sort_values(["indicateurs", "Date"]).groupby("indicateurs").tail(1)
print(recent[["indicateurs", "Date", "Value", "Unit"]])

recent.to_csv("indicateurs_nationaux_recents.csv", index=False)
print("\nFichier sauvegardé : indicateurs_nationaux_recents.csv")

















