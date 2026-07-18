import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuration page
st.set_page_config(
    page_title="Education Togo - Analyse Défi",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============= CHARGER OU GÉNÉRER LES DONNÉES =============
@st.cache_data
def load_data():
    """Charge les données, les génère si nécessaire"""
    
    # Vérifier si les fichiers existent
    if not os.path.exists("dashboard_data.csv") or not os.path.exists("categories_prefectures.csv"):
        st.warning("⏳ Génération des données en cours...")
        generate_data()
    
    df = pd.read_csv("dashboard_data.csv")
    df = df.sort_values("indice_priorite", ascending=False).reset_index(drop=True)
    cat = pd.read_csv("categories_prefectures.csv")
    
    return df, cat

def generate_data():
    """Génère les fichiers CSV s'ils n'existent pas"""
    import re
    
    try:
        # Étape 1 : Charger et traiter les données brutes
        if not os.path.exists("agregation_prefectures.csv"):
            # Créer des données d'exemple si les fichiers originaux n'existent pas
            st.error("⚠️ Les fichiers de données sources (etablissements.csv, etc.) sont manquants.")
            st.info("Pour utiliser l'app correctement, assurez-vous que les fichiers CSV sont dans le repo.")
            st.stop()
        
        # Charger agregation_prefectures.csv
        df = pd.read_csv("agregation_prefectures.csv")
        
        # Normalisation min-max
        def normalize(colonne):
            return (colonne - colonne.min()) / (colonne.max() - colonne.min())
        
        df["toilettes_norm"] = normalize(df["ratio_toilettes_par_etab"])
        df["batiments_norm"] = normalize(df["ratio_batiments_par_etab"])
        df["bibliotheque_norm"] = df["a_bibliotheque"].astype(float)
        
        # Score composite et indice de priorité
        df["score_infrastructure"] = (
            (df["toilettes_norm"] + df["batiments_norm"] + df["bibliotheque_norm"]) / 3
        ).round(4)
        df["indice_priorite"] = (1 - df["score_infrastructure"]).round(4)
        
        # Sauvegarder
        df.to_csv("dashboard_data.csv", index=False)
        st.success("✅ dashboard_data.csv généré")
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la génération des données : {e}")
        st.stop()

# Charger les données
df, cat = load_data()

# Couleurs
BLEU = "#5b5fc7"
TURQUOISE = "#20c9ac"
ROSE = "#e0507f"
PALETTE = ["#5b5fc7", "#20c9ac", "#f5a623", "#e0507f", "#7fc9e0"]

# ============= SIDEBAR =============
st.sidebar.markdown(f"### 🎓 Education Togo")
st.sidebar.markdown("Togo AI Lab - Défi Education")
st.sidebar.markdown("---")

# Filtres
region = st.sidebar.selectbox(
    "Région",
    options=[None] + sorted(df["region_nom_bdd"].unique().tolist()),
    format_func=lambda x: "Toutes" if x is None else x
)

prefecture = st.sidebar.selectbox(
    "Préfecture",
    options=[None] + sorted(df["prefecture_nom_bdd"].unique().tolist()),
    format_func=lambda x: "Toutes" if x is None else x
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Sources:** [geodata.gouv.tg](https://geodata.gouv.tg) | [opendata.gouv.tg](https://opendata.gouv.tg)"
)

# Appliquer les filtres
dff = df.copy()
if region:
    dff = dff[dff["region_nom_bdd"] == region]
if prefecture:
    dff = dff[dff["prefecture_nom_bdd"] == prefecture]

# ============= HEADER =============
st.markdown(
    f"<h1 style='color: {BLEU};'>🎓 Education au Togo</h1>",
    unsafe_allow_html=True
)
st.markdown("Index de priorité d'investissement par préfecture — **Togo AI Lab, Défi Education**")
st.markdown("---")

# ============= KPI =============
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📚 Établissements", f"{dff['total_etablissements'].sum():,}".replace(",", " "))

with col2:
    st.metric("🏛️ Préfectures", len(dff))

with col3:
    st.metric("📖 Avec bibliothèque", int(dff['a_bibliotheque'].sum()))

with col4:
    top_pref = dff.iloc[0]["prefecture_nom_bdd"] if len(dff) > 0 else "-"
    st.metric("🔴 Plus prioritaire", top_pref)

st.markdown("---")

# ============= GRAPHIQUES =============
col1, col2 = st.columns(2)

# Carte
with col1:
    st.subheader("📍 Carte des préfectures")
    if len(dff) > 0:
        fig_map = px.scatter_mapbox(
            dff,
            lat="lat",
            lon="lon",
            size="total_etablissements",
            color="indice_priorite",
            color_continuous_scale=["#20c9ac", "#f5a623", "#e0507f"],
            hover_name="prefecture_nom_bdd",
            hover_data={"total_etablissements": True, "indice_priorite": ":.3f", "lat": False, "lon": False},
            zoom=5,
            mapbox_style="open-street-map",
            height=400
        )
        fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Aucune donnée pour cette sélection")

# Donut
with col2:
    st.subheader("📊 Répartition par catégorie")
    prefs_visibles = dff["prefecture_nom_bdd"].tolist()
    cat_f = cat[cat["prefecture_nom_bdd"].isin(prefs_visibles)]
    
    if len(cat_f) > 0:
        cat_totaux = cat_f[["College", "Ecole primaire", "Jardin (maternelle)", "Lycée"]].sum().reset_index()
        cat_totaux.columns = ["Categorie", "Total"]
        
        fig_donut = px.pie(
            cat_totaux,
            names="Categorie",
            values="Total",
            hole=0.55,
            color_discrete_sequence=PALETTE,
            height=400
        )
        fig_donut.update_layout(margin=dict(l=10, r=10, t=0, b=10))
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("Aucune donnée pour cette sélection")

# Radar
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Top 3 - Profil d'infrastructure")
    top3 = dff.nlargest(3, "indice_priorite")
    
    if len(top3) > 0:
        fig_radar = go.Figure()
        for _, row in top3.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row["toilettes_norm"], row["batiments_norm"], row["bibliotheque_norm"]],
                theta=["Toilettes", "Bâtiments", "Bibliothèque"],
                fill="toself",
                name=row["prefecture_nom_bdd"]
            ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            height=400,
            margin=dict(l=40, r=40, t=0, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# Bar chart
with col2:
    st.subheader("📈 Top 10 - Priorité d'investissement")
    top10 = dff.sort_values("indice_priorite", ascending=False).head(10)
    
    if len(top10) > 0:
        fig_bar = px.bar(
            top10,
            x="indice_priorite",
            y="prefecture_nom_bdd",
            orientation="h",
            color="indice_priorite",
            color_continuous_scale=["#20c9ac", "#f5a623", "#e0507f"],
            labels={"prefecture_nom_bdd": "", "indice_priorite": "Indice"},
            height=400
        )
        fig_bar.update_layout(
            margin=dict(l=150, r=0, t=0, b=0),
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False,
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# ============= TABLEAU DÉTAILLÉ =============
st.subheader("📋 Table détaillée")

if len(dff) > 0:
    table_display = dff[[
        "region_nom_bdd",
        "prefecture_nom_bdd",
        "total_etablissements",
        "ratio_toilettes_par_etab",
        "ratio_batiments_par_etab",
        "a_bibliotheque",
        "indice_priorite"
    ]].copy()
    
    table_display.columns = [
        "Région", "Préfecture", "Nb établissements",
        "Toilettes/étab.", "Bâtiments/étab.", "Bibliothèque", "Indice priorité"
    ]
    
    st.dataframe(
        table_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Indice priorité": st.column_config.NumberColumn(format="%.4f"),
            "Toilettes/étab.": st.column_config.NumberColumn(format="%.2f"),
            "Bâtiments/étab.": st.column_config.NumberColumn(format="%.2f"),
        }
    )
else:
    st.info("Aucune donnée pour cette sélection")

# ============= FOOTER =============
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888; font-size: 12px;'>"
    "Sources: geodata.gouv.tg, opendata.gouv.tg — Togo AI Lab Data Challenge Education"
    "</p>",
    unsafe_allow_html=True
)
