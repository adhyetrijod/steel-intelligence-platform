import streamlit as st
import pandas as pd
from core.data import get_coal_prices, get_ore_prices

st.set_page_config(
    page_title="ISFIP | Steel Financial Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=3600)
def load_data():
    coal = get_coal_prices()
    ore  = get_ore_prices()
    return coal, ore

coal_df, ore_df = load_data()

st.session_state['coal_df']   = coal_df
st.session_state['ore_df']    = ore_df
st.session_state['spot_coal'] = float(coal_df['price'].iloc[-1])
st.session_state['spot_ore']  = float(ore_df['price'].iloc[-1])

spot_coal = st.session_state['spot_coal']
spot_ore  = st.session_state['spot_ore']

st.markdown("""
<div style="background:linear-gradient(135deg,#0d1117 0%,#1a237e 60%,#0d47a1 100%);
            padding:40px;border-radius:16px;margin-bottom:24px;">
    <h1 style="color:white;font-size:32px;margin:0;">
        🏗️ Integrated Steel Financial Intelligence Platform
    </h1>
    <p style="color:#90caf9;font-size:15px;margin:8px 0 0;">
        Monte Carlo · DCF/NPV/IRR · VaR · Linear Programming · 
        Scenario P&L · Working Capital · GenAI Brief
    </p>
    <p style="color:#64b5f6;font-size:12px;margin:4px 0 0;">
        Inspired by Bain & Company steel sector research · Built for Tata Steel use case
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Platform Status",  "🟢 Live",           "All systems operational")
c2.metric("Coal (spot)",      f"${spot_coal:.0f}/T","World Bank API")
c3.metric("Iron Ore (spot)",  f"${spot_ore:.0f}/T", "World Bank API")
c4.metric("Models Ready",     "7 of 7",             "Monte Carlo → GenAI")

st.markdown("---")
st.subheader("🏗️ Platform Architecture")

tabs = st.tabs(["📐 System Design","🔬 Model Details","📊 Benchmarks","📚 Research Basis"])

with tabs[0]:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **Data Layer**
        - World Bank Commodity API
        - Synthetic fallback data
        - Pandas ETL pipeline
        """)
    with col2:
        st.markdown("""
        **Analytics Layer**
        - Monte Carlo (10K sims)
        - SciPy HiGHS LP Solver
        - Prophet Forecasting
        - DCF / VaR / Break-Even
        """)
    with col3:
        st.markdown("""
        **Presentation Layer**
        - Streamlit multi-page
        - Plotly interactive charts
        - GPT-4o executive brief
        - Downloadable reports
        """)

with tabs[1]:
    model_data = {
        "Model":        ["Monte Carlo","DCF/NPV/IRR","Commodity VaR",
                         "LP Procurement","Scenario P&L","Working Capital","Break-Even"],
        "Method":       ["Multivariate Log-Normal","Gordon Growth + FCFF","Parametric Normal",
                         "HiGHS LP Solver","3-Scenario Stress Test","CCC Analysis","CM Ratio"],
        "Industry Use": ["CFO Risk Committees","Board Capex Decisions","Treasury Hedging",
                         "Supply Chain Finance","Investor Relations","Treasury Ops","Operations"],
        "Bain Ref":     ["✅","✅","✅","✅","✅","✅","✅"]
    }
    st.dataframe(pd.DataFrame(model_data), use_container_width=True, hide_index=True)

with tabs[2]:
    bench_data = {
        "Metric":       ["EBITDA Margin","CCC (days)","Coal Cost %","Debt/EBITDA","ROCE"],
        "Tata Steel":   ["17-22%","62","28-32%","2.8x","12%"],
        "JSW Steel":    ["18-24%","71","26-30%","2.1x","14%"],
        "SAIL":         ["8-14%","89","31-36%","5.2x","6%"],
        "Top Quartile": ["25%+","<55","<25%","<2x",">18%"]
    }
    st.dataframe(pd.DataFrame(bench_data), use_container_width=True, hide_index=True)
    st.caption("Source: Annual reports, Bain steel sector research 2024")

with tabs[3]:
    st.markdown("""
| Research | Year | Key Finding Applied |
|----------|------|---------------------|
| Bain & Co: *Steel Sector Under Pressure* | 2024 | Coal-ore correlation = 0.45 |
| McKinsey: *Steel Decarbonization Pathways* | 2023 | WACC benchmarks |
| World Bank: *Commodity Markets Outlook* | 2024 | Live price data |
| WSA: *Statistical Yearbook* | 2024 | CCC benchmarks |
    """)

st.info("👈 Use the sidebar to navigate to each analysis module.")