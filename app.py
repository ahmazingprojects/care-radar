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

today = date.today()

def status(d):
    d = datetime.strptime(d, "%Y-%m-%d").date()
    if d < today:
        return "❌ Overdue"
    if (d - today).days <= 7:
        return "⚠ Due soon"
    return "✅ OK"

def priority(s):
    if s == "❌ Overdue":
        return 0
    if s == "⚠ Due soon":
        return 1
    return 2

# ---- Add client form ----
st.header("Add Client")
with st.form("new_client"):
    name = st.text_input("Client Name")
    last_seen = st.date_input("Last Seen", value=date.today())
    submitted = st.form_submit_button("Add")

    if submitted and name:
        due_30 = last_seen + timedelta(days=30)
        new_row = {"Client": name, "30-Day Due": due_30.strftime("%Y-%m-%d")}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Added {name}")

# ---- Compute status ----
if not df.empty:
    df["Status"] = df["30-Day Due"].apply(status)
    df["Priority"] = df["Status"].apply(priority)

# ---- Summary cards ----
st.header("Radar Summary")

if df.empty:
    st.info("No clients yet. Add one above.")
    st.stop()

ok_count = (df["Status"] == "✅ OK").sum()
soon_count = (df["Status"] == "⚠ Due soon").sum()
overdue_count = (df["Status"] == "❌ Overdue").sum()

c1, c2, c3 = st.columns(3)
c1.metric("✅ OK", int(ok_count))
c2.metric("⚠ Due soon", int(soon_count))
c3.metric("❌ Overdue", int(overdue_count))

# ---- Filters ----
st.subheader("Filters")
col1, col2 = st.columns(2)
with col1:
    show_overdue = st.checkbox("Show overdue only", value=False)
with col2:
    show_due_soon = st.checkbox("Show due soon only", value=False)

view = df.copy()

if show_overdue:
    view = view[view["Status"] == "❌ Overdue"]
if show_due_soon:
    view = view[view["Status"] == "⚠ Due soon"]

# sort by urgency, then by due date
view = view.sort_values(by=["Priority", "30-Day Due"], ascending=[True, True])

st.header("Caseload (Most urgent first)")
st.dataframe(view.drop(columns=["Priority"]), use_container_width=True)

# ---- Delete client ----
st.subheader("Remove a client")
to_delete = st.selectbox("Select client to remove", options=["(none)"] + df["Client"].tolist())

if st.button("Delete selected client"):
    if to_delete != "(none)":
        df = df[df["Client"] != to_delete].copy()
        df.drop(columns=[c for c in ["Status", "Priority"] if c in df.columns], inplace=True, errors="ignore")
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Deleted {to_delete}. Refreshing...")
        st.rerun()
