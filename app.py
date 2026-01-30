import streamlit as st
import random
import json
import itertools

DATA_FILE = "nfl_qb_rankings.json"

# -----------------------
# Load / Save ratings
# -----------------------
def load_qbs():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "Jordan Love": 1500,
            "Caleb Williams": 1500,
            "JJ McCarthy": 1500,
            "Jared Goff": 1500,
            "Dak Prescott": 1500,
            "Jaxon Dart": 1500,
            "Jalen Hurts": 1500,
            "Jayden Daniels": 1500,
            "Matt Stafford": 1500,
            "Sam Darnold": 1500,
            "Kyler Murray": 1500,
            "Brock Purdy": 1500,
            "Tyler Shough": 1500,
            "Baker Mayfield": 1500,
            "Bryce Young": 1500,
            "Michael Penix": 1500,
            "Josh Allen": 1500,
            "Tua Tagovailoa": 1500,
            "Drake Maye": 1500,
            "Justin Fields": 1500,
            "Cam Ward": 1500,
            "Trevor Lawrence": 1500,
            "CJ Stroud": 1500,
            "Daniel Jones": 1500,
            "Shedeur Sanders": 1500,
            "Lamar Jackson": 1500,
            "Aaron Rodgers": 1500,
            "Joe Burrow": 1500,
            "Justin Herbert": 1500,
            "Geno Smith": 1500,
            "Bo Nix": 1500,
            "Patrick Mahomes": 1500
        }

def save_qbs(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# -----------------------
# Elo function (yours)
# -----------------------
def update_elo(a, b, winner, k=32):
    expected_a = 1 / (1 + 10 ** ((b - a) / 400))
    expected_b = 1 - expected_a
    if winner == "A":
        return a + k * (1 - expected_a), b + k * (0 - expected_b)
    else:
        return a + k * (0 - expected_a), b + k * (1 - expected_b)

# -----------------------
# App state
# -----------------------
if "ratings" not in st.session_state:
    st.session_state.ratings = load_qbs()

if "pairs" not in st.session_state:
    st.session_state.pairs = list(itertools.combinations(st.session_state.ratings.keys(), 2))
    random.shuffle(st.session_state.pairs)

# Track index instead of popping (prevents regeneration issues)
if "pair_index" not in st.session_state:
    st.session_state.pair_index = 0

def get_current_pair():
    if st.session_state.pair_index >= len(st.session_state.pairs):
        return None
    return st.session_state.pairs[st.session_state.pair_index]

st.session_state.current_pair = get_current_pair()


# -----------------------
# UI
# -----------------------
st.title("🏈 QB Rankings")
st.write("Tap the QB you prefer")

if st.session_state.current_pair is None:
    st.success("All matchups completed!")
    st.stop()

qb_a, qb_b = st.session_state.current_pair

col1, col2 = st.columns(2)

with col1:
    if st.button(qb_a):
        new_a, new_b = update_elo(
            st.session_state.ratings[qb_a],
            st.session_state.ratings[qb_b],
            "A"
        )
        st.session_state.ratings[qb_a] = new_a
        st.session_state.ratings[qb_b] = new_b
        save_qbs(st.session_state.ratings)
        st.session_state.pair_index += 1 if st.session_state.pairs else None
        st.experimental_rerun()

with col2:
    if st.button(qb_b):
        new_a, new_b = update_elo(
            st.session_state.ratings[qb_a],
            st.session_state.ratings[qb_b],
            "B"
        )
        st.session_state.ratings[qb_a] = new_a
        st.session_state.ratings[qb_b] = new_b
        save_qbs(st.session_state.ratings)
        st.session_state.pair_index += 1 if st.session_state.pairs else None
        st.experimental_rerun()

# -----------------------
# Rankings
# -----------------------
st.divider()
st.subheader("Current Rankings")

ranked = sorted(
    st.session_state.ratings.items(),
    key=lambda x: x[1],
    reverse=True
)

for i, (qb, elo) in enumerate(ranked, start=1):
    st.write(f"{i}. {qb} — {round(elo)}")
