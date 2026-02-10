import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import os

st.title("Continuum of Care Radar")



columns = [
    "Client",
    "Last Seen",
    "Intake Complete",
    "Treatment Plan Date",
]
DATA_FILE = "clients.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=columns)

# -------- Add client --------
st.header("Add Client")

with st.form("new_client"):
    name = st.text_input("Client Name")
    last_seen = st.date_input("Last Seen", value=date.today())
    intake = st.checkbox("Intake complete?", value=True)
    tp_date = st.date_input("Treatment plan date", value=date.today())

    submitted = st.form_submit_button("Add")

    if submitted and name:
        new = {
            "Client": name,
            "Last Seen": last_seen.strftime("%Y-%m-%d"),
            "Intake Complete": intake,
            "Treatment Plan Date": tp_date.strftime("%Y-%m-%d"),
        }
        df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

# -------- Status logic --------

today = date.today()

def days_since(d):
    return (today - datetime.strptime(d, "%Y-%m-%d").date()).days

def task_status(days, good, warn):
    if days > warn:
        return "❌ Overdue"
    if days > good:
        return "⚠ Due soon"
    return "✅ OK"

# -------- Client continuum view --------

st.header("Continuum Checklist")

if df.empty:
    st.info("No clients yet.")
else:
    for i, row in df.iterrows():
        with st.expander(f"{row['Client']}"):

            intake_status = "✅ OK" if row["Intake Complete"] else "❌ Missing"

            tp_days = days_since(row["Treatment Plan Date"])
            tp_status = task_status(tp_days, 75, 90)

            seen_days = days_since(row["Last Seen"])
            seen_status = task_status(seen_days, 21, 30)

            st.write(f"Intake: {intake_status}")
            st.write(f"Treatment plan: {tp_status}")
            st.write(f"Last seen: {seen_status}")
