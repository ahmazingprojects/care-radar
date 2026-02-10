import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

st.title("Continuum of Care Radar")

if "clients" not in st.session_state:
    st.session_state.clients = []

# ---- Add client form ----
st.header("Add Client")

with st.form("new_client"):
    name = st.text_input("Client Name")
    last_seen = st.date_input("Last Seen", value=date.today())
    submitted = st.form_submit_button("Add")

    if submitted and name:
        due_30 = last_seen + timedelta(days=30)

        st.session_state.clients.append({
            "Client": name,
            "30-Day Due": due_30.strftime("%Y-%m-%d")
        })

# ---- Build dataframe ----
df = pd.DataFrame(st.session_state.clients)

today = date.today()

def status(d):
    d = datetime.strptime(d, "%Y-%m-%d").date()
    if d < today:
        return "❌ Overdue"
    if (d - today).days <= 7:
        return "⚠ Due soon"
    return "✅ OK"

if not df.empty:
    df["Status"] = df["30-Day Due"].apply(status)

    st.header("Caseload")
    st.dataframe(df)
else:
    st.info("No clients yet. Add one above.")
