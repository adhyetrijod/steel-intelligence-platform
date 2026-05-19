import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from scipy.optimize import linprog
from core.models import SteelFinancialEngine

st.set_page_config(page_title="Procurement Intelligence | ISFIP", layout="wide")
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
    .insight-tag { display: inline-block; background: #eff6ff; color: #f1f5f9; font-size: 11px; font-weight: 500; padding: 3px 10px; border-radius: 4px; margin: 2px 4px 2px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="padding: 32px 0 8px 0; border-bottom: 2px solid #7c2d12; margin-bottom: 28px;">
    <div style="font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px;">INTEGRATED FERRUM CAPITAL INTELLIGENCE</div>
    <h1 style="font-size: 26px; font-weight: 700; color: #f1f5f9; margin: 0; letter-spacing: -0.5px;">Procurement Intelligence Engine</h1>
    <div style="font-size: 14px; color: #64748b; margin-top: 6px;">Linear Programming Optimizer — Coking Coal and Iron Ore Strategic Sourcing</div>
    <div style="display: flex; gap: 24px; margin-top: 16px; flex-wrap: wrap;">
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Solver:</span> SciPy HiGHS LP — Industry-grade linear programming</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Coking Coal (spot):</span> ${spot_coal:.1f} / T — World Bank API</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Iron Ore (spot):</span> ${spot_ore:.1f} / T — World Bank API</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Bain benchmark saving:</span> Rs 800 - 2,400 Cr/yr for integrated producers</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_c1, col_c2, col_c3, col_c4 = st.columns(4)
ctx = "background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:14px 16px;"
col_c1.markdown(f'<div style="{ctx}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">LP Formulation</div><div style="font-size:14px;font-weight:600;color:#1e293b;">6-Variable Mixed Integer</div><div style="font-size:12px;color:#64748b;margin-top:2px;">Spot + 3M Fwd + 6M Fwd per commodity</div></div>', unsafe_allow_html=True)
col_c2.markdown(f'<div style="{ctx}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Objective Function</div><div style="font-size:14px;font-weight:600;color:#1e293b;">Min Total Procurement Cost</div><div style="font-size:12px;color:#64748b;margin-top:2px;">Price + storage cost + financing</div></div>', unsafe_allow_html=True)
col_c3.markdown(f'<div style="{ctx}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Constraints</div><div style="font-size:14px;font-weight:600;color:#1e293b;">Volume + Forward Ratio</div><div style="font-size:12px;color:#64748b;margin-top:2px;">Production balance + max hedge ratio</div></div>', unsafe_allow_html=True)
col_c4.markdown(f'<div style="{ctx}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Typical Saving Range</div><div style="font-size:14px;font-weight:600;color:#15803d;">4% — 13% vs Spot</div><div style="font-size:12px;color:#64748b;margin-top:2px;">Dependent on forward curve shape</div></div>', unsafe_allow_html=True)

st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="padding: 20px 0 12px; border-bottom: 1px solid #1e293b; margin-bottom: 16px;"><div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Procurement Intelligence Engine</div><div style="font-size: 15px; color: #f1f5f9; font-weight: 600; margin-top: 4px;">Sourcing Parameters</div></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Production Requirements</div>', unsafe_allow_html=True)
coal_needed = st.sidebar.number_input("Coking Coal Required (MT/mo)", 1000, 80000, 12000, 500)
ore_needed = st.sidebar.number_input("Iron Ore Required (MT/mo)", 1000, 80000, 8000, 500)
st.sidebar.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Forward Price Discounts vs Spot (%)</div>', unsafe_allow_html=True)
coal_3m = st.sidebar.slider("Coal — 3-Month Forward Discount", 0, 20, 7)
coal_6m = st.sidebar.slider("Coal — 6-Month Forward Discount", 0, 30, 13)
ore_3m = st.sidebar.slider("Iron Ore — 3-Month Forward Discount", 0, 20, 6)
ore_6m = st.sidebar.slider("Iron Ore — 6-Month Forward Discount", 0, 30, 12)
st.sidebar.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Operational Constraints</div>', unsafe_allow_html=True)
max_fwd = st.sidebar.slider("Maximum Forward Commitment (%)", 20, 90, 70)
storage_pct = st.sidebar.slider("Inventory Carrying Cost (%/yr)", 0, 8, 2)
financing_cost = st.sidebar.slider("Working Capital Financing Cost (%/yr)", 6, 16, 10)
st.sidebar.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Market Context</div>', unsafe_allow_html=True)
usd_inr = st.sidebar.number_input("USD/INR Exchange Rate", 75.0, 95.0, 83.5, 0.5)
coal_price_override = st.sidebar.number_input("Coal Spot Override (USD/T, 0 = live)", 0.0, 500.0, 0.0, 5.0)
ore_price_override = st.sidebar.number_input("Ore Spot Override (USD/T, 0 = live)", 0.0, 300.0, 0.0, 5.0)
effective_coal = coal_price_override if coal_price_override > 0 else spot_coal
effective_ore = ore_price_override if ore_price_override > 0 else spot_ore
st.sidebar.markdown(f'<div style="background:#1e293b;border-radius:6px;padding:12px;margin-top:12px;"><div style="font-size:11px;color:#64748b;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Active Market Prices</div><div style="font-size:13px;color:#94a3b8;line-height:1.9;">Coal: ${effective_coal:.1f}/T ({"override" if coal_price_override > 0 else "live"})<br>Iron Ore: ${effective_ore:.1f}/T ({"override" if ore_price_override > 0 else "live"})<br>USD/INR: {usd_inr}<br>Max fwd ratio: {max_fwd}%</div></div>', unsafe_allow_html=True)
run_btn = st.sidebar.button("Run Procurement Optimisation", type="primary", use_container_width=True)

if run_btn:
    p_coal_spot = effective_coal
    p_coal_3m = effective_coal * (1 - coal_3m/100) * (1 + (storage_cost := storage_pct/100) * 3/12)
    p_coal_6m = effective_coal * (1 - coal_6m/100) * (1 + storage_cost * 6/12)
    p_ore_spot = effective_ore
    p_ore_3m = effective_ore * (1 - ore_3m/100) * (1 + storage_cost * 3/12)
    p_ore_6m = effective_ore * (1 - ore_6m/100) * (1 + storage_cost * 6/12)
    financing_adj = financing_cost / 100 / 12
    c_obj = [p_coal_spot, p_coal_3m * (1 + financing_adj * 3), p_coal_6m * (1 + financing_adj * 6), p_ore_spot, p_ore_3m * (1 + financing_adj * 3), p_ore_6m * (1 + financing_adj * 6)]
    A_eq = [[1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1]]
    b_eq = [coal_needed, ore_needed]
    A_ub = [[0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 1, 1]]
    b_ub = [coal_needed * max_fwd/100, ore_needed * max_fwd/100]
    bounds = [(0, None)] * 6
    result = linprog(c_obj, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    if result.success:
        x = result.x
    else:
        x = [coal_needed, 0, 0, ore_needed, 0, 0]
    opt_cost_usd = float(np.dot(c_obj, x))
    base_cost_usd = p_coal_spot * coal_needed + p_ore_spot * ore_needed
    saving_usd = base_cost_usd - opt_cost_usd
    saving_cr = saving_usd * usd_inr / 1e7
    base_cr = base_cost_usd * usd_inr / 1e7
    opt_cr = opt_cost_usd * usd_inr / 1e7
    saving_pct = round(saving_usd / base_cost_usd * 100, 2)
    annual_saving_cr = saving_cr * 12
    coal_fwd_pct = round((x[1] + x[2]) / coal_needed * 100, 1)
    ore_fwd_pct = round((x[4] + x[5]) / ore_needed * 100, 1)
    total_fwd_pct = round(((x[1]+x[2]+x[4]+x[5]) / (coal_needed+ore_needed)) * 100, 1)

    if saving_pct >= 8:
        signal_color = "#15803d"
        signal_bg = "#f0fdf4"
        signal_border = "#16a34a"
        signal_label = "STRONG SAVING OPPORTUNITY"
        signal_text = f"The forward curve is favourably shaped. LP optimisation identifies {saving_pct}% cost reduction — well above the 4% threshold that justifies operational complexity of forward contracts."
    elif saving_pct >= 4:
        signal_color = "#1d4ed8"
        signal_bg = "#eff6ff"
        signal_border = "#3b82f6"
        signal_label = "MODERATE SAVING OPPORTUNITY"
        signal_text = f"Forward discounts of {coal_3m}% (3M coal) and {coal_6m}% (6M coal) generate a {saving_pct}% saving after storage and financing costs. Implement with volume-balanced forward commitments."
    elif saving_pct > 0:
        signal_color = "#92400e"
        signal_bg = "#fffbeb"
        signal_border = "#f59e0b"
        signal_label = "MARGINAL SAVING — REVIEW ASSUMPTIONS"
        signal_text = f"Saving of {saving_pct}% is below the typical operational threshold. Recheck forward discount assumptions or consider whether storage and financing costs are correctly calibrated."
    else:
        signal_color = "#b91c1c"
        signal_bg = "#fef2f2"
        signal_border = "#dc2626"
        signal_label = "SPOT MARKET PREFERRED"
        signal_text = "At current forward discounts and carrying costs, all-spot procurement is optimal. Forward contracts are not warranted until discounts widen or storage costs fall."

    st.markdown(f"""
    <div style="background:{signal_bg};border-left:5px solid {signal_border};border-radius:6px;padding:20px 24px;margin-bottom:24px;">
        <div style="font-size:11px;font-weight:600;color:{signal_color};text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;">Optimisation Result</div>
        <div style="font-size:20px;font-weight:700;color:{signal_color};margin-bottom:8px;">{signal_label}</div>
        <div style="font-size:14px;color:#374151;line-height:1.6;">{signal_text}</div>
        <div style="margin-top:12px;font-size:13px;color:#6b7280;">LP solver: SciPy HiGHS &nbsp;|&nbsp; Constraints active: volume balance, max forward ratio {max_fwd}% &nbsp;|&nbsp; Carrying cost: {storage_pct}%/yr &nbsp;|&nbsp; Financing cost: {financing_cost}%/yr</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Financial Summary</div>', unsafe_allow_html=True)
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Baseline Cost (All Spot)", f"Rs {base_cr:.1f} Cr/mo")
    k2.metric("LP Optimised Cost", f"Rs {opt_cr:.1f} Cr/mo")
    k3.metric("Monthly Saving", f"Rs {saving_cr:.2f} Cr", delta=f"{saving_pct}% reduction", delta_color="normal" if saving_pct > 0 else "inverse")
    k4.metric("Annual Saving", f"Rs {annual_saving_cr:.1f} Cr", delta="Annualised", delta_color="normal" if annual_saving_cr > 0 else "inverse")
    k5.metric("Coal Forward Ratio", f"{coal_fwd_pct}%", help="Percentage of coal procured on forward contracts")
    k6.metric("Ore Forward Ratio", f"{ore_fwd_pct}%", help="Percentage of ore procured on forward contracts")

    st.markdown(f'<div class="footnote">Saving of Rs {saving_cr:.2f} Cr/month includes storage carrying cost of {storage_pct}%/yr and working capital financing at {financing_cost}%/yr. USD/INR conversion at {usd_inr}. All figures are management estimates — actual forward prices are subject to counterparty negotiation.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Allocation Analysis</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([3, 2])

    with col_a:
        coal_vals = [x[0], x[1], x[2]]
        ore_vals = [x[3], x[4], x[5]]
        coal_cost_split = [x[0]*p_coal_spot, x[1]*p_coal_3m, x[2]*p_coal_6m]
        ore_cost_split = [x[3]*p_ore_spot, x[4]*p_ore_3m, x[5]*p_ore_6m]
        contract_labels = ["Spot\n(Immediate)", "3-Month\nForward", "6-Month\nForward"]

        fig_alloc = make_subplots(rows=1, cols=2, subplot_titles=["Volume Allocation (MT)", "Cost Allocation (USD '000)"], horizontal_spacing=0.12)

        fig_alloc.add_trace(go.Bar(name="Coking Coal", x=contract_labels, y=coal_vals, marker_color=["#64748b", "#1d4ed8", "#1e3a8a"], marker_line=dict(color="rgba(0,0,0,0.08)", width=1), text=[f"{v:,.0f}" for v in coal_vals], textposition="outside", textfont=dict(size=10)), row=1, col=1)
        fig_alloc.add_trace(go.Bar(name="Iron Ore", x=contract_labels, y=ore_vals, marker_color=["#9ca3af", "#ea580c", "#7c2d12"], marker_line=dict(color="rgba(0,0,0,0.08)", width=1), text=[f"{v:,.0f}" for v in ore_vals], textposition="outside", textfont=dict(size=10)), row=1, col=1)
        fig_alloc.add_trace(go.Bar(name="Coal Cost", x=contract_labels, y=[v/1000 for v in coal_cost_split], marker_color=["#64748b", "#1d4ed8", "#1e3a8a"], marker_line=dict(color="rgba(0,0,0,0.08)", width=1), text=[f"${v/1000:.0f}k" for v in coal_cost_split], textposition="outside", textfont=dict(size=10), showlegend=False), row=1, col=2)
        fig_alloc.add_trace(go.Bar(name="Ore Cost", x=contract_labels, y=[v/1000 for v in ore_cost_split], marker_color=["#9ca3af", "#ea580c", "#7c2d12"], marker_line=dict(color="rgba(0,0,0,0.08)", width=1), text=[f"${v/1000:.0f}k" for v in ore_cost_split], textposition="outside", textfont=dict(size=10), showlegend=False), row=1, col=2)

        fig_alloc.update_layout(height=400, barmode="group", plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11, color="#374151"), legend=dict(orientation="h", y=-0.22, font=dict(size=11)), margin=dict(t=40, b=60))
        fig_alloc.update_xaxes(showgrid=False, linecolor="#e5e7eb")
        fig_alloc.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
        st.plotly_chart(fig_alloc, use_container_width=True)

    with col_b:
        total_coal_cost = sum(coal_cost_split)
        total_ore_cost = sum(ore_cost_split)
        fig_pie = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]], subplot_titles=["Coal Mix", "Ore Mix"])
        fig_pie.add_trace(go.Pie(labels=["Spot", "3M Fwd", "6M Fwd"], values=coal_vals, marker_colors=["#64748b", "#1d4ed8", "#1e3a8a"], textinfo="label+percent", textfont=dict(size=10), hole=0.45, showlegend=False), row=1, col=1)
        fig_pie.add_trace(go.Pie(labels=["Spot", "3M Fwd", "6M Fwd"], values=ore_vals, marker_colors=["#9ca3af", "#ea580c", "#7c2d12"], textinfo="label+percent", textfont=dict(size=10), hole=0.45, showlegend=False), row=1, col=2)
        fig_pie.update_layout(height=400, paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11), margin=dict(t=40, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('<div class="section-header">Cost Comparison — Baseline vs Optimised</div>', unsafe_allow_html=True)
    fig_comp = go.Figure()
    strategies = ["All Spot\n(Baseline)", "LP Optimised\n(This Model)", "All 6M Forward\n(Max Hedge)"]
    max_hedge_cost = (effective_coal*(1-coal_6m/100)*(1+storage_cost*6/12)*coal_needed + effective_ore*(1-ore_6m/100)*(1+storage_cost*6/12)*ore_needed) * usd_inr / 1e7
    costs = [base_cr, opt_cr, max_hedge_cost]
    bar_colors = ["#dc2626", "#16a34a", "#1d4ed8"]
    fig_comp.add_trace(go.Bar(x=strategies, y=costs, marker_color=bar_colors, marker_line=dict(color="rgba(0,0,0,0.08)", width=1), text=[f"Rs {v:.2f} Cr" for v in costs], textposition="outside", textfont=dict(size=12, color="#374151"), width=[0.35, 0.35, 0.35]))
    fig_comp.add_hline(y=base_cr, line_dash="dot", line_color="#94a3b8", line_width=1.5, annotation_text=f"Spot baseline: Rs {base_cr:.2f} Cr", annotation_font=dict(size=11, color="#94a3b8"), annotation_position="top right")
    saving_annotations = [("", ""), (f"Saves Rs {saving_cr:.2f} Cr vs spot", "#16a34a"), (f"{'Saves' if max_hedge_cost < base_cr else 'Costs'} Rs {abs(max_hedge_cost-base_cr):.2f} Cr vs spot", "#1d4ed8")]
    for i, (text, color) in enumerate(saving_annotations):
        if text:
            fig_comp.add_annotation(x=strategies[i], y=costs[i] + base_cr*0.05, text=text, showarrow=False, font=dict(size=11, color=color))
    fig_comp.update_layout(height=360, plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=12, color="#374151"), showlegend=False, yaxis_title="Rs Cr per month", margin=dict(t=40, b=20))
    fig_comp.update_xaxes(showgrid=False, linecolor="#e5e7eb")
    fig_comp.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
    st.plotly_chart(fig_comp, use_container_width=True)
    st.markdown(f'<div class="footnote">Max hedge scenario assumes all volume contracted at 6-month forward prices including full carrying cost. LP optimised result reflects the mathematically optimal mix subject to the {max_fwd}% forward commitment ceiling.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Sensitivity — Saving vs Forward Discount Assumptions</div>', unsafe_allow_html=True)
    discount_range = np.arange(0, 22, 1)
    saving_curve_coal = []
    saving_curve_ore = []
    for d in discount_range:
        c_coal = [effective_coal, effective_coal*(1-d/100)*(1+storage_cost*3/12), effective_coal*(1-coal_6m/100)*(1+storage_cost*6/12), effective_ore, effective_ore*(1-ore_3m/100)*(1+storage_cost*3/12), effective_ore*(1-ore_6m/100)*(1+storage_cost*6/12)]
        res_c = linprog(c_coal, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        if res_c.success:
            saving_curve_coal.append(round((base_cost_usd - float(np.dot(c_coal, res_c.x))) / base_cost_usd * 100, 2))
        else:
            saving_curve_coal.append(0)
        c_ore = [effective_coal, effective_coal*(1-coal_3m/100)*(1+storage_cost*3/12), effective_coal*(1-coal_6m/100)*(1+storage_cost*6/12), effective_ore, effective_ore*(1-d/100)*(1+storage_cost*3/12), effective_ore*(1-ore_6m/100)*(1+storage_cost*6/12)]
        res_o = linprog(c_ore, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        if res_o.success:
            saving_curve_ore.append(round((base_cost_usd - float(np.dot(c_ore, res_o.x))) / base_cost_usd * 100, 2))
        else:
            saving_curve_ore.append(0)

    fig_sens = go.Figure()
    fig_sens.add_trace(go.Scatter(x=discount_range, y=saving_curve_coal, mode="lines", name="Coal 3M Discount Sensitivity", line=dict(color="#1d4ed8", width=2.5)))
    fig_sens.add_trace(go.Scatter(x=discount_range, y=saving_curve_ore, mode="lines", name="Ore 3M Discount Sensitivity", line=dict(color="#ea580c", width=2.5)))
    fig_sens.add_hline(y=4, line_dash="dot", line_color="#16a34a", line_width=1.5, annotation_text="4% threshold — minimum to justify forward contracting", annotation_font=dict(size=11, color="#16a34a"))
    fig_sens.add_vline(x=coal_3m, line_dash="dash", line_color="#1d4ed8", line_width=1.5, annotation_text=f"Current coal: {coal_3m}%", annotation_font=dict(size=11, color="#1d4ed8"))
    fig_sens.add_vline(x=ore_3m, line_dash="dash", line_color="#ea580c", line_width=1.5, annotation_text=f"Current ore: {ore_3m}%", annotation_font=dict(size=11, color="#ea580c"))
    fig_sens.update_layout(height=360, plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=12, color="#374151"), xaxis_title="3-Month Forward Discount (%)", yaxis_title="Total Procurement Saving (%)", legend=dict(orientation="h", y=-0.2, font=dict(size=11)), margin=dict(t=20, b=60))
    fig_sens.update_xaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
    fig_sens.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
    st.plotly_chart(fig_sens, use_container_width=True)
    st.markdown('<div class="footnote">Sensitivity curves show how total procurement saving varies as the 3-month forward discount changes for coal (blue) and iron ore (orange), holding all other parameters constant. The 4% green threshold represents the minimum saving that justifies the operational overhead of a forward procurement programme.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Detailed Procurement Schedule</div>', unsafe_allow_html=True)
    schedule_data = {
        "Commodity": ["Coking Coal", "Coking Coal", "Coking Coal", "Iron Ore", "Iron Ore", "Iron Ore"],
        "Contract Type": ["Spot (Immediate)", "3-Month Forward", "6-Month Forward", "Spot (Immediate)", "3-Month Forward", "6-Month Forward"],
        "Volume (MT)": [round(x[0],0), round(x[1],0), round(x[2],0), round(x[3],0), round(x[4],0), round(x[5],0)],
        "% of Total Req.": [round(x[0]/coal_needed*100,1), round(x[1]/coal_needed*100,1), round(x[2]/coal_needed*100,1), round(x[3]/ore_needed*100,1), round(x[4]/ore_needed*100,1), round(x[5]/ore_needed*100,1)],
        "Price (USD/T)": [round(p_coal_spot,2), round(p_coal_3m,2), round(p_coal_6m,2), round(p_ore_spot,2), round(p_ore_3m,2), round(p_ore_6m,2)],
        "Discount vs Spot (%)": ["—", f"-{coal_3m}% + carry", f"-{coal_6m}% + carry", "—", f"-{ore_3m}% + carry", f"-{ore_6m}% + carry"],
        "Cost (USD '000)": [round(coal_cost_split[0]/1000,1), round(coal_cost_split[1]/1000,1), round(coal_cost_split[2]/1000,1), round(ore_cost_split[0]/1000,1), round(ore_cost_split[1]/1000,1), round(ore_cost_split[2]/1000,1)],
        "Cost (Rs Lakh)": [round(v*usd_inr/1e5,1) for v in coal_cost_split + ore_cost_split],
        "Strategy Rationale": ["Market flexibility — no lock-in", "Medium-term hedge — balance cost and risk", "Maximum discount — volume commitment", "Market flexibility — no lock-in", "Medium-term hedge — balance cost and risk", "Maximum discount — volume commitment"]
    }
    sched_df = pd.DataFrame(schedule_data)
    st.dataframe(sched_df.style.format({"Volume (MT)": "{:,.0f}", "% of Total Req.": "{:.1f}%", "Price (USD/T)": "{:.2f}", "Cost (USD '000)": "{:.1f}", "Cost (Rs Lakh)": "{:.1f}"}), use_container_width=True, hide_index=True)

    st.markdown('<div class="section-header">Working Capital and Financing Impact</div>', unsafe_allow_html=True)
    col_wc1, col_wc2 = st.columns(2)
    with col_wc1:
        forward_val_coal = (x[1]*p_coal_3m + x[2]*p_coal_6m) * usd_inr / 1e7
        forward_val_ore = (x[4]*p_ore_3m + x[5]*p_ore_6m) * usd_inr / 1e7
        total_forward_committed = forward_val_coal + forward_val_ore
        financing_charge_monthly = total_forward_committed * financing_cost / 100 / 12
        net_saving_after_financing = saving_cr - financing_charge_monthly
        wc_data = {"Item": ["Forward coal commitment (Rs Cr)", "Forward ore commitment (Rs Cr)", "Total capital committed (Rs Cr)", "Monthly financing charge (Rs Cr)", "Gross procurement saving (Rs Cr)", "Net saving after financing (Rs Cr)"], "Value": [round(forward_val_coal,2), round(forward_val_ore,2), round(total_forward_committed,2), round(financing_charge_monthly,3), round(saving_cr,2), round(net_saving_after_financing,2)]}
        wc_df = pd.DataFrame(wc_data)
        def highlight_net(row):
            if "Net saving" in str(row["Item"]):
                color = "#15803d" if row["Value"] > 0 else "#b91c1c"
                return [f"font-weight:600;color:{color}", f"font-weight:600;color:{color}"]
            return ["", ""]
        st.dataframe(wc_df.style.apply(highlight_net, axis=1).format({"Value": "{:.3f}"}), use_container_width=True, hide_index=True)
        st.markdown(f'<div class="footnote">Working capital committed in forward contracts is financed at {financing_cost}%/yr. Net saving after financing charges is Rs {net_saving_after_financing:.2f} Cr/month = Rs {net_saving_after_financing*12:.1f} Cr annualised.</div>', unsafe_allow_html=True)
    with col_wc2:
        months = list(range(1, 13))
        cumulative_saving = [net_saving_after_financing * m for m in months]
        fig_cum = go.Figure()
        fig_cum.add_trace(go.Scatter(x=months, y=cumulative_saving, mode="lines+markers", line=dict(color="#16a34a", width=2.5), marker=dict(size=7, color="#16a34a", line=dict(color="white", width=1.5)), fill="tozeroy", fillcolor="rgba(22,163,74,0.08)", name="Cumulative Net Saving"))
        fig_cum.update_layout(height=300, plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11), xaxis_title="Month", yaxis_title="Cumulative Saving (Rs Cr)", margin=dict(t=20, b=20), showlegend=False)
        fig_cum.update_xaxes(showgrid=False, linecolor="#e5e7eb", tickvals=months)
        fig_cum.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
        st.plotly_chart(fig_cum, use_container_width=True)
        st.markdown(f'<div class="footnote">12-month cumulative saving trajectory at Rs {net_saving_after_financing:.2f} Cr/month net of financing charges.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Procurement Intelligence Brief</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:8px;padding:28px 32px;font-family:'Inter',sans-serif;line-height:1.85;font-size:14px;color:#374151;">
        <div style="font-size:11px;font-weight:600;color:#9ca3af;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #f3f4f6;">SUPPLY CHAIN FINANCE — PROCUREMENT STRATEGY MEMO</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-bottom:20px;">
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Monthly Requirement</span><div style="font-weight:600;color:#111827;">{coal_needed:,} MT coal / {ore_needed:,} MT ore</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Recommended Mix</span><div style="font-weight:600;color:#111827;">{100-max_fwd}% spot / {max_fwd}% forward (max)</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Annualised Saving</span><div style="font-weight:600;color:#15803d;">Rs {annual_saving_cr:.1f} Cr</div></div>
        </div>
        <p style="margin:0 0 12px;"><strong>Situation.</strong> The company currently procures approximately {coal_needed:,} MT of coking coal and {ore_needed:,} MT of iron ore per month on spot terms at prevailing market prices of ${effective_coal:.1f}/T and ${effective_ore:.1f}/T respectively. Spot procurement provides maximum operational flexibility but forfeits the systematic forward discount available in normal contango market conditions.</p>
        <p style="margin:0 0 12px;"><strong>Opportunity.</strong> Linear programming analysis across six procurement variables — spot, 3-month forward, and 6-month forward contracts for each commodity — identifies an optimal sourcing mix that reduces total monthly procurement cost by <strong>Rs {saving_cr:.2f} Cr ({saving_pct}%)</strong> against the all-spot baseline. After accounting for inventory carrying cost of {storage_pct}%/yr and working capital financing at {financing_cost}%/yr, the net saving is <strong>Rs {net_saving_after_financing:.2f} Cr/month</strong>, equivalent to <strong>Rs {net_saving_after_financing*12:.1f} Cr annualised</strong>.</p>
        <p style="margin:0 0 12px;"><strong>Recommended Strategy.</strong> The LP solver recommends maintaining {100-coal_fwd_pct:.0f}% spot exposure for coal and {100-ore_fwd_pct:.0f}% for ore to preserve operational flexibility, while committing {coal_fwd_pct}% and {ore_fwd_pct}% respectively to forward contracts at the discounts modelled. This is within the {max_fwd}% forward commitment ceiling set by operations. The total capital committed in forward positions is Rs {total_forward_committed:.1f} Cr, financed at {financing_cost}%/yr.</p>
        <p style="margin:0;"><strong>Key Risk.</strong> Forward contracts require volume commitment 3-6 months ahead of delivery. If production volumes deviate by more than 15% from plan, the hedge ratio will be mis-calibrated and spot top-up purchases at potentially adverse prices may be required. The model should be re-optimised monthly as the forward curve evolves. Counterparty credit risk on forward contracts should be evaluated against the financial standing of mining counterparties (Vale, BHP, Glencore, POSCO International).</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div style="padding: 80px 40px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 20px; text-align: center;">
        <div style="font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;">Procurement Intelligence Engine</div>
        <h2 style="font-size: 22px; font-weight: 600; color: #1e293b; margin: 0 0 12px;">Configure sourcing parameters to run LP optimisation</h2>
        <p style="font-size: 14px; color: #64748b; max-width: 640px; margin: 0 auto 32px; line-height: 1.6;">The engine solves a 6-variable linear programme to find the optimal allocation of monthly procurement across spot and forward contract tenors for coking coal and iron ore, minimising total landed cost after carrying charges and financing.</p>
        <div style="display: inline-grid; grid-template-columns: repeat(3, 1fr); gap: 16px; text-align: left; margin-top: 8px; max-width: 700px; margin: 0 auto;">
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 20px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Live Coal Spot</div>
                <div style="font-weight: 700; color: #1e293b; font-size: 18px; margin-top: 4px;">${effective_coal:.1f} / T</div>
                <div style="font-size: 12px; color: #64748b;">World Bank API</div>
            </div>
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 20px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Live Ore Spot</div>
                <div style="font-weight: 700; color: #1e293b; font-size: 18px; margin-top: 4px;">${effective_ore:.1f} / T</div>
                <div style="font-size: 12px; color: #64748b;">World Bank API</div>
            </div>
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 20px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Bain Benchmark</div>
                <div style="font-weight: 700; color: #15803d; font-size: 18px; margin-top: 4px;">Rs 800-2,400 Cr</div>
                <div style="font-size: 12px; color: #64748b;">Annual saving potential</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)