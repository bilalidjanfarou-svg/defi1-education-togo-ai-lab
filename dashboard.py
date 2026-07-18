import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table

df = pd.read_csv("dashboard_data.csv")
df = df.sort_values("indice_priorite", ascending=False).reset_index(drop=True)
cat = pd.read_csv("categories_prefectures.csv")

app = Dash(__name__)
app.title = "Priorite Education Togo"

fig_map = px.scatter_map(
    df, lat="lat", lon="lon",
    size="total_etablissements", color="indice_priorite",
    color_continuous_scale="RdYlGn_r", hover_name="prefecture_nom_bdd",
    zoom=6, center={"lat": 8.6, "lon": 1.1}, map_style="carto-positron",
    height=550, title="Carte des prefectures",
)

fig_bar = px.bar(
    df.sort_values("indice_priorite"),
    x="indice_priorite", y="prefecture_nom_bdd", orientation="h",
    color="indice_priorite", color_continuous_scale="RdYlGn_r",
    title="Classement complet par priorite", height=800,
)

cat_totaux = cat[["College", "Ecole primaire", "Jardin (maternelle)", "Lycée"]].sum().reset_index()
cat_totaux.columns = ["Categorie", "Total"]
fig_cat = px.pie(
    cat_totaux, names="Categorie", values="Total",
    title="Repartition nationale par categorie", height=400,
)

app.layout = html.Div(style={"fontFamily": "Arial", "padding": "20px"}, children=[
    html.H1("Education au Togo - Index de priorite d'investissement"),
    html.P("Data Challenge Education - Defi 1 - Togo AI Lab"),

    html.H3("Contexte national (2022)"),
    html.Div([
        html.Div([html.H4("15 194"), html.P("Ecoles au Togo")], style={"border": "1px solid #ddd", "padding": "10px", "flex": 1}),
        html.Div([html.H4("76 862"), html.P("Enseignants")], style={"border": "1px solid #ddd", "padding": "10px", "flex": 1}),
        html.Div([html.H4("14.7%"), html.P("Budget national alloue a education")], style={"border": "1px solid #ddd", "padding": "10px", "flex": 1}),
        html.Div([html.H4("39.6%"), html.P("Analphabetisme adulte (2017)")], style={"border": "1px solid #ddd", "padding": "10px", "flex": 1}),
    ], style={"display": "flex", "gap": "10px", "marginBottom": "20px"}),

    html.H3("Disparites territoriales"),
    html.Div([
        html.Div([dcc.Graph(figure=fig_map)], style={"width": "58%", "display": "inline-block"}),
        html.Div([dcc.Graph(figure=fig_bar)], style={"width": "40%", "display": "inline-block", "marginLeft": "2%"}),
    ]),

    html.Div([dcc.Graph(figure=fig_cat)]),

    html.H3("Table detaillee"),
    dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[
            {"name": "Region", "id": "region_nom_bdd"},
            {"name": "Prefecture", "id": "prefecture_nom_bdd"},
            {"name": "Nb etablissements", "id": "total_etablissements"},
            {"name": "Toilettes/etab.", "id": "ratio_toilettes_par_etab"},
            {"name": "Batiments/etab.", "id": "ratio_batiments_par_etab"},
            {"name": "Bibliotheque", "id": "a_bibliotheque"},
            {"name": "Indice priorite", "id": "indice_priorite"},
        ],
        sort_action="native", page_size=15,
        style_cell={"textAlign": "left", "padding": "6px"},
        style_header={"fontWeight": "bold", "backgroundColor": "#e9ecef"},
    ),
])

if __name__ == "__main__":
    app.run(debug=True, port=8050)
