import streamlit as st
from model import predict_project
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Project Predictor",
    page_icon="🚀",
    layout="wide"
)

# ------------------ HEADER ------------------
st.title("🚀 AI Project Cost & Timeline Predictor")
st.markdown("### Smart Decision Support System")

st.divider()

# ------------------ SIDEBAR ------------------
st.sidebar.title("ℹ️ About")
st.sidebar.info("""
This AI system predicts **project cost and timeline**
based on:
- Team size 👨‍💻  
- Budget 💰  
- Tools 🧰  
- Complexity 📊  

It helps in **better planning and decision-making**.
""")

# ------------------ INPUT SECTION ------------------
st.markdown("## 🔧 Project Inputs")

col1, col2 = st.columns(2)

with col1:
    team = st.slider("👨‍💻 Team Size", 1, 50, 10)
    tools = st.slider("🧰 Tools Level", 1, 10, 5)

with col2:
    budget = st.number_input("💰 Budget ($)", 10000, 10000000, 500000)
    complexity = st.selectbox("📊 Complexity", ["Low", "Medium", "High"])

complexity_map = {"Low": 1, "Medium": 2, "High": 3}
complexity_val = complexity_map[complexity]

st.divider()

# ------------------ SESSION STATE ------------------
if "result" not in st.session_state:
    st.session_state.result = None

# ------------------ PREDICT BUTTON ------------------
if st.button("🚀 Predict", use_container_width=True):
    cost, time = predict_project(team, budget, tools, complexity_val)
    st.session_state.result = (cost, time)

# ------------------ RESULTS ------------------
if st.session_state.result:
    cost, time = st.session_state.result

    st.markdown("## 📈 Prediction Results")

    col3, col4 = st.columns(2)

    # Cost Card
    with col3:
        st.markdown(f"""
        <div style="background-color:#1f4e3d;padding:25px;border-radius:12px">
        <h2 style="color:white;">💰 Estimated Cost</h2>
        <h1 style="color:white;">${int(cost):,}</h1>
        </div>
        """, unsafe_allow_html=True)

    # Time Card
    with col4:
        st.markdown(f"""
        <div style="background-color:#1f3d5c;padding:25px;border-radius:12px">
        <h2 style="color:white;">⏱ Estimated Time</h2>
        <h1 style="color:white;">{int(time)} days</h1>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ------------------ BUDGET ANALYSIS ------------------
    st.markdown("## 💰 Budget Analysis")

    if cost > budget:
        st.error(f"⚠ Over Budget by ${int(cost - budget):,}")
    else:
        st.success(f"✅ Under Budget by ${int(budget - cost):,}")

    # ------------------ GRAPH ------------------
    st.markdown("## 📊 Cost vs Team Size")

    teams = list(range(1, 50))
    costs = []

    for t in teams:
        c, _ = predict_project(t, budget, tools, complexity_val)
        costs.append(c)

    df = pd.DataFrame({
        "Team Size": teams,
        "Estimated Cost": costs
    })

    st.line_chart(df.set_index("Team Size"))

    # ------------------ EXPLANATION ------------------
    st.markdown("## 🧠 Explanation")

    st.write(f"""
    - Increasing **team size** reduces project time but may increase cost.
    - **Budget** indicates planned spending.
    - **Tools level** improves efficiency.
    - Higher **complexity** increases cost and duration.
    """)
