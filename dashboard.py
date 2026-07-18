import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table, Input, Output

df = pd.read_csv("dashboard_data.csv")
df = df.sort_values("indice_priorite", ascending=False).reset_index(drop=True)
cat = pd.read_csv("categories_prefectures.csv")

app = Dash(__name__)
app.title = "Priorite Education Togo"

app.index_string = """
<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
<style>
html, body { background-color: #ffffff !important; margin: 0; padding: 0; }
</style>
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
"""

BLEU = "#5b5fc7"
TURQUOISE = "#20c9ac"
ROSE = "#e0507f"
PALETTE = ["#5b5fc7", "#20c9ac", "#f5a623", "#e0507f", "#7fc9e0"]

page_style = {"fontFamily": "Segoe UI, Arial, sans-serif", "backgroundColor": "#ffffff", "minHeight": "100vh", "display": "flex"}
sidebar_style = {"width": "260px", "backgroundColor": "#f8f9fc", "padding": "24px 20px", "borderRight": "1px solid #eee"}
main_style = {"flex": 1, "padding": "24px 30px", "backgroundColor": "#ffffff"}
header_style = {"background": f"linear-gradient(90deg, {BLEU} 0%, {TURQUOISE} 100%)", "borderRadius": "16px", "padding": "20px 28px", "color": "white", "marginBottom": "20px"}
kpi_style = {"background": "white", "borderRadius": "12px", "padding": "16px", "flex": 1, "textAlign": "left", "boxShadow": "0 1px 6px rgba(0,0,0,0.08)", "borderLeft": f"4px solid {BLEU}"}
card_style = {"backgroundColor": "white", "borderRadius": "14px", "padding": "18px", "boxShadow": "0 1px 6px rgba(0,0,0,0.08)", "marginBottom": "20px"}
card_left = {"backgroundColor": "white", "borderRadius": "14px", "padding": "18px", "boxShadow": "0 1px 6px rgba(0,0,0,0.08)", "marginBottom": "20px", "width": "48%"}
card_right = {"backgroundColor": "white", "borderRadius": "14px", "padding": "18px", "boxShadow": "0 1px 6px rgba(0,0,0,0.08)", "marginBottom": "20px", "width": "48%", "marginLeft": "4%"}

app.layout = html.Div(style=page_style, children=[

    html.Div([
        html.Div("🎓", style={"fontSize": "48px", "textAlign": "center", "marginBottom": "10px"}),
        html.H3("Education Togo", style={"textAlign": "center", "color": BLEU, "margin": "0 0 4px 0"}),
        html.P("Togo AI Lab - Defi Education", style={"textAlign": "center", "color": "#888", "fontSize": "12px", "marginBottom": "24px"}),
        html.Hr(),
        html.Label("Region", style={"fontWeight": "bold", "marginTop": "20px", "display": "block"}),
        dcc.Dropdown(id="region-filter", options=[{"label": r, "value": r} for r in sorted(df["region_nom_bdd"].unique())], placeholder="Toutes", style={"marginBottom": "20px"}),
        html.Label("Prefecture", style={"fontWeight": "bold", "display": "block"}),
        dcc.Dropdown(id="pref-filter", options=[{"label": p, "value": p} for p in sorted(df["prefecture_nom_bdd"].unique())], placeholder="Toutes", style={"marginBottom": "20px"}),
    ], style=sidebar_style),

    html.Div(style=main_style, children=[
        html.Div([
            html.H1("Education au Togo", style={"margin": "0"}),
            html.P("Index de priorite d'investissement par prefecture — Togo AI Lab, Defi Education", style={"marginTop": "6px", "opacity": 0.9}),
        ], style=header_style),

        html.Div(id="kpi-container", style={"display": "flex", "gap": "14px", "marginBottom": "20px"}),

        html.Div([
            html.Div([html.H3("Carte des prefectures", style={"marginTop": 0, "color": "#1a1a2e"}), dcc.Graph(id="map-graph")], style=card_style),
        ]),

        html.Div([
            html.Div([html.H3("Repartition par categorie", style={"marginTop": 0, "color": "#1a1a2e"}), dcc.Graph(id="donut-graph")], style=card_left),
            html.Div([html.H3("Profil - Top 3 prioritaires", style={"marginTop": 0, "color": "#1a1a2e"}), dcc.Graph(id="radar-graph")], style=card_right),
        ], style={"display": "flex"}),

        html.Div([
            html.Div([html.H3("Top 10 - Priorite d'investissement", style={"marginTop": 0, "color": "#1a1a2e"}), dcc.Graph(id="bar-graph")], style=card_style),
        ]),

        html.Div([
            html.H3("Table detaillee", style={"marginTop": 0, "color": "#1a1a2e"}),
            html.Div(id="table-container"),
        ], style=card_style),

        html.P("Sources: geodata.gouv.tg, opendata.gouv.tg - Togo AI Lab Data Challenge Education", style={"color": "#888", "fontSize": "12px", "textAlign": "center"}),
    ]),
])

@app.callback(
    Output("map-graph", "figure"),
    Output("donut-graph", "figure"),
    Output("radar-graph", "figure"),
    Output("bar-graph", "figure"),
    Output("kpi-container", "children"),
    Output("table-container", "children"),
    Input("region-filter", "value"),
    Input("pref-filter", "value"),
)
def update_dashboard(region, prefecture):
    dff = df.copy()
    if region:
        dff = dff[dff["region_nom_bdd"] == region]
    if prefecture:
        dff = dff[dff["prefecture_nom_bdd"] == prefecture]

    fig_map = px.scatter_map(dff, lat="lat", lon="lon", size="total_etablissements", color="indice_priorite", color_continuous_scale=["#20c9ac", "#f5a623", "#e0507f"], hover_name="prefecture_nom_bdd", zoom=6, center={"lat": 8.6, "lon": 1.1}, map_style="carto-positron", height=440)
    fig_map.update_layout(margin=dict(l=0, r=0, t=10, b=0))

    prefs_visibles = dff["prefecture_nom_bdd"].tolist()
    cat_f = cat[cat["prefecture_nom_bdd"].isin(prefs_visibles)]
    cat_totaux = cat_f[["College", "Ecole primaire", "Jardin (maternelle)", "Lycée"]].sum().reset_index()
    cat_totaux.columns = ["Categorie", "Total"]
    fig_donut = px.pie(cat_totaux, names="Categorie", values="Total", hole=0.55, color_discrete_sequence=PALETTE, height=350)
    fig_donut.update_layout(margin=dict(l=10, r=10, t=10, b=10))

    top3 = dff.nlargest(3, "indice_priorite")
    fig_radar = go.Figure()
    for _, row in top3.iterrows():
        fig_radar.add_trace(go.Scatterpolar(r=[row["toilettes_norm"], row["batiments_norm"], row["bibliotheque_norm"]], theta=["Toilettes", "Batiments", "Bibliotheque"], fill="toself", name=row["prefecture_nom_bdd"]))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), height=350, margin=dict(l=40, r=40, t=20, b=20))

    fig_bar = px.bar(dff.sort_values("indice_priorite", ascending=False).head(10), x="indice_priorite", y="prefecture_nom_bdd", orientation="h", color="indice_priorite", color_continuous_scale=["#20c9ac", "#5b5fc7"], height=400)
    fig_bar.update_layout(margin=dict(l=0, r=0, t=10, b=0), yaxis_title="", xaxis_title="Indice de priorite", yaxis=dict(autorange="reversed"), coloraxis_showscale=False)

    kpis = [
        html.Div([html.P("Etablissements", style={"margin": 0, "fontSize": "12px", "color": "#888"}), html.H2(f"{dff['total_etablissements'].sum():,}".replace(",", " "), style={"margin": "6px 0 0 0", "color": BLEU})], style=kpi_style),
        html.Div([html.P("Prefectures affichees", style={"margin": 0, "fontSize": "12px", "color": "#888"}), html.H2(str(len(dff)), style={"margin": "6px 0 0 0", "color": BLEU})], style=kpi_style),
        html.Div([html.P("Avec bibliotheque", style={"margin": 0, "fontSize": "12px", "color": "#888"}), html.H2(f"{int(dff['a_bibliotheque'].sum())}", style={"margin": "6px 0 0 0", "color": BLEU})], style=kpi_style),
        html.Div([html.P("Plus prioritaire", style={"margin": 0, "fontSize": "12px", "color": "#888"}), html.H2(dff.iloc[0]["prefecture_nom_bdd"] if len(dff) else "-", style={"margin": "6px 0 0 0", "fontSize": "20px", "color": BLEU})], style=kpi_style),
    ]

    table = dash_table.DataTable(
        data=dff.to_dict("records"),
        columns=[
            {"name": "Region", "id": "region_nom_bdd"},
            {"name": "Prefecture", "id": "prefecture_nom_bdd"},
            {"name": "Nb etablissements", "id": "total_etablissements"},
            {"name": "Toilettes/etab.", "id": "ratio_toilettes_par_etab"},
            {"name": "Batiments/etab.", "id": "ratio_batiments_par_etab"},
            {"name": "Bibliotheque", "id": "a_bibliotheque"},
            {"name": "Indice priorite", "id": "indice_priorite"},
        ],
        sort_action="native", page_size=12,
        style_cell={"textAlign": "left", "padding": "10px", "fontSize": "13px", "border": "none"},
        style_header={"fontWeight": "bold", "color": "white", "backgroundColor": BLEU, "border": "none"},
        style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#f8f9fc"}],
        style_table={"borderRadius": "10px", "overflow": "hidden"},
    )

    return fig_map, fig_donut, fig_radar, fig_bar, kpis, table


if __name__ == "__main__":
    app.run(debug=True, port=8050)

