# AC Caste Vote Share Simulator
## Setup & Run (5 minutes)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run caste_vote_simulator.py
```
Opens at http://localhost:8501

---

## How to use with your Google Sheet

1. Open your Google Sheet with caste data
2. File → Download → CSV (.csv)
3. In the app sidebar → select "📊 Paste Google Sheet CSV"
4. Paste the CSV contents in the text area

**Required columns:** `AC Name`, `Caste (Eng)`, `Caste % [29 May]`, `Category`

---

## Features

| Feature | What it does |
|---------|-------------|
| **AC Selector** | Pick any constituency from your sheet |
| **Survey Inputs** | Enter your field survey vote % from the sidebar |
| **Scenario Builder** | Tab 2 — adjust each caste's party split using number inputs |
| **Impact Analysis** | Tab 3 — tornado chart of which castes swing the result most |
| **Caste-Party Matrix** | Tab 4 — heatmap of all caste affinities |
| **Turnout Adjustment** | Toggle in sidebar — apply differential turnout by category |
| **Seat Flip Alert** | Auto-detects when scenario changes the projected winner |

---

## Data Model

The app ships with default UP caste-party affinities based on 2022 VS patterns:

| Caste | Category | Leans Toward |
|-------|----------|-------------|
| Muslim | Muslim | SP+INC (~75%) |
| Jatav | SC | BSP (~80%) |
| Thakur | GEN | BJP+ (~70%) |
| Brahmin | GEN | BJP+ (~65%) |
| Baniya | GEN | BJP+ (~72%) |
| Jat | GEN/OBC | RLD/BJP split |
| Yadav (via SP+INC) | OBC | SP+INC |
| Kashyap/Nishad | OBC | BJP+ (~45%) |
| Saini | OBC | BJP+/SP split |

These are starting points — override in the Scenario Builder tab for each AC.
