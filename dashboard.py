import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table

df = pd.read_csv("dashboard_data.csv")
df = df.sort_values("indice_priorite", ascending=False).reset_index(drop=True)
cat = pd.read_csv("categories_prefectures.csv")

app = Dash(__name__)
app.title = "Priorite Education Togo"

card_left = {"backgroundColor": "white", "borderRadius": "10px", "padding": "20px", "boxShadow": "0 1px 4px rgba(0,0,0,0.1)", "marginBottom": "24px", "width": "56%"}
card_right = {"backgroundColor": "white", "borderRadius": "10px", "padding": "20px", "boxShadow": "0 1px 4px rgba(0,0,0,0.1)", "marginBottom": "24px", "width": "41%", "marginLeft": "3%"}
card_style = {"backgroundColor": "white", "borderRadius": "10px", "padding": "20px", "boxShadow": "0 1px 4px rgba(0,0,0,0.1)", "marginBottom": "24px"}
kpi_style = {"backgroundColor": "white", "borderRadius": "10px", "padding": "16px 20px", "boxShadow": "0 1px 4px rgba(0,0,0,0.1)", "flex": 1, "textAlign": "center"}
page_style = {"fontFamily": "Segoe UI, Arial, sans-serif", "backgroundColor": "#f4f5f7", "padding": "30px", "minHeight": "100vh"}

fig_map = px.scatter_map(df, lat="lat", lon="lon", size="total_etablissements", color="indice_priorite", color_continuous_scale="RdYlGn_r", hover_name="prefecture_nom_bdd", zoom=6, center={"lat": 8.6, "lon": 1.1}, map_style="carto-positron", height=520)
fig_map.update_layout(margin=dict(l=0, r=0, t=10, b=0))

fig_bar = px.bar(df.sort_values("indice_priorite"), x="indice_priorite", y="prefecture_nom_bdd", orientation="h", color="indice_priorite", color_continuous_scale="RdYlGn_r", height=780)
fig_bar.update_layout(margin=dict(l=0, r=0, t=10, b=0), coloraxis_showscale=False, yaxis_title="", xaxis_title="Indice de priorite")

cat_totaux = cat[["College", "Ecole primaire", "Jardin (maternelle)", "Lycée"]].sum().reset_index()
cat_totaux.columns = ["Categorie", "Total"]
fig_cat = px.pie(cat_totaux, names="Categorie", values="Total", height=380, color_discrete_sequence=px.colors.qualitative.Set2)
fig_cat.update_layout(margin=dict(l=10, r=10, t=10, b=10))

fig_scatter = px.scatter(df, x="ratio_toilettes_par_etab", y="ratio_batiments_par_etab", color="region_nom_bdd", size="total_etablissements", hover_name="prefecture_nom_bdd", height=450, color_discrete_sequence=px.colors.qualitative.Set2)
fig_scatter.update_layout(margin=dict(l=10, r=10, t=10, b=10))

app.layout = html.Div(style=page_style, children=[
    html.Div([
        html.H1("Education au Togo", style={"margin": "0", "color": "#1a1a2e"}),
        html.P("Index de priorite d'investissement par prefecture", style={"color": "#666", "marginTop": "4px"}),
    ], style={"marginBottom": "24px"}),

    html.Div([
        html.Div([html.H2("15 194", style={"margin": 0}), html.P("Ecoles au Togo", style={"color": "#888", "margin": 0})], style=kpi_style),
        html.Div([html.H2("76 862", style={"margin": 0}), html.P("Enseignants", style={"color": "#888", "margin": 0})], style=kpi_style),
        html.Div([html.H2("14.7%", style={"margin": 0}), html.P("Budget alloue a education", style={"color": "#888", "margin": 0})], style=kpi_style),
        html.Div([html.H2("6/39", style={"margin": 0}), html.P("Prefectures avec bibliotheque", style={"color": "#888", "margin": 0})], style=kpi_style),
    ], style={"display": "flex", "gap": "16px", "marginBottom": "24px"}),

    html.Div([
        html.Div([html.H3("Carte des prefectures", style={"marginTop": 0}), dcc.Graph(figure=fig_map)], style=card_left),
        html.Div([html.H3("Classement complet", style={"marginTop": 0}), dcc.Graph(figure=fig_bar)], style=card_right),
    ], style={"display": "flex"}),

    html.Div([
        html.Div([html.H3("Repartition par categorie", style={"marginTop": 0}), dcc.Graph(figure=fig_cat)], style=card_right),
        html.Div([html.H3("Toilettes vs Batiments", style={"marginTop": 0}), dcc.Graph(figure=fig_scatter)], style=card_left),
    ], style={"display": "flex"}),

    html.Div([
        html.H3("Table detaillee", style={"marginTop": 0}),
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
            style_cell={"textAlign": "left", "padding": "8px", "fontSize": "13px"},
            style_header={"fontWeight": "bold", "backgroundColor": "#f4f5f7", "border": "none"},
        ),
    ], style=card_style),

    html.P("Sources: geodata.gouv.tg, opendata.gouv.tg - Togo AI Lab Data Challenge Education", style={"color": "#aaa", "fontSize": "12px", "textAlign": "center"}),
])

if __name__ == "__main__":
    app.run(debug=True, port=8050)
