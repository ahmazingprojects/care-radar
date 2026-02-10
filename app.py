import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import os

st.title("Continuum of Care Radar")

DATA_FILE = "clients.csv"

columns = ["Client", "Last Seen", "Intake Complete", "Treatment Plan Date"]

# ---------- Load ----------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=columns)

# ---------- Migration / safety ----------
for c in columns:
    if c not in df.columns:
        df[c] = ""

def to_bool(v):
    if isinstance(v, bool):
        return v
    s = str(v).strip().lower()
    return s in ["true", "1", "yes", "y"]

df["Intake Complete"] = df["Intake Complete"].apply(to_bool)

# ---------- Date parsing that won't explode ----------
today = date.today()

def days_since(d):
    if d is None:
        return 10**9
    s = str(d).strip()
    if s == "" or s.lower() == "nan":
        return 10**9
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return (today - datetime.strptime(s, fmt).date()).days
        except ValueError:
            pass
    return 10**9

def status_from_days(days, good, warn):
    if days > warn:
        return "❌ Overdue"
    if days > good:
        return "⚠ Due soon"
    return "✅ OK"

# ---------- Add client ----------
st.header("Add Client")

with st.form("new_client"):
    name = st.text_input("Client Name")
    last_seen = st.date_input("Last Seen", value=today)
    intake = st.checkbox("Intake complete?", value=True)
    tp_date = st.date_input("Treatment plan date", value=today)
    submitted = st.form_submit_button("Add")

    if submitted and name:
        new = {
            "Client": name,
            "Last Seen": last_seen.strftime("%Y-%m-%d"),
            "Intake Complete": bool(intake),
            "Treatment Plan Date": tp_date.strftime("%Y-%m-%d"),
        }
        df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

# ---------- Compute continuum + next action ----------
def compute_row(row):
    intake_ok = bool(row["Intake Complete"])
    intake_status = "✅ OK" if intake_ok else "❌ Missing"

    tp_days = days_since(row["Treatment Plan Date"])
    tp_status = status_from_days(tp_days, good=75, warn=90)

    seen_days = days_since(row["Last Seen"])
    seen_status = status_from_days(seen_days, good=21, warn=30)

    # Next action logic (simple, but useful)
    if not intake_ok:
        next_action = "Complete intake"
        urgency = 100
    elif seen_status == "❌ Overdue":
        next_action = "Schedule / outreach (no recent visit)"
        urgency = 90 + min(seen_days, 60)
    elif tp_status == "❌ Overdue":
        next_action = "Update treatment plan"
        urgency = 80 + min(tp_days, 60)
    elif seen_status == "⚠ Due soon":
        next_action = "Follow up soon"
        urgency = 50 + min(seen_days, 30)
    elif tp_status == "⚠ Due soon":
        next_action = "Prep treatment plan update"
        urgency = 40 + min(tp_days, 30)
    else:
        next_action = "No action needed"
        urgency = 0

    # Overall status = worst
    statuses = [intake_status, tp_status, seen_status]
    if "❌ Overdue" in statuses or "❌ Missing" in statuses:
        overall = "❌ Needs attention"
    elif "⚠ Due soon" in statuses:
        overall = "⚠ Watch"
    else:
        overall = "✅ OK"

    return pd.Series({
        "Intake Status": intake_status,
        "Treatment Plan Status": tp_status,
        "Last Seen Status": seen_status,
        "Overall": overall,
        "Next Action": next_action,
        "Urgency": urgency,
        "Days Since Seen": seen_days,
        "Days Since TP": tp_days,
    })

if not df.empty:
    computed = df.apply(compute_row, axis=1)
    view = pd.concat([df, computed], axis=1)
    view = view.sort_values("Urgency", ascending=False)

    st.header("Caseload (Most urgent first)")
    st.dataframe(
        view[["Client","Overall","Next Action","Urgency","Intake Status","Last Seen Status","Treatment Plan Status"]],
        use_container_width=True
    )

    st.header("Continuum Checklist")

for _, row in view.iterrows():
    with st.expander(f"{row['Client']} — {row['Overall']} — {row['Next Action']}"):
        st.write(f"Intake: {row['Intake Status']}")
        st.write(f"Last seen: {row['Last Seen Status']} ({int(row['Days Since Seen'])} days)")
        st.write(f"Treatment plan: {row['Treatment Plan Status']} ({int(row['Days Since TP'])} days)")
else:
    st.info("No clients yet.")

            st.write(f"Intake: {intake_status}")
            st.write(f"Treatment plan: {tp_status}")
            st.write(f"Last seen: {seen_status}")
