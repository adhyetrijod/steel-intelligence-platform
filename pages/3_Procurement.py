# pages/3_Procurement.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from core.models import SteelFinancialEngine

st.set_page_config(page_title="Procurement Optimizer", layout="wide")

engine    = SteelFinancialEngine()
spot_coal = st.session_state.get('spot_coal', 180)
spot_ore  = st.session_state.get('spot_ore',  120)

st.title("🔧 Procurement Optimizer — Linear Programming")
st.caption("Optimal spot / forward buy mix | SciPy HiGHS solver | Cost minimization")

with st.expander("📖 Methodology"):
    st.markdown(f"""
    **Problem:** Decide how much coal and iron ore to buy at spot vs 3-month vs 6-month 
    forward contracts to minimize total procurement cost.
    
    **Constraints:**
    - Total procurement = production requirement
    - Forward contracts ≤ 70% of total (operational flexibility)
    - Non-negativity
    
    **Current spot:** Coal = ${spot_coal:.0f}/T | Ore = ${spot_ore:.0f}/T  
    *(Typical forward discount in current market: 3M = 7%, 6M = 13%)*
    
    **Why this matters:** Bain identified that Indian steel producers could save 
    ₹800–2,400 Cr annually through systematic forward procurement strategies 
    — vs. ad-hoc spot buying.
    """)

st.sidebar.header("Procurement Parameters")
coal_needed = st.sidebar.number_input("Coal Required (MT/mo)",   1000, 50000, 12000, 500)
ore_needed  = st.sidebar.number_input("Iron Ore Required (MT/mo)",1000, 50000, 8000, 500)

st.sidebar.markdown("**Forward Price Discount vs Spot**")
coal_3m_disc = st.sidebar.slider("Coal 3M Discount (%)", 0, 20, 7)
coal_6m_disc = st.sidebar.slider("Coal 6M Discount (%)", 0, 25, 13)
ore_3m_disc  = st.sidebar.slider("Ore 3M Discount (%)",  0, 20, 6)
ore_6m_disc  = st.sidebar.slider("Ore 6M Discount (%)",  0, 25, 12)
max_fwd      = st.sidebar.slider("Max Forward Ratio (%)", 30, 90, 70)
storage_cost = st.sidebar.slider("Storage Cost (%/yr)", 0, 5, 2)

if st.sidebar.button("▶ Optimize Procurement", type="primary"):
    opt = engine.optimize_procurement(
        spot_coal, spot_coal * (1 - coal_3m_disc/100), spot_coal * (1 - coal_6m_disc/100),
        spot_ore,  spot_ore  * (1 - ore_3m_disc/100),  spot_ore  * (1 - ore_6m_disc/100),
        coal_needed, ore_needed, max_fwd/100, storage_cost/100
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Baseline Cost (Spot)",   f"₹{opt['baseline_cost']/1e4:.1f} Cr")
    k2.metric("Optimized Cost",         f"₹{opt['optimal_cost']/1e4:.1f} Cr")
    k3.metric("Monthly Savings",        f"₹{opt['savings']/1e4:.1f} Cr")
    k4.metric("Savings %",              f"{opt['savings_pct']}%",
              delta=f"₹{opt['savings']*12/1e4:.0f} Cr/yr")

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        labels = ['Spot', '3M Forward', '6M Forward']
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Coking Coal', x=labels,
            y=[opt['coal_spot'], opt['coal_3m'], opt['coal_6m']],
            marker_color=['#aec7e8', '#1f77b4', '#08519c'],
            text=[f"{v:,.0f} MT" for v in [opt['coal_spot'], opt['coal_3m'], opt['coal_6m']]],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='Iron Ore', x=labels,
            y=[opt['ore_spot'], opt['ore_3m'], opt['ore_6m']],
            marker_color=['#fdae6b', '#e6550d', '#7f2704'],
            text=[f"{v:,.0f} MT" for v in [opt['ore_spot'], opt['ore_3m'], opt['ore_6m']]],
            textposition='outside'
        ))
        fig.update_layout(
            title="Optimal Procurement Split (MT)",
            barmode='group', height=380,
            plot_bgcolor='white', paper_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # Cost comparison
        fig2 = go.Figure(go.Bar(
            x=['All Spot (Baseline)', 'LP Optimized'],
            y=[opt['baseline_cost']/1e4, opt['optimal_cost']/1e4],
            marker_color=['#d62728', '#2ca02c'],
            text=[f"₹{v/1e4:.1f}Cr" for v in [opt['baseline_cost'], opt['optimal_cost']]],
            textposition='outside'
        ))
        fig2.update_layout(
            title=f"Cost Comparison — Saving ₹{opt['savings']/1e4:.1f}Cr/month",
            yaxis_title="₹ Cr", height=380,
            plot_bgcolor='white', paper_bgcolor='white',
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Recommendation table
    st.subheader("📋 Procurement Schedule")
    df = pd.DataFrame({
        'Commodity':  ['Coking Coal', 'Coking Coal', 'Coking Coal',
                       'Iron Ore',    'Iron Ore',    'Iron Ore'],
        'Type':       ['Spot', '3M Forward', '6M Forward'] * 2,
        'Volume (MT)':[opt['coal_spot'], opt['coal_3m'], opt['coal_6m'],
                       opt['ore_spot'],  opt['ore_3m'],  opt['ore_6m']],
        'Price ($/T)': [spot_coal,
                        spot_coal*(1-coal_3m_disc/100),
                        spot_coal*(1-coal_6m_disc/100),
                        spot_ore,
                        spot_ore*(1-ore_3m_disc/100),
                        spot_ore*(1-ore_6m_disc/100)],
    })
    df['Cost (₹ Lakh)'] = (df['Volume (MT)'] * df['Price ($/T)'] * 83 / 1e5).round(1)
    st.dataframe(df.style.format({
        'Volume (MT)': '{:,.0f}', 'Price ($/T)': '{:.1f}', 'Cost (₹ Lakh)': '{:.1f}'
    }), use_container_width=True, hide_index=True)

else:
    st.info("👈 Configure parameters and click **Optimize Procurement**")