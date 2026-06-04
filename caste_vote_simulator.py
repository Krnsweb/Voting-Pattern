import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import re
import pandas as pd
import streamlit as st
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
    --rld:       #F4A261;
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

# ─── Default caste-party affinity (based on UP political dynamics) ─────────────
DEFAULT_CASTE_PARTY_AFFINITY = {
    "Muslim":           {"BJP+": 5,  "SP+INC": 75, "BSP": 12, "RLD": 3,  "Others": 5},
    "Jatav":            {"BJP+": 5,  "SP+INC": 10, "BSP": 80, "RLD": 2,  "Others": 3},
    "Jat":              {"BJP+": 45, "SP+INC": 15, "BSP": 5,  "RLD": 30, "Others": 5},
    "Saini":            {"BJP+": 40, "SP+INC": 35, "BSP": 15, "RLD": 5,  "Others": 5},
    "Kashyap/Nishad":   {"BJP+": 45, "SP+INC": 30, "BSP": 15, "RLD": 5,  "Others": 5},
    "Thakur":           {"BJP+": 70, "SP+INC": 15, "BSP": 5,  "RLD": 5,  "Others": 5},
    "Kamboj":           {"BJP+": 50, "SP+INC": 25, "BSP": 15, "RLD": 5,  "Others": 5},
    "Brahmin":          {"BJP+": 65, "SP+INC": 15, "BSP": 5,  "RLD": 8,  "Others": 7},
    "Kumhar/Prajapat":  {"BJP+": 40, "SP+INC": 30, "BSP": 20, "RLD": 5,  "Others": 5},
    "Gujjar":           {"BJP+": 45, "SP+INC": 20, "BSP": 10, "RLD": 20, "Others": 5},
    "Pal/Gadariya":     {"BJP+": 35, "SP+INC": 35, "BSP": 20, "RLD": 5,  "Others": 5},
    "Valmiki":          {"BJP+": 35, "SP+INC": 20, "BSP": 35, "RLD": 5,  "Others": 5},
    "Baniya":           {"BJP+": 72, "SP+INC": 12, "BSP": 5,  "RLD": 5,  "Others": 6},
    "Tyagi":            {"BJP+": 60, "SP+INC": 20, "BSP": 5,  "RLD": 10, "Others": 5},
    "Teli":             {"BJP+": 45, "SP+INC": 30, "BSP": 15, "RLD": 5,  "Others": 5},
    "Dhobi":            {"BJP+": 25, "SP+INC": 25, "BSP": 42, "RLD": 3,  "Others": 5},
    "Punjabi":          {"BJP+": 65, "SP+INC": 15, "BSP": 5,  "RLD": 10, "Others": 5},
    "OBC_Others":       {"BJP+": 40, "SP+INC": 30, "BSP": 20, "RLD": 5,  "Others": 5},
    "Gen_Others":       {"BJP+": 50, "SP+INC": 25, "BSP": 10, "RLD": 8,  "Others": 7},
    "SC_Others":        {"BJP+": 25, "SP+INC": 20, "BSP": 45, "RLD": 5,  "Others": 5},
    "ST_Others":        {"BJP+": 35, "SP+INC": 25, "BSP": 25, "RLD": 5,  "Others": 10},
    "Jat (OBC)":        {"BJP+": 45, "SP+INC": 20, "BSP": 5,  "RLD": 25, "Others": 5},
    "Dheemar/Dhimar":   {"BJP+": 40, "SP+INC": 30, "BSP": 20, "RLD": 5,  "Others": 5},
    "Khatik/Sonkar":    {"BJP+": 30, "SP+INC": 20, "BSP": 42, "RLD": 3,  "Others": 5},
    "Kayastha":         {"BJP+": 60, "SP+INC": 20, "BSP": 5,  "RLD": 8,  "Others": 7},
}

PARTY_COLORS = {
    "BJP+":   "#FF6B35",
    "SP+INC": "#E63946",
    "BSP":    "#457B9D",
    "RLD":    "#F4A261",
    "Others": "#9B5DE5",
}

PARTIES = list(PARTY_COLORS.keys())

# ─── Helper: compute vote share from caste splits ─────────────────────────────
def compute_vote_share(caste_data: pd.DataFrame, splits: dict) -> dict:
    """
    caste_data: DataFrame with columns [Caste, caste_pct]
    splits: { caste_name: {party: pct, ...}, ... }
    Returns: {party: vote_share_pct}
    """
    totals = {p: 0.0 for p in PARTIES}
    total_pct = caste_data["caste_pct"].sum()

    for _, row in caste_data.iterrows():
        caste = row["Caste"]
        weight = row["caste_pct"] / 100.0
        if caste in splits:
            for party, share in splits[caste].items():
                if party in totals:
                    totals[party] += weight * share

    # Normalize to 100%
    s = sum(totals.values())
    if s > 0:
        totals = {p: round(v * 100 / s, 2) for p, v in totals.items()}
    return totals

def normalize_split(split_dict: dict) -> dict:
    """Normalize a party split dict to sum to 100."""
    s = sum(split_dict.values())
    if s == 0:
        return split_dict
    return {k: round(v * 100 / s, 2) for k, v in split_dict.items()}

def caste_impact_score(caste_pct: float, split_before: dict, split_after: dict, party: str) -> float:
    """How many points does this caste swing contribute to `party`."""
    delta = split_after.get(party, 0) - split_before.get(party, 0)
    return (caste_pct / 100) * delta

    # ─── GOOGLE SHEET BACKEND ─────────────────────────────────────────────
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSonf79A9F3Ezu86qSskR5ed0pdVxZvIgQ6ymaN2omhWALmH-SfoNwUQ3CPLSK4xTOrRAU64TXG8wLj/pub?output=csv"
GOOGLE_SHEET_URL = st.secrets.get(
    "GOOGLE_SHEET_URL",
    ""
)

@st.cache_data(ttl=300)
def load_master_sheet():
    df = pd.read_csv(GOOGLE_SHEET_URL)

    df.columns = [c.strip() for c in df.columns]

    return df

# ─── Sidebar ──────────────────────────────────────────────────────────

with st.sidebar:

    st.markdown(
        '<div class="section-header">CONSTITUENCY SELECTION</div>',
        unsafe_allow_html=True
    )

    if not GOOGLE_SHEET_URL:

        st.error(
            "GOOGLE_SHEET_URL missing in Streamlit secrets."
        )

        st.stop()

    try:

        raw_df = load_master_sheet()

        st.success(
            f"Loaded {len(raw_df):,} caste records"
        )

    except Exception as e:

        st.error(
            f"Google Sheet Load Failed: {e}"
        )

        st.stop()

    districts = sorted(
        raw_df["District"]
        .dropna()
        .unique()
    )

    selected_district = st.selectbox(
        "District",
        districts
    )

    acs = sorted(
        raw_df[
            raw_df["District"] == selected_district
        ]["AC Name"]
        .dropna()
        .unique()
    )

    selected_ac = st.selectbox(
        "Assembly Constituency",
        acs
    )

    st.markdown(
        '<div class="section-header">SURVEY INPUTS</div>',
        unsafe_allow_html=True
    )

    survey_bjp = st.number_input(
        "BJP+ Survey Vote %",
        0.0,
        100.0,
        44.0
    )

    survey_sp = st.number_input(
        "SP+INC Survey Vote %",
        0.0,
        100.0,
        38.0
    )

    survey_bsp = st.number_input(
        "BSP Survey Vote %",
        0.0,
        100.0,
        12.0
    )

    survey_rld = st.number_input(
        "RLD Survey Vote %",
        0.0,
        100.0,
        4.0
    )

    survey_others = st.number_input(
        "Others Survey Vote %",
        0.0,
        100.0,
        2.0
    )

    st.markdown(
        '<div class="section-header">TURNOUT</div>',
        unsafe_allow_html=True
    )

    muslim_turnout = st.slider(
        "Muslim Turnout %",
        50,
        100,
        100
    )

    obc_turnout = st.slider(
        "OBC Turnout %",
        50,
        100,
        100
    )

    sc_turnout = st.slider(
        "SC Turnout %",
        50,
        100,
        100
    )

    gen_turnout = st.slider(
        "GEN Turnout %",
        50,
        100,
        100
    )

    refresh = st.button(
        "🔄 Refresh Data"
    )

    if refresh:

        st.cache_data.clear()

        st.rerun()

    ac_df = raw_df[
    raw_df["AC Name"] == selected_ac
].copy()

ac_df["caste_pct"] = pd.to_numeric(
    ac_df["Caste % [29 May]"],
    errors="coerce"
).fillna(0)

ac_df["Caste"] = (
    ac_df["Caste (Eng)"]
    .astype(str)
    .str.strip()
)

ac_df = ac_df[
    ac_df["caste_pct"] > 0
]

ac_df = ac_df.sort_values(
    "caste_pct",
    ascending=False
)

    st.markdown('<div class="section-header">SURVEY INPUTS</div>', unsafe_allow_html=True)
    survey_bjp    = st.number_input("BJP+ Survey Vote %",    min_value=0.0, max_value=100.0, value=44.0, step=0.5, format="%.1f")
    survey_sp     = st.number_input("SP+INC Survey Vote %",  min_value=0.0, max_value=100.0, value=38.0, step=0.5, format="%.1f")
    survey_bsp    = st.number_input("BSP Survey Vote %",     min_value=0.0, max_value=100.0, value=12.0, step=0.5, format="%.1f")
    survey_rld    = st.number_input("RLD Survey Vote %",     min_value=0.0, max_value=100.0, value=4.0,  step=0.5, format="%.1f")
    survey_others = st.number_input("Others Survey Vote %",  min_value=0.0, max_value=100.0, value=2.0,  step=0.5, format="%.1f")

    survey_input = {
        "BJP+": survey_bjp, "SP+INC": survey_sp,
        "BSP": survey_bsp, "RLD": survey_rld, "Others": survey_others
    }
    survey_total = sum(survey_input.values())
    if abs(survey_total - 100) > 1:
        st.markdown(f'<div class="warn-box">⚠️ Survey totals {survey_total:.1f}%. Ideally should be 100%.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">TURNOUT ADJUSTMENT</div>', unsafe_allow_html=True)
    apply_turnout = st.toggle("Apply differential turnout", value=False)
    if apply_turnout:
        st.caption("Set expected turnout % for each category")
        gen_turnout = st.slider("GEN Turnout %",     40, 95, 68)
        obc_turnout = st.slider("OBC Turnout %",     40, 95, 72)
        sc_turnout  = st.slider("SC Turnout %",      40, 95, 70)
        st_turnout  = st.slider("ST Turnout %",      40, 95, 65)
        muslim_turnout = st.slider("Muslim Turnout %", 40, 95, 75)
        turnout_map = {"GEN": gen_turnout, "OBC": obc_turnout,
                       "SC": sc_turnout, "ST": st_turnout, "Muslim": muslim_turnout}
    else:
        turnout_map = None

# ─── Main Layout ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🗳️ AC Caste Vote Share Simulator</h1>
  <p>Constituency-level caste equation modelling · Scenario switching · Vote share projection</p>
</div>
""", unsafe_allow_html=True)

# ─── Parse & Select AC ────────────────────────────────────────────────────────
if raw_df is not None:
    # Standardise column names
    raw_df.columns = [c.strip() for c in raw_df.columns]
    # Find caste% column (flexible naming)
    pct_col = next((c for c in raw_df.columns if "caste %" in c.lower() or "caste%" in c.lower()), None)
    caste_col = next((c for c in raw_df.columns if "caste (eng)" in c.lower() or (c.lower() == "caste" and "local" not in c.lower())), None)
    ac_col  = next((c for c in raw_df.columns if "ac name" in c.lower()), None)
    cat_col = next((c for c in raw_df.columns if "category" in c.lower()), None)

    if pct_col and caste_col and ac_col:
        raw_df["caste_pct"] = pd.to_numeric(raw_df[pct_col], errors="coerce").fillna(0)
        raw_df["Caste"]     = raw_df[caste_col].astype(str).str.strip()

        ac_list = sorted(raw_df[ac_col].unique().tolist())

        col_ac, col_zone = st.columns([3, 2])
        with col_ac:
            selected_ac = st.selectbox("🏛️ Select Assembly Constituency (AC)", ac_list, index=0)
        with col_zone:
            if "AC Zone" in raw_df.columns:
                zone_info = raw_df[raw_df[ac_col] == selected_ac]["AC Zone"].iloc[0] if len(raw_df[raw_df[ac_col] == selected_ac]) > 0 else "—"
                st.metric("Zone", zone_info)

        ac_df = raw_df[raw_df[ac_col] == selected_ac].copy()
        # Add category if available
        if cat_col:
            ac_df["Category"] = ac_df[cat_col].astype(str)
        else:
            ac_df["Category"] = "OBC"

        # Filter to castes with >0 population
        ac_df = ac_df[ac_df["caste_pct"] > 0].copy()
        ac_df = ac_df.sort_values("caste_pct", ascending=False).reset_index(drop=True)

        # Apply turnout adjustment if enabled
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
            total_electors = pd.to_numeric(raw_df[raw_df[ac_col] == selected_ac]["Total Electors [29 May]"], errors="coerce").iloc[0]

        # ─── Build initial splits from default affinity ────────────────────
        caste_splits_base = {}
        for _, row in ac_df.iterrows():
            c = row["Caste"]
            # Try exact match, then partial
            affinity = DEFAULT_CASTE_PARTY_AFFINITY.get(c)
            if affinity is None:
                for key in DEFAULT_CASTE_PARTY_AFFINITY:
                    if key.lower() in c.lower() or c.lower() in key.lower():
                        affinity = DEFAULT_CASTE_PARTY_AFFINITY[key]
                        break
            if affinity is None:
                cat = str(row.get("Category", "OBC")).upper()
                if cat == "SC":
                    affinity = {"BJP+": 25, "SP+INC": 20, "BSP": 45, "RLD": 5, "Others": 5}
                elif cat == "ST":
                    affinity = {"BJP+": 35, "SP+INC": 25, "BSP": 25, "RLD": 5, "Others": 10}
                elif cat == "GEN":
                    affinity = {"BJP+": 55, "SP+INC": 20, "BSP": 10, "RLD": 8, "Others": 7}
                elif cat == "MUSLIM":
                    affinity = {"BJP+": 5, "SP+INC": 75, "BSP": 12, "RLD": 3, "Others": 5}
                else:
                    affinity = {"BJP+": 40, "SP+INC": 30, "BSP": 20, "RLD": 5, "Others": 5}
            caste_splits_base[c] = normalize_split(affinity.copy())

        # ─── TABS ─────────────────────────────────────────────────────────
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 AC Overview",
            "🎛️ Scenario Builder",
            "📈 Impact Analysis",
            "📋 Caste-Party Matrix"
        ])

        # ══════════════════════════════════════════════════════════════════
        # TAB 1 — AC OVERVIEW
        # ══════════════════════════════════════════════════════════════════
        with tab1:
            # Metrics row
            m1, m2, m3, m4 = st.columns(4)
            base_vs = compute_vote_share(ac_df, caste_splits_base)
            with m1:
                st.markdown(f"""
                <div class="metric-card">
                  <div class="metric-label">Total Electors</div>
                  <div class="metric-value">{int(total_electors):,}</div>
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
                top_party = max(base_vs, key=base_vs.get)
                runner_up = sorted(base_vs, key=base_vs.get, reverse=True)[1]
                margin    = base_vs[top_party] - base_vs[runner_up]
                color = PARTY_COLORS.get(top_party, "#fff")
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid {color};">
                  <div class="metric-label">Projected Winner (Base)</div>
                  <div class="metric-value" style="color:{color};font-size:1.4rem">{top_party}</div>
                  <div class="metric-delta delta-pos">+{margin:.1f}% margin</div>
                </div>""", unsafe_allow_html=True)
            with m4:
                n_castes = len(ac_df)
                st.markdown(f"""
                <div class="metric-card">
                  <div class="metric-label">Caste Groups</div>
                  <div class="metric-value">{n_castes}</div>
                  <div class="metric-delta delta-neu">With non-zero population</div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-header">CASTE COMPOSITION</div>', unsafe_allow_html=True)
            col_chart, col_table = st.columns([5, 4])

            with col_chart:
                # Treemap of caste composition
                fig_tree = px.treemap(
                    ac_df,
                    path=["Category", "Caste"],
                    values="caste_pct",
                    color="caste_pct",
                    color_continuous_scale=["#0d1117", "#1f6feb", "#79c0ff"],
                    title=f"Caste Composition — {selected_ac} AC",
                )
                fig_tree.update_layout(
                    paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                    font=dict(family="IBM Plex Sans", color="#e6edf3"),
                    title_font=dict(family="Rajdhani", size=16, color="#79c0ff"),
                    margin=dict(t=40, l=0, r=0, b=0),
                    height=380,
                    coloraxis_showscale=False,
                )
                fig_tree.update_traces(
                    textfont=dict(family="IBM Plex Sans", color="white"),
                    marker=dict(line=dict(width=2, color="#0d1117"))
                )
                st.plotly_chart(fig_tree, use_container_width=True)

            with col_table:
                display_df = ac_df[["Caste", "Category", "caste_pct"]].copy()
                display_df.columns = ["Caste", "Category", "Share %"]
                display_df["Share %"] = display_df["Share %"].apply(lambda x: f"{x:.2f}%")
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    height=380,
                )

            st.markdown('<div class="section-header">BASE SCENARIO: PROJECTED VOTE SHARE</div>', unsafe_allow_html=True)
            # Bar chart
            fig_bar = go.Figure()
            parties_sorted = sorted(base_vs, key=base_vs.get, reverse=True)
            for p in parties_sorted:
                col = PARTY_COLORS.get(p, "#888")
                fig_bar.add_trace(go.Bar(
                    x=[p], y=[base_vs[p]],
                    marker_color=col,
                    text=[f"{base_vs[p]:.1f}%"],
                    textposition="outside",
                    textfont=dict(family="Rajdhani", size=16, color=col),
                    name=p,
                ))
            # Survey comparison
            for p in parties_sorted:
                col = PARTY_COLORS.get(p, "#888")
                fig_bar.add_trace(go.Bar(
                    x=[p], y=[survey_input.get(p, 0)],
                    marker_color=col, opacity=0.3,
                    marker_line=dict(color=col, width=2),
                    text=[f"Survey: {survey_input.get(p,0):.1f}%"],
                    textposition="outside",
                    textfont=dict(family="Rajdhani", size=12, color="#8b949e"),
                    name=f"{p} (Survey)",
                    showlegend=True,
                ))
            fig_bar.update_layout(
                paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Sans", color="#e6edf3"),
                barmode="group",
                showlegend=False,
                xaxis=dict(showgrid=False, tickfont=dict(family="Rajdhani", size=14)),
                yaxis=dict(showgrid=True, gridcolor="#30363d", range=[0, 100],
                           ticksuffix="%", tickfont=dict(family="IBM Plex Mono")),
                margin=dict(t=20, l=0, r=0, b=0),
                height=280,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # ══════════════════════════════════════════════════════════════════
        # TAB 2 — SCENARIO BUILDER
        # ══════════════════════════════════════════════════════════════════
        with tab2:
            st.markdown('<div class="info-box">💡 Adjust how each caste splits its vote between parties. The simulator will instantly recompute the projected vote share and show you the delta vs the base scenario.</div>', unsafe_allow_html=True)

            # Build editable splits in session state
            if "modified_splits" not in st.session_state:
                st.session_state["modified_splits"] = {k: v.copy() for k, v in caste_splits_base.items()}

            # Filter selector
            filter_cat = st.multiselect(
                "Filter castes by category:",
                options=["All"] + sorted(ac_df["Category"].unique().tolist()),
                default=["All"]
            )
            show_all = "All" in filter_cat or not filter_cat
            cats_to_show = ac_df["Category"].unique() if show_all else filter_cat

            filtered_df = ac_df[ac_df["Category"].isin(cats_to_show)].copy()

            scenario_splits = {k: v.copy() for k, v in caste_splits_base.items()}

            for _, row in filtered_df.iterrows():
                caste = row["Caste"]
                cpct  = row["caste_pct"]
                cat   = row.get("Category", "")
                cur   = st.session_state["modified_splits"].get(caste, caste_splits_base.get(caste, {}))

                with st.expander(f"🔹 **{caste}** ({cat}) — {cpct:.2f}% of AC voters", expanded=cpct > 10):
                    ec1, ec2, ec3, ec4, ec5 = st.columns(5)
                    new_split = {}
                    cols_exp = [ec1, ec2, ec3, ec4, ec5]
                    for i, party in enumerate(PARTIES):
                        with cols_exp[i]:
                            pcol = PARTY_COLORS[party]
                            val = st.number_input(
                                f"{party}",
                                min_value=0.0, max_value=100.0,
                                value=float(cur.get(party, 0)),
                                step=1.0, format="%.1f",
                                key=f"split_{caste}_{party}"
                            )
                            new_split[party] = val

                    split_total = sum(new_split.values())
                    if abs(split_total - 100) > 0.5:
                        st.warning(f"⚠️ Split totals {split_total:.1f}% — will be normalized to 100%")
                    normalized = normalize_split(new_split)
                    st.session_state["modified_splits"][caste] = normalized
                    scenario_splits[caste] = normalized

                    # Mini visualization inside expander
                    mini_fig = go.Figure()
                    for party in PARTIES:
                        mini_fig.add_trace(go.Bar(
                            x=[party],
                            y=[normalized.get(party, 0)],
                            marker_color=PARTY_COLORS[party],
                            text=[f"{normalized.get(party,0):.0f}%"],
                            textposition="outside",
                            textfont=dict(size=10)
                        ))
                    mini_fig.update_layout(
                        paper_bgcolor="#1c2333", plot_bgcolor="#1c2333",
                        height=140, showlegend=False,
                        margin=dict(t=10, l=0, r=0, b=0),
                        yaxis=dict(range=[0, 110], showgrid=False, showticklabels=False),
                        xaxis=dict(showgrid=False, tickfont=dict(size=10, family="Rajdhani")),
                    )
                    st.plotly_chart(mini_fig, use_container_width=True)

            # ── Result comparison ─────────────────────────────────────────
            scenario_vs = compute_vote_share(ac_df, scenario_splits)

            st.markdown('<div class="section-header">SCENARIO RESULT vs BASE</div>', unsafe_allow_html=True)
            rcols = st.columns(5)
            for i, party in enumerate(PARTIES):
                base_val = base_vs.get(party, 0)
                scen_val = scenario_vs.get(party, 0)
                delta    = scen_val - base_val
                delta_class = "delta-pos" if delta > 0 else ("delta-neg" if delta < 0 else "delta-neu")
                delta_sign  = "+" if delta > 0 else ""
                pcol = PARTY_COLORS[party]
                with rcols[i]:
                    st.markdown(f"""
                    <div class="metric-card" style="border-left: 4px solid {pcol};">
                      <div class="metric-label">{party}</div>
                      <div class="metric-value" style="color:{pcol}">{scen_val:.1f}%</div>
                      <div class="metric-delta {delta_class}">{delta_sign}{delta:.1f}% vs base</div>
                    </div>""", unsafe_allow_html=True)

            # Winner analysis
            scen_top = max(scenario_vs, key=scenario_vs.get)
            scen_2nd = sorted(scenario_vs, key=scenario_vs.get, reverse=True)[1]
            scen_margin = scenario_vs[scen_top] - scenario_vs[scen_2nd]
            base_top = max(base_vs, key=base_vs.get)

            if scen_top != base_top:
                st.markdown(f"""
                <div class="warn-box">
                🔄 <b>SEAT FLIP DETECTED!</b> Base scenario winner: <b>{base_top}</b> ({base_vs[base_top]:.1f}%)
                → Scenario winner: <b>{scen_top}</b> ({scenario_vs[scen_top]:.1f}%). Margin: {scen_margin:.1f}%.
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="info-box">
                ✅ <b>{scen_top}</b> remains projected winner. Margin vs {scen_2nd}: <b>{scen_margin:.1f}%</b>.
                </div>""", unsafe_allow_html=True)

            col_rl, col_rr = st.columns(2)
            with col_rl:
                # Radar chart
                cats_radar  = PARTIES
                base_vals   = [base_vs.get(p, 0) for p in PARTIES]
                scen_vals   = [scenario_vs.get(p, 0) for p in PARTIES]
                fig_radar   = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=base_vals + [base_vals[0]],
                    theta=cats_radar + [cats_radar[0]],
                    fill="toself", name="Base",
                    line=dict(color="#79c0ff"), fillcolor="rgba(121,192,255,0.15)"
                ))
                fig_radar.add_trace(go.Scatterpolar(
                    r=scen_vals + [scen_vals[0]],
                    theta=cats_radar + [cats_radar[0]],
                    fill="toself", name="Scenario",
                    line=dict(color="#f78166"), fillcolor="rgba(247,129,102,0.15)"
                ))
                fig_radar.update_layout(
                    polar=dict(
                        bgcolor="#1c2333",
                        radialaxis=dict(visible=True, range=[0, 80], color="#8b949e"),
                        angularaxis=dict(color="#e6edf3")
                    ),
                    paper_bgcolor="#161b22",
                    font=dict(family="IBM Plex Sans", color="#e6edf3"),
                    legend=dict(font=dict(family="Rajdhani")),
                    title=dict(text="Base vs Scenario — Radar", font=dict(family="Rajdhani", color="#79c0ff", size=14)),
                    margin=dict(t=40, l=20, r=20, b=20),
                    height=320,
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            with col_rr:
                # Delta waterfall
                delta_data = {p: scenario_vs.get(p, 0) - base_vs.get(p, 0) for p in PARTIES}
                fig_delta  = go.Figure(go.Bar(
                    x=list(delta_data.keys()),
                    y=list(delta_data.values()),
                    marker_color=["#56d364" if v >= 0 else "#f78166" for v in delta_data.values()],
                    text=[f"{'+' if v >= 0 else ''}{v:.1f}%" for v in delta_data.values()],
                    textposition="outside",
                    textfont=dict(family="Rajdhani", size=13),
                ))
                fig_delta.update_layout(
                    paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                    title=dict(text="Vote Share Delta (Scenario − Base)", font=dict(family="Rajdhani", color="#79c0ff", size=14)),
                    font=dict(family="IBM Plex Sans", color="#e6edf3"),
                    yaxis=dict(showgrid=True, gridcolor="#30363d", ticksuffix="%",
                               zeroline=True, zerolinecolor="#8b949e", zerolinewidth=1,
                               tickfont=dict(family="IBM Plex Mono")),
                    xaxis=dict(showgrid=False, tickfont=dict(family="Rajdhani", size=13)),
                    margin=dict(t=40, l=0, r=0, b=0),
                    height=320,
                )
                st.plotly_chart(fig_delta, use_container_width=True)

        # ══════════════════════════════════════════════════════════════════
        # TAB 3 — IMPACT ANALYSIS
        # ══════════════════════════════════════════════════════════════════
        with tab3:
            st.markdown('<div class="section-header">CASTE IMPACT ON EACH PARTY</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">This tab shows how much each caste contributes to a party\'s vote share (Base scenario), and how much it swings under the current scenario. Select a party to analyze:</div>', unsafe_allow_html=True)

            focus_party = st.selectbox("Analyze impact for party:", PARTIES, index=0)

            impact_rows = []
            for _, row in ac_df.iterrows():
                caste    = row["Caste"]
                cpct     = row["caste_pct"]
                base_sp  = caste_splits_base.get(caste, {}).get(focus_party, 0)
                scen_sp  = st.session_state["modified_splits"].get(caste, caste_splits_base.get(caste, {})).get(focus_party, 0)
                base_contrib  = (cpct / 100) * base_sp
                scen_contrib  = (cpct / 100) * scen_sp
                swing         = scen_contrib - base_contrib
                impact_rows.append({
                    "Caste":      caste,
                    "Caste %":    cpct,
                    "Base Split": base_sp,
                    "Scen Split": scen_sp,
                    "Base Contrib": round(base_contrib, 2),
                    "Scen Contrib": round(scen_contrib, 2),
                    "Swing":      round(swing, 2),
                })

            impact_df = pd.DataFrame(impact_rows).sort_values("Base Contrib", ascending=False)

            # Visual impact bars
            pcol_focus = PARTY_COLORS.get(focus_party, "#79c0ff")

            for _, irow in impact_df.iterrows():
                bc   = irow["Base Contrib"]
                sc   = irow["Scen Contrib"]
                sw   = irow["Swing"]
                max_c = impact_df["Base Contrib"].max() or 1
                bar_w = int((bc / max_c) * 100)
                sw_class = "delta-pos" if sw > 0 else ("delta-neg" if sw < 0 else "delta-neu")
                sw_str   = f"+{sw:.2f}" if sw > 0 else f"{sw:.2f}"
                st.markdown(f"""
                <div class="impact-bar-wrap">
                  <div class="impact-bar-label">
                    <span><b>{irow['Caste']}</b> <span style="color:#8b949e;font-size:0.78rem">({irow['Caste %']:.1f}% of AC | base split {irow['Base Split']:.0f}% → scen {irow['Scen Split']:.0f}%)</span></span>
                    <span>Base: <b>{bc:.2f}pp</b> &nbsp; Swing: <span class="{sw_class}"><b>{sw_str}pp</b></span></span>
                  </div>
                  <div class="impact-bar-bg">
                    <div class="impact-bar-fill" style="width:{bar_w}%;background:{pcol_focus};opacity:0.85"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

            # Tornado chart — biggest swingers
            st.markdown('<div class="section-header">SWING TORNADO — TOP MOVERS FOR {}</div>'.format(focus_party), unsafe_allow_html=True)
            tornado_df = impact_df.sort_values("Swing", key=abs, ascending=False).head(10)

            fig_tornado = go.Figure()
            fig_tornado.add_trace(go.Bar(
                y=tornado_df["Caste"],
                x=tornado_df["Swing"],
                orientation="h",
                marker_color=[pcol_focus if v >= 0 else "#f78166" for v in tornado_df["Swing"]],
                text=[f"{'+' if v >= 0 else ''}{v:.2f}pp" for v in tornado_df["Swing"]],
                textposition="outside",
                textfont=dict(family="Rajdhani", size=12),
            ))
            fig_tornado.update_layout(
                paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Sans", color="#e6edf3"),
                title=dict(text=f"Top 10 Caste Swing Drivers for {focus_party}", font=dict(family="Rajdhani", color=pcol_focus, size=15)),
                xaxis=dict(showgrid=True, gridcolor="#30363d", zeroline=True,
                           zerolinecolor="#8b949e", ticksuffix="pp",
                           tickfont=dict(family="IBM Plex Mono")),
                yaxis=dict(showgrid=False, tickfont=dict(family="IBM Plex Sans", size=12)),
                margin=dict(t=40, l=0, r=60, b=0),
                height=380,
            )
            st.plotly_chart(fig_tornado, use_container_width=True)

            # Caste contribution stacked chart
            st.markdown('<div class="section-header">CASTE CONTRIBUTION TO EACH PARTY</div>', unsafe_allow_html=True)
            contrib_fig = go.Figure()
            for party in PARTIES:
                contribs = []
                for _, row in ac_df.iterrows():
                    c = row["Caste"]
                    sp = caste_splits_base.get(c, {}).get(party, 0)
                    contribs.append((row["caste_pct"] / 100) * sp)
                contrib_fig.add_trace(go.Bar(
                    name=party,
                    x=ac_df["Caste"].tolist(),
                    y=contribs,
                    marker_color=PARTY_COLORS[party],
                ))
            contrib_fig.update_layout(
                barmode="stack",
                paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Sans", color="#e6edf3"),
                title=dict(text="Caste-wise Vote Contribution to Each Party (Base)", font=dict(family="Rajdhani", color="#79c0ff", size=14)),
                xaxis=dict(showgrid=False, tickangle=-35, tickfont=dict(family="IBM Plex Sans", size=10)),
                yaxis=dict(showgrid=True, gridcolor="#30363d", ticksuffix="pp",
                           tickfont=dict(family="IBM Plex Mono")),
                legend=dict(font=dict(family="Rajdhani")),
                margin=dict(t=40, l=0, r=0, b=80),
                height=380,
            )
            st.plotly_chart(contrib_fig, use_container_width=True)

        # ══════════════════════════════════════════════════════════════════
        # TAB 4 — CASTE-PARTY MATRIX
        # ══════════════════════════════════════════════════════════════════
        with tab4:
            st.markdown('<div class="section-header">CASTE–PARTY AFFINITY MATRIX</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">Heatmap shows base caste split %. Darker = stronger affinity. Castes with >5% population are highlighted as "dominant."</div>', unsafe_allow_html=True)

            matrix_rows = []
            for _, row in ac_df.iterrows():
                c    = row["Caste"]
                cpct = row["caste_pct"]
                sp   = caste_splits_base.get(c, {})
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
                text=[[f"{v:.0f}%" for v in row] for row in matrix_df.values],
                texttemplate="%{text}",
                textfont=dict(family="IBM Plex Mono", size=11, color="white"),
                showscale=True,
                colorbar=dict(
                    ticksuffix="%",
                    tickfont=dict(family="IBM Plex Mono", color="#e6edf3"),
                    bgcolor="#161b22",
                    bordercolor="#30363d",
                )
            ))
            fig_hm.update_layout(
                paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                font=dict(family="IBM Plex Sans", color="#e6edf3"),
                title=dict(text="Caste–Party Affinity Matrix (Base Scenario)", font=dict(family="Rajdhani", color="#79c0ff", size=15)),
                xaxis=dict(tickfont=dict(family="Rajdhani", size=13, color="#e6edf3"), side="top"),
                yaxis=dict(tickfont=dict(family="IBM Plex Sans", size=10, color="#e6edf3"), autorange="reversed"),
                margin=dict(t=60, l=0, r=0, b=0),
                height=max(400, len(matrix_df) * 28 + 80),
            )
            st.plotly_chart(fig_hm, use_container_width=True)

            # Dominant caste table
            st.markdown('<div class="section-header">DOMINANT CASTES (>5% of AC) — KEY BATTLEGROUND</div>', unsafe_allow_html=True)
            dominant = ac_df[ac_df["caste_pct"] >= 5].copy()
            if len(dominant) == 0:
                dominant = ac_df.head(5)

            for _, dr in dominant.iterrows():
                caste = dr["Caste"]
                cpct  = dr["caste_pct"]
                sp    = caste_splits_base.get(caste, {})
                top_p = max(sp, key=sp.get)
                top_v = sp[top_p]
                pc    = PARTY_COLORS.get(top_p, "#888")

                badges = " ".join([
                    f'<span class="party-badge" style="background:{PARTY_COLORS.get(p,"#888")}22;color:{PARTY_COLORS.get(p,"#888")};border:1px solid {PARTY_COLORS.get(p,"#888")}44">{p}: {sp.get(p,0):.0f}%</span>'
                    for p in PARTIES if sp.get(p, 0) > 5
                ])
                est_votes = int(dr.get("caste_pct", 0) * (total_electors or 100000) / 100) if total_electors else "—"

                st.markdown(f"""
                <div class="impact-bar-wrap" style="border-left:4px solid {pc}">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                    <span style="font-family:Rajdhani;font-size:1.1rem;font-weight:700;color:#e6edf3">{caste}</span>
                    <span style="font-family:IBM Plex Mono;font-size:0.75rem;color:#8b949e">{cpct:.1f}% of AC · ~{est_votes:,} voters</span>
                  </div>
                  <div style="margin-bottom:4px">{badges}</div>
                  <div style="font-size:0.8rem;color:#8b949e">Leans: <span style="color:{pc};font-weight:600">{top_p} ({top_v:.0f}%)</span></div>
                </div>""", unsafe_allow_html=True)

    else:
        st.error("❌ Could not find required columns. Please ensure your CSV has: AC Name, Caste (Eng), and Caste % columns.")

else:
    # Manual entry mode
    st.markdown('<div class="section-header">MANUAL CASTE ENTRY</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Enter your constituency\'s caste data manually below.</div>', unsafe_allow_html=True)
    st.info("Use the sidebar to switch to 'Use Sample Data' for a pre-loaded example.")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:40px;padding:16px 24px;background:#161b22;border:1px solid #30363d;border-radius:10px;
            font-family:'IBM Plex Mono';font-size:0.72rem;color:#8b949e;text-align:center">
  AC Caste Vote Simulator · CT01 2026 UP AE CAPI R1 · Survey Analytics Platform · For internal use only
</div>
""", unsafe_allow_html=True)
