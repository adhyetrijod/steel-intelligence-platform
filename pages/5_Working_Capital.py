# pages/5_Working_Capital.py
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from core.models import SteelFinancialEngine

st.set_page_config(page_title="Working Capital", layout="wide")

engine = SteelFinancialEngine()

st.title("🔄 Working Capital & Break-Even Intelligence")
st.caption("Cash Conversion Cycle | WC Optimization | Break-Even | Operating Leverage")

with st.expander("📖 Why This Matters for Steel"):
    st.markdown("""
    Steel producers are among the most **working capital intensive** businesses globally:
    - **Long inventory cycles:** Ore → coke → pig iron → crude steel = 45–75 days
    - **Extended receivables:** B2B contracts with auto/infra customers: 30–60 days
    - **Negotiation leverage on payables:** Large volumes give bargaining power with miners
    
    Bain's operational excellence work for Tata Steel found that a 10-day CCC reduction
    freed ₹800–1,200 Cr in cash — equivalent to 6–9 months of capex budget.
    """)

st.sidebar.header("Working Capital Parameters")
revenue      = st.sidebar.slider("Revenue (₹ Cr/mo)",    100, 2000, 500, 25)
units        = st.sidebar.slider("Production (MT/mo)",  5000, 80000, 20000, 1000)
fixed_costs  = st.sidebar.slider("Fixed Costs (₹ Cr/mo)", 20, 400, 80, 10)
rec_days     = st.sidebar.slider("Receivables Days",  10, 90, 45)
pay_days     = st.sidebar.slider("Payables Days",     10, 90, 35)
inv_days     = st.sidebar.slider("Inventory Days",    15, 90, 60)

st.sidebar.markdown("---")
st.sidebar.subheader("Break-Even Inputs")
spot_coal = st.session_state.get('spot_coal', 180)
spot_ore  = st.session_state.get('spot_ore',  120)
price_per_unit    = st.sidebar.number_input("Selling Price (₹/MT)", 10000, 150000, 55000, 1000)
var_cost_per_unit = st.sidebar.number_input("Variable Cost (₹/MT)", 5000,  120000, 37000, 1000)

if st.sidebar.button("▶ Run Analysis", type="primary"):
    cogs = (spot_coal/1000 + spot_ore/1000) * units + fixed_costs * 0.3
    wc   = engine.working_capital(revenue, cogs, rec_days, pay_days, inv_days)
    be   = engine.breakeven(fixed_costs, price_per_unit, var_cost_per_unit, units)

    # WC KPIs
    st.subheader("🔄 Working Capital Dashboard")
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Net Working Capital",   f"₹{wc['nwc']} Cr")
    k2.metric("Cash Conv. Cycle",      f"{wc['ccc']} days")
    k3.metric("Receivables",           f"₹{wc['receivables']} Cr",
              help=f"{wc['rec_days']} days")
    k4.metric("Inventory",             f"₹{wc['inventory']} Cr",
              help=f"{wc['inv_days']} days")
    k5.metric("Cash Freed (if -15d payables)", f"₹{wc['freed']} Cr",
              delta=f"+{wc['freed']} Cr", delta_color="normal")

    col_a, col_b = st.columns(2)

    with col_a:
        fig = make_subplots(rows=1, cols=2,
            subplot_titles=['WC Components (₹ Cr)', 'CCC Waterfall (Days)'])
        fig.add_trace(go.Bar(
            x=['Receivables', 'Inventory', 'Payables (-)'],
            y=[wc['receivables'], wc['inventory'], -wc['payables']],
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
            text=[f"₹{v:.0f}Cr" for v in [wc['receivables'], wc['inventory'], -wc['payables']]],
            textposition='outside'
        ), row=1, col=1)
        fig.add_trace(go.Bar(
            x=['Rec. Days', 'Inv. Days', 'Pay. Days', 'CCC'],
            y=[wc['rec_days'], wc['inv_days'], -wc['pay_days'], wc['ccc']],
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd'],
            text=[f"{v}d" for v in [wc['rec_days'], wc['inv_days'], -wc['pay_days'], wc['ccc']]],
            textposition='outside'
        ), row=1, col=2)
        fig.update_layout(height=380, showlegend=False,
                          plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        ccc_industry = 68
        ccc_color = 'green' if wc['ccc'] < ccc_industry else 'red'
        st.markdown(f"""
        #### 📊 CCC Benchmarking

        | Company | Cash Conv. Cycle |
        |---------|-----------------|
        | Tata Steel India | ~62 days |
        | JSW Steel | ~71 days |
        | SAIL | ~89 days |
        | **Your Model** | **{wc['ccc']} days** |
        | Industry Avg | {ccc_industry} days |

        **Status:** {'✅ Better than average' if wc['ccc'] < ccc_industry else '⚠️ Above average — improvement opportunity'}

        **Optimization lever:**  
        Extend supplier payables by 15 days → free  
        **₹{wc['freed']} Cr** in working capital.
        
        *Bain operational excellence benchmark: Top-quartile steel 
        producers maintain CCC < 55 days.*
        """)

    st.markdown("---")
    st.subheader("📉 Break-Even & Operating Leverage")
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Break-Even Volume",   f"{int(be['bep_units']):,} MT")
    k2.metric("Break-Even Revenue",  f"₹{be['bep_revenue']:.0f} Cr")
    k3.metric("Contribution Margin", f"{be['cm_ratio']:.1f}%")
    k4.metric("Margin of Safety",    f"{be['mos_pct']:.1f}%",
              help=f"{int(be['mos_units']):,} MT buffer above BEP")
    k5.metric("Op. Leverage (DOL)",  f"{be['dol']:.2f}x",
              help="1% revenue change → {:.2f}% EBITDA change".format(be['dol']))

    # Break-even chart
    import numpy as np
    vol_range = np.linspace(0, units * 1.3, 100)
    rev_line  = vol_range * price_per_unit / 1e7
    cost_line = (vol_range * var_cost_per_unit + fixed_costs * 1e7) / 1e7

    fig_be = go.Figure()
    fig_be.add_trace(go.Scatter(x=vol_range/1000, y=rev_line,  name='Revenue',    line=dict(color='green', width=2)))
    fig_be.add_trace(go.Scatter(x=vol_range/1000, y=cost_line, name='Total Cost', line=dict(color='red',   width=2)))
    fig_be.add_vline(x=be['bep_units']/1000, line_dash='dash', line_color='navy',
                     annotation_text=f"BEP: {int(be['bep_units']):,} MT")
    fig_be.add_vline(x=units/1000, line_dash='dot', line_color='purple',
                     annotation_text=f"Current: {units:,} MT")
    fig_be.update_layout(
        title="Break-Even Analysis",
        xaxis_title="Production Volume ('000 MT)",
        yaxis_title="₹ Cr (×10M)",
        height=380, plot_bgcolor='white', paper_bgcolor='white'
    )
    st.plotly_chart(fig_be, use_container_width=True)

    st.markdown(f"""
    **DOL = {be['dol']:.2f}x** means a 1% drop in revenue causes a 
    **{be['dol']:.2f}% drop in EBITDA** — reflecting the high fixed-cost 
    structure of integrated steel production. This is the core reason Bain 
    recommends variable-cost restructuring before capacity expansion.
    """)

else:
    st.info("👈 Set parameters and click **Run Analysis**")