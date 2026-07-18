import pandas as pd
import re

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

# Charger les 4 fichiers
etabs = pd.read_csv("etablissements.csv")
# Extraire longitude et latitude depuis la colonne geometry
def extraire_coordonnees(texte_point):
    match = re.match(r"POINT \(([-\d.]+) ([-\d.]+)\)", str(texte_point))
    if match:
        longitude = float(match.group(1))
        latitude = float(match.group(2))
        return pd.Series([longitude, latitude])
    return pd.Series([None, None])

etabs[["lon", "lat"]] = etabs["geometry"].apply(extraire_coordonnees)

print("\nAperçu des coordonnées extraites :")
print(etabs[["etablissement_nom", "lon", "lat"]].head())
toilettes = pd.read_csv("toilettes.csv")
batiments = pd.read_csv("batiments.csv")
biblio = pd.read_csv("bibliotheques.csv")

# Vérifier que tout est bien chargé
print("Établissements :", etabs.shape)
print("Toilettes      :", toilettes.shape)
print("Bâtiments      :", batiments.shape)
print("Bibliothèques  :", biblio.shape)


# Compter le nombre d'établissements par préfecture (et par région, pour garder l'info)
etabs_par_pref = etabs.groupby(["region_nom_bdd", "prefecture_nom_bdd"]).size().reset_index(name="total_etablissements")

print("\nÉtablissements par préfecture :")
print(etabs_par_pref)


# Compter le nombre de toilettes par préfecture
toilettes_par_pref = toilettes.groupby("prefecture_nom_bdd").size().reset_index(name="nb_toilettes")

print("\nToilettes par préfecture :")
print(toilettes_par_pref)

# Compter le nombre de bâtiments par préfecture
batiments_par_pref = batiments.groupby("prefecture_nom_bdd").size().reset_index(name="nb_batiments")

print("\nBâtiments par préfecture :")
print(batiments_par_pref)

# Compter le nombre de bibliothèques par préfecture
biblio_par_pref = biblio.groupby("prefecture_nom_bdd").size().reset_index(name="nb_bibliotheques")

print("\nBibliothèques par préfecture :")
print(biblio_par_pref)

# Fusionner les 4 tableaux ensemble, en gardant toutes les préfectures
df = etabs_par_pref.merge(toilettes_par_pref, on="prefecture_nom_bdd", how="left")
df = df.merge(batiments_par_pref, on="prefecture_nom_bdd", how="left")
df = df.merge(biblio_par_pref, on="prefecture_nom_bdd", how="left")

# Remplacer les valeurs manquantes par 0 (préfectures sans bibliothèque = 0, pas "vide")
df["nb_bibliotheques"] = df["nb_bibliotheques"].fillna(0)

print("\nTableau final fusionné :")
print(df)

# Calculer les ratios (arrondis à 2 décimales)
df["ratio_toilettes_par_etab"] = (df["nb_toilettes"] / df["total_etablissements"]).round(2)
df["ratio_batiments_par_etab"] = (df["nb_batiments"] / df["total_etablissements"]).round(2)

# Indicateur binaire : la préfecture a-t-elle au moins une bibliothèque ?
df["a_bibliotheque"] = (df["nb_bibliotheques"] > 0).astype(int)

print("\nTableau avec ratios :")
print(df[["region_nom_bdd", "prefecture_nom_bdd", "ratio_toilettes_par_etab", "ratio_batiments_par_etab", "a_bibliotheque"]])

# Sauvegarder le tableau final
df.to_csv("agregation_prefectures.csv", index=False)
print("\nFichier sauvegardé : agregation_prefectures.csv")

# Calculer le centre géographique (centroïde) de chaque préfecture
centroides = etabs.groupby("prefecture_nom_bdd")[["lat", "lon"]].mean().reset_index()

print("\nCentroïdes par préfecture :")
print(centroides)

# Fusionner les centroïdes avec le tableau agrégé
df = df.merge(centroides, on="prefecture_nom_bdd", how="left")

df.to_csv("agregation_prefectures.csv", index=False)
print("\nFichier ré-sauvegardé avec coordonnées : agregation_prefectures.csv")


# ============================================================
# Répartition par catégorie d'établissement, par préfecture
# ============================================================
cat_par_pref = (
    etabs.groupby(["prefecture_nom_bdd", "etablissement_categorie"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)
print("\nRépartition par catégorie et préfecture :")
print(cat_par_pref)

cat_par_pref.to_csv("categories_prefectures.csv", index=False)
print("\nFichier sauvegardé : categories_prefectures.csv")


























