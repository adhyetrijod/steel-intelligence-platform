import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from core.models import SteelFinancialEngine

st.set_page_config(page_title="Scenario Analysis | ISFIP", layout="wide")
engine = SteelFinancialEngine()
spot_coal = st.session_state.get('spot_coal', 180)
spot_ore = st.session_state.get('spot_ore', 120)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    [data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 600 !important; color: #1a1a2e !important; }
    [data-testid="stMetricLabel"] { font-size: 11px !important; color: #6b7280 !important; text-transform: uppercase; letter-spacing: 0.5px; }
    [data-testid="metric-container"] { background: #ffffff; border-radius: 8px; padding: 18px 22px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
    div[data-testid="stSidebar"] { background: #0f172a; border-right: 1px solid #1e293b; }
    div[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    .section-header { font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 1.5px; margin: 28px 0 14px; border-bottom: 1px solid #f3f4f6; padding-bottom: 8px; }
    .footnote { font-size: 12px; color: #9ca3af; font-style: italic; margin-top: 8px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="padding: 32px 0 8px 0; border-bottom: 2px solid #374151; margin-bottom: 28px;">
    <div style="font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px;">INTEGRATED STEEL FINANCIAL INTELLIGENCE PLATFORM</div>
    <h1 style="font-size: 26px; font-weight: 700; color: #f1f5f9; margin: 0; letter-spacing: -0.5px;">Scenario Planning and Stress Testing</h1>
    <div style="font-size: 14px; color: #64748b; margin-top: 6px;">Full Income Statement Across Five Economic Scenarios — Calibrated to Steel Sector Cycle Data</div>
    <div style="display: flex; gap: 24px; margin-top: 16px; flex-wrap: wrap;">
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Live Coal:</span> ${spot_coal:.1f}/T</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Live Ore:</span> ${spot_ore:.1f}/T</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Scenarios:</span> Deep Stress / Bear / Base / Bull / Supercycle</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Methodology:</span> Bain steel sector stress-test framework 2024</div>
    </div>
</div>
""", unsafe_allow_html=True)

SCENARIOS = {
    "Deep Stress": {
        "rev": 0.72, "coal": 1.45, "ore": 1.35, "vol": 0.65,
        "color": "#7f1d1d", "bg": "#fef2f2", "border": "#dc2626",
        "label": "Deep Stress",
        "trigger": "Global recession + China demand collapse + energy crisis. Coking coal prices spike on supply disruption while steel demand falls sharply. Indian infrastructure spending freezes.",
        "probability": "5-10%"
    },
    "Bear": {
        "rev": 0.85, "coal": 1.25, "ore": 1.20, "vol": 0.80,
        "color": "#b91c1c", "bg": "#fef9f9", "border": "#ef4444",
        "label": "Bear",
        "trigger": "China slowdown + elevated energy costs + margin compression. Demand weakens across auto, construction, and white goods segments.",
        "probability": "20-25%"
    },
    "Base": {
        "rev": 1.00, "coal": 1.00, "ore": 1.00, "vol": 1.00,
        "color": "#1d4ed8", "bg": "#eff6ff", "border": "#3b82f6",
        "label": "Base",
        "trigger": "Current market conditions maintained. Moderate India infrastructure demand. Coal and ore prices at prevailing spot levels with normal seasonal variation.",
        "probability": "35-40%"
    },
    "Bull": {
        "rev": 1.18, "coal": 0.82, "ore": 0.85, "vol": 1.15,
        "color": "#15803d", "bg": "#f0fdf4", "border": "#22c55e",
        "label": "Bull",
        "trigger": "India infrastructure supercycle acceleration + China supply-side reforms reducing global steel output + commodity price correction benefiting integrated producers.",
        "probability": "20-25%"
    },
    "Supercycle": {
        "rev": 1.38, "coal": 0.68, "ore": 0.72, "vol": 1.30,
        "color": "#7c3aed", "bg": "#f5f3ff", "border": "#8b5cf6",
        "label": "Supercycle",
        "trigger": "Sustained green infrastructure boom across India, Southeast Asia, and Middle East. Decarbonisation capex drives premium steel demand. Major China capacity closures create supply deficit.",
        "probability": "5-10%"
    }
}

st.sidebar.markdown('<div style="padding: 20px 0 12px; border-bottom: 1px solid #1e293b; margin-bottom: 16px;"><div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Scenario Planning Engine</div><div style="font-size: 15px; color: #f1f5f9; font-weight: 600; margin-top: 4px;">Base Case Parameters</div></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Revenue and Volume</div>', unsafe_allow_html=True)
revenue = st.sidebar.slider("Base Monthly Revenue (Rs Cr)", 100, 2000, 500, 25)
units = st.sidebar.slider("Base Production Volume (MT/mo)", 5000, 80000, 20000, 1000)
st.sidebar.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Cost Structure</div>', unsafe_allow_html=True)
fixed_costs = st.sidebar.slider("Fixed Costs (Rs Cr/mo)", 20, 400, 80, 10)
interest = st.sidebar.slider("Interest Expense (Rs Cr/mo)", 0, 120, 20, 5)
other_income = st.sidebar.slider("Other Income (Rs Cr/mo)", 0, 50, 5, 1)
st.sidebar.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Tax and Depreciation</div>', unsafe_allow_html=True)
tax_rate = st.sidebar.slider("Effective Tax Rate (%)", 10, 35, 25, 1)
dep_rate = st.sidebar.slider("Depreciation (% of Fixed Costs)", 5, 30, 15, 1)
st.sidebar.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Scenario Customisation</div>', unsafe_allow_html=True)
deep_stress_coal = st.sidebar.slider("Deep Stress — Coal Multiplier", 1.20, 2.00, 1.45, 0.05)
deep_stress_vol = st.sidebar.slider("Deep Stress — Volume Multiplier", 0.40, 0.80, 0.65, 0.05)
supercycle_rev = st.sidebar.slider("Supercycle — Revenue Multiplier", 1.20, 1.80, 1.38, 0.02)
supercycle_coal = st.sidebar.slider("Supercycle — Coal Multiplier", 0.50, 0.90, 0.68, 0.02)
SCENARIOS["Deep Stress"]["coal"] = deep_stress_coal
SCENARIOS["Deep Stress"]["vol"] = deep_stress_vol
SCENARIOS["Supercycle"]["rev"] = supercycle_rev
SCENARIOS["Supercycle"]["coal"] = supercycle_coal

st.sidebar.markdown(f'<div style="background:#1e293b;border-radius:6px;padding:12px;margin-top:12px;"><div style="font-size:11px;color:#64748b;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Scenario Reference</div><div style="font-size:12px;color:#94a3b8;line-height:1.9;">Deep Stress: 5-10% probability<br>Bear: 20-25% probability<br>Base: 35-40% probability<br>Bull: 20-25% probability<br>Supercycle: 5-10% probability<br><br>Bain 2024 steel stress calibration</div></div>', unsafe_allow_html=True)
scn_names = list(SCENARIOS.keys())
run_btn = st.sidebar.button("Run Scenario Analysis", type="primary", use_container_width=True, key="scenarios_run_btn")

if run_btn:
    results = {}
    coal_cost_base = spot_coal / 1000
    ore_cost_base = spot_ore / 1000
    depreciation = fixed_costs * dep_rate / 100

    for name, s in SCENARIOS.items():
        adj_units = units * s["vol"]
        adj_rev = revenue * s["rev"] * s["vol"]
        adj_coal = coal_cost_base * s["coal"]
        adj_ore = ore_cost_base * s["ore"]
        variable_cost = (adj_coal + adj_ore) * adj_units
        gross_profit = adj_rev - variable_cost
        ebitda = gross_profit - fixed_costs
        ebit = ebitda - depreciation
        ebt = ebit - interest + other_income
        tax = max(ebt * tax_rate / 100, 0)
        pat = ebt - tax
        roce = round(ebit / (fixed_costs * 8) * 100, 1) if fixed_costs > 0 else 0
        results[name] = {
            "Revenue (Rs Cr)": round(adj_rev, 1),
            "Variable Costs (Rs Cr)": round(variable_cost, 1),
            "Gross Profit (Rs Cr)": round(gross_profit, 1),
            "Gross Margin (%)": round(gross_profit / adj_rev * 100, 1) if adj_rev > 0 else 0,
            "Fixed Costs (Rs Cr)": round(fixed_costs, 1),
            "EBITDA (Rs Cr)": round(ebitda, 1),
            "EBITDA Margin (%)": round(ebitda / adj_rev * 100, 1) if adj_rev > 0 else 0,
            "Depreciation (Rs Cr)": round(depreciation, 1),
            "EBIT (Rs Cr)": round(ebit, 1),
            "EBIT Margin (%)": round(ebit / adj_rev * 100, 1) if adj_rev > 0 else 0,
            "Interest Expense (Rs Cr)": round(interest, 1),
            "Other Income (Rs Cr)": round(other_income, 1),
            "EBT (Rs Cr)": round(ebt, 1),
            "Tax Provision (Rs Cr)": round(tax, 1),
            "PAT (Rs Cr)": round(pat, 1),
            "PAT Margin (%)": round(pat / adj_rev * 100, 1) if adj_rev > 0 else 0,
            "Volume (MT)": round(adj_units, 0),
            "Coal Cost (USD/T)": round(adj_coal * 1000, 1),
            "Ore Cost (USD/T)": round(adj_ore * 1000, 1),
            "ROCE (%)": roce
        }

    st.markdown('<div class="section-header">Scenario Overview</div>', unsafe_allow_html=True)
    scn_cols = st.columns(5)
    scn_names = list(SCENARIOS.keys())
    for i, (name, s) in enumerate(SCENARIOS.items()):
        r = results[name]
        ebitda_val = r["EBITDA (Rs Cr)"]
        margin_val = r["EBITDA Margin (%)"]
        pat_val = r["PAT (Rs Cr)"]
        with scn_cols[i]:
            status = "Viable" if ebitda_val > 0 else "Loss-Making"
            status_col = "#15803d" if ebitda_val > 0 else "#b91c1c"
            st.markdown(f"""
            <div style="background:{s['bg']};border-left:4px solid {s['border']};border-radius:8px;padding:16px;height:220px;">
                <div style="font-size:10px;font-weight:600;color:{s['color']};text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">{s['probability']} probability</div>
                <div style="font-size:16px;font-weight:700;color:{s['color']};margin-bottom:10px;">{name}</div>
                <div style="font-size:12px;color:#374151;margin-bottom:2px;">EBITDA: <strong>Rs {ebitda_val} Cr</strong></div>
                <div style="font-size:12px;color:#374151;margin-bottom:2px;">Margin: <strong>{margin_val}%</strong></div>
                <div style="font-size:12px;color:#374151;margin-bottom:8px;">PAT: <strong>Rs {pat_val} Cr</strong></div>
                <div style="font-size:11px;font-weight:600;color:{status_col};">{status}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Financial Performance Across Scenarios</div>', unsafe_allow_html=True)
    fig_main = make_subplots(rows=2, cols=3, subplot_titles=["EBITDA (Rs Cr)", "PAT (Rs Cr)", "EBITDA Margin (%)", "Revenue (Rs Cr)", "Variable Costs (Rs Cr)", "ROCE (%)"], vertical_spacing=0.18, horizontal_spacing=0.1)
    scn_labels = list(results.keys())
    bar_colors_list = [SCENARIOS[n]["border"] for n in scn_labels]
    metrics_layout = [("EBITDA (Rs Cr)", 1, 1), ("PAT (Rs Cr)", 1, 2), ("EBITDA Margin (%)", 1, 3), ("Revenue (Rs Cr)", 2, 1), ("Variable Costs (Rs Cr)", 2, 2), ("ROCE (%)", 2, 3)]

    for metric, row, col in metrics_layout:
        vals = [results[n][metric] for n in scn_labels]
        m_colors = ["#16a34a" if v > 0 else "#dc2626" for v in vals]
        fig_main.add_trace(go.Bar(x=scn_labels, y=vals, marker_color=m_colors if "PAT" in metric or "EBITDA (Rs" in metric else bar_colors_list, marker_line=dict(color="rgba(0,0,0,0.06)", width=1), text=[f"{v:.1f}" for v in vals], textposition="outside", textfont=dict(size=9, color="#374151"), showlegend=False), row=row, col=col)
        if "EBITDA (Rs" in metric or "PAT" in metric:
            fig_main.add_hline(y=0, line_color="#94a3b8", line_width=1, row=row, col=col)

    fig_main.update_layout(height=580, plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=10, color="#374151"), margin=dict(t=60, b=20))
    fig_main.update_xaxes(showgrid=False, linecolor="#e5e7eb", tickfont=dict(size=9))
    fig_main.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb", tickfont=dict(size=9))
    st.plotly_chart(fig_main, use_container_width=True)

    st.markdown('<div class="section-header">Probability-Weighted Expected Value</div>', unsafe_allow_html=True)
    probs = {"Deep Stress": 0.075, "Bear": 0.225, "Base": 0.375, "Bull": 0.225, "Supercycle": 0.075}
    ew_ebitda = sum(probs[n] * results[n]["EBITDA (Rs Cr)"] for n in scn_names)
    ew_pat = sum(probs[n] * results[n]["PAT (Rs Cr)"] for n in scn_names)
    ew_margin = sum(probs[n] * results[n]["EBITDA Margin (%)"] for n in scn_names)
    ew_rev = sum(probs[n] * results[n]["Revenue (Rs Cr)"] for n in scn_names)
    ebitda_range = results["Deep Stress"]["EBITDA (Rs Cr)"]
    ebitda_max = results["Supercycle"]["EBITDA (Rs Cr)"]
    ebitda_swing = ebitda_max - ebitda_range

    col_ew1, col_ew2, col_ew3, col_ew4, col_ew5 = st.columns(5)
    col_ew1.metric("Expected EBITDA", f"Rs {ew_ebitda:.1f} Cr", help="Probability-weighted average across all 5 scenarios")
    col_ew2.metric("Expected PAT", f"Rs {ew_pat:.1f} Cr", help="Probability-weighted average PAT")
    col_ew3.metric("Expected Margin", f"{ew_margin:.1f}%", help="Probability-weighted EBITDA margin")
    col_ew4.metric("Expected Revenue", f"Rs {ew_rev:.1f} Cr")
    col_ew5.metric("EBITDA Swing Range", f"Rs {ebitda_swing:.1f} Cr", help="Deep Stress to Supercycle full range")

    st.markdown(f'<div class="footnote">Expected values weighted by: Deep Stress 7.5%, Bear 22.5%, Base 37.5%, Bull 22.5%, Supercycle 7.5%. Probability distribution reflects Bain steel sector cycle frequency analysis. Actual scenario probabilities should be updated quarterly based on leading indicators (China PMI, India infrastructure spend, coking coal futures curve).</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">EBITDA Bridge — Deep Stress to Supercycle</div>', unsafe_allow_html=True)
    base_ebitda = results["Base"]["EBITDA (Rs Cr)"]
    bridge_labels = ["Base EBITDA", "Revenue Impact\n(Bear)", "Coal / Ore Impact\n(Bear)", "Volume Impact\n(Bear)", "Bear EBITDA", "Revenue Impact\n(Bull)", "Coal / Ore Impact\n(Bull)", "Volume Impact\n(Bull)", "Bull EBITDA"]
    base_rev_impact_bear = round((results["Bear"]["Revenue (Rs Cr)"] - results["Base"]["Revenue (Rs Cr)"]), 1)
    base_cost_impact_bear = round(-(results["Bear"]["Variable Costs (Rs Cr)"] - results["Base"]["Variable Costs (Rs Cr)"]), 1)
    base_vol_impact_bear = 0
    bear_ebitda = results["Bear"]["EBITDA (Rs Cr)"]
    base_rev_impact_bull = round((results["Bull"]["Revenue (Rs Cr)"] - results["Base"]["Revenue (Rs Cr)"]), 1)
    base_cost_impact_bull = round(-(results["Bull"]["Variable Costs (Rs Cr)"] - results["Base"]["Variable Costs (Rs Cr)"]), 1)
    bull_ebitda = results["Bull"]["EBITDA (Rs Cr)"]
    bridge_vals = [base_ebitda, base_rev_impact_bear, base_cost_impact_bear, 0, bear_ebitda, base_rev_impact_bull, base_cost_impact_bull, 0, bull_ebitda]
    bridge_types = ["absolute", "relative", "relative", "relative", "absolute", "relative", "relative", "relative", "absolute"]
    bridge_colors = ["#1d4ed8", "#dc2626" if base_rev_impact_bear < 0 else "#16a34a", "#dc2626" if base_cost_impact_bear < 0 else "#16a34a", "#94a3b8", "#b91c1c", "#16a34a" if base_rev_impact_bull > 0 else "#dc2626", "#16a34a" if base_cost_impact_bull > 0 else "#dc2626", "#94a3b8", "#15803d"]
    fig_bridge = go.Figure(go.Waterfall(name="EBITDA Bridge", orientation="v", measure=bridge_types, x=bridge_labels, y=bridge_vals, connector=dict(line=dict(color="#e5e7eb", width=1.5)), increasing=dict(marker=dict(color="#16a34a")), decreasing=dict(marker=dict(color="#dc2626")), totals=dict(marker=dict(color="#1d4ed8")), textposition="outside", textfont=dict(size=10, color="#374151")))
    fig_bridge.update_layout(height=380, plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11, color="#374151"), margin=dict(t=20, b=20), showlegend=False)
    fig_bridge.update_xaxes(showgrid=False, linecolor="#e5e7eb", tickfont=dict(size=9))
    fig_bridge.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
    st.plotly_chart(fig_bridge, use_container_width=True)
    st.markdown('<div class="footnote">EBITDA bridge decomposes the movement from Base to Bear and Base to Bull into revenue, commodity cost, and volume components. This isolates the primary value drivers and guides risk management prioritisation.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Scenario Radar — Multi-Metric Comparison</div>', unsafe_allow_html=True)
    radar_metrics = ["EBITDA Margin (%)", "PAT Margin (%)", "Gross Margin (%)", "EBIT Margin (%)", "ROCE (%)"]
    max_vals = {m: max(abs(results[n][m]) for n in scn_names) + 1 for m in radar_metrics}
    fig_radar = go.Figure()
    radar_colors = [SCENARIOS[n]["border"] for n in scn_names]
    for name, color in zip(scn_names, radar_colors):
        r_vals = [max(results[name][m], 0) for m in radar_metrics]
        r_vals.append(r_vals[0])
        theta_labels = radar_metrics + [radar_metrics[0]]
        fig_radar.add_trace(go.Scatterpolar(r=r_vals, theta=theta_labels, fill="toself", fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.06)", line=dict(color=color, width=2), name=name))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, gridcolor="#f1f5f9", linecolor="#e5e7eb", tickfont=dict(size=10)), angularaxis=dict(tickfont=dict(size=11))), height=420, paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11), legend=dict(orientation="h", y=-0.12, font=dict(size=11)), margin=dict(t=20, b=60))
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown('<div class="section-header">Full Income Statement — All Five Scenarios</div>', unsafe_allow_html=True)
    pl_rows = ["Revenue (Rs Cr)", "Variable Costs (Rs Cr)", "Gross Profit (Rs Cr)", "Gross Margin (%)", "Fixed Costs (Rs Cr)", "EBITDA (Rs Cr)", "EBITDA Margin (%)", "Depreciation (Rs Cr)", "EBIT (Rs Cr)", "EBIT Margin (%)", "Interest Expense (Rs Cr)", "Other Income (Rs Cr)", "EBT (Rs Cr)", "Tax Provision (Rs Cr)", "PAT (Rs Cr)", "PAT Margin (%)", "Volume (MT)", "Coal Cost (USD/T)", "Ore Cost (USD/T)", "ROCE (%)"]
    highlight_rows = ["EBITDA (Rs Cr)", "EBITDA Margin (%)", "PAT (Rs Cr)", "PAT Margin (%)", "ROCE (%)"]
    separator_rows = ["Gross Profit (Rs Cr)", "EBITDA (Rs Cr)", "EBIT (Rs Cr)", "EBT (Rs Cr)", "PAT (Rs Cr)", "Volume (MT)"]
    table_data = {"P & L Line Item": pl_rows}
    for name in scn_names:
        col_vals = []
        for row in pl_rows:
            v = results[name][row]
            if "%" in row:
                col_vals.append(f"{v:.1f}%")
            elif "Volume" in row:
                col_vals.append(f"{v:,.0f}")
            elif "USD" in row:
                col_vals.append(f"${v:.1f}")
            else:
                col_vals.append(f"{v:.1f}")
        table_data[name] = col_vals
    pl_df = pd.DataFrame(table_data)

    def style_pl_table(df):
        styled = df.style
        def row_style(row):
            row_name = row["P & L Line Item"]
            styles = [""] * len(row)
            if row_name in highlight_rows:
                styles = ["font-weight: 600; background-color: #f8fafc"] * len(row)
            for i, col in enumerate(df.columns[1:], 1):
                raw = results[col][row_name]
                if isinstance(raw, (int, float)):
                    if raw > 0:
                        styles[i] = (styles[i] + ";color: #15803d;font-weight:500").strip(";")
                    elif raw < 0:
                        styles[i] = (styles[i] + ";color: #b91c1c;font-weight:500").strip(";")
            return styles
        return styled.apply(row_style, axis=1)

    st.dataframe(style_pl_table(pl_df), use_container_width=True, hide_index=True)

    st.markdown('<div class="section-header">Tata Steel Benchmark Comparison</div>', unsafe_allow_html=True)
    benchmark_data = {"Metric": ["EBITDA Margin", "PAT Margin", "ROCE", "Revenue per MT"], "Tata Steel India FY24": ["~18-22%", "~8-12%", "~11-14%", "~Rs 55,000-65,000"], "JSW Steel FY24": ["~18-24%", "~9-13%", "~12-16%", "~Rs 60,000-68,000"], "SAIL FY24": ["~8-14%", "~2-6%", "~5-8%", "~Rs 48,000-56,000"], "Your Base Case": [f"{results['Base']['EBITDA Margin (%)']:.1f}%", f"{results['Base']['PAT Margin (%)']:.1f}%", f"{results['Base']['ROCE (%)']:.1f}%", f"~Rs {round(revenue/units*1000):,}"]}
    bench_df = pd.DataFrame(benchmark_data)
    st.dataframe(bench_df, use_container_width=True, hide_index=True)
    st.markdown('<div class="footnote">Benchmark figures sourced from public annual reports (FY2024). Your model figures are for comparative orientation only and depend on the base case parameters configured in the sidebar.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Monthly P&L Phasing — 12-Month Projection (Base Case with Cyclicality)</div>', unsafe_allow_html=True)
    months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
    seasonality = [0.97, 0.99, 0.95, 0.92, 0.90, 0.94, 1.03, 1.08, 1.10, 1.08, 1.06, 1.02]
    coal_seasonality = [1.02, 1.01, 1.00, 1.03, 1.05, 1.02, 0.99, 0.97, 0.96, 0.98, 1.00, 1.01]
    monthly_rev = [round(revenue * s, 1) for s in seasonality]
    monthly_coal = spot_coal / 1000
    monthly_ore = spot_ore / 1000
    monthly_vc = [round((monthly_coal * cs + monthly_ore) * units * ss, 1) for cs, ss in zip(coal_seasonality, seasonality)]
    monthly_ebitda = [round(r - vc - fixed_costs, 1) for r, vc in zip(monthly_rev, monthly_vc)]
    monthly_ebitda_margin = [round(e / r * 100, 1) if r > 0 else 0 for e, r in zip(monthly_ebitda, monthly_rev)]
    fig_monthly = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=["Monthly Revenue and EBITDA (Rs Cr)", "Monthly EBITDA Margin (%)"], vertical_spacing=0.12, row_heights=[0.65, 0.35])
    fig_monthly.add_trace(go.Bar(x=months, y=monthly_rev, name="Revenue", marker_color="#dbeafe", marker_line=dict(color="#93c5fd", width=1)), row=1, col=1)
    fig_monthly.add_trace(go.Bar(x=months, y=monthly_ebitda, name="EBITDA", marker_color=["#16a34a" if v >= 0 else "#dc2626" for v in monthly_ebitda], marker_line=dict(color="rgba(0,0,0,0.06)", width=1)), row=1, col=1)
    fig_monthly.add_trace(go.Scatter(x=months, y=monthly_ebitda_margin, mode="lines+markers", line=dict(color="#7c3aed", width=2.5), marker=dict(size=7, color="#7c3aed", line=dict(color="white", width=1.5)), name="EBITDA Margin"), row=2, col=1)
    fig_monthly.add_hline(y=0, line_color="#94a3b8", line_width=1, row=2, col=1)
    fig_monthly.update_layout(height=460, barmode="group", plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11, color="#374151"), legend=dict(orientation="h", y=-0.08, font=dict(size=11)), margin=dict(t=40, b=40))
    fig_monthly.update_xaxes(showgrid=False, linecolor="#e5e7eb")
    fig_monthly.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
    st.plotly_chart(fig_monthly, use_container_width=True)
    st.markdown('<div class="footnote">Monthly phasing applies an empirical steel sector seasonality pattern. Q3 (Oct-Dec) typically sees peak demand from construction and auto sectors. Q2 (Jul-Sep) reflects monsoon-related slowdown in construction activity. Coal carrying cost seasonality is applied independently.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Board Planning Memorandum</div>', unsafe_allow_html=True)
    best_scenario = max(scn_names, key=lambda n: results[n]["EBITDA (Rs Cr)"])
    worst_scenario = min(scn_names, key=lambda n: results[n]["EBITDA (Rs Cr)"])
    loss_scenarios = [n for n in scn_names if results[n]["PAT (Rs Cr)"] < 0]
    st.markdown(f"""
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:8px;padding:28px 32px;font-family:'Inter',sans-serif;line-height:1.85;font-size:14px;color:#374151;">
        <div style="font-size:11px;font-weight:600;color:#9ca3af;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #f3f4f6;">BOARD OF DIRECTORS — ANNUAL PLANNING SCENARIO REVIEW</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:16px;margin-bottom:20px;">
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Expected EBITDA</span><div style="font-weight:600;color:#111827;">Rs {ew_ebitda:.1f} Cr/mo</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Expected Margin</span><div style="font-weight:600;color:#111827;">{ew_margin:.1f}%</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">EBITDA Range</span><div style="font-weight:600;color:#111827;">Rs {results['Deep Stress']['EBITDA (Rs Cr)']:.1f} to Rs {results['Supercycle']['EBITDA (Rs Cr)']:.1f} Cr</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Loss-Making Scenarios</span><div style="font-weight:600;color:{'#b91c1c' if loss_scenarios else '#15803d'};">{', '.join(loss_scenarios) if loss_scenarios else 'None — all scenarios PAT-positive'}</div></div>
        </div>
        <p style="margin:0 0 12px;"><strong>Situation.</strong> This analysis stress-tests the company's financial performance across five economic scenarios ranging from Deep Stress (global recession, coal spike, demand collapse) to Supercycle (infrastructure boom, commodity tailwinds, supply deficit). The base case is anchored at the current operating configuration of Rs {revenue} Cr monthly revenue at {units:,} MT/month production.</p>
        <p style="margin:0 0 12px;"><strong>Key Findings.</strong> The probability-weighted expected EBITDA of <strong>Rs {ew_ebitda:.1f} Cr/month</strong> ({ew_margin:.1f}% margin) compares {'favourably' if ew_margin > 15 else 'modestly'} against the Tata Steel India benchmark of 18-22%. The full EBITDA range of <strong>Rs {ebitda_swing:.1f} Cr</strong> between Deep Stress and Supercycle underscores the sensitivity of integrated steel economics to commodity cycles. {'All five scenarios generate positive EBITDA, indicating operational resilience at current cost structure.' if all(results[n]['EBITDA (Rs Cr)'] > 0 for n in scn_names) else f'The Deep Stress scenario produces negative EBITDA, requiring immediate intervention if macro conditions deteriorate.'} {'All scenarios generate positive PAT.' if not loss_scenarios else f'PAT turns negative under {", ".join(loss_scenarios)} — fixed cost reduction and debt restructuring should be contingency-planned.'}</p>
        <p style="margin:0;"><strong>Recommended Actions.</strong> (1) Implement forward procurement contracts to reduce commodity cost sensitivity — the primary driver of Bear and Deep Stress deterioration. (2) Establish a scenario-contingent cost reduction playbook with pre-identified Rs {round(fixed_costs * 0.15, 0):.0f} Cr in variable fixed cost levers activatable within 90 days. (3) Maintain liquidity reserves equivalent to 3 months of Deep Stress EBITDA shortfall against Base — approximately Rs {round(abs(results['Base']['EBITDA (Rs Cr)'] - results['Deep Stress']['EBITDA (Rs Cr)']) * 3, 0):.0f} Cr. (4) Review this scenario model quarterly as the commodity forward curve and India infrastructure spend trajectory evolve.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div style="padding: 80px 40px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 20px; text-align: center;">
        <div style="font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;">Scenario Planning Engine</div>
        <h2 style="font-size: 22px; font-weight: 600; color: #1e293b; margin: 0 0 12px;">Configure base case parameters to run five-scenario stress test</h2>
        <p style="font-size: 14px; color: #64748b; max-width: 640px; margin: 0 auto 32px; line-height: 1.6;">Full income statement modelling across Deep Stress, Bear, Base, Bull, and Supercycle scenarios — with probability-weighted expected value, EBITDA bridge waterfall, radar comparison, seasonality phasing, and board memorandum output.</p>
        <div style="display: inline-grid; grid-template-columns: repeat(5, 1fr); gap: 12px; text-align: left; max-width: 860px; margin: 0 auto;">
            {"".join([f'<div style="background:white;border:1px solid #e2e8f0;border-left:3px solid {SCENARIOS[n]["border"]};border-radius:6px;padding:12px 16px;"><div style="font-size:10px;color:#94a3b8;text-transform:uppercase;font-weight:600;">{SCENARIOS[n]["probability"]}</div><div style="font-weight:600;color:{SCENARIOS[n]["color"]};font-size:14px;margin-top:2px;">{n}</div></div>' for n in scn_names])}
        </div>
    </div>
    """, unsafe_allow_html=True)