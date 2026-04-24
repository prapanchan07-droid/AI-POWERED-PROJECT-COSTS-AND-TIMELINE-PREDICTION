import streamlit as st
from model import predict_project
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Optimizer", layout="wide")

# ------------------ PREMIUM CSS ------------------
st.markdown("""
<style>

/* Background */
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Title */
.main-title {
    font-size: 42px;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 16px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Card title */
.card-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 15px;
    color: #38bdf8;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #6366f1, #38bdf8);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 18px;
    font-weight: 600;
}

/* Success / Error */
.success {
    color: #22c55e;
    font-weight: 600;
}

.error {
    color: #ef4444;
    font-weight: 600;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown('<div class="main-title">🚀 AI Project Optimizer</div>', unsafe_allow_html=True)
st.markdown("### Smart Decision Support for Cost & Timeline")

st.divider()

# ------------------ SESSION STATE ------------------
if "team" not in st.session_state:
    st.session_state.team = 1
if "tools" not in st.session_state:
    st.session_state.tools = 1
if "budget" not in st.session_state:
    st.session_state.budget = 0
if "complexity" not in st.session_state:
    st.session_state.complexity = "Low"

# ------------------ INPUTS ------------------
col1, col2 = st.columns(2)

with col1:
    st.session_state.team = st.slider("👨‍💻 Team Size", 1, 50, st.session_state.team)
    st.session_state.tools = st.slider("🧰 Tools Level", 1, 10, st.session_state.tools)

with col2:
    st.session_state.budget = st.number_input("💰 Budget ($)", 0, 10000000, st.session_state.budget)
    st.session_state.complexity = st.selectbox(
        "📊 Complexity", ["Low", "Medium", "High"],
        index=["Low","Medium","High"].index(st.session_state.complexity)
    )

team = st.session_state.team
tools = st.session_state.tools
budget = st.session_state.budget
complexity = st.session_state.complexity

complexity_map = {"Low": 1, "Medium": 2, "High": 3}
complexity_val = complexity_map[complexity]

# ------------------ PREDICTION ------------------
cost, time = predict_project(team, budget, tools, complexity_val)

# ------------------ TABS ------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Overview",
    "💰 Budget",
    "🧠 Planning",
    "🔄 Scenario",
    "🤖 Advisor",
    "📊 Analysis"
])

# ------------------ OVERVIEW ------------------
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📈 Prediction Results</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.metric("Estimated Cost", f"${int(cost):,}")
    with col4:
        st.metric("Estimated Time", f"{int(time)} days")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ BUDGET ------------------
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">💰 Budget Analysis</div>', unsafe_allow_html=True)

    gap = cost - budget
    if gap > 0:
        st.markdown(f'<p class="error">Over budget by ${int(gap):,}</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="success">Under budget by ${int(-gap):,}</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ PLANNING ------------------
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🧠 Auto Planning</div>', unsafe_allow_html=True)

    best_plan = None

    for t in range(5, 50):
        for tool in range(1, 10):
            c, tm = predict_project(t, budget, tool, complexity_val)
            if c <= budget:
                best_plan = (t, tool, c, tm)
                break
        if best_plan:
            break

    if best_plan:
        st.success(f"""
        ✔ Team: {best_plan[0]} | Tools: {best_plan[1]}  
        Cost: ${int(best_plan[2]):,} | Time: {int(best_plan[3])} days
        """)

        if st.button("🚀 Apply Optimal Plan"):
            st.session_state.team = best_plan[0]
            st.session_state.tools = best_plan[1]
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ SCENARIO ------------------
with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔄 Scenario Comparison</div>', unsafe_allow_html=True)

    if best_plan:
        opt_cost, opt_time = best_plan[2], best_plan[3]
    else:
        opt_cost, opt_time = cost, time

    df = pd.DataFrame({
        "Scenario": ["Current", "Optimized"],
        "Cost": [cost, opt_cost],
        "Time": [time, opt_time]
    })

    st.dataframe(df)

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ ADVISOR ------------------
with tab5:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🤖 Smart Advisor</div>', unsafe_allow_html=True)

    reduced_team = max(1, team - 5)
    inc_team = min(50, team + 5)

    st.write(f"Reduce team → Save cost, increase time")
    st.write(f"Increase team → Increase cost, reduce time")

    colA, colB = st.columns(2)

    with colA:
        if st.button("⬇ Reduce Team"):
            st.session_state.team = reduced_team
            st.rerun()

    with colB:
        if st.button("⬆ Increase Team"):
            st.session_state.team = inc_team
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ ANALYSIS ------------------
with tab6:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📊 What-if Analysis</div>', unsafe_allow_html=True)

    teams = list(range(1, 50))
    costs = []

    for t in teams:
        c, _ = predict_project(t, budget, tools, complexity_val)
        costs.append(c)

    df = pd.DataFrame({"Team": teams, "Cost": costs})
    st.line_chart(df.set_index("Team"))

    st.markdown('</div>', unsafe_allow_html=True)