import streamlit as st
import random
from datetime import datetime
import pandas as pd

from core.trends import get_trend
from core.scoring import calculate_opportunity

from database import (
    init_db,
    create_user,
    login_user,
    get_plan,
    save_analysis,
    get_user_analyses
)

# -----------------------
# INIT
# -----------------------
init_db()

st.set_page_config(
    page_title="Ad Intelligence PRO",
    page_icon="📊",
    layout="wide"
)

# -----------------------
# STATE
# -----------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "payment_success" not in st.session_state:
    st.session_state.payment_success = False

# -----------------------
# AUTH
# -----------------------
if not st.session_state.user:

    st.title("📊 Ad Intelligence SaaS")
    st.caption("Analyse marché + opportunités publicitaires")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Login")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(u, p)
            if user:
                st.session_state.user = user[0]
                st.rerun()
            else:
                st.error("Identifiants incorrects")

    with col2:
        st.subheader("Créer compte")
        u2 = st.text_input("New username")
        p2 = st.text_input("New password", type="password")

        if st.button("Créer compte"):
            if create_user(u2, p2):
                st.success("Compte créé")
            else:
                st.error("Utilisateur déjà existant")

    st.stop()

# -----------------------
# USER INFO
# -----------------------
user = st.session_state.user
plan = "pro" if st.session_state.payment_success else get_plan(user)
history = get_user_analyses(user)

# -----------------------
# HEADER PRO
# -----------------------
st.title("📊 Ad Intelligence PRO Dashboard")
st.caption(f"👤 {user} • Plan: {plan.upper()}")

st.divider()

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.title("⚙️ Analyse")

keyword = st.sidebar.text_input("Mot-clé", "sérum visage")
mode = st.sidebar.selectbox("Mode analyse", ["Standard", "Avancé"])

st.sidebar.divider()
st.sidebar.info("💡 SaaS Marketing Intelligence Engine")

# -----------------------
# LIMIT FREE
# -----------------------
if plan == "free" and len(history) >= 5:
    st.error("❌ Limite Free atteinte (5 analyses)")
    st.stop()

# -----------------------
# ANALYSE
# -----------------------
if st.button("🚀 Lancer analyse", use_container_width=True):

    trend = get_trend(keyword)
    competition = max(5, min(100, int(100 - trend + random.randint(-10, 10))))
    opportunity, level = calculate_opportunity(trend, competition)

    platform = (
        "Meta Ads" if competition < 40 else
        "Google Ads" if trend > 60 else
        "TikTok Ads"
    )

    save_analysis({
        "username": user,
        "keyword": keyword,
        "trend": trend,
        "competition": competition,
        "opportunity": opportunity,
        "platform": platform,
        "date": str(datetime.now())
    })

    # -----------------------
    # KPI CARDS (PRO STYLE)
    # -----------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📈 Demande", f"{trend:.1f}")
    col2.metric("📊 Concurrence", competition)
    col3.metric("🧠 Opportunité", f"{opportunity:.1f}")
    col4.metric("🎯 Plateforme", platform)

    st.divider()

    # -----------------------
    # GRAPH INSIGHT
    # -----------------------
    st.subheader("📊 Évolution du marché")

    data = [trend + random.randint(-8, 8) for _ in range(12)]
    df = pd.DataFrame({"trend": data})

    st.line_chart(df)

    st.divider()

    # -----------------------
    # ANALYSIS BLOCK
    # -----------------------
    left, right = st.columns(2)

    with left:
        st.subheader("🧠 Analyse marché")

        if opportunity > 70:
            st.success("🔥 Marché excellent")
        elif opportunity > 40:
            st.warning("⚖️ Marché moyen")
        else:
            st.error("⚠️ Marché difficile")

        st.info(level)

    with right:
        st.subheader("📈 Score global")

        score = (trend * 0.4 + (100 - competition) * 0.4 + opportunity * 0.2)

        st.metric("Market Score", f"{score:.1f}/100")

        if score > 70:
            st.success("🔥 Fort potentiel de scalabilité")
        elif score > 40:
            st.warning("⚖️ Potentiel moyen")
        else:
            st.error("⚠️ Risque élevé")

    st.divider()

    # -----------------------
    # STRATEGY
    # -----------------------
    st.subheader("📌 Recommandation stratégique")

    if trend < 30:
        st.write("👉 Créer la demande (contenu / branding)")
    elif trend > 60:
        st.write("👉 Scaler rapidement (ads agressives)")
    else:
        st.write("👉 Tester et optimiser")

# -----------------------
# HISTORY
# -----------------------
st.divider()
st.subheader("📚 Historique utilisateur")

if history:
    for row in history:
        st.write(row)
else:
    st.info("Aucune donnée")

# -----------------------
# PAYPAL FINAL
# -----------------------
st.divider()

st.subheader("💰 Passer en Pro")

paypal_button = """
<script src="https://www.paypal.com/sdk/js?client-id=ASBpxQl2J7S7VTBDBJVRW8t4h8DOIjE9XwHNbM9uTtKgbCs4q97N79A5gn-X76yjb927dCKpHfYfD1r6&currency=EUR"></script>

<div style="display:flex; justify-content:center; margin-top:20px;">
    <div id="paypal-button-container"></div>
</div>

<script>
paypal.Buttons({
    style: {
        layout: 'vertical',
        color: 'blue',
        shape: 'rect',
        label: 'paypal'
    },
    createOrder: function(data, actions) {
        return actions.order.create({
            purchase_units: [{
                amount: { value: '9.99' }
            }]
        });
    },
    onApprove: function(data, actions) {
        return actions.order.capture().then(function() {
            alert('🚀 Upgrade Pro activé - Bienvenue !');
        });
    }
}).render('#paypal-button-container');
</script>
"""

st.components.v1.html(paypal_button, height=350)