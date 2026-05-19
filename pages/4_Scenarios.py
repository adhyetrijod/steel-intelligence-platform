# pages/4_Scenarios.py
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from core.models import SteelFinancialEngine

st.set_page_config(page_title="Scenario Analysis", layout="wide")

engine    = SteelFinancialEngine()
spot_coal = st.session_state.get('spot_coal', 180)
spot_ore  = st.session_state.get('spot_ore',  120)

st.title("📊 Scenario P&L — Bear / Base / Bull")
st.caption("Full income statement | Stress-tested scenarios | Board-ready output")

with st.expander("📖 Scenario Assumptions"):
    st.markdown("""
    | Driver | Bear 🐻 | Base 📊 | Bull 🐂 |
    |--------|---------|---------|---------|
    | Revenue | -15% | Base | +18% |
    | Coal Cost | +25% | Base | -18% |
    | Ore Cost | +20% | Base | -15% |
    | Production Vol | -20% | Base | +15% |
    
    *Calibrated to Bain's steel sector stress ranges and historical cycle data.*
    """)

st.sidebar.header("Base Case Parameters")
revenue      = st.sidebar.slider("Revenue (₹ Cr/mo)",     100, 2000, 500, 25)
units        = st.sidebar.slider("Production (MT/mo)",   5000, 80000, 20000, 1000)
fixed_costs  = st.sidebar.slider("Fixed Costs (₹ Cr/mo)", 20, 400, 80, 10)
interest     = st.sidebar.slider("Interest Expense (₹ Cr/mo)", 0, 100, 20, 5)

if st.sidebar.button("▶ Run Scenario Analysis", type="primary"):
    scn = engine.scenario_pl(
        revenue, spot_coal/1000, spot_ore/1000,
        fixed_costs, units, interest
    )

    # Highlight cards
    cols = st.columns(3)
    colors_bg = ['#fde8e8', '#e8f4fd', '#e8fdf0']
    colors_bd = ['#c62828', '#1565c0', '#2e7d32']
    icons = ['🐻', '📊', '🐂']

    for i, (name, data) in enumerate(scn.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="background:{colors_bg[i]}; border-left:5px solid {colors_bd[i]};
                        padding:16px; border-radius:8px;">
                <h3 style="margin:0;">{icons[i]} {name}</h3>
                <p style="margin:4px 0; font-size:22px; font-weight:700;">
                    EBITDA: ₹{data['EBITDA']} Cr</p>
                <p style="margin:0; color:{colors_bd[i]};">
                    Margin: {data['EBITDA Margin']}% | PAT: ₹{data['PAT']} Cr</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Full P&L table
    st.subheader("📋 Full Income Statement Comparison")
    line_items = ['Revenue', 'Variable Costs', 'Gross Profit', 'Fixed Costs',
                  'EBITDA', 'Depreciation', 'EBIT', 'Interest', 'EBT', 'Tax',
                  'PAT', 'EBITDA Margin', 'PAT Margin']
    highlight  = ['EBITDA', 'PAT', 'EBITDA Margin', 'PAT Margin']

    rows = []
    for item in line_items:
        rows.append({
            'P&L Line':   item,
            'Bear 🐻':    f"{scn['Bear 🐻'][item]}{'%' if 'Margin' in item else ' Cr'}",
            'Base 📊':    f"{scn['Base 📊'][item]}{'%' if 'Margin' in item else ' Cr'}",
            'Bull 🐂':    f"{scn['Bull 🐂'][item]}{'%' if 'Margin' in item else ' Cr'}",
        })

    df = pd.DataFrame(rows)
    st.dataframe(
        df.style.apply(lambda row: [
            'font-weight:bold; background:#fff9c4' if row['P&L Line'] in highlight
            else '' for _ in row
        ], axis=1),
        use_container_width=True, hide_index=True
    )

    # Charts
    st.markdown("---")
    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=['EBITDA (₹ Cr)', 'PAT (₹ Cr)', 'EBITDA Margin (%)'])
    names  = list(scn.keys())
    colors = ['#d62728', '#1f77b4', '#2ca02c']

    for i, (n, c) in enumerate(zip(names, colors)):
        fig.add_trace(go.Bar(x=[n], y=[scn[n]['EBITDA']], marker_color=c,
                             text=[f"₹{scn[n]['EBITDA']}Cr"], textposition='outside',
                             showlegend=False), row=1, col=1)
        fig.add_trace(go.Bar(x=[n], y=[scn[n]['PAT']], marker_color=c,
                             text=[f"₹{scn[n]['PAT']}Cr"], textposition='outside',
                             showlegend=False), row=1, col=2)
        fig.add_trace(go.Bar(x=[n], y=[scn[n]['EBITDA Margin']], marker_color=c,
                             text=[f"{scn[n]['EBITDA Margin']}%"], textposition='outside',
                             showlegend=False), row=1, col=3)

    fig.update_layout(height=380, plot_bgcolor='white', paper_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 Set base case parameters and click **Run Scenario Analysis**")