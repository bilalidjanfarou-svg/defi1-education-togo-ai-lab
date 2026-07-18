# Défi 1 Education — Togo AI Lab

Analyse des disparités territoriales du système éducatif togolais à partir 
des données ouvertes de geodata.gouv.tg et opendata.gouv.tg.

## Objectif

Identifier les préfectures prioritaires pour l'investissement en 
infrastructures scolaires (toilettes, bâtiments, bibliothèques).

## Données utilisées

- Établissements scolaires (15 454 écoles, 39 préfectures)
- Toilettes scolaires (10 228)
- Bâtiments scolaires (28 055)
- Bibliothèques scolaires (11)

Sources : [geodata.gouv.tg](https://geodata.gouv.tg) et [opendata.gouv.tg](https://opendata.gouv.tg)

## Méthodologie

1. Agrégation des 4 datasets par préfecture (39 préfectures, 5 régions)
2. Calcul de ratios d'infrastructure (toilettes/établissement, bâtiments/établissement, présence bibliothèque)
3. Normalisation min-max de chaque indicateur
4. Score composite pondéré (poids égaux) → indice de priorité d'investissement

## Résultats clés

- Agoè-Nyivé, Danyi et Wawa ressortent comme les préfectures les plus prioritaires
- Seules 6 préfectures sur 39 disposent d'au moins une bibliothèque scolaire
- Les disparités toilettes/établissement varient d'un facteur 3 selon les préfectures

## Structure du projet

- `01_exploration.py` à `04_exploration_bibliotheques.py` : exploration de chaque dataset
- `05_agregation.py` : agrégation par préfecture + calcul des coordonnées
- `06_score_priorite.py` : normalisation et score composite
- `dashboard.py` : dashboard interactif (Dash/Plotly)

## Lancer le dashboard