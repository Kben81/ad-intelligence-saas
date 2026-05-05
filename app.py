import streamlit as st
import random
import requests
from datetime import datetime

from core.trends import get_trend
from core.scoring import calculate_opportunity
from database import init_db, create_user, login_user, save_analysis, get_history

st.set_page_config(page_title="Ad Intelligence SaaS", layout="wide")

init_db()

st.title("📊 Ad Intelligence SaaS (LEVEL 8 💰)")

# -----------------------
# AUTH SYSTEM
# -----------------------
menu = st.sidebar.selectbox("Menu", ["Login", "Créer un compte"])

if "user" not in st.session_state:
    st.session_state["user"] = None

if menu == "Créer un compte":
    st.subheader("Créer un compte")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Créer"):
        if create_user(new_user, new_pass):
            st.success("Compte créé ✔")
        else:
            st.error("Utilisateur déjà existant ❌")

    st.stop()

elif menu == "Login":
    st.subheader("Connexion")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Se connecter"):
        if login_user(username, password):
            st.session_state["user"] = username
            st.success("Connecté ✔")
        else:
            st.error("Identifiants incorrects ❌")

    if not st.session_state["user"]:
        st.stop()

user = st.session_state["user"]

st.success(f"👤 Connecté : {user}")


# -----------------------
# BUZZ
# -----------------------
def get_buzz(keyword):
    try:
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": keyword,
            "mode": "timelinevol",
            "format": "json",
            "timespan": "7d"
        }

        r = requests.get(url, params=params, timeout=10)

        if r.status_code != 200:
            return 10

        data = r.json()

        if "timeline" not in data:
            return 10

        timeline = data["timeline"]

        if not timeline:
            return 10

        return len(timeline[0].get("data", [])) * 2

    except:
        return 10


# -----------------------
# INPUT
# -----------------------
keyword = st.text_input("Mot-clé", "sérum visage")


# -----------------------
# ANALYSE
# -----------------------
if st.button("🚀 Analyser"):

    trend = get_trend(keyword)

    competition = max(
        5,
        min(
            100,
            int((100 - trend) * 0.7 + random.randint(5, 20))
        )
    )

    buzz = get_buzz(keyword)

    opportunity, level = calculate_opportunity(
        trend + buzz * 0.3,
        competition
    )

    if competition < 40 and trend > 40:
        platform = "Meta Ads"
    elif trend > 60:
        platform = "Google Ads"
    else:
        platform = "TikTok Ads"

    col1, col2, col3 = st.columns(3)

    col1.metric("📈 Demande", round(trend, 1))
    col2.metric("📊 Concurrence", competition)
    col3.metric("🔥 Buzz", buzz)

    st.subheader("🧠 Résultat")
    st.success(level)
    st.info(platform)

    save_analysis({
        "user": user,
        "keyword": keyword,
        "trend": trend,
        "competition": competition,
        "buzz": buzz,
        "opportunity": opportunity,
        "level": level,
        "platform": platform,
        "date": str(datetime.now())
    })


# -----------------------
# HISTORY
# -----------------------
st.subheader("📚 Ton historique")

rows = get_history(user)

for r in rows:
    st.write({
        "keyword": r[0],
        "trend": r[1],
        "competition": r[2],
        "buzz": r[3],
        "opportunity": r[4],
        "level": r[5],
        "platform": r[6],
        "date": r[7]
    })