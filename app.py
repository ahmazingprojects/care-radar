"""
OMNIVEIL — CLINICAL RADAR
"""
import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import os

st.set_page_config(page_title="Omniveil — Caseload Manager", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp { background-color: #f7f6f3; color: #1a1a2e; font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem 2.5rem; max-width: 1300px; }

.top-bar { display: flex; align-items: center; justify-content: space-between; padding-bottom: 20px; margin-bottom: 28px; border-bottom: 1px solid #e8e5df; }
.brand { display: flex; align-items: center; gap: 12px; }
.brand-icon { width: 38px; height: 38px; background: #2d6a4f; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
.brand-name { font-family: 'DM Serif Display', serif; font-size: 22px; color: #1a1a2e; letter-spacing: -0.5px; line-height: 1; }
.brand-tagline { font-size: 11px; color: #8a8a9a; letter-spacing: 0.5px; margin-top: 2px; }
.top-date { font-size: 13px; color: #8a8a9a; }

.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }
.stat-card { background: white; border-radius: 14px; padding: 20px 22px; border: 1px solid #e8e5df; box-shadow: 0 1px 3px rgba(0,0,0,0.04); display: flex; align-items: center; gap: 16px; }
.stat-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.stat-icon.teal { background: #e8f4f0; } .stat-icon.red { background: #fdecea; } .stat-icon.amber { background: #fef6e4; } .stat-icon.blue { background: #e8f0fe; }
.stat-number { font-size: 32px; font-weight: 600; line-height: 1; letter-spacing: -1px; }
.stat-card.teal-card .stat-number { color: #2d6a4f; } .stat-card.red-card .stat-number { color: #c0392b; } .stat-card.amber-card .stat-number { color: #d4880a; } .stat-card.blue-card .stat-number { color: #2563eb; }
.stat-label { font-size: 12px; color: #8a8a9a; font-weight: 500; margin-top: 3px; }

.section-head { font-size: 13px; font-weight: 600; color: #8a8a9a; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px; }

.table-head { display: grid; grid-template-columns: 36px 2.2fr 150px 90px 90px 90px 2fr 90px 44px; gap: 12px; padding: 0 16px 10px 16px; font-size: 11px; font-weight: 600; color: #a0a0b0; letter-spacing: 0.8px; text-transform: uppercase; border-bottom: 2px solid #e8e5df; margin-bottom: 6px; }

.patient-row { background: white; border: 1px solid #e8e5df; border-radius: 12px; padding: 14px 16px; margin-bottom: 4px; display: grid; grid-template-columns: 36px 2.2fr 150px 90px 90px 90px 2fr 90px 44px; align-items: center; gap: 12px; transition: box-shadow 0.15s; }
.patient-row:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.07); border-color: #d0cdc6; }
.patient-row.flag-red   { border-left: 4px solid #e74c3c; }
.patient-row.flag-amber { border-left: 4px solid #f39c12; }
.patient-row.flag-teal  { border-left: 4px solid #2d6a4f; }
.patient-row.flag-blue  { border-left: 4px solid #2563eb; }

.rank-num { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; }
.rank-num.critical { background: #fdecea; color: #c0392b; }
.rank-num.warning  { background: #fef6e4; color: #d4880a; }
.rank-num.normal   { background: #e8f4f0; color: #2d6a4f; }

.client-name { font-size: 15px; font-weight: 600; color: #1a1a2e; }
.client-sub  { font-size: 11px; color: #a0a0b0; margin-top: 2px; }

.pill { display: inline-flex; align-items: center; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; white-space: nowrap; }
.pill-red   { background: #fdecea; color: #c0392b; }
.pill-amber { background: #fef6e4; color: #d4880a; }
.pill-teal  { background: #e8f4f0; color: #2d6a4f; }
.pill-blue  { background: #e8f0fe; color: #2563eb; }

.metric-cell { text-align: center; }
.metric-val  { font-size: 15px; font-weight: 600; line-height: 1.1; }
.metric-val.ok      { color: #2d6a4f; }
.metric-val.warn    { color: #d4880a; }
.metric-val.overdue { color: #c0392b; }
.metric-val.na      { color: #c0c0d0; }
.metric-lbl { font-size: 10px; color: #b0b0c0; font-weight: 500; margin-top: 2px; }

.next-action        { font-size: 12px; color: #5a5a7a; line-height: 1.5; }
.next-action.urgent { color: #c0392b; font-weight: 500; }

.urgency-wrap  { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; }
.urgency-track { width: 100%; height: 5px; background: #f0ede8; border-radius: 3px; overflow: hidden; }
.urgency-fill  { height: 100%; border-radius: 3px; }
.urgency-label { font-size: 10px; color: #a0a0b0; font-weight: 500; }

.profile-panel { background: #fafaf8; border: 1px solid #e8e5df; border-top: none; border-radius: 0 0 12px 12px; padding: 20px 20px 16px 20px; margin-top: -4px; margin-bottom: 4px; }
.profile-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 14px; }
.profile-field { background: white; border-radius: 8px; padding: 10px 12px; border: 1px solid #e8e5df; }
.profile-label { font-size: 10px; font-weight: 600; color: #a0a0b0; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 3px; }
.profile-value { font-size: 13px; font-weight: 500; color: #1a1a2e; }
.action-box { border-radius: 8px; padding: 12px 16px; margin-bottom: 14px; }
.action-box.ok     { background: #e8f4f0; }
.action-box.urgent { background: #fdecea; }
.action-box-label { font-size: 10px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 3px; }
.action-box-label.ok     { color: #2d6a4f; }
.action-box-label.urgent { color: #c0392b; }
.action-box-text { font-size: 13px; font-weight: 500; color: #1a1a2e; }
.edit-section-label { font-size: 11px; font-weight: 700; color: #a0a0b0; letter-spacing: 0.8px; text-transform: uppercase; padding-top: 12px; margin-top: 8px; border-top: 1px solid #e8e5df; margin-bottom: 10px; }

.stTextInput > div > div > input, .stTextArea > div > div > textarea { background: white !important; border: 1px solid #e0ddd8 !important; border-radius: 8px !important; color: #1a1a2e !important; font-size: 14px !important; padding: 10px 14px !important; }
.stSelectbox > div > div { background: white !important; border: 1px solid #e0ddd8 !important; border-radius: 8px !important; }
label, .stCheckbox > label > span { color: #5a5a7a !important; font-size: 13px !important; font-weight: 500 !important; }
.stDateInput > div > div > input { background: white !important; border: 1px solid #e0ddd8 !important; border-radius: 8px !important; color: #1a1a2e !important; }
.stButton > button { background: #2d6a4f !important; border: none !important; color: white !important; font-size: 13px !important; font-weight: 600 !important; border-radius: 8px !important; padding: 10px 22px !important; }
.stButton > button:hover { background: #245a40 !important; }
.toggle-btn > button { background: #f0ede8 !important; color: #5a5a7a !important; font-size: 11px !important; font-weight: 600 !important; padding: 4px 10px !important; border-radius: 6px !important; }
.toggle-btn > button:hover { background: #e0ddd8 !important; }

.empty-state { text-align: center; padding: 72px 0; }
.empty-icon  { font-size: 48px; margin-bottom: 16px; }
.empty-text  { font-size: 16px; font-weight: 500; color: #a0a0b0; }
.empty-sub   { font-size: 13px; margin-top: 6px; color: #c0c0d0; }
hr { border-color: #e8e5df !important; }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "clients.csv"
columns = ["Client","DOB","Intake Date","Last Seen","Intake Complete","Treatment Plan Date","Discharge Ready","Notes","PHQ-9 Completed Date","GAD-7 Completed Date"]

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=columns)

for c in columns:
    if c not in df.columns:
        df[c] = ""

def to_bool(v):
    if isinstance(v, bool): return v
    return str(v).lower() in ["true","1","yes","y"]

for col in ["PHQ-9 Complete","GAD-7 Complete","PHQ-9 Due Date","GAD-7 Due Date","90-Day Complete","90-Day Due Date","Continuum Status"]:
    if col in df.columns:
        df = df.drop(columns=[col], errors="ignore")

for col in ["DOB","Intake Date","Last Seen","Treatment Plan Date","PHQ-9 Completed Date","GAD-7 Completed Date"]:
    if col not in df.columns:
        df[col] = ""

df["Notes"] = df["Notes"].fillna("").astype(str)
df["DOB"] = df["DOB"].fillna("").astype(str)
df["PHQ-9 Completed Date"] = df["PHQ-9 Completed Date"].fillna("").astype(str)
df["GAD-7 Completed Date"] = df["GAD-7 Completed Date"].fillna("").astype(str)
if "Discharge Ready" not in df.columns:
    df["Discharge Ready"] = False
df["Discharge Ready"] = df["Discharge Ready"].fillna(False).apply(to_bool)

# Deduplicate on load - keep last entry for each name
df = df.drop_duplicates(subset=["Client"], keep="last").reset_index(drop=True)
df.to_csv(DATA_FILE, index=False)

today = date.today()
min_dob = date(today.year - 100, 1, 1)

def _parse_date(d):
    if d is None or (isinstance(d, float) and pd.isna(d)) or str(d).strip() == "":
        return None
    s = str(d).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except:
            pass
    return None

def _derive_intake_complete(row):
    if _parse_date(row.get("Intake Date","")) is not None:
        return True
    return to_bool(row.get("Intake Complete", False))

df["Intake Complete"] = df.apply(_derive_intake_complete, axis=1)

def days_since(d):
    parsed = _parse_date(d)
    return (today - parsed).days if parsed else None

def compute_90_day(phq9_date_str, gad7_date_str):
    phq9_d = _parse_date(phq9_date_str)
    gad7_d = _parse_date(gad7_date_str)
    if phq9_d is None and gad7_d is None:
        return {"pct_complete":0,"next_90_due":None,"status_label":"Not started","urgency_90":40,"is_overdue":False,"due_within_2_weeks":False}
    base = min(d for d in [phq9_d, gad7_d] if d is not None)
    days_since_base = (today - base).days
    k = max(0, days_since_base // 90)
    cycle_start = base + timedelta(days=90*k)
    cycle_end = base + timedelta(days=90*(k+1))
    in_phq9 = phq9_d is not None and cycle_start <= phq9_d < cycle_end
    in_gad7 = gad7_d is not None and cycle_start <= gad7_d < cycle_end
    pct = sum([in_phq9, in_gad7]) * 50
    prev_complete = 2
    if k >= 1:
        ps = base + timedelta(days=90*(k-1))
        pe = base + timedelta(days=90*k)
        prev_complete = sum([phq9_d is not None and ps <= phq9_d < pe, gad7_d is not None and ps <= gad7_d < pe])
    is_overdue = k >= 1 and prev_complete < 2
    due_2wk = (cycle_end - today).days <= 14
    if is_overdue:   sl, u = "Overdue", 88
    elif due_2wk:    sl, u = "Due in 2 weeks", 72
    elif pct == 100: sl, u = "Complete", 40
    elif pct == 50:  sl, u = "In progress (50%)", 55
    else:            sl, u = "Not started", 45
    return {"pct_complete":pct,"next_90_due":cycle_end,"status_label":sl,"urgency_90":u,"is_overdue":is_overdue,"due_within_2_weeks":due_2wk}

def compute_continuum_status(row, ninety, seen_days, tp_days):
    sd = seen_days if seen_days is not None else 10**9
    td = tp_days if tp_days is not None else 10**9
    if ninety.get("is_overdue") or td > 90:
        reasons = []
        if ninety.get("is_overdue"): reasons.append("90-day assessment")
        if td > 90: reasons.append("treatment plan")
        return ("Compliance Risk","Complete overdue: " + " & ".join(reasons),100)
    if not row["Intake Complete"]:
        return ("Intake Pending","Complete intake documentation",95)
    if sd > 30:
        return ("Needs Scheduling",f"Schedule visit — last seen {sd} days ago",85)
    pct = ninety["pct_complete"]
    if pct == 100 and td <= 75 and sd <= 30 and row.get("Discharge Ready",False):
        return ("Discharge Ready","Client ready for discharge",40)
    if pct == 100 and 75 < td <= 90:
        return ("Maintenance","Treatment plan renewal coming up",55)
    if pct >= 50:
        if ninety.get("due_within_2_weeks"):
            return ("Active Treatment","90-day assessment due within 2 weeks",70)
        if 75 < td <= 90:
            return ("Active Treatment","Treatment plan due soon",70)
        return ("Active Treatment","Complete 90-day assessment (1 of 2 done)" if pct==50 else "On track — no action needed", 70 if pct==50 else 58)
    return ("Active Treatment","Schedule PHQ-9 and GAD-7 assessments",65)

def compute(row):
    sd = days_since(row["Last Seen"])
    td = days_since(row["Treatment Plan Date"])
    ninety = compute_90_day(row["PHQ-9 Completed Date"], row["GAD-7 Completed Date"])
    status_label, next_action, urgency = compute_continuum_status(row, ninety, sd, td)
    return pd.Series({
        "Continuum Status":status_label,"Seen Days":sd,"TP Days":td,
        "90-Day Pct":ninety["pct_complete"],"90-Day Status":ninety["status_label"],
        "90-Day Next Due":ninety["next_90_due"].strftime("%b %d, %Y") if ninety["next_90_due"] else "—",
        "Next Action":next_action,"Urgency":urgency,
    })

if "expanded" not in st.session_state:
    st.session_state.expanded = {}

# ── HEADER ──────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-bar">
  <div class="brand">
    <div class="brand-icon">🌿</div>
    <div><div class="brand-name">Omniveil</div><div class="brand-tagline">Caseload Intelligence</div></div>
  </div>
  <div class="top-date">{today.strftime("%A, %B %d, %Y")}</div>
</div>
""", unsafe_allow_html=True)

if not df.empty:
    view = pd.concat([df, df.apply(compute, axis=1)], axis=1)
    view = view.sort_values("Urgency", ascending=False).reset_index(drop=True)
    total            = len(view)
    non_compliant    = len(view[view["Continuum Status"]=="Compliance Risk"])
    needs_scheduling = len(view[view["Continuum Status"]=="Needs Scheduling"])
    intake_pending   = len(view[view["Continuum Status"]=="Intake Pending"])

    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-card teal-card"><div class="stat-icon teal">👥</div><div><div class="stat-number">{total}</div><div class="stat-label">Total Caseload</div></div></div>
      <div class="stat-card red-card"><div class="stat-icon red">⚠️</div><div><div class="stat-number">{non_compliant}</div><div class="stat-label">Non-Compliant</div></div></div>
      <div class="stat-card amber-card"><div class="stat-icon amber">📅</div><div><div class="stat-number">{needs_scheduling}</div><div class="stat-label">Need Scheduling</div></div></div>
      <div class="stat-card blue-card"><div class="stat-icon blue">📋</div><div><div class="stat-number">{intake_pending}</div><div class="stat-label">Intake Pending</div></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-head">Caseload · Sorted by Priority</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-head"><div></div><div>Client</div><div>Status</div><div style="text-align:center">Last Seen</div><div style="text-align:center">Tx Plan</div><div style="text-align:center">90-Day</div><div>Next Action</div><div style="text-align:right">Priority</div><div></div></div>', unsafe_allow_html=True)

    for i, (_, row) in enumerate(view.iterrows()):
        # Use i (position in sorted view) as unique key — never duplicates
        key = f"row_{i}"
        s   = row["Continuum Status"]
        u   = row["Urgency"]
        client_name = row["Client"]
        # Find original df index for saving
        matches = df[df["Client"]==client_name]
        idx = matches.index[0] if len(matches) > 0 else None

        if u >= 85:   rank_cls = "critical"
        elif u >= 65: rank_cls = "warning"
        else:         rank_cls = "normal"

        if s == "Compliance Risk":                       flag, pill_cls = "flag-red",   "pill-red"
        elif s in ("Intake Pending","Needs Scheduling"): flag, pill_cls = "flag-amber", "pill-amber"
        elif s == "Discharge Ready":                     flag, pill_cls = "flag-blue",  "pill-blue"
        else:                                            flag, pill_cls = "flag-teal",  "pill-teal"

        bar_color = "#e74c3c" if u>=85 else "#f39c12" if u>=60 else "#2d6a4f"

        sd = row.get("Seen Days")
        seen_val = "—" if sd is None else f"{sd}d"
        seen_cls = "na" if sd is None else "overdue" if sd>30 else "warn" if sd>21 else "ok"

        td = row.get("TP Days")
        tp_val = "—" if td is None else f"{td}d"
        tp_cls = "na" if td is None else "overdue" if td>90 else "warn" if td>75 else "ok"

        pct      = row["90-Day Pct"]
        pct_cls  = "overdue" if "Overdue" in row["90-Day Status"] else "warn" if pct<100 else "ok"
        next_act = row["Next Action"]
        action_cls = "urgent" if rank_cls == "critical" else ""

        dob_v      = row.get("DOB") or "—"
        intake_v   = row.get("Intake Date") or "—"
        last_seen_v= row.get("Last Seen") or "—"
        tp_date_v  = row.get("Treatment Plan Date") or "—"
        phq9_v     = row.get("PHQ-9 Completed Date") or "—"
        gad7_v     = row.get("GAD-7 Completed Date") or "—"
        next_due_v = row.get("90-Day Next Due") or "—"
        discharge_v= "Yes" if row.get("Discharge Ready") else "No"
        notes_v    = str(row.get("Notes") or "").strip()
        is_open    = st.session_state.expanded.get(key, False)

        row_cols = st.columns([36, 220, 150, 90, 90, 90, 200, 90, 44])
        with row_cols[0]:
            st.markdown(f'<div class="rank-num {rank_cls}" style="margin-top:6px;">{i+1}</div>', unsafe_allow_html=True)
        with row_cols[1]:
            st.markdown(f'<div class="client-name">{client_name}</div><div class="client-sub">DOB: {dob_v} · Intake: {intake_v}</div>', unsafe_allow_html=True)
        with row_cols[2]:
            st.markdown(f'<span class="pill {pill_cls}">{s}</span>', unsafe_allow_html=True)
        with row_cols[3]:
            st.markdown(f'<div class="metric-cell"><div class="metric-val {seen_cls}">{seen_val}</div><div class="metric-lbl">Last Seen</div></div>', unsafe_allow_html=True)
        with row_cols[4]:
            st.markdown(f'<div class="metric-cell"><div class="metric-val {tp_cls}">{tp_val}</div><div class="metric-lbl">Tx Plan Age</div></div>', unsafe_allow_html=True)
        with row_cols[5]:
            st.markdown(f'<div class="metric-cell"><div class="metric-val {pct_cls}">{pct}%</div><div class="metric-lbl">90-Day</div></div>', unsafe_allow_html=True)
        with row_cols[6]:
            st.markdown(f'<div class="next-action {action_cls}">{next_act}</div>', unsafe_allow_html=True)
        with row_cols[7]:
            st.markdown(f'<div class="urgency-wrap"><div class="urgency-label">{u}/100</div><div class="urgency-track"><div class="urgency-fill" style="width:{u}%;background:{bar_color};"></div></div></div>', unsafe_allow_html=True)
        with row_cols[8]:
            btn_label = "▲" if is_open else "▼"
            st.markdown('<div class="toggle-btn">', unsafe_allow_html=True)
            if st.button(btn_label, key=f"btn_{key}"):
                st.session_state.expanded[key] = not is_open
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:2px;"></div>', unsafe_allow_html=True)

        if is_open and idx is not None:
            action_box_cls   = "urgent" if rank_cls=="critical" else "ok"
            action_label_cls = "urgent" if rank_cls=="critical" else "ok"
            notes_block = f'<div style="background:white;border:1px solid #e8e5df;border-radius:8px;padding:10px 12px;margin-bottom:14px;"><div class="profile-label">Notes</div><div style="font-size:13px;color:#5a5a7a;margin-top:3px;">{notes_v}</div></div>' if notes_v else ""

            st.markdown(f"""
            <div class="profile-panel">
              <div class="action-box {action_box_cls}">
                <div class="action-box-label {action_label_cls}">Recommended Next Action</div>
                <div class="action-box-text">{next_act}</div>
              </div>
              <div class="profile-grid">
                <div class="profile-field"><div class="profile-label">Date of Birth</div><div class="profile-value">{dob_v}</div></div>
                <div class="profile-field"><div class="profile-label">Intake Date</div><div class="profile-value">{intake_v}</div></div>
                <div class="profile-field"><div class="profile-label">Last Seen</div><div class="profile-value">{last_seen_v}</div></div>
                <div class="profile-field"><div class="profile-label">Treatment Plan</div><div class="profile-value">{tp_date_v}</div></div>
                <div class="profile-field"><div class="profile-label">PHQ-9 Completed</div><div class="profile-value">{phq9_v}</div></div>
                <div class="profile-field"><div class="profile-label">GAD-7 Completed</div><div class="profile-value">{gad7_v}</div></div>
                <div class="profile-field"><div class="profile-label">Next 90-Day Due</div><div class="profile-value">{next_due_v}</div></div>
                <div class="profile-field"><div class="profile-label">Discharge Ready</div><div class="profile-value">{discharge_v}</div></div>
              </div>
              {notes_block}
              <div class="edit-section-label">Edit Client</div>
            </div>
            """, unsafe_allow_html=True)

            with st.form(f"edit_{key}"):
                c1, c2 = st.columns(2)
                with c1:
                    edit_name   = st.text_input("Client Name", value=client_name, key=f"name_{key}")
                    edit_dob    = st.date_input("Date of Birth", value=_parse_date(row.get("DOB","")) or date(1980,1,1), min_value=min_dob, max_value=today, key=f"dob_{key}")
                    edit_intake = st.date_input("Intake Date", value=_parse_date(row.get("Intake Date","")) or today, key=f"intake_{key}")
                    edit_seen   = st.date_input("Last Seen", value=_parse_date(row.get("Last Seen","")) or today, key=f"seen_{key}")
                    edit_tp     = st.date_input("Treatment Plan Date", value=_parse_date(row.get("Treatment Plan Date","")) or today, key=f"tp_{key}")
                with c2:
                    edit_phq9   = st.date_input("PHQ-9 Completed On", value=_parse_date(row.get("PHQ-9 Completed Date","")), key=f"phq9_{key}")
                    edit_gad7   = st.date_input("GAD-7 Completed On", value=_parse_date(row.get("GAD-7 Completed Date","")), key=f"gad7_{key}")
                    edit_dc     = st.checkbox("Discharge Ready", value=to_bool(row.get("Discharge Ready",False)), key=f"dc_{key}")
                    edit_notes  = st.text_area("Notes", value=notes_v, height=80, key=f"notes_{key}")
                col1, col2 = st.columns([2,1])
                with col1: save_btn   = st.form_submit_button("💾 Save Changes")
                with col2: remove_btn = st.form_submit_button("🗑 Remove Client")
                if save_btn:
                    def edate(d): return d.strftime("%Y-%m-%d") if d else ""
                    df.at[idx,"Client"]=edit_name; df.at[idx,"DOB"]=edate(edit_dob)
                    df.at[idx,"Intake Date"]=edate(edit_intake); df.at[idx,"Last Seen"]=edit_seen.strftime("%Y-%m-%d")
                    df.at[idx,"Intake Complete"]=True; df.at[idx,"Treatment Plan Date"]=edit_tp.strftime("%Y-%m-%d")
                    df.at[idx,"Discharge Ready"]=edit_dc; df.at[idx,"Notes"]=edit_notes or ""
                    df.at[idx,"PHQ-9 Completed Date"]=edate(edit_phq9); df.at[idx,"GAD-7 Completed Date"]=edate(edit_gad7)
                    df.to_csv(DATA_FILE, index=False)
                    st.session_state.expanded[key] = False
                    st.toast(f"✓ {edit_name} updated", icon="💾")
                    st.rerun()
                if remove_btn:
                    df = df.drop(index=idx).reset_index(drop=True)
                    df.to_csv(DATA_FILE, index=False)
                    st.session_state.expanded.pop(key, None)
                    st.toast(f"✓ {client_name} removed", icon="🗑")
                    st.rerun()

else:
    st.markdown('<div class="empty-state"><div class="empty-icon">🌿</div><div class="empty-text">No clients yet</div><div class="empty-sub">Add your first client below to get started</div></div>', unsafe_allow_html=True)

# ── ADD CLIENT ───────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-head">Add New Client</div>', unsafe_allow_html=True)
with st.expander("➕  Add a new client"):
    with st.form("new_client", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name           = st.text_input("Client Name *")
            dob            = st.date_input("Date of Birth", value=None, min_value=min_dob, max_value=today, key="dob_new")
            intake_date    = st.date_input("Intake Date", today, key="intake_new")
            last_seen      = st.date_input("Last Seen", today, key="seen_new")
            tp             = st.date_input("Treatment Plan Date", today, key="tp_new")
        with c2:
            phq9_completed = st.date_input("PHQ-9 Completed On", value=None, key="phq9_new")
            gad7_completed = st.date_input("GAD-7 Completed On", value=None, key="gad7_new")
            discharge_ready= st.checkbox("Mark as Discharge Ready", key="dc_new")
            notes          = st.text_area("Notes (optional)", height=80, key="notes_new")
        submitted = st.form_submit_button("Add Client")
        if submitted:
            if not name.strip():
                st.error("Client name is required.")
            elif name.strip() in df["Client"].astype(str).tolist():
                st.error(f"'{name.strip()}' already exists.")
            else:
                def dstr(d): return d.strftime("%Y-%m-%d") if d else ""
                df = pd.concat([df, pd.DataFrame([{
                    "Client":name.strip(), "DOB":dstr(dob),
                    "Intake Date":dstr(intake_date), "Last Seen":last_seen.strftime("%Y-%m-%d"),
                    "Intake Complete":True, "Treatment Plan Date":tp.strftime("%Y-%m-%d"),
                    "Discharge Ready":discharge_ready, "Notes":notes or "",
                    "PHQ-9 Completed Date":dstr(phq9_completed), "GAD-7 Completed Date":dstr(gad7_completed),
                }])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.toast(f"✓ {name.strip()} added to caseload", icon="✅")
                st.rerun()

st.markdown('<div style="margin-top:48px;padding-top:20px;border-top:1px solid #e8e5df;font-size:11px;color:#c0c0d0;text-align:center;">Omniveil · Clinical decision support tool · Not a diagnostic instrument · All client data stored locally</div>', unsafe_allow_html=True)
