import streamlit as st
import pandas as pd
from datetime import date, datetime

st.title("Continuum of Care Radar")

rows = [
    {"Client": "Client A", "30-Day Due": "2026-02-10"},
    {"Client": "Client B", "30-Day Due": "2026-01-15"},
]

df = pd.DataFrame(rows)

today = date.today()

def status(d):
    d = datetime.strptime(d, "%Y-%m-%d").date()
    if d < today:
        return "❌ Overdue"
    if (d - today).days < 7:
        return "⚠ Due soon"
    return "✅ OK"

df["Status"] = df["30-Day Due"].apply(status)

st.dataframe(df)
