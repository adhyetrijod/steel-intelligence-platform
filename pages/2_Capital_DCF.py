# pages/2_Capital_DCF.py
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from core.models import SteelFinancialEngine

st.set_page_config(page_title="Capital Decisions", layout="wide")

engine = SteelFinancialEngine()
st.title("💰 Capital Decision Engine — DCF / NPV / IRR")
st.caption("Full discounted cash flow | Terminal value | Investment decision framework")

with st.expander("📖 Methodology"):
    st.markdown("""
    **Use case:** Evaluating capex for blast furnace upgrades, DRI plants, EAF transitions,
    or greenfield expansions — the decisions Bain advises steel boards on.
    
    **WACC benchmark for Indian steel:** Typically 9.5–12.5% (Tata Steel: ~10.2%, JSW: ~10.8%).
    
    **Terminal growth:** Steel sector long-run: 2.0–2.5% (aligned with global GDP growth).
    
    **Decision rule:** NPV > 0 AND IRR > WACC → Invest.
    """)

st.sidebar.header("DCF Parameters")
investment   = st.sidebar.number_input("Initial Investment (₹ Cr)", 100, 10000, 1000, 100)
annual_ebitda= st.sidebar.number_input("Year-1 EBITDA (₹ Cr/yr)",   50, 5000, 600, 50)
growth_rate  = st.sidebar.slider("Revenue Growth Rate (%/yr)", 0.0, 12.0, 3.0, 0.5)
wacc         = st.sidebar.slider("WACC (%)", 6.0, 18.0, 10.0, 0.5)
tax_rate     = st.sidebar.slider("Effective Tax Rate (%)", 10, 35, 25, 1)
depreciation = st.sidebar.number_input("Annual Depreciation (₹ Cr)", 10, 500, 60, 10)
capex_maint  = st.sidebar.number_input("Maintenance CapEx (₹ Cr/yr)",  5, 300, 30, 5)
delta_wc     = st.sidebar.number_input("Δ Working Capital (₹ Cr/yr)", 0, 100, 10, 5)
term_growth  = st.sidebar.slider("Terminal Growth Rate (%)", 1.0, 4.0, 2.5, 0.25)
years        = st.sidebar.slider("Projection Period (years)", 5, 15, 10)

if st.sidebar.button("▶ Run DCF Analysis", type="primary"):
    dcf = engine.dcf_analysis(
        investment, annual_ebitda, growth_rate/100, wacc/100,
        tax_rate/100, depreciation, capex_maint, delta_wc,
        term_growth/100, years
    )

    decision_color = "green" if "INVEST" in dcf['decision'] else "red"

    st.markdown(f"""
    <div style="background:{'#e8fdf0' if 'INVEST' in dcf['decision'] else '#fde8e8'};
                border-left:6px solid {'green' if 'INVEST' in dcf['decision'] else 'red'};
                padding:16px; border-radius:8px; font-size:18px; font-weight:700;">
        Investment Decision: {dcf['decision']}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("NPV",           f"₹{dcf['npv']:.0f} Cr")
    k2.metric("IRR",           f"{dcf['irr']}%",
              delta=f"WACC: {wacc}%")
    k3.metric("Payback Period",f"{dcf['payback_years']} yrs")
    k4.metric("PV Cash Flows", f"₹{dcf['pv_cashflows']:.0f} Cr")
    k5.metric("Terminal Value",f"₹{dcf['pv_terminal']:.0f} Cr")

    st.markdown("---")

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=['Free Cash Flow to Firm (₹ Cr)', 'Present Value of Cash Flows (₹ Cr)']
    )

    colors = ['#2ca02c' if v > 0 else '#d62728' for v in dcf['cashflows']]
    fig.add_trace(go.Bar(x=dcf['years'], y=dcf['cashflows'],
                         marker_color=colors, text=[f"₹{v:.0f}" for v in dcf['cashflows']],
                         textposition='outside'), row=1, col=1)

    fig.add_trace(go.Bar(x=dcf['years'], y=dcf['pv_annual'],
                         marker_color='rgba(31,119,180,0.7)',
                         text=[f"₹{v:.0f}" for v in dcf['pv_annual']],
                         textposition='outside'), row=1, col=2)

    fig.update_layout(
        height=400, showlegend=False,
        plot_bgcolor='white', paper_bgcolor='white'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Detailed table
    st.subheader("📋 Detailed Cash Flow Schedule")
    import pandas as pd
    cf_table = pd.DataFrame({
        'Year':        dcf['years'],
        'FCFF (₹ Cr)': dcf['cashflows'],
        'PV (₹ Cr)':   dcf['pv_annual'],
        'Cum. PV':     [round(sum(dcf['pv_annual'][:i+1]), 2) for i in range(len(dcf['years']))]
    })
    st.dataframe(cf_table.style.format({
        'FCFF (₹ Cr)': '{:.1f}', 'PV (₹ Cr)': '{:.1f}', 'Cum. PV': '{:.1f}'
    }), use_container_width=True, hide_index=True)

else:
    st.info("👈 Configure the investment parameters and click **Run DCF Analysis**")