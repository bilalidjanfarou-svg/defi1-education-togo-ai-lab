import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Charger les données
df = pd.read_csv("dashboard_data.csv")

# Créer l'application Dash
app = Dash(__name__)

# Graphique 1 : classement en barres
fig_bar = px.bar(
    df.sort_values("indice_priorite"),
    x="indice_priorite",
    y="prefecture_nom_bdd",
    orientation="h",
    title="Indice de priorité d'investissement par préfecture",
    height=800,
)

# Graphique 2 : carte du Togo
fig_map = px.scatter_map(
    df,
    lat="lat",
    lon="lon",
    size="total_etablissements",
    color="indice_priorite",
    color_continuous_scale="RdYlGn_r",
    hover_name="prefecture_nom_bdd",
    zoom=6,
    center={"lat": 8.6, "lon": 1.1},
    map_style="carto-positron",
    height=600,
    title="Carte des préfectures (taille = nb établissements, couleur = priorité)",
)

# Structure de la page
app.layout = html.Div([
    html.H1("Éducation au Togo — Priorités d'investissement"),
    dcc.Graph(figure=fig_map),
    dcc.Graph(figure=fig_bar),
])

if __name__ == "__main__":
    app.run(debug=True, port=8050)