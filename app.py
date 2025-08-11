# app.py
import streamlit as st
import json
import difflib
from pathlib import Path

# ---------- Config ----------
MAPPING_FILE = "data/drug_name_mapping.json"
INTERACTIONS_FILE = "data/interactions_db.json"
SIDE_EFFECTS_FILE = "data/side_effects_db.json"
FUZZY_CUTOFF = 0.5
MAX_SUGGESTIONS = 10

# ---------- Helpers ----------
@st.cache_data
def load_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

def normalize(s: str):
    return s.strip().lower()

def get_closest_matches(input_name, candidates, n=MAX_SUGGESTIONS, cutoff=FUZZY_CUTOFF):
    return difflib.get_close_matches(input_name.lower(), candidates, n=n, cutoff=cutoff)

def lookup_generic_from_brand(brand_name, normalized_mapping):
    key = normalize(brand_name)
    return normalized_mapping.get(key)

def build_pair_key(g1, g2, sep="|"):
    return f"{g1}{sep}{g2}"

def find_interaction(db, g1, g2):
    """Check interaction regardless of order or separator."""
    g1 = normalize(g1)
    g2 = normalize(g2)
    # Try both orders with both separators
    possible_keys = [
        build_pair_key(g1, g2, "|"),
        build_pair_key(g2, g1, "|"),
        build_pair_key(g1, g2, "||"),
        build_pair_key(g2, g1, "||")
    ]
    for key in possible_keys:
        if key in db:
            return db[key]
    return None

# ---------- Load data ----------
st.set_page_config(page_title="Drug Interaction Checker",page_icon="icon.png", layout="wide")
st.title("💊Drug Interaction & Side Effects Checker🧠")

drug_mapping = load_json(MAPPING_FILE)
if not drug_mapping:
    st.error(f"Missing or empty {MAPPING_FILE}. Put your mapping file in the app folder.")
    st.stop()

normalized_mapping = {k.strip().lower(): v.lower() for k, v in drug_mapping.items()}
all_brand_names = sorted(normalized_mapping.keys())

interactions_db = load_json(INTERACTIONS_FILE)
side_effects_db = load_json(SIDE_EFFECTS_FILE)

# ---------- UI ----------
st.markdown("Enter two drug names (brand or generic). The app will suggest matches from the local dataset.")

col1, col2 = st.columns(2)
with col1:
    raw1 = st.text_input("Enter the first drug name", key="drug1_raw")
with col2:
    raw2 = st.text_input("Enter the second drug name", key="drug2_raw")

def suggest_and_choose(raw_value, label_suffix):
    if not raw_value:
        return None, None
    normalized = normalize(raw_value)
    if normalized in normalized_mapping:
        generic = normalized_mapping[normalized]
        return normalized, generic
    suggestions = get_closest_matches(normalized, all_brand_names, n=MAX_SUGGESTIONS, cutoff=FUZZY_CUTOFF)
    if suggestions:
        chosen = st.selectbox(f"Did you mean (for {label_suffix})?", ["-- choose --"] + suggestions, key=f"suggest_{label_suffix}")
        if chosen and chosen != "-- choose --":
            return chosen, normalized_mapping[chosen]
    for brand, gen in normalized_mapping.items():
        if gen == normalized:
            return brand, normalized
    return None, None

with st.spinner("Finding matches..."):
    brand1_key, generic1 = suggest_and_choose(raw1, "drug1")
    brand2_key, generic2 = suggest_and_choose(raw2, "drug2")

st.write("---")
st.write("**Selected mapping:**")
st.write({
    "drug1_brand_key": brand1_key,
    "drug1_generic": generic1,
    "drug2_brand_key": brand2_key,
    "drug2_generic": generic2
})

if st.button("🔍 Check Interaction"):
    if not raw1 or not raw2:
        st.error("Please enter both drug names.")
    else:
        if not generic1 or not generic2:
            st.error("❌ One or both drug names not recognized.")
            st.write("Closest matches for drug 1:", get_closest_matches(normalize(raw1), all_brand_names, n=5))
            st.write("Closest matches for drug 2:", get_closest_matches(normalize(raw2), all_brand_names, n=5))
        else:
            st.success(f"✅ Generic names matched: **{generic1.title()}** and **{generic2.title()}**")
            interaction = find_interaction(interactions_db, generic1, generic2)
            if interaction:
                severity = interaction.get("severity", "unknown").title()
                st.warning(f"⚠️ Interaction severity: {severity}")
                st.write(interaction.get("description"))
                st.info("Advice: " + interaction.get("advice", "Follow clinical guidance."))
            else:
                st.success("✅ No interaction found in local DB for this pair.")

            st.subheader(f"🔬 Side Effects of {raw1.title()}")
            s1 = side_effects_db.get(generic1, [])
            st.write(s1 or "No local side effects data available.")

            st.subheader(f"🔬 Side Effects of {raw2.title()}")
            s2 = side_effects_db.get(generic2, [])
            st.write(s2 or "No local side effects data available.")
