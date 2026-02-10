import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

st.title("Continuum of Care Radar")

DATA_FILE = "clients.csv"
columns = ["Client", "Last Seen", "Intake Complete", "Treatment Plan Date"]

# ---------- Load ----------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=columns)

for c in columns:
    if c not in df.columns:
        df[c] = ""

def to_bool(v):
    if isinstance(v, bool):
        return v
    return str(v).lower() in ["true", "1", "yes", "y"]

df["Intake Complete"] = df["Intake Complete"].apply(to_bool)

today = date.today()

def days_since(d):
    if not d or str(d).lower() == "nan":
        return 10**9
    s = str(d)
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return (today - datetime.strptime(s, fmt).date()).days
        except:
            pass
    return 10**9

def status(days, good, warn):
    if days > warn:
        return "❌ Overdue"
    if days > good:
        return "⚠ Due soon"
    return "✅ OK"

# ---------- Add client ----------
st.header("Add Client")

with st.form("new"):
    name = st.text_input("Client Name")
    last_seen = st.date_input("Last Seen", today)
    intake = st.checkbox("Intake complete?", True)
    tp = st.date_input("Treatment plan date", today)
    submit = st.form_submit_button("Add")

    if submit and name:
        new = {
            "Client": name,
            "Last Seen": last_seen.strftime("%Y-%m-%d"),
            "Intake Complete": intake,
            "Treatment Plan Date": tp.strftime("%Y-%m-%d")
        }
        df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

# ---------- Compute ----------
def compute(row):
    intake_status = "✅ OK" if row["Intake Complete"] else "❌ Missing"

    seen_days = days_since(row["Last Seen"])
    seen_status = status(seen_days, 21, 30)

    tp_days = days_since(row["Treatment Plan Date"])
    tp_status = status(tp_days, 75, 90)

    if not row["Intake Complete"]:
        next_action = "Complete intake"
        urgency = 100
    elif seen_status == "❌ Overdue":
        next_action = "Schedule visit"
        urgency = 90
    elif tp_status == "❌ Overdue":
        next_action = "Update treatment plan"
        urgency = 80
    else:
        next_action = "No action needed"
        urgency = 0

    return pd.Series({
        "Intake Status": intake_status,
        "Seen Status": seen_status,
        "TP Status": tp_status,
        "Next Action": next_action,
        "Urgency": urgency
    })

if not df.empty:
    view = pd.concat([df, df.apply(compute, axis=1)], axis=1)
    view = view.sort_values("Urgency", ascending=False)

    st.header("Caseload (Most urgent first)")
    st.dataframe(view[["Client","Next Action","Urgency"]])

    st.header("Continuum Checklist")

    for _, row in view.iterrows():
        with st.expander(row["Client"]):
            st.write("Intake:", row["Intake Status"])
            st.write("Last seen:", row["Seen Status"])
            st.write("Treatment plan:", row["TP Status"])
else:
    st.info("No clients yet.")
