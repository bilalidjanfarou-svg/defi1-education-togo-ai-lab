import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table

df = pd.read_csv("dashboard_data.csv")
df = df.sort_values("indice_priorite", ascending=False).reset_index(drop=True)

app = Dash(__name__)
app.title = "Priorité Éducation Togo"

fig_map = px.scatter_map(
    df, lat="lat", lon="lon",
    size="total_etablissements", color="indice_priorite",
    color_continuous_scale="RdYlGn_r", hover_name="prefecture_nom_bdd",
    hover_data={"region_nom_bdd": True, "ratio_toilettes_par_etab": ":.2f",
                "ratio_batiments_par_etab": ":.2f", "a_bibliotheque": True,
                "lat": False, "lon": False},
    zoom=6, center={"lat": 8.6, "lon": 1.1}, map_style="carto-positron",
    height=550, title="Carte des préfectures",
)

fig_bar = px.bar(
    df.sort_values("indice_priorite"),
    x="indice_priorite", y="prefecture_nom_bdd", orientation="h",
    color="indice_priorite", color_continuous_scale="RdYlGn_r",
    title="Classement complet par priorité", height=800,
)

app.layout = html.Div(style={"fontFamily": "Arial", "padding": "20px"}, children=[
    html.H1("Éducation au Togo — Index de priorité d'investissement"),
    html.P("Data Challenge Education – Défi 1 — Togo AI Lab"),

    html.Div([
        html.Div([
            html.H3(f"{df['total_etablissements'].sum():,}".replace(",", " ")),
            html.P("Établissements au total"),
        ], style={"border": "1px solid #ddd", "padding": "10px", "flex": 1}),
        html.Div([
            html.H3(f"{int(df['a_bibliotheque'].sum())}/39"),
            html.P("Préfectures avec bibliothèque"),
        ], style={"border": "1px solid #ddd", "padding": "10px", "flex": 1}),
        html.Div([
            html.H3(df.iloc[0]["prefecture_nom_bdd"]),
            html.P("Préfecture la plus prioritaire"),
        ], style={"border": "1px solid #ddd", "padding": "10px", "flex": 1}),
    ], style={"display": "flex", "gap": "10px", "marginBottom": "20px"}),

    html.Div([
        html.Div([dcc.Graph(figure=fig_map)], style={"width": "58%", "display": "inline-block"}),
        html.Div([dcc.Graph(figure=fig_bar)], style={"width": "40%", "display": "inline-block", "marginLeft": "2%"}),
    ]),

    html.H3("Table détaillée"),
    dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[
            {"name": "Région", "id": "region_nom_bdd"},
            {"name": "Préfecture", "id": "prefecture_nom_bdd"},
            {"name": "Nb établissements", "id": "total_etablissements"},
            {"name": "Toilettes/étab.", "id": "ratio_toilettes_par_etab"},
            {"name": "Bâtiments/étab.", "id": "ratio_batiments_par_etab"},
            {"name": "Bibliothèque", "id": "a_bibliotheque"},
            {"name": "Indice priorité", "id": "indice_priorite"},
        ],
        sort_action="native", page_size=15,
        style_cell={"textAlign": "left", "padding": "6px"},
        style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
    ),
])

if __name__ == "__main__":
    app.run(debug=True, port=8050)