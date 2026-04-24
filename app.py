import streamlit as st
from model import predict_project
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Project Predictor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
    /* Main container padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-card h3 {
        color: #a0a0a0;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .metric-card .value {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
    }
    .metric-card.cost { border-left: 4px solid #00d4aa; }
    .metric-card.time { border-left: 4px solid #667eea; }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .status-success {
        background: rgba(0, 212, 170, 0.15);
        color: #00d4aa;
        border: 1px solid rgba(0, 212, 170, 0.3);
    }
    .status-warning {
        background: rgba(255, 107, 107, 0.15);
        color: #ff6b6b;
        border: 1px solid rgba(255, 107, 107, 0.3);
    }
    
    /* Input section styling */
    .input-section {
        background: rgba(255,255,255,0.02);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }
    
    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("### 🎯 About This Tool")
    st.markdown("""
    Predict project **cost** and **timeline** using machine learning trained on historical project data.
    """)
    
    st.markdown("---")
    
    st.markdown("### 📌 Input Guide")
    st.markdown("""
    | Factor | Impact |
    |--------|--------|
    | **Team Size** | More people → faster delivery, higher cost |
    | **Budget** | Your planned spend limit |
    | **Tools** | Better tools → improved efficiency |
    | **Complexity** | Higher → more time & cost |
    """)
    
    st.markdown("---")
    st.caption("Built with Streamlit + scikit-learn")

# ------------------ HEADER ------------------
st.markdown("""
# 🚀 Project Predictor
### Estimate cost and timeline before you commit
""")

st.markdown("<br>", unsafe_allow_html=True)

# ------------------ INPUT SECTION ------------------
st.markdown("#### Configure Your Project")

col1, col2, col3, col4 = st.columns(4)

with col1:
    team = st.number_input(
        "👥 Team Size",
        min_value=1,
        max_value=50,
        value=10,
        help="Number of people working on the project"
    )

with col2:
    budget = st.number_input(
        "💵 Budget",
        min_value=10000,
        max_value=10000000,
        value=500000,
        step=50000,
        format="%d",
        help="Total planned budget in USD"
    )

with col3:
    tools = st.select_slider(
        "🛠 Tools Level",
        options=list(range(1, 11)),
        value=5,
        help="1 = Basic tools, 10 = Enterprise-grade tooling"
    )

with col4:
    complexity = st.selectbox(
        "📊 Complexity",
        options=["Low", "Medium", "High"],
        index=1,
        help="Overall project complexity"
    )

complexity_map = {"Low": 1, "Medium": 2, "High": 3}
complexity_val = complexity_map[complexity]

st.markdown("<br>", unsafe_allow_html=True)

# Center the button
col_btn = st.columns([1, 2, 1])
with col_btn[1]:
    predict_clicked = st.button("🔮 Generate Prediction", use_container_width=True)

# ------------------ SESSION STATE ------------------
if predict_clicked:
    with st.spinner("Analyzing project parameters..."):
        import time
        time.sleep(0.5)  # Brief delay for UX feedback
        cost, duration = predict_project(team, budget, tools, complexity_val)
        st.session_state.result = (cost, duration)
        st.session_state.inputs = (team, budget, tools, complexity_val)

# ------------------ RESULTS ------------------
if "result" in st.session_state and st.session_state.result:
    cost, duration = st.session_state.result
    
    st.markdown("---")
    st.markdown("#### 📈 Prediction Results")
    
    # Metrics row
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.markdown(f"""
        <div class="metric-card cost">
            <h3>💰 Estimated Cost</h3>
            <div class="value">${int(cost):,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m2:
        st.markdown(f"""
        <div class="metric-card time">
            <h3>⏱ Estimated Duration</h3>
            <div class="value">{int(duration)} days</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m3:
        # Budget status
        diff = budget - cost
        if diff >= 0:
            status_html = f"""
            <div class="metric-card" style="border-left: 4px solid #00d4aa;">
                <h3>📊 Budget Status</h3>
                <div class="status-badge status-success">✓ Under budget by ${int(diff):,}</div>
            </div>
            """
        else:
            status_html = f"""
            <div class="metric-card" style="border-left: 4px solid #ff6b6b;">
                <h3>📊 Budget Status</h3>
                <div class="status-badge status-warning">⚠ Over budget by ${int(abs(diff)):,}</div>
            </div>
            """
        st.markdown(status_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ------------------ SENSITIVITY ANALYSIS ------------------
    st.markdown("#### 🔍 Sensitivity Analysis")
    
    tab1, tab2 = st.tabs(["Cost vs Team Size", "Cost vs Tools Level"])
    
    with tab1:
        teams = list(range(1, 51))
        costs = [predict_project(t, budget, tools, complexity_val)[0] for t in teams]
        
        df_team = pd.DataFrame({"Team Size": teams, "Estimated Cost ($)": costs})
        st.area_chart(df_team.set_index("Team Size"), color="#667eea")
        st.caption("How estimated cost changes as you scale the team")
    
    with tab2:
        tool_levels = list(range(1, 11))
        costs_tools = [predict_project(team, budget, t, complexity_val)[0] for t in tool_levels]
        
        df_tools = pd.DataFrame({"Tools Level": tool_levels, "Estimated Cost ($)": costs_tools})
        st.area_chart(df_tools.set_index("Tools Level"), color="#00d4aa")
        st.caption("Impact of better tooling on project cost")
    
    # ------------------ KEY INSIGHTS ------------------
    st.markdown("#### 💡 Key Insights")
    
    col_i1, col_i2 = st.columns(2)
    
    with col_i1:
        st.info(f"""
        **Team Efficiency**: A team of **{team}** people at complexity **{complexity.lower()}** 
        is projected to complete in **{int(duration)} days**.
        """)
    
    with col_i2:
        budget_util = (cost / budget) * 100
        if budget_util <= 80:
            st.success(f"**Budget Utilization**: {budget_util:.0f}% — Good buffer for contingencies.")
        elif budget_util <= 100:
            st.warning(f"**Budget Utilization**: {budget_util:.0f}% — Limited margin for changes.")
        else:
            st.error(f"**Budget Utilization**: {budget_util:.0f}% — Consider reducing scope or increasing budget.")

else:
    # Empty state
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #666;">
        <h3>👆 Configure your project inputs above</h3>
        <p>Click <strong>Generate Prediction</strong> to see cost and timeline estimates</p>
    </div>
    """, unsafe_allow_html=True)
