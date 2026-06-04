import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import re
from urllib.parse import urlparse
from io import StringIO

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AC Caste Vote Simulator",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:        #0d1117;
    --surface:   #161b22;
    --surface2:  #1c2333;
    --border:    #30363d;
    --accent:    #f78166;
    --accent2:   #79c0ff;
    --accent3:   #56d364;
    --accent4:   #e3b341;
    --text:      #e6edf3;
    --muted:     #8b949e;
    --bjp:       #FF6B35;
    --sp:        #E63946;
    --bsp:       #457B9D;
    --inc:       #2DC653;
    --others:    #9B5DE5;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

.stApp { background-color: var(--bg); }

/* Header */
.main-header {
    background: linear-gradient(135deg, #161b22 0%, #1c2333 50%, #0d1117 100%);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #f78166, #79c0ff, #56d364, #e3b341);
}
.main-header h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #e6edf3;
    margin: 0 0 4px 0;
    letter-spacing: 1px;
}
.main-header p {
    color: #8b949e;
    margin: 0;
    font-size: 0.9rem;
}

/* Cards */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: var(--accent2);
    border-radius: 4px 0 0 4px;
}
.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}
.metric-delta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    margin-top: 4px;
}
.delta-pos { color: var(--accent3); }
.delta-neg { color: var(--accent); }
.delta-neu { color: var(--muted); }

/* Section Headers */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--accent2);
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin: 20px 0 14px 0;
}

/* Party badge */
.party-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    margin: 2px;
}

/* Caste impact bar */
.impact-bar-wrap {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    margin: 6px 0;
}
.impact-bar-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
    font-size: 0.85rem;
}
.impact-bar-bg {
    height: 8px;
    background: var(--border);
    border-radius: 4px;
    overflow: hidden;
}
.impact-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.4s ease;
}

/* Sliders */
.stSlider > div > div { background: var(--surface2) !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

/* Dataframe */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* Selectbox */
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* Number input */
.stNumberInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #1f6feb, #388bfd) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(56, 139, 253, 0.3) !important;
}

/* Alert box */
.info-box {
    background: rgba(121, 192, 255, 0.08);
    border: 1px solid rgba(121, 192, 255, 0.3);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 0.85rem;
    color: var(--accent2);
    margin: 10px 0;
}
.warn-box {
    background: rgba(227, 179, 65, 0.08);
    border: 1px solid rgba(227, 179, 65, 0.3);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 0.85rem;
    color: var(--accent4);
    margin: 10px 0;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px 10px 0 0;
    border-bottom: 1px solid var(--border);
    gap: 4px;
    padding: 8px 8px 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    color: var(--muted) !important;
    background: transparent !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent2) !important;
    background: var(--surface2) !important;
    border-bottom: 2px solid var(--accent2) !important;
}

div[data-testid="stVerticalBlock"] { gap: 12px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PARTIES — RLD merged into BJP+ (alliance)
# ══════════════════════════════════════════════════════════════════════════════
PARTY_COLORS = {
    "BJP+":   "#FF6B35",
    "SP+INC": "#E63946",
    "BSP":    "#457B9D",
    "Others": "#9B5DE5",
}
PARTIES = list(PARTY_COLORS.keys())

# ─── Default caste-party affinity (RLD folded into BJP+) ─────────────────────
DEFAULT_CASTE_PARTY_AFFINITY = {
    "Muslim":           {"BJP+": 0,   "SP+INC": 95, "BSP": 5, "Others": 0},
    "Jatav":            {"BJP+": 10,   "SP+INC": 30, "BSP": 60, "Others": 0},
    "Jat":              {"BJP+": 75,  "SP+INC": 20, "BSP": 0,  "Others": 5},
    "Saini":            {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Kashyap/Nishad":   {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Thakur":           {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Kamboj":           {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Brahmin":          {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Kumhar/Prajapat":  {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Gujjar":           {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Pal/Gadariya":     {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Valmiki":          {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Baniya":           {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Tyagi":            {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Teli":             {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Dhobi":            {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Punjabi":          {"BJP+": 75,  "SP+INC": 22, "BSP": 0,  "Others": 5},
    "OBC_Others":       {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Gen_Others":       {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "SC_Others":        {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "ST_Others":        {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Jat (OBC)":        {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Dheemar/Dhimar":   {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Khatik/Sonkar":    {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
    "Kayastha":         {"BJP+": 90,  "SP+INC": 10, "BSP": 0, "Others": 0},
}

# ─── Helpers ──────────────────────────────────────────────────────────────────
def compute_vote_share(caste_data: pd.DataFrame, splits: dict) -> dict:
    totals = {p: 0.0 for p in PARTIES}
    for _, row in caste_data.iterrows():
        caste = row["Caste"]
        weight = row["caste_pct"] / 100.0
        if caste in splits:
            for party, share in splits[caste].items():
                if party in totals:
                    totals[party] += weight * share
    s = sum(totals.values())
    if s > 0:
        totals = {p: round(v * 100 / s, 2) for p, v in totals.items()}
    return totals

def normalize_split(split_dict: dict) -> dict:
    s = sum(split_dict.values())
    if s == 0:
        return split_dict
    return {k: round(v * 100 / s, 2) for k, v in split_dict.items()}

def _init_store():
    if "ac_data_store" not in st.session_state:
        st.session_state["ac_data_store"] = {}
 
def store_has(ac, table):
    _init_store()
    return (ac in st.session_state["ac_data_store"]
            and table in st.session_state["ac_data_store"][ac]
            and len(st.session_state["ac_data_store"][ac][table]) > 0)
 
def store_load(ac, table):
    _init_store()
    return st.session_state["ac_data_store"].get(ac, {}).get(table, {})
 
def store_save(ac, table, data):
    _init_store()
    if ac not in st.session_state["ac_data_store"]:
        st.session_state["ac_data_store"][ac] = {}
    st.session_state["ac_data_store"][ac][table] = data
 
def store_clear(ac, table):
    _init_store()
    if ac in st.session_state["ac_data_store"]:
        st.session_state["ac_data_store"][ac].pop(table, None)
 
def store_export():
    import json
    _init_store()
    return json.dumps(st.session_state["ac_data_store"], indent=2, ensure_ascii=False)
 
def store_import(json_str):
    import json
    try:
        data = json.loads(json_str)
        _init_store()
        for ac, tables in data.items():
            if ac not in st.session_state["ac_data_store"]:
                st.session_state["ac_data_store"][ac] = {}
            st.session_state["ac_data_store"][ac].update(tables)
        return True, f"Imported {len(data)} AC(s): {', '.join(data.keys())}"
    except Exception as e:
        return False, str(e)
 
def splits_to_df(caste_list, caste_pcts, splits_dict, parties):
    """Convert {caste: {party: val}} dict → wide DataFrame for data_editor."""
    rows = []
    for c, pct in zip(caste_list, caste_pcts):
        row = {"Caste": c, "Pop %": round(pct, 2)}
        sp  = splits_dict.get(c, {p: 0.0 for p in parties})
        for p in parties:
            row[p] = float(sp.get(p, 0.0))
        row["Total"] = round(sum(sp.get(p, 0.0) for p in parties), 1)
        rows.append(row)
    return pd.DataFrame(rows)
 
def df_to_splits(df, parties):
    """Convert wide DataFrame back to {caste: {party: val}} after editing."""
    result = {}
    for _, row in df.iterrows():
        c  = row["Caste"]
        sp = {p: float(row.get(p, 0.0)) for p in parties}
        result[c] = normalize_split(sp)
    return result
# ─── Google Sheet ─────────────────────────────────────────────────────────────
GOOGLE_SHEET_URL = st.secrets.get(
    "GOOGLE_SHEET_URL",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vSonf79A9F3Ezu86qSskR5ed0pdVxZvIgQ6ymaN2omhWALmH-SfoNwUQ3CPLSK4xTOrRAU64TXG8wLj/pub?output=csv"
)

@st.cache_data(ttl=300)
def load_master_sheet():
    df = pd.read_csv(GOOGLE_SHEET_URL)
    df.columns = [c.strip() for c in df.columns]
    return df

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-header">CONSTITUENCY SELECTION</div>', unsafe_allow_html=True)

    if not GOOGLE_SHEET_URL:
        st.error("GOOGLE_SHEET_URL missing in Streamlit secrets.")
        st.stop()

    try:
        raw_df = load_master_sheet()
        st.success(f"Loaded {len(raw_df):,} caste records")
    except Exception as e:
        st.error(f"Google Sheet Load Failed: {e}")
        st.stop()

    districts = sorted(raw_df["District"].dropna().unique())
    selected_district = st.selectbox("District", districts)

    acs = sorted(
        raw_df[raw_df["District"] == selected_district]["AC Name"]
        .dropna().unique()
    )
    selected_ac = st.selectbox("Assembly Constituency", acs)

    st.markdown('<div class="section-header">SURVEY INPUTS (BASELINE)</div>', unsafe_allow_html=True)
    st.caption("Enter field survey data — this is your baseline for all comparisons")
    survey_bjp    = st.number_input("BJP+ (incl. RLD) Survey %", min_value=0.0, max_value=100.0, value=48.0, step=0.5, format="%.1f")
    survey_sp     = st.number_input("SP+INC Survey %",          min_value=0.0, max_value=100.0, value=38.0, step=0.5, format="%.1f")
    survey_bsp    = st.number_input("BSP Survey %",             min_value=0.0, max_value=100.0, value=12.0, step=0.5, format="%.1f")
    survey_others = st.number_input("Others Survey %",          min_value=0.0, max_value=100.0, value=2.0,  step=0.5, format="%.1f")

    survey_input = {"BJP+": survey_bjp, "SP+INC": survey_sp, "BSP": survey_bsp, "Others": survey_others}
    survey_total = sum(survey_input.values())
    if abs(survey_total - 100) > 1:
        st.markdown(f'<div class="warn-box">⚠️ Survey totals {survey_total:.1f}%. Ideally 100%.</div>', unsafe_allow_html=True)

    # Normalize survey to exactly 100%
    if survey_total > 0:
        survey_norm = {p: round(v * 100 / survey_total, 2) for p, v in survey_input.items()}
    else:
        survey_norm = survey_input.copy()

    st.markdown('<div class="section-header">TURNOUT ADJUSTMENT</div>', unsafe_allow_html=True)
    apply_turnout = st.toggle("Apply differential turnout", value=False)
    if apply_turnout:
        st.caption("Set expected turnout % for each category")
        gen_turnout    = st.slider("GEN Turnout %",     40, 95, 68)
        obc_turnout    = st.slider("OBC Turnout %",     40, 95, 72)
        sc_turnout     = st.slider("SC Turnout %",      40, 95, 70)
        st_turnout     = st.slider("ST Turnout %",      40, 95, 65)
        muslim_turnout = st.slider("Muslim Turnout %",  40, 95, 75)
        turnout_map = {"GEN": gen_turnout, "OBC": obc_turnout,
                       "SC": sc_turnout, "ST": st_turnout, "Muslim": muslim_turnout}
    else:
        turnout_map = None

    refresh = st.button("🔄 Refresh Data")
    if refresh:
        st.cache_data.clear()
        st.rerun()

# ─── Main Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🗳️ AC Caste Vote Share Simulator</h1>
  <p>Constituency caste modelling · Scenario vs Survey comparison · BJP+RLD alliance mode</p>
</div>
""", unsafe_allow_html=True)

# ─── Data Prep ────────────────────────────────────────────────────────────────
if raw_df is not None:
    raw_df.columns = [c.strip() for c in raw_df.columns]
    pct_col   = next((c for c in raw_df.columns if "caste %" in c.lower() or "caste%" in c.lower()), None)
    caste_col = next((c for c in raw_df.columns if "caste (eng)" in c.lower()), None)
    if caste_col is None:
        caste_col = next((c for c in raw_df.columns if c.lower() == "caste" and "local" not in c.lower()), None)
    ac_col  = next((c for c in raw_df.columns if "ac name" in c.lower()), None)
    cat_col = next((c for c in raw_df.columns if "category" in c.lower()), None)

    if pct_col and caste_col and ac_col:
        raw_df["caste_pct"] = pd.to_numeric(
            raw_df[pct_col].astype(str).str.replace('%', '', regex=False).str.strip(),
            errors="coerce"
        ).fillna(0)
        raw_df["Caste"] = raw_df[caste_col].astype(str).str.strip()

        # Zone info
        if "AC Zone" in raw_df.columns:
            zone_rows = raw_df[raw_df[ac_col] == selected_ac]
            if len(zone_rows) > 0:
                st.metric("Zone", zone_rows["AC Zone"].iloc[0])

        ac_df = raw_df[raw_df[ac_col] == selected_ac].copy()
        if cat_col:
            ac_df["Category"] = ac_df[cat_col].astype(str)
        else:
            ac_df["Category"] = "OBC"

        ac_df = ac_df[ac_df["caste_pct"] > 0].copy()
        ac_df = ac_df.sort_values("caste_pct", ascending=False).reset_index(drop=True)

        if ac_df.empty:
            st.warning(f"⚠️ No caste data found for **{selected_ac}**. Try another constituency.")
            st.stop()

        # Apply turnout
        if apply_turnout and turnout_map and "Category" in ac_df.columns:
            def get_turnout(row):
                cat = str(row.get("Category", "OBC")).strip().upper()
                caste = str(row.get("Caste", "")).strip()
                if caste.lower() == "muslim" or cat == "MUSLIM":
                    return turnout_map.get("Muslim", 70)
                return turnout_map.get(cat, 70)
            ac_df["turnout"]   = ac_df.apply(get_turnout, axis=1)
            ac_df["adj_pct"]   = ac_df["caste_pct"] * ac_df["turnout"] / 100
            total_adj          = ac_df["adj_pct"].sum()
            ac_df["caste_pct"] = (ac_df["adj_pct"] / total_adj * 100).round(2)

        total_electors = None
        if "Total Electors [29 May]" in raw_df.columns:
            _te = pd.to_numeric(raw_df[raw_df[ac_col] == selected_ac]["Total Electors [29 May]"], errors="coerce").iloc[0]
            total_electors = int(_te) if pd.notna(_te) else None

        # ─── Build default caste splits ───────────────────────────────────
        caste_splits_base = {}
        for _, row in ac_df.iterrows():
            c = row["Caste"]
            affinity = DEFAULT_CASTE_PARTY_AFFINITY.get(c)
            if affinity is None:
                for key in DEFAULT_CASTE_PARTY_AFFINITY:
                    if key.lower() in c.lower() or c.lower() in key.lower():
                        affinity = DEFAULT_CASTE_PARTY_AFFINITY[key]
                        break
            if affinity is None:
                cat = str(row.get("Category", "OBC")).upper()
                if cat == "SC":
                    affinity = {"BJP+": 30, "SP+INC": 20, "BSP": 45, "Others": 5}
                elif cat == "ST":
                    affinity = {"BJP+": 40, "SP+INC": 25, "BSP": 25, "Others": 10}
                elif cat == "GEN":
                    affinity = {"BJP+": 60, "SP+INC": 20, "BSP": 10, "Others": 10}
                elif cat == "MUSLIM":
                    affinity = {"BJP+": 8,  "SP+INC": 75, "BSP": 12, "Others": 5}
                else:
                    affinity = {"BJP+": 45, "SP+INC": 30, "BSP": 20, "Others": 5}
            caste_splits_base[c] = normalize_split(affinity.copy())

        # ─── SINGLE SOURCE OF TRUTH: active_splits in session_state ───────
        # ─── SINGLE SOURCE OF TRUTH: active_splits in session_state ───────
        # Reset when AC changes so scenario starts fresh from caste model
        if (
            "active_splits" not in st.session_state
            or st.session_state.get("_current_ac") != selected_ac
        ):
            st.session_state["active_splits"] = {k: v.copy() for k, v in caste_splits_base.items()}
            st.session_state["_current_ac"] = selected_ac
        # Convenience: current active splits
        active_splits = st.session_state["active_splits"]

        # Compute all three vote shares once — used by ALL tabs
        base_vs     = compute_vote_share(ac_df, caste_splits_base)
        scenario_vs = compute_vote_share(ac_df, active_splits)

        # ─── TABS ─────────────────────────────────────────────────────────
        tab1, tab2, tab3, tab4, tab5= st.tabs([
            "📊 AC Overview & Survey",
            "🎛️ Scenario Builder",
            "📈 Impact Analysis",
            "📋 Caste-Party Matrix",
            "🎯 Impact Planner"
        ])

        # ══════════════════════════════════════════════════════════════════
        # TAB 1 — AC OVERVIEW & SURVEY BASELINE
        # ══════════════════════════════════════════════════════════════════
        with tab1:
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                <div class="metric-card">
                  <div class="metric-label">Total Electors</div>
                  <div class="metric-value">{total_electors:,}</div>
                  <div class="metric-delta delta-neu">As of 29 May</div>
                </div>""" if total_electors else """<div class="metric-card"><div class="metric-label">Total Electors</div><div class="metric-value">—</div></div>""",
                unsafe_allow_html=True)
            with m2:
                top_caste = ac_df.iloc[0]
                st.markdown(f"""
                <div class="metric-card">
                  <div class="metric-label">Dominant Caste</div>
                  <div class="metric-value" style="font-size:1.4rem">{top_caste['Caste']}</div>
                  <div class="metric-delta delta-pos">{top_caste['caste_pct']:.1f}% of voters</div>
                </div>""", unsafe_allow_html=True)
            with m3:
                surv_top = max(survey_norm, key=survey_norm.get)
                surv_2nd = sorted(survey_norm, key=survey_norm.get, reverse=True)[1]
                surv_margin = survey_norm[surv_top] - survey_norm[surv_2nd]
                color = PARTY_COLORS.get(surv_top, "#fff")
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid {color};">
                  <div class="metric-label">Survey Leader</div>
                  <div class="metric-value" style="color:{color};font-size:1.4rem">{surv_top}</div>
                  <div class="metric-delta delta-pos">+{surv_margin:.1f}% margin</div>
                </div>""", unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                <div class="metric-card">
                  <div class="metric-label">Caste Groups</div>
                  <div class="metric-value">{len(ac_df)}</div>
                  <div class="metric-delta delta-neu">With non-zero population</div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-header">CASTE COMPOSITION</div>', unsafe_allow_html=True)
            col_chart, col_table = st.columns([5, 4])

            with col_chart:
                fig_tree = px.treemap(
                    ac_df, path=["Category", "Caste"], values="caste_pct",
                    color="caste_pct",
                    color_continuous_scale=["#0d1117", "#1f6feb", "#79c0ff"],
                    title=f"Caste Composition — {selected_ac} AC",
                )
                fig_tree.update_layout(
                    paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                    font=dict(family="IBM Plex Sans", color="#e6edf3"),
                    title_font=dict(family="Rajdhani", size=16, color="#79c0ff"),
                    margin=dict(t=40, l=0, r=0, b=0), height=380,
                    coloraxis_showscale=False,
                )
                fig_tree.update_traces(
                    textfont=dict(family="IBM Plex Sans", color="white"),
                    marker=dict(line=dict(width=2, color="#0d1117"))
                )
                st.plotly_chart(fig_tree, width="stretch", key="tab1_treemap")

            with col_table:
                display_df = ac_df[["Caste", "Category", "caste_pct"]].copy()
                display_df.columns = ["Caste", "Category", "Share %"]
                display_df["Share %"] = display_df["Share %"].apply(lambda x: f"{x:.2f}%")
                st.dataframe(display_df, width="stretch", hide_index=True, height=380)

            # Survey vs Model bar chart
            st.markdown('<div class="section-header">SURVEY BASELINE vs CASTE MODEL vs SCENARIO</div>', unsafe_allow_html=True)
            fig_bar = go.Figure()
            for trace_name, trace_data, opacity, pattern in [
                ("Survey (Baseline)", survey_norm, 1.0, None),
                ("Caste Model (Default)", base_vs, 0.5, None),
                ("Scenario (Your Edits)", scenario_vs, 0.8, dict(shape="/", size=6, solidity=0.3)),
            ]:
                fig_bar.add_trace(go.Bar(
                    x=PARTIES,
                    y=[trace_data.get(p, 0) for p in PARTIES],
                    name=trace_name,
                    marker_color=[PARTY_COLORS[p] for p in PARTIES],
                    marker_pattern=pattern, opacity=opacity,
                    text=[f"{trace_data.get(p,0):.1f}%" for p in PARTIES],
                    textposition="outside",
                    textfont=dict(family="Rajdhani", size=12),
                ))
            fig_bar.update_layout(
                barmode="group",
                paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Sans", color="#e6edf3"),
                xaxis=dict(showgrid=False, tickfont=dict(family="Rajdhani", size=14)),
                yaxis=dict(showgrid=True, gridcolor="#30363d", range=[0, 100],
                           ticksuffix="%", tickfont=dict(family="IBM Plex Mono")),
                legend=dict(font=dict(family="Rajdhani", size=12), orientation="h",
                            yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                margin=dict(t=60, l=0, r=0, b=0), height=300,
            )
            st.plotly_chart(fig_bar, width="stretch", key="tab1_3way_bar")

        # ══════════════════════════════════════════════════════════════════
        # TAB 2 — SCENARIO BUILDER
        # ══════════════════════════════════════════════════════════════════
        with tab2:
            st.markdown('<div class="info-box">💡 Adjust caste vote splits below. Changes apply to <b>all tabs</b> instantly. Compare your scenario against the <b>survey baseline</b> at the bottom.</div>', unsafe_allow_html=True)

            filter_cat = st.multiselect(
                "Filter castes by category:",
                options=["All"] + sorted(ac_df["Category"].unique().tolist()),
                default=["All"], key="tab2_filter"
            )
            show_all = "All" in filter_cat or not filter_cat
            cats_to_show = ac_df["Category"].unique() if show_all else filter_cat
            filtered_df = ac_df[ac_df["Category"].isin(cats_to_show)].copy()

            for _, row in filtered_df.iterrows():
                caste = row["Caste"]
                cpct  = row["caste_pct"]
                cat   = row.get("Category", "")
                cur   = active_splits.get(caste, caste_splits_base.get(caste, {}))

                with st.expander(f"🔹 **{caste}** ({cat}) — {cpct:.2f}% of AC voters", expanded=cpct > 10):
                    ec1, ec2, ec3, ec4 = st.columns(4)
                    new_split = {}
                    cols_exp = [ec1, ec2, ec3, ec4]
                    for i, party in enumerate(PARTIES):
                        with cols_exp[i]:
                            val = st.number_input(
                                f"{party}", min_value=0.0, max_value=100.0,
                                value=float(cur.get(party, 0)),
                                step=1.0, format="%.1f",
                                key=f"split_{caste}_{party}"
                            )
                            new_split[party] = val

                    split_total = sum(new_split.values())
                    if abs(split_total - 100) > 0.5:
                        st.warning(f"⚠️ Split totals {split_total:.1f}% — will normalize to 100%")
                    normalized = normalize_split(new_split)
                    st.session_state["active_splits"][caste] = normalized

                    mini_fig = go.Figure()
                    for party in PARTIES:
                        mini_fig.add_trace(go.Bar(
                            x=[party], y=[normalized.get(party, 0)],
                            marker_color=PARTY_COLORS[party],
                            text=[f"{normalized.get(party,0):.0f}%"],
                            textposition="outside", textfont=dict(size=10)
                        ))
                    mini_fig.update_layout(
                        paper_bgcolor="#1c2333", plot_bgcolor="#1c2333",
                        height=140, showlegend=False,
                        margin=dict(t=10, l=0, r=0, b=0),
                        yaxis=dict(range=[0, 110], showgrid=False, showticklabels=False),
                        xaxis=dict(showgrid=False, tickfont=dict(size=10, family="Rajdhani")),
                    )
                    st.plotly_chart(mini_fig, width="stretch", key=f"mini_{caste}")

            # Quick Swing
            st.markdown('<div class="section-header">QUICK SWING SIMULATOR</div>', unsafe_allow_html=True)
            swing_caste = st.selectbox("Caste", filtered_df["Caste"].tolist(), key="swing_caste")
            from_party  = st.selectbox("From Party", PARTIES, key="swing_from")
            to_party    = st.selectbox("To Party", PARTIES, index=1, key="swing_to")
            swing_pct   = st.slider("Vote Shift %", 0, 20, 5, key="swing_pct")

            if st.button("Apply Swing"):
                sp = st.session_state["active_splits"][swing_caste].copy()
                sp[from_party] = max(0, sp[from_party] - swing_pct)
                sp[to_party]  += swing_pct
                st.session_state["active_splits"][swing_caste] = normalize_split(sp)
                st.success(f"{swing_pct}% shifted {from_party} → {to_party} for {swing_caste}")

            # ── RESULTS: Scenario vs Survey ───────────────────────────────
            scenario_vs = compute_vote_share(ac_df, st.session_state["active_splits"])

            st.markdown('<div class="section-header">SCENARIO RESULT vs SURVEY BASELINE</div>', unsafe_allow_html=True)
            rcols = st.columns(len(PARTIES))
            for i, party in enumerate(PARTIES):
                sv   = survey_norm.get(party, 0)
                sc   = scenario_vs.get(party, 0)
                d    = sc - sv
                dc   = "delta-pos" if d > 0 else ("delta-neg" if d < 0 else "delta-neu")
                ds   = "+" if d > 0 else ""
                pcol = PARTY_COLORS[party]
                with rcols[i]:
                    st.markdown(f"""
                    <div class="metric-card" style="border-left: 4px solid {pcol};">
                      <div class="metric-label">{party}</div>
                      <div class="metric-value" style="color:{pcol}">{sc:.1f}%</div>
                      <div class="metric-delta {dc}">{ds}{d:.1f}% vs survey ({sv:.1f}%)</div>
                    </div>""", unsafe_allow_html=True)

            # Winner analysis
            scen_top = max(scenario_vs, key=scenario_vs.get)
            surv_top = max(survey_norm, key=survey_norm.get)
            scen_2nd = sorted(scenario_vs, key=scenario_vs.get, reverse=True)[1]
            scen_margin = scenario_vs[scen_top] - scenario_vs[scen_2nd]

            if scen_top != surv_top:
                st.markdown(f"""
                <div class="warn-box">
                🔄 <b>SCENARIO ≠ SURVEY!</b> Survey says <b>{surv_top}</b> ({survey_norm[surv_top]:.1f}%)
                but your caste scenario predicts <b>{scen_top}</b> ({scenario_vs[scen_top]:.1f}%). Margin: {scen_margin:.1f}%.
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="info-box">
                ✅ Scenario agrees with survey: <b>{scen_top}</b> wins. Margin: <b>{scen_margin:.1f}%</b>.
                </div>""", unsafe_allow_html=True)

            # Charts
            col_rl, col_rr = st.columns(2)
            with col_rl:
                surv_vals = [survey_norm.get(p, 0) for p in PARTIES]
                scen_vals = [scenario_vs.get(p, 0) for p in PARTIES]
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=surv_vals + [surv_vals[0]], theta=PARTIES + [PARTIES[0]],
                    fill="toself", name="Survey",
                    line=dict(color="#56d364"), fillcolor="rgba(86,211,100,0.12)"
                ))
                fig_radar.add_trace(go.Scatterpolar(
                    r=scen_vals + [scen_vals[0]], theta=PARTIES + [PARTIES[0]],
                    fill="toself", name="Scenario",
                    line=dict(color="#f78166"), fillcolor="rgba(247,129,102,0.12)"
                ))
                fig_radar.update_layout(
                    polar=dict(bgcolor="#1c2333",
                               radialaxis=dict(visible=True, range=[0, 80], color="#8b949e"),
                               angularaxis=dict(color="#e6edf3")),
                    paper_bgcolor="#161b22",
                    font=dict(family="IBM Plex Sans", color="#e6edf3"),
                    legend=dict(font=dict(family="Rajdhani")),
                    title=dict(text="Survey vs Scenario — Radar", font=dict(family="Rajdhani", color="#79c0ff", size=14)),
                    margin=dict(t=40, l=20, r=20, b=20), height=340,
                )
                st.plotly_chart(fig_radar, width="stretch", key="tab2_radar")

            with col_rr:
                gap = {p: scenario_vs.get(p,0) - survey_norm.get(p,0) for p in PARTIES}
                fig_gap = go.Figure(go.Bar(
                    x=PARTIES, y=list(gap.values()),
                    marker_color=["#56d364" if v >= 0 else "#f78166" for v in gap.values()],
                    text=[f"{'+' if v>=0 else ''}{v:.1f}%" for v in gap.values()],
                    textposition="outside", textfont=dict(family="Rajdhani", size=13),
                ))
                fig_gap.update_layout(
                    paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                    title=dict(text="Scenario − Survey Gap", font=dict(family="Rajdhani", color="#e3b341", size=14)),
                    font=dict(family="IBM Plex Sans", color="#e6edf3"),
                    yaxis=dict(showgrid=True, gridcolor="#30363d", ticksuffix="%",
                               zeroline=True, zerolinecolor="#8b949e"),
                    xaxis=dict(showgrid=False, tickfont=dict(family="Rajdhani", size=13)),
                    margin=dict(t=40, l=0, r=0, b=0), height=340,
                )
                st.plotly_chart(fig_gap, width="stretch", key="tab2_gap")

            # Comparison table
            st.markdown('<div class="section-header">DETAILED COMPARISON</div>', unsafe_allow_html=True)
            comp_rows = []
            for p in PARTIES:
                sv = survey_norm.get(p, 0)
                sc = scenario_vs.get(p, 0)
                bv = base_vs.get(p, 0)
                comp_rows.append({
                    "Party": p,
                    "Survey %": f"{sv:.1f}",
                    "Scenario %": f"{sc:.1f}",
                    "Caste Model %": f"{bv:.1f}",
                    "Scenario vs Survey": f"{'+' if sc-sv>=0 else ''}{sc-sv:.1f}",
                    "Scenario vs Model": f"{'+' if sc-bv>=0 else ''}{sc-bv:.1f}",
                })
            st.dataframe(pd.DataFrame(comp_rows), width="stretch", hide_index=True, key="tab2_table")

        # ══════════════════════════════════════════════════════════════════
        # TAB 3 — IMPACT ANALYSIS (uses active_splits, compares to survey)
        # ══════════════════════════════════════════════════════════════════
        with tab3:
            st.markdown('<div class="section-header">CASTE IMPACT ON EACH PARTY</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">Shows each caste\'s contribution using your <b>current scenario splits</b>, compared against the <b>survey baseline</b>.</div>', unsafe_allow_html=True)

            focus_party = st.selectbox("Analyze impact for party:", PARTIES, index=0, key="tab3_party")

            # Recompute scenario from active_splits (reflects Tab 2 edits)
            scenario_vs = compute_vote_share(ac_df, st.session_state["active_splits"])

            impact_rows = []
            for _, row in ac_df.iterrows():
                caste = row["Caste"]
                cpct  = row["caste_pct"]
                scen_sp = st.session_state["active_splits"].get(caste, caste_splits_base.get(caste, {})).get(focus_party, 0)
                base_sp = caste_splits_base.get(caste, {}).get(focus_party, 0)
                scen_contrib = (cpct / 100) * scen_sp
                base_contrib = (cpct / 100) * base_sp
                swing = scen_contrib - base_contrib
                impact_rows.append({
                    "Caste": caste, "Caste %": cpct,
                    "Default Split": base_sp, "Scenario Split": scen_sp,
                    "Default Contrib": round(base_contrib, 2),
                    "Scenario Contrib": round(scen_contrib, 2),
                    "Swing": round(swing, 2),
                })

            impact_df = pd.DataFrame(impact_rows).sort_values("Scenario Contrib", ascending=False)
            pcol_focus = PARTY_COLORS.get(focus_party, "#79c0ff")

            for _, irow in impact_df.iterrows():
                sc  = irow["Scenario Contrib"]
                sw  = irow["Swing"]
                max_c = impact_df["Scenario Contrib"].max() or 1
                bar_w = int((sc / max_c) * 100) if max_c > 0 else 0
                sw_class = "delta-pos" if sw > 0 else ("delta-neg" if sw < 0 else "delta-neu")
                sw_str = f"+{sw:.2f}" if sw > 0 else f"{sw:.2f}"
                st.markdown(f"""
                <div class="impact-bar-wrap">
                  <div class="impact-bar-label">
                    <span><b>{irow['Caste']}</b> <span style="color:#8b949e;font-size:0.78rem">({irow['Caste %']:.1f}% of AC | default {irow['Default Split']:.0f}% → scenario {irow['Scenario Split']:.0f}%)</span></span>
                    <span>Contrib: <b>{sc:.2f}pp</b> &nbsp; Swing: <span class="{sw_class}"><b>{sw_str}pp</b></span></span>
                  </div>
                  <div class="impact-bar-bg">
                    <div class="impact-bar-fill" style="width:{bar_w}%;background:{pcol_focus};opacity:0.85"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

            # Tornado
            st.markdown(f'<div class="section-header">SWING TORNADO — TOP MOVERS FOR {focus_party}</div>', unsafe_allow_html=True)
            tornado_df = impact_df.sort_values("Swing", key=abs, ascending=False).head(10)
            fig_tornado = go.Figure()
            fig_tornado.add_trace(go.Bar(
                y=tornado_df["Caste"], x=tornado_df["Swing"], orientation="h",
                marker_color=[pcol_focus if v >= 0 else "#f78166" for v in tornado_df["Swing"]],
                text=[f"{'+' if v>=0 else ''}{v:.2f}pp" for v in tornado_df["Swing"]],
                textposition="outside", textfont=dict(family="Rajdhani", size=12),
            ))
            fig_tornado.update_layout(
                paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Sans", color="#e6edf3"),
                title=dict(text=f"Top Caste Swing Drivers for {focus_party}", font=dict(family="Rajdhani", color=pcol_focus, size=15)),
                xaxis=dict(showgrid=True, gridcolor="#30363d", zeroline=True, zerolinecolor="#8b949e", ticksuffix="pp"),
                yaxis=dict(showgrid=False, tickfont=dict(family="IBM Plex Sans", size=12)),
                margin=dict(t=40, l=0, r=60, b=0), height=380,
            )
            st.plotly_chart(fig_tornado, width="stretch", key="tab3_tornado")

            # Stacked contribution (scenario splits)
            st.markdown('<div class="section-header">CASTE CONTRIBUTION TO EACH PARTY (SCENARIO)</div>', unsafe_allow_html=True)
            contrib_fig = go.Figure()
            for party in PARTIES:
                contribs = []
                for _, row in ac_df.iterrows():
                    c = row["Caste"]
                    sp = st.session_state["active_splits"].get(c, caste_splits_base.get(c, {})).get(party, 0)
                    contribs.append((row["caste_pct"] / 100) * sp)
                contrib_fig.add_trace(go.Bar(
                    name=party, x=ac_df["Caste"].tolist(), y=contribs,
                    marker_color=PARTY_COLORS[party],
                ))
            contrib_fig.update_layout(
                barmode="stack",
                paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Sans", color="#e6edf3"),
                title=dict(text="Caste-wise Vote Contribution (Scenario Splits)", font=dict(family="Rajdhani", color="#79c0ff", size=14)),
                xaxis=dict(showgrid=False, tickangle=-35, tickfont=dict(family="IBM Plex Sans", size=10)),
                yaxis=dict(showgrid=True, gridcolor="#30363d", ticksuffix="pp"),
                legend=dict(font=dict(family="Rajdhani")),
                margin=dict(t=40, l=0, r=0, b=80), height=380,
            )
            st.plotly_chart(contrib_fig, width="stretch", key="tab3_contrib")

            # Survey vs Scenario summary for this tab
            st.markdown('<div class="section-header">SCENARIO vs SURVEY SUMMARY</div>', unsafe_allow_html=True)
            sum_cols = st.columns(len(PARTIES))
            for i, p in enumerate(PARTIES):
                sv = survey_norm.get(p, 0)
                sc = scenario_vs.get(p, 0)
                d  = sc - sv
                dc = "delta-pos" if d > 0 else ("delta-neg" if d < 0 else "delta-neu")
                with sum_cols[i]:
                    st.markdown(f"""
                    <div class="metric-card" style="border-left:4px solid {PARTY_COLORS[p]}">
                      <div class="metric-label">{p}</div>
                      <div class="metric-value" style="color:{PARTY_COLORS[p]}">{sc:.1f}%</div>
                      <div class="metric-delta {dc}">Survey: {sv:.1f}% | Gap: {'+' if d>=0 else ''}{d:.1f}%</div>
                    </div>""", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════
        # TAB 4 — CASTE-PARTY MATRIX (uses active_splits)
        # ══════════════════════════════════════════════════════════════════
        with tab4:
            st.markdown('<div class="section-header">CASTE–PARTY AFFINITY MATRIX (SCENARIO)</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">Heatmap reflects your <b>current scenario splits</b> — edits in Tab 2 update here instantly.</div>', unsafe_allow_html=True)

            matrix_rows = []
            for _, row in ac_df.iterrows():
                c    = row["Caste"]
                cpct = row["caste_pct"]
                sp   = st.session_state["active_splits"].get(c, caste_splits_base.get(c, {}))
                matrix_rows.append({
                    "Caste": f"{c} ({cpct:.1f}%)" if cpct >= 1 else c,
                    **{p: sp.get(p, 0) for p in PARTIES}
                })

            matrix_df = pd.DataFrame(matrix_rows).set_index("Caste")

            fig_hm = go.Figure(go.Heatmap(
                z=matrix_df.values,
                x=matrix_df.columns.tolist(),
                y=matrix_df.index.tolist(),
                colorscale=[[0, "#0d1117"], [0.3, "#1f3a5f"], [0.6, "#1f6feb"], [1.0, "#79c0ff"]],
                text=[[f"{v:.0f}%" for v in r] for r in matrix_df.values],
                texttemplate="%{text}",
                textfont=dict(family="IBM Plex Mono", size=11, color="white"),
                showscale=True,
                colorbar=dict(ticksuffix="%", tickfont=dict(family="IBM Plex Mono", color="#e6edf3"),
                              bgcolor="#161b22", bordercolor="#30363d")
            ))
            fig_hm.update_layout(
                paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Sans", color="#e6edf3"),
                title=dict(text="Caste–Party Affinity Matrix (Scenario)", font=dict(family="Rajdhani", color="#79c0ff", size=15)),
                xaxis=dict(tickfont=dict(family="Rajdhani", size=13, color="#e6edf3"), side="top"),
                yaxis=dict(tickfont=dict(family="IBM Plex Sans", size=10, color="#e6edf3"), autorange="reversed"),
                margin=dict(t=60, l=0, r=0, b=0),
                height=max(400, len(matrix_df) * 28 + 80),
            )
            st.plotly_chart(fig_hm, width="stretch", key="tab4_heatmap")

            # Dominant castes
            st.markdown('<div class="section-header">DOMINANT CASTES (>5% of AC) — SCENARIO LEANINGS</div>', unsafe_allow_html=True)
            dominant = ac_df[ac_df["caste_pct"] >= 5].copy()
            if len(dominant) == 0:
                dominant = ac_df.head(5)

            for _, dr in dominant.iterrows():
                caste = dr["Caste"]
                cpct  = dr["caste_pct"]
                sp    = st.session_state["active_splits"].get(caste, caste_splits_base.get(caste, {}))
                top_p = max(sp, key=sp.get)
                top_v = sp[top_p]
                pc    = PARTY_COLORS.get(top_p, "#888")

                badges = " ".join([
                    f'<span class="party-badge" style="background:{PARTY_COLORS.get(p,"#888")}22;color:{PARTY_COLORS.get(p,"#888")};border:1px solid {PARTY_COLORS.get(p,"#888")}44">{p}: {sp.get(p,0):.0f}%</span>'
                    for p in PARTIES if sp.get(p, 0) > 5
                ])
                est_str = f"{int(cpct * total_electors / 100):,}" if total_electors else "—"

                st.markdown(f"""
                <div class="impact-bar-wrap" style="border-left:4px solid {pc}">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                    <span style="font-family:Rajdhani;font-size:1.1rem;font-weight:700;color:#e6edf3">{caste}</span>
                    <span style="font-family:IBM Plex Mono;font-size:0.75rem;color:#8b949e">{cpct:.1f}% of AC · ~{est_str} voters</span>
                  </div>
                  <div style="margin-bottom:4px">{badges}</div>
                  <div style="font-size:0.8rem;color:#8b949e">Leans: <span style="color:{pc};font-weight:600">{top_p} ({top_v:.0f}%)</span></div>
                </div>""", unsafe_allow_html=True)

            # Survey vs Scenario summary
            st.markdown('<div class="section-header">SCENARIO vs SURVEY — FINAL SUMMARY</div>', unsafe_allow_html=True)
            scenario_vs = compute_vote_share(ac_df, st.session_state["active_splits"])
            final_cols = st.columns(len(PARTIES))
            for i, p in enumerate(PARTIES):
                sv = survey_norm.get(p, 0)
                sc = scenario_vs.get(p, 0)
                d  = sc - sv
                dc = "delta-pos" if d > 0 else ("delta-neg" if d < 0 else "delta-neu")
                with final_cols[i]:
                    st.markdown(f"""
                    <div class="metric-card" style="border-left:4px solid {PARTY_COLORS[p]}">
                      <div class="metric-label">{p}</div>
                      <div class="metric-value" style="color:{PARTY_COLORS[p]}">{sc:.1f}%</div>
                      <div class="metric-delta {dc}">Survey: {sv:.1f}% | Δ {'+' if d>=0 else ''}{d:.1f}%</div>
                    </div>""", unsafe_allow_html=True)

        with tab5:
            st.markdown('<div class="section-header">CASTE MOVEMENT IMPACT PLANNER</div>', unsafe_allow_html=True)
 
            # ── toolbar ───────────────────────────────────────────────────
            _init_store()
            saved_acs = sorted(st.session_state["ac_data_store"].keys())
 
            top_l, top_r = st.columns([5, 3])
            with top_l:
                if saved_acs:
                    st.markdown(
                        f'<div class="info-box">💾 Saved data for <b>{len(saved_acs)}</b> AC(s): '
                        f'{", ".join(saved_acs[:8])}{"…" if len(saved_acs) > 8 else ""}</div>',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        '<div class="warn-box">📭 No saved AC data yet — edit tables and click 💾 Save.</div>',
                        unsafe_allow_html=True)
 
            with top_r:
                with st.expander("📤 Export / 📥 Import"):
                    if st.button("📤 Export JSON", key="t5_export_btn"):
                        st.session_state["_t5_export"] = store_export()
                    if "_t5_export" in st.session_state:
                        st.download_button("⬇️ Download", data=st.session_state["_t5_export"],
                                           file_name="ac_splits.json", mime="application/json",
                                           key="t5_dl")
                    st.divider()
                    up = st.file_uploader("Upload JSON", type=["json"], key="t5_up")
                    if up and st.button("📥 Import", key="t5_imp"):
                        ok, msg = store_import(up.read().decode())
                        (st.success if ok else st.error)(msg)
                        if ok: st.rerun()
 
            st.markdown(
                '<div class="info-box" style="margin-top:8px">'
                '📌 Fill the three Excel-style tables below. '
                '<b>VS 2022</b> and <b>CAPI</b> are saved per-AC — switch constituencies and your data stays. '
                '<b>Best Case</b> is a planning scratch pad. '
                'Click a cell to edit, Tab to move, Enter to confirm. '
                'Rows auto-normalise to 100% on save.'
                '</div>', unsafe_allow_html=True)
 
            # ── focus party + filter ──────────────────────────────────────
            fp_col, flt_col = st.columns([3, 2])
            with fp_col:
                impact_party = st.selectbox("📊 Size-of-impact on party:",
                                            PARTIES, index=0, key="t5_fp")
            with flt_col:
                show_small = st.toggle("Include castes < 1%", value=False, key="t5_small")
 
            pc_imp    = PARTY_COLORS[impact_party]
            t5_castes = ac_df.copy() if show_small else ac_df[ac_df["caste_pct"] >= 1.0].copy()
            caste_list = t5_castes["Caste"].tolist()
            caste_pcts = t5_castes["caste_pct"].tolist()
 
            # ── column config for data_editor ─────────────────────────────
            party_col_cfg = {
                p: st.column_config.NumberColumn(
                    p,
                    help=f"{p} vote share % for this caste",
                    min_value=0.0, max_value=100.0,
                    step=1.0, format="%.1f",
                    width="small",
                )
                for p in PARTIES
            }
            fixed_col_cfg = {
                "Caste": st.column_config.TextColumn("Caste", disabled=True, width="medium"),
                "Pop %": st.column_config.NumberColumn("Pop %", disabled=True,
                                                        format="%.2f", width="small"),
                "Total": st.column_config.NumberColumn("Total", disabled=True,
                                                        format="%.1f", width="small",
                                                        help="Should sum to ~100%"),
            }
            col_cfg = {**fixed_col_cfg, **party_col_cfg}
            editable_cols = PARTIES  # only party columns are editable
 
            # ── working-copy keys (per-AC, per-table) ─────────────────────
            wk = {t: f"t5_wk_{t}_{selected_ac}" for t in ["vs22", "capi", "best"]}
 
            def _default_best(capi_wk):
                out = {}
                for c in caste_list:
                    sp  = capi_wk.get(c, {p: 0.0 for p in PARTIES})
                    cur = sp.get(impact_party, 0)
                    boost = min(cur + 10, 95)
                    rest  = {p: v for p, v in sp.items() if p != impact_party}
                    rs    = sum(rest.values()) or 1
                    nd    = {p: round(v * (100 - boost) / rs, 1) for p, v in rest.items()}
                    nd[impact_party] = round(boost, 1)
                    out[c] = nd
                return out
 
            # Initialise working copies: persistent store > default affinity
            if wk["vs22"] not in st.session_state:
                saved = store_load(selected_ac, "vs22")
                st.session_state[wk["vs22"]] = {
                    c: saved.get(c, {p: float(caste_splits_base.get(c, {}).get(p, 0)) for p in PARTIES})
                    for c in caste_list
                }
            if wk["capi"] not in st.session_state:
                saved = store_load(selected_ac, "capi")
                st.session_state[wk["capi"]] = {
                    c: saved.get(c, {
                        p: float(st.session_state["active_splits"]
                                 .get(c, caste_splits_base.get(c, {})).get(p, 0))
                        for p in PARTIES
                    })
                    for c in caste_list
                }
            if wk["best"] not in st.session_state:
                st.session_state[wk["best"]] = _default_best(st.session_state[wk["capi"]])
 
            # ── helper: render one data_editor table ──────────────────────
            def render_editor(table_key, label, color, desc, persistent):
                """Render one st.data_editor table. Returns edited splits dict."""
 
                saved_badge = ""
                if persistent:
                    has_saved = store_has(selected_ac, table_key)
                    saved_badge = (
                        ' <span style="font-size:0.7rem;background:#56d36422;color:#56d364;'
                        'padding:2px 8px;border-radius:10px">✓ Saved</span>'
                        if has_saved else
                        ' <span style="font-size:0.7rem;background:#e3b34122;color:#e3b341;'
                        'padding:2px 8px;border-radius:10px">Unsaved</span>'
                    )
 
                st.markdown(
                    f'<div style="background:{color}18;border:1px solid {color}55;border-radius:8px;'
                    f'padding:9px 14px;margin-bottom:8px">'
                    f'<span style="font-family:Rajdhani;font-size:1rem;font-weight:700;color:{color}">'
                    f'{label}</span>{saved_badge}'
                    f'<div style="font-size:0.74rem;color:#8b949e;margin-top:2px">{desc}</div></div>',
                    unsafe_allow_html=True)
 
                wk_key  = wk[table_key]
                init_df = splits_to_df(caste_list, caste_pcts,
                                       st.session_state[wk_key], PARTIES)
 
                edited_df = st.data_editor(
                    init_df,
                    key=f"de_{table_key}_{selected_ac}",
                    use_container_width=True,
                    hide_index=True,
                    num_rows="fixed",
                    column_config=col_cfg,
                    disabled=["Caste", "Pop %", "Total"],
                    column_order=["Caste", "Pop %"] + PARTIES + ["Total"],
                    height=min(40 + len(caste_list) * 35, 700),
                )
 
                # Recompute Total column live for visual feedback
                for p in PARTIES:
                    edited_df[p] = pd.to_numeric(edited_df[p], errors="coerce").fillna(0.0)
                edited_df["Total"] = edited_df[PARTIES].sum(axis=1).round(1)
 
                # Warn rows that don't sum to ~100
                bad_rows = edited_df[abs(edited_df["Total"] - 100) > 1]
                if not bad_rows.empty:
                    bad_names = ", ".join(bad_rows["Caste"].tolist())
                    st.markdown(
                        f'<div class="warn-box">⚠️ These rows don\'t sum to 100%: <b>{bad_names}</b> '
                        f'— values will be normalised on save.</div>',
                        unsafe_allow_html=True)
 
                # Update working copy from editor in real-time
                new_splits = df_to_splits(edited_df, PARTIES)
                st.session_state[wk_key] = new_splits
 
                # Save / Clear buttons
                if persistent:
                    sc1, sc2 = st.columns(2)
                    with sc1:
                        if st.button(f"💾 Save {label}", key=f"save_{table_key}_{selected_ac}",
                                     use_container_width=True):
                            store_save(selected_ac, table_key, new_splits)
                            st.success(f"✅ {label} saved for {selected_ac}!")
                            st.rerun()
                    with sc2:
                        if st.button("🗑️ Clear saved", key=f"clr_{table_key}_{selected_ac}",
                                     use_container_width=True):
                            store_clear(selected_ac, table_key)
                            if wk_key in st.session_state:
                                del st.session_state[wk_key]
                            st.rerun()
                else:
                    if st.button("🔄 Rebuild from CAPI (+10pp boost)",
                                 key=f"rebuild_best_{selected_ac}"):
                        st.session_state[wk["best"]] = _default_best(
                            st.session_state[wk["capi"]])
                        if f"de_best_{selected_ac}" in st.session_state:
                            del st.session_state[f"de_best_{selected_ac}"]
                        st.rerun()
 
                return new_splits
 
            # ── render the three tables — full width, one below another ──
            vs22_splits = render_editor("vs22", "🗳️ VS 2022",   "#1f6feb",
                                        "Actual 2022 VS result splits", persistent=True)

            st.markdown("<hr style='border-color:#30363d;margin:20px 0'>", unsafe_allow_html=True)

            capi_splits = render_editor("capi", "📋 CAPI Survey", "#e3b341",
                                        "Field survey (CAPI) measured splits", persistent=True)

            st.markdown("<hr style='border-color:#30363d;margin:20px 0'>", unsafe_allow_html=True)

            best_splits = render_editor("best", "🚀 Best Case",  "#56d364",
                                        "Target / planning scenario — not saved", persistent=False)
 
            # ── compute vote shares from the three tables ─────────────────
            def vs_from_splits(splits):
                totals = {p: 0.0 for p in PARTIES}
                for c, pct in zip(caste_list, caste_pcts):
                    w  = pct / 100.0
                    sp = splits.get(c, {})
                    for p in PARTIES:
                        totals[p] += w * sp.get(p, 0)
                s = sum(totals.values())
                return {p: round(v * 100 / s, 2) for p, v in totals.items()} if s > 0 else totals
 
            vs22_vs  = vs_from_splits(vs22_splits)
            capi_vs  = vs_from_splits(capi_splits)
            best_vs  = vs_from_splits(best_splits)
 
            # ── vote share summary row ────────────────────────────────────
            st.markdown("<hr style='border-color:#30363d;margin:16px 0'>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">VOTE SHARE ACROSS THREE SCENARIOS</div>',
                        unsafe_allow_html=True)
 
            def dc(v): return "delta-pos" if v >= 0 else "delta-neg"
            def ds(v): return f"+{v:.1f}" if v >= 0 else f"{v:.1f}"
 
            for p in PARTIES:
                v22  = vs22_vs.get(p, 0)
                vcap = capi_vs.get(p, 0)
                vbst = best_vs.get(p, 0)
                d_cv = vcap - v22
                d_bv = vbst - vcap
                d_tv = vbst - v22
                pc_p = PARTY_COLORS[p]
                bdr  = f"border:2px solid {pc_p};" if p == impact_party else "border:1px solid #30363d;"
                st.markdown(f"""
                <div class="impact-bar-wrap" style="{bdr}margin:5px 0">
                  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">
                    <span style="font-family:Rajdhani;font-size:1.05rem;font-weight:700;color:{pc_p}">
                      {p}{"  ← FOCUS" if p==impact_party else ""}
                    </span>
                    <div style="display:flex;gap:18px;font-family:IBM Plex Mono;font-size:0.8rem;flex-wrap:wrap">
                      <span><span style="color:#8b949e">VS22:</span>
                        <b style="color:#1f6feb">{v22:.1f}%</b></span>
                      <span><span style="color:#8b949e">CAPI:</span>
                        <b style="color:#e3b341">{vcap:.1f}%</b>
                        <span class="{dc(d_cv)}">({ds(d_cv)})</span></span>
                      <span><span style="color:#8b949e">Best:</span>
                        <b style="color:#56d364">{vbst:.1f}%</b>
                        <span class="{dc(d_bv)}">({ds(d_bv)})</span></span>
                      <span><span style="color:#8b949e">Total Δ:</span>
                        <b class="{dc(d_tv)}">{ds(d_tv)}%</b></span>
                    </div>
                  </div>
                  <div style="margin-top:7px;display:flex;gap:3px">
                    <div style="flex:1;background:#1f6feb18;border-radius:3px;height:5px">
                      <div style="width:{min(v22,100):.0f}%;height:5px;background:#1f6feb;border-radius:3px"></div></div>
                    <div style="flex:1;background:#e3b34118;border-radius:3px;height:5px">
                      <div style="width:{min(vcap,100):.0f}%;height:5px;background:#e3b341;border-radius:3px"></div></div>
                    <div style="flex:1;background:#56d36418;border-radius:3px;height:5px">
                      <div style="width:{min(vbst,100):.0f}%;height:5px;background:#56d364;border-radius:3px"></div></div>
                  </div>
                </div>""", unsafe_allow_html=True)
 
            # ── size of impact per caste ──────────────────────────────────
            st.markdown("<hr style='border-color:#30363d;margin:16px 0'>", unsafe_allow_html=True)
            st.markdown(f'<div class="section-header">SIZE OF IMPACT PER CASTE — {impact_party}</div>',
                        unsafe_allow_html=True)
            st.markdown(
                f'<div class="info-box">Size of Impact = (caste pop% / 100) × '
                f'(Best Case split − CAPI split) for <b>{impact_party}</b>. '
                f'Sorted by absolute impact.</div>', unsafe_allow_html=True)
 
            impact_rows = []
            for c, pct in zip(caste_list, caste_pcts):
                v22s  = vs22_splits.get(c, {}).get(impact_party, 0)
                caps  = capi_splits.get(c, {}).get(impact_party, 0)
                bsts  = best_splits.get(c, {}).get(impact_party, 0)
                cat   = ac_df[ac_df["Caste"] == c]["Category"].iloc[0] if c in ac_df["Caste"].values else ""
                soi_h = round((pct / 100) * (caps - v22s), 3)
                soi_o = round((pct / 100) * (bsts - caps), 3)
                soi_t = round((pct / 100) * (bsts - v22s), 3)
                if abs(soi_o) < 0.001 and abs(soi_h) < 0.001:
                    continue
                impact_rows.append(dict(caste=c, cat=cat, pct=pct,
                                        v22s=v22s, caps=caps, bsts=bsts,
                                        soi_h=soi_h, soi_o=soi_o, soi_t=soi_t))
 
            impact_rows.sort(key=lambda x: abs(x["soi_o"]), reverse=True)
            max_bar = max((abs(r["soi_o"]) for r in impact_rows), default=1)
 
            for r in impact_rows:
                soi   = r["soi_o"]
                bc    = "#56d364" if soi >= 0 else "#f78166"
                bw    = int(abs(soi) / max_bar * 100)
                est_v = int(r["pct"] * (total_electors or 100000) / 100)
                st.markdown(f"""
                <div class="impact-bar-wrap" style="margin:5px 0">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:5px">
                    <div>
                      <span style="font-family:Rajdhani;font-size:1rem;font-weight:700;color:#e6edf3">{r['caste']}</span>
                      <span style="font-family:IBM Plex Mono;font-size:0.7rem;color:#8b949e;margin-left:8px">
                        {r['pct']:.1f}% · ~{est_v:,} voters · {r['cat']}</span>
                    </div>
                    <div style="font-family:IBM Plex Mono;font-size:0.74rem;text-align:right">
                      <span style="color:#1f6feb">VS22:{r['v22s']:.0f}%</span> →
                      <span style="color:#e3b341">CAPI:{r['caps']:.0f}%</span> →
                      <span style="color:#56d364">Best:{r['bsts']:.0f}%</span>
                    </div>
                  </div>
                  <div class="impact-bar-bg">
                    <div class="impact-bar-fill" style="width:{bw}%;background:{bc};opacity:0.85"></div>
                  </div>
                  <div style="display:flex;justify-content:space-between;margin-top:5px;
                               font-family:IBM Plex Mono;font-size:0.74rem">
                    <span>VS22→CAPI: <span class="{dc(r['soi_h'])}"><b>{ds(r['soi_h'])}pp</b></span></span>
                    <span>Opportunity (CAPI→Best): <span class="{dc(soi)}"><b>{ds(soi)}pp</b></span></span>
                    <span>Total (VS22→Best): <span class="{dc(r['soi_t'])}"><b>{ds(r['soi_t'])}pp</b></span></span>
                  </div>
                </div>""", unsafe_allow_html=True)
 
            # ── actionable summary ────────────────────────────────────────
            st.markdown("<hr style='border-color:#30363d;margin:16px 0'>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">📋 ACTIONABLE SUMMARY</div>', unsafe_allow_html=True)
 
            gains  = [r for r in impact_rows if r["soi_o"] >  0.01]
            losses = [r for r in impact_rows if r["soi_o"] < -0.01]
            t_opp  = sum(r["soi_o"] for r in gains)
            t_risk = sum(r["soi_o"] for r in losses)
            t_net  = sum(r["soi_o"] for r in impact_rows)
 
            k1, k2, k3, k4 = st.columns(4)
            def kpi(col, lbl, val, sub, col_hex, cls):
                col.markdown(f"""<div class="metric-card" style="border-left:4px solid {col_hex}">
                <div class="metric-label">{lbl}</div>
                <div class="metric-value" style="color:{col_hex}">{val}</div>
                <div class="metric-delta {cls}">{sub}</div></div>""", unsafe_allow_html=True)
 
            kpi(k1,"Total Opportunity",f"+{t_opp:.2f}pp","Gains if achieved","#56d364","dpos")
            kpi(k2,"Total Risk",f"{t_risk:.2f}pp","If losses occur","#f78166","dneg")
            nc = "#56d364" if t_net >= 0 else "#f78166"
            kpi(k3,"Net Impact",f"{ds(t_net)}pp",f"{impact_party} overall",nc,"dpos" if t_net>=0 else "dneg")
            kpi(k4,"Projected Best",f"{best_vs.get(impact_party,0):.1f}%",
                f"vs CAPI {capi_vs.get(impact_party,0):.1f}%",pc_imp,"dpos")
 
            if gains:
                st.markdown(
                    '<div style="font-family:Rajdhani;font-weight:600;font-size:1rem;'
                    'color:#56d364;margin:14px 0 8px">✅ OPPORTUNITIES</div>',
                    unsafe_allow_html=True)
                for r in gains:
                    pri = "🔴 Critical" if r["soi_o"]>=1 else ("🟡 Important" if r["soi_o"]>=0.5 else "🟢 Marginal")
                    est_v = int(r["pct"] * (total_electors or 100000) / 100)
                    st.markdown(f"""
                    <div style="background:#56d36410;border:1px solid #56d36440;border-left:4px solid #56d364;
                    border-radius:8px;padding:12px 16px;margin:5px 0">
                      <div style="font-family:IBM Plex Sans;font-size:0.9rem;color:#e6edf3">
                        {pri} &nbsp;·&nbsp; Need to consolidate <b>{r['caste']}</b> from
                        <span style="color:#e3b341;font-weight:600">{r['caps']:.0f}%</span> →
                        <span style="color:#56d364;font-weight:600">{r['bsts']:.0f}%</span>
                        which will make <span style="color:{pc_imp};font-weight:700">{impact_party}</span>
                        vote share increase by
                        <span style="color:#56d364;font-weight:700">+{r['soi_o']:.2f}pp</span>
                      </div>
                      <div style="font-family:IBM Plex Mono;font-size:0.7rem;color:#8b949e;margin-top:3px">
                        {r['pct']:.1f}% of AC · ~{est_v:,} voters · {r['cat']}
                      </div>
                    </div>""", unsafe_allow_html=True)
 
            if losses:
                st.markdown(
                    '<div style="font-family:Rajdhani;font-weight:600;font-size:1rem;'
                    'color:#f78166;margin:14px 0 8px">⚠️ RISKS</div>',
                    unsafe_allow_html=True)
                for r in losses:
                    pri = "🔴 Critical" if abs(r["soi_o"])>=1 else ("🟡 Important" if abs(r["soi_o"])>=0.5 else "🟢 Manageable")
                    est_v = int(r["pct"] * (total_electors or 100000) / 100)
                    st.markdown(f"""
                    <div style="background:#f7816610;border:1px solid #f7816640;border-left:4px solid #f78166;
                    border-radius:8px;padding:12px 16px;margin:5px 0">
                      <div style="font-family:IBM Plex Sans;font-size:0.9rem;color:#e6edf3">
                        {pri} &nbsp;·&nbsp; Risk: <b>{r['caste']}</b> dropping from
                        <span style="color:#e3b341;font-weight:600">{r['caps']:.0f}%</span> →
                        <span style="color:#f78166;font-weight:600">{r['bsts']:.0f}%</span>
                        will reduce <span style="color:{pc_imp};font-weight:700">{impact_party}</span> by
                        <span style="color:#f78166;font-weight:700">{r['soi_o']:.2f}pp</span>
                      </div>
                      <div style="font-family:IBM Plex Mono;font-size:0.7rem;color:#8b949e;margin-top:3px">
                        {r['pct']:.1f}% of AC · ~{est_v:,} voters · {r['cat']}
                      </div>
                    </div>""", unsafe_allow_html=True)
 
            # ── plain text copy-paste ─────────────────────────────────────
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-header">📤 PLAIN TEXT SUMMARY</div>', unsafe_allow_html=True)
            lines = [
                f"Impact Planner — {selected_ac} | Focus: {impact_party}",
                "="*60, "",
                "VOTE SHARE:",
                f"  VS 2022 : {vs22_vs.get(impact_party,0):.1f}%",
                f"  CAPI    : {capi_vs.get(impact_party,0):.1f}%",
                f"  Best    : {best_vs.get(impact_party,0):.1f}%",
                "", "ACTIONABLE TARGETS:",
            ]
            for r in gains:
                lines.append(f"  ✅ Increase {r['caste']} from {r['caps']:.0f}% → {r['bsts']:.0f}%"
                              f"  →  {impact_party} +{r['soi_o']:.2f}pp")
            for r in losses:
                lines.append(f"  ⚠️  {r['caste']} risk: {r['caps']:.0f}% → {r['bsts']:.0f}%"
                              f"  →  {impact_party} {r['soi_o']:.2f}pp")
            lines += ["", f"Net:  {ds(t_net)}pp  |  Gains: +{t_opp:.2f}pp  |  Risk: {t_risk:.2f}pp"]
            st.text_area("", value="\n".join(lines), height=240, key="t5_txt") 
    else:
        st.error("❌ Could not find required columns (AC Name, Caste (Eng), Caste %).")

else:
    st.markdown('<div class="section-header">MANUAL CASTE ENTRY</div>', unsafe_allow_html=True)
    st.info("Use the sidebar to load data.")

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:40px;padding:16px 24px;background:#161b22;border:1px solid #30363d;border-radius:10px;
            font-family:'IBM Plex Mono';font-size:0.72rem;color:#8b949e;text-align:center">
  AC Caste Vote Simulator · CT01 2026 UP AE CAPI R1 · BJP+RLD Alliance Mode · Survey Analytics Platform
</div>
""", unsafe_allow_html=True)
