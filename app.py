import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import os

st.title("Continuum of Care Radar")

DATA_FILE = "clients.csv"

# ---- Load saved data ----
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Client", "30-Day Due"])

# ---- Add client form ----
st.header("Add Client")

with st.form("new_client"):
    name = st.text_input("Client Name")
    last_seen = st.date_input("Last Seen", value=date.today())
    submitted = st.form_submit_button("Add")

    if submitted and name:
        due_30 = last_seen + timedelta(days=30)
        new_row = {
            "Client": name,
            "30-Day Due": due_30.strftime("%Y-%m-%d")
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

# ---- Status logic ----
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
