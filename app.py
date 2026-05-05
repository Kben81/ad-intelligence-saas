import streamlit as st
import random

from core.trends import get_trend
from core.scoring import calculate_opportunity

st.set_page_config(
    page_title="Ad Intelligence SaaS",
    page_icon="📊",
    layout="wide"
)

# -----------------------
# HEADER
# -----------------------
st.title("📊 Ad Intelligence SaaS")
st.caption("Analyse marché + opportunités publicitaires en temps réel")

st.divider()

# -----------------------
# INPUT
# -----------------------
keyword = st.text_input("🔍 Mot-clé à analyser", "sérum visage")

# -----------------------
# ACTION
# -----------------------
if st.button("🚀 Lancer l'analyse"):

    # DATA
    trend = get_trend(keyword)
    competition = max(5, min(100, int(100 - trend + random.randint(-10, 10))))
    opportunity, level = calculate_opportunity(trend, competition)

    # PLATFORM LOGIC
    if competition < 40 and trend > 40:
        platform = "Meta Ads (Facebook / Instagram)"
    elif trend > 60:
        platform = "Google Ads (Search / Shopping)"
    else:
        platform = "TikTok Ads"

    # -----------------------
    # KPI CARDS
    # -----------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📈 Demande", f"{trend:.1f}")

    with col2:
        st.metric("📊 Concurrence", competition)

    with col3:
        st.metric("🧠 Opportunité", f"{opportunity:.1f}")

    with col4:
        st.metric("🎯 Plateforme", platform)

    st.divider()

    # -----------------------
    # ANALYSIS SECTION
    # -----------------------
    st.subheader("🧠 Analyse marché")

    if opportunity > 70:
        st.success("🔥 Excellent marché : forte opportunité commerciale")
    elif opportunity > 40:
        st.warning("⚖️ Marché moyen : potentiel intéressant mais compétitif")
    else:
        st.error("⚠️ Marché difficile : faible opportunité")

    st.info(level)

    st.divider()

    # -----------------------
    # STRATEGY SECTION
    # -----------------------
    st.subheader("📌 Stratégie recommandée")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("### 🎯 Plateforme pub")
        st.success(platform)

        st.markdown("### 📊 Niveau de marché")
        st.write(level)

    with colB:
        st.markdown("### 💡 Recommandation rapide")

        if platform == "Meta Ads (Facebook / Instagram)":
            st.write("- Créatifs visuels + UGC")
            st.write("- Audience large + retargeting")

        elif platform == "Google Ads (Search / Shopping)":
            st.write("- Mots-clés intention achat")
            st.write("- Landing page optimisée")

        else:
            st.write("- Vidéos courtes virales")
            st.write("- Hook fort dans les 3 premières secondes")

    st.divider()

    # -----------------------
    # FOOTER INSIGHT
    # -----------------------
    st.caption("💡 Version SaaS MVP - Ad Intelligence Engine")