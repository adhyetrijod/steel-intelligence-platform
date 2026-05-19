import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from core.models import SteelFinancialEngine

st.set_page_config(page_title="Working Capital | ISFIP", layout="wide")
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
<div style="padding: 32px 0 8px 0; border-bottom: 2px solid #0c4a6e; margin-bottom: 28px;">
    <div style="font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px;">INTEGRATED FERRUM CAPITAL INTELLIGENCE</div>
    <h1 style="font-size: 26px; font-weight: 700; color: #f1f5f9; margin: 0; letter-spacing: -0.5px;">Working Capital and Operational Efficiency</h1>
    <div style="font-size: 14px; color: #64748b; margin-top: 6px;">Cash Conversion Cycle Analysis — Treasury Optimisation — Break-Even and Operating Leverage</div>
    <div style="display: flex; gap: 24px; margin-top: 16px; flex-wrap: wrap;">
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">CCC Formula:</span> Receivables Days + Inventory Days - Payables Days</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Industry Average CCC:</span> 65 days (Indian integrated steel)</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Bain benchmark finding:</span> 10-day CCC reduction frees Rs 800-1,200 Cr</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_c1, col_c2, col_c3, col_c4 = st.columns(4)
ctx = "background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:14px 16px;"
col_c1.markdown(f'<div style="{ctx}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Tata Steel India CCC</div><div style="font-size:15px;font-weight:600;color:#1e293b;">~62 days</div><div style="font-size:12px;color:#64748b;">FY2024 benchmark</div></div>', unsafe_allow_html=True)
col_c2.markdown(f'<div style="{ctx}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">JSW Steel CCC</div><div style="font-size:15px;font-weight:600;color:#1e293b;">~71 days</div><div style="font-size:12px;color:#64748b;">FY2024 benchmark</div></div>', unsafe_allow_html=True)
col_c3.markdown(f'<div style="{ctx}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">SAIL CCC</div><div style="font-size:15px;font-weight:600;color:#1e293b;">~89 days</div><div style="font-size:12px;color:#64748b;">FY2024 benchmark</div></div>', unsafe_allow_html=True)
col_c4.markdown(f'<div style="{ctx}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Top Quartile Global</div><div style="font-size:15px;font-weight:600;color:#15803d;"><55 days</div><div style="font-size:12px;color:#64748b;">Best-in-class target</div></div>', unsafe_allow_html=True)

st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

st.sidebar.markdown('<div style="padding: 20px 0 12px; border-bottom: 1px solid #1e293b; margin-bottom: 16px;"><div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Working Capital Engine</div><div style="font-size: 15px; color: #f1f5f9; font-weight: 600; margin-top: 4px;">Operating Parameters</div></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Revenue and Cost Base</div>', unsafe_allow_html=True)
revenue = st.sidebar.slider("Monthly Revenue (Rs Cr)", 100, 2000, 500, 25)
units = st.sidebar.slider("Monthly Production (MT)", 5000, 80000, 20000, 1000)
fixed_costs = st.sidebar.slider("Fixed Costs (Rs Cr/mo)", 20, 400, 80, 10)
st.sidebar.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Working Capital Days</div>', unsafe_allow_html=True)
rec_days = st.sidebar.slider("Receivables Days (DSO)", 10, 120, 45, 1, help="Days Sales Outstanding — credit terms to steel customers")
pay_days = st.sidebar.slider("Payables Days (DPO)", 10, 90, 35, 1, help="Days Payables Outstanding — payment terms with miners")
inv_days = st.sidebar.slider("Inventory Days (DIO)", 15, 150, 60, 1, help="Days Inventory Outstanding — total raw material to finished goods cycle")
st.sidebar.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Optimisation Scenarios</div>', unsafe_allow_html=True)
payables_extension = st.sidebar.slider("Payables Extension Target (days)", 0, 30, 15, 1, help="Additional days negotiated with mining counterparties")
inventory_reduction = st.sidebar.slider("Inventory Reduction Target (days)", 0, 30, 10, 1, help="Days reduction through lean procurement and JIT")
receivables_reduction = st.sidebar.slider("Receivables Reduction Target (days)", 0, 20, 5, 1, help="Days reduction through tighter credit terms or factoring")
financing_rate = st.sidebar.slider("Working Capital Financing Rate (%/yr)", 6, 16, 10, 1)
st.sidebar.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">Break-Even Inputs</div>', unsafe_allow_html=True)
selling_price = st.sidebar.number_input("Selling Price (Rs per MT)", 10000, 150000, 55000, 1000)
variable_cost_unit = st.sidebar.number_input("Variable Cost (Rs per MT)", 5000, 120000, 37000, 1000)
st.sidebar.markdown(f'<div style="background:#1e293b;border-radius:6px;padding:12px;margin-top:12px;"><div style="font-size:11px;color:#64748b;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Live Commodity Prices</div><div style="font-size:12px;color:#94a3b8;line-height:1.9;">Coking Coal: ${spot_coal:.1f}/T<br>Iron Ore: ${spot_ore:.1f}/T<br>Financing rate: {financing_rate}%/yr</div></div>', unsafe_allow_html=True)
run_btn = st.sidebar.button("Run Working Capital Analysis", type="primary", use_container_width=True)

if run_btn:
    cogs = (spot_coal/1000 + spot_ore/1000) * units + fixed_costs * 0.3
    daily_rev = revenue / 30
    daily_cogs = cogs / 30
    receivables = round(daily_rev * rec_days, 1)
    payables = round(daily_cogs * pay_days, 1)
    inventory = round(daily_cogs * inv_days, 1)
    nwc = round(receivables + inventory - payables, 1)
    ccc = rec_days + inv_days - pay_days
    opt_rec_days = rec_days - receivables_reduction
    opt_pay_days = pay_days + payables_extension
    opt_inv_days = inv_days - inventory_reduction
    opt_receivables = round(daily_rev * opt_rec_days, 1)
    opt_payables = round(daily_cogs * opt_pay_days, 1)
    opt_inventory = round(daily_cogs * opt_inv_days, 1)
    opt_nwc = round(opt_receivables + opt_inventory - opt_payables, 1)
    opt_ccc = opt_rec_days + opt_inv_days - opt_pay_days
    cash_freed = round(nwc - opt_nwc, 1)
    annual_financing_saving = round(cash_freed * financing_rate / 100, 2)
    cm = selling_price - variable_cost_unit
    cm_ratio = cm / selling_price if selling_price > 0 else 0
    bep_units = fixed_costs * 1e7 / cm if cm > 0 else 0
    bep_revenue = fixed_costs / cm_ratio if cm_ratio > 0 else 0
    mos_units = units - bep_units
    mos_pct = mos_units / units * 100 if units > 0 else 0
    dol = (units * cm) / (units * cm - fixed_costs * 1e7) if (units * cm - fixed_costs * 1e7) != 0 else 0
    ebitda = revenue - (spot_coal/1000 + spot_ore/1000) * units - fixed_costs

    if ccc < 55:
        ccc_rating = "Top Quartile"
        ccc_color = "#15803d"
        ccc_bg = "#f0fdf4"
        ccc_border = "#22c55e"
        ccc_note = "CCC is below the 55-day top-quartile global threshold. Working capital efficiency is best-in-class."
    elif ccc < 65:
        ccc_rating = "Above Average"
        ccc_color = "#1d4ed8"
        ccc_bg = "#eff6ff"
        ccc_border = "#3b82f6"
        ccc_note = "CCC is below the Indian industry average of 65 days. Solid working capital management with room for further optimisation."
    elif ccc < 75:
        ccc_rating = "Industry Average"
        ccc_color = "#92400e"
        ccc_bg = "#fffbeb"
        ccc_border = "#f59e0b"
        ccc_note = f"CCC of {ccc} days is within the industry average band. Payables extension and inventory reduction present near-term optimisation opportunities."
    else:
        ccc_rating = "Below Average"
        ccc_color = "#b91c1c"
        ccc_bg = "#fef2f2"
        ccc_border = "#dc2626"
        ccc_note = f"CCC of {ccc} days is above the 75-day threshold, indicating working capital intensity above peers. Immediate programme recommended."

    st.markdown(f"""
    <div style="background:{ccc_bg};border-left:5px solid {ccc_border};border-radius:6px;padding:20px 24px;margin-bottom:24px;">
        <div style="font-size:11px;font-weight:600;color:{ccc_color};text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;">Working Capital Assessment</div>
        <div style="font-size:20px;font-weight:700;color:{ccc_color};margin-bottom:8px;">Cash Conversion Cycle: {ccc} Days — {ccc_rating}</div>
        <div style="font-size:14px;color:#374151;line-height:1.6;">{ccc_note}</div>
        <div style="margin-top:10px;font-size:13px;color:#6b7280;">Optimised CCC: {opt_ccc} days | Cash freed: Rs {cash_freed} Cr | Annual financing saving: Rs {annual_financing_saving} Cr</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Working Capital Dashboard</div>', unsafe_allow_html=True)
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Net Working Capital", f"Rs {nwc} Cr", help="Receivables + Inventory - Payables")
    k2.metric("Cash Conversion Cycle", f"{ccc} days", delta=f"{'Above' if ccc > 65 else 'Below'} avg 65d", delta_color="inverse" if ccc > 65 else "normal")
    k3.metric("Receivables", f"Rs {receivables} Cr", help=f"{rec_days} days outstanding")
    k4.metric("Inventory", f"Rs {inventory} Cr", help=f"{inv_days} days of COGS")
    k5.metric("Payables", f"Rs {payables} Cr", help=f"{pay_days} days outstanding")
    k6.metric("Cash Freed (Optimised)", f"Rs {cash_freed} Cr", delta=f"{opt_ccc}d target CCC", delta_color="normal" if cash_freed > 0 else "inverse")

    st.markdown('<div class="section-header">Working Capital Composition and Optimisation</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        fig_wc = make_subplots(rows=1, cols=2, subplot_titles=["Current Working Capital (Rs Cr)", "CCC Components (Days)"], horizontal_spacing=0.14)
        wc_items = ["Receivables", "Inventory", "Payables (-)"]
        wc_vals = [receivables, inventory, -payables]
        wc_colors = ["#1d4ed8", "#ea580c", "#16a34a"]
        fig_wc.add_trace(go.Bar(x=wc_items, y=wc_vals, marker_color=wc_colors, marker_line=dict(color="rgba(0,0,0,0.06)", width=1), text=[f"Rs {abs(v):.0f}" for v in wc_vals], textposition="outside", textfont=dict(size=10), showlegend=False), row=1, col=1)
        fig_wc.add_hline(y=0, line_color="#94a3b8", line_width=1, row=1, col=1)
        ccc_items = ["DSO\n(Receivables)", "DIO\n(Inventory)", "DPO\n(Payables)", "CCC"]
        ccc_vals = [rec_days, inv_days, -pay_days, ccc]
        ccc_colors_bar = ["#1d4ed8", "#ea580c", "#16a34a", "#7c3aed"]
        fig_wc.add_trace(go.Bar(x=ccc_items, y=ccc_vals, marker_color=ccc_colors_bar, marker_line=dict(color="rgba(0,0,0,0.06)", width=1), text=[f"{abs(v)}d" for v in ccc_vals], textposition="outside", textfont=dict(size=10), showlegend=False), row=1, col=2)
        fig_wc.add_hline(y=65, line_dash="dot", line_color="#f59e0b", line_width=1.5, annotation_text="Industry avg: 65d", annotation_font=dict(size=10, color="#f59e0b"), row=1, col=2)
        fig_wc.add_hline(y=55, line_dash="dot", line_color="#16a34a", line_width=1.5, annotation_text="Top quartile: 55d", annotation_font=dict(size=10, color="#16a34a"), row=1, col=2)
        fig_wc.update_layout(height=380, plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11, color="#374151"), margin=dict(t=40, b=20))
        fig_wc.update_xaxes(showgrid=False, linecolor="#e5e7eb")
        fig_wc.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
        st.plotly_chart(fig_wc, use_container_width=True)

    with col_b:
        bench_companies = ["SAIL\n(89d)", "JSW\n(71d)", "Industry\nAvg (65d)", "Tata Steel\n(62d)", f"Your Model\n({ccc}d)", "Top\nQuartile\n(<55d)"]
        bench_ccc = [89, 71, 65, 62, ccc, 52]
        bench_colors = ["#dc2626", "#f59e0b", "#f59e0b", "#1d4ed8", ccc_color, "#15803d"]
        fig_bench = go.Figure()
        fig_bench.add_trace(go.Bar(x=bench_companies, y=bench_ccc, marker_color=bench_colors, marker_line=dict(color="rgba(0,0,0,0.06)", width=1), text=[f"{v}d" for v in bench_ccc], textposition="outside", textfont=dict(size=10)))
        fig_bench.add_hline(y=65, line_dash="dot", line_color="#f59e0b", line_width=1.5)
        fig_bench.add_hline(y=55, line_dash="dot", line_color="#16a34a", line_width=1.5)
        fig_bench.update_layout(title="CCC Benchmarking — Indian Steel Sector", height=380, plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11, color="#374151"), showlegend=False, yaxis_title="Cash Conversion Cycle (Days)", margin=dict(t=50, b=20))
        fig_bench.update_xaxes(showgrid=False, linecolor="#e5e7eb", tickfont=dict(size=9))
        fig_bench.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
        st.plotly_chart(fig_bench, use_container_width=True)

    st.markdown('<div class="section-header">Optimisation Impact Analysis</div>', unsafe_allow_html=True)
    col_opt1, col_opt2 = st.columns(2)

    with col_opt1:
        opt_categories = ["Receivables\nReduction", "Payables\nExtension", "Inventory\nReduction", "Total\nCash Freed"]
        rec_freed = round(receivables - opt_receivables, 1)
        pay_freed = round(opt_payables - payables, 1)
        inv_freed = round(inventory - opt_inventory, 1)
        opt_vals = [rec_freed, pay_freed, inv_freed, cash_freed]
        opt_colors = ["#1d4ed8", "#16a34a", "#ea580c", "#7c3aed"]
        fig_opt = go.Figure()
        fig_opt.add_trace(go.Bar(x=opt_categories, y=opt_vals, marker_color=opt_colors, marker_line=dict(color="rgba(0,0,0,0.06)", width=1), text=[f"Rs {v:.1f} Cr" for v in opt_vals], textposition="outside", textfont=dict(size=10)))
        fig_opt.update_layout(title=f"Working Capital Release — Rs {cash_freed} Cr Total", height=340, plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11, color="#374151"), showlegend=False, yaxis_title="Rs Cr Released", margin=dict(t=50, b=20))
        fig_opt.update_xaxes(showgrid=False, linecolor="#e5e7eb")
        fig_opt.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
        st.plotly_chart(fig_opt, use_container_width=True)

    with col_opt2:
        quarters = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]
        cumulative_savings = [round(annual_financing_saving * q / 4, 2) for q in range(1, 9)]
        fig_cum = go.Figure()
        fig_cum.add_trace(go.Scatter(x=quarters, y=cumulative_savings, mode="lines+markers", line=dict(color="#16a34a", width=2.5), marker=dict(size=8, color="#16a34a", line=dict(color="white", width=1.5)), fill="tozeroy", fillcolor="rgba(22,163,74,0.07)", name="Cumulative Financing Saving"))
        fig_cum.update_layout(title=f"Cumulative Financing Saving — Rs {annual_financing_saving} Cr/yr", height=340, plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11, color="#374151"), xaxis_title="Quarter", yaxis_title="Cumulative Saving (Rs Cr)", showlegend=False, margin=dict(t=50, b=20))
        fig_cum.update_xaxes(showgrid=False, linecolor="#e5e7eb")
        fig_cum.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
        st.plotly_chart(fig_cum, use_container_width=True)

    st.markdown('<div class="section-header">Detailed Working Capital Schedule</div>', unsafe_allow_html=True)
    wc_schedule = pd.DataFrame({
        "Component": ["Receivables (Current)", "Inventory (Current)", "Payables Current", "Net Working Capital (Current)", "Receivables (Optimised)", "Inventory (Optimised)", "Payables (Optimised)", "Net Working Capital (Optimised)", "Cash Released", "Annual Financing Saving"],
        "Days": [rec_days, inv_days, pay_days, ccc, opt_rec_days, opt_inv_days, opt_pay_days, opt_ccc, "-", "-"],
        "Rs Cr": [receivables, inventory, payables, nwc, opt_receivables, opt_inventory, opt_payables, opt_nwc, cash_freed, annual_financing_saving],
        "Category": ["Current", "Current", "Current", "Current Summary", "Optimised", "Optimised", "Optimised", "Optimised Summary", "Impact", "Impact"],
        "Lever": ["Customer credit terms and collection efficiency", "Raw material procurement JIT and lean buffer", "Supplier negotiation — mining counterparties", "CCC = DSO + DIO - DPO", f"Target DSO reduction of {receivables_reduction} days", f"Target DIO reduction of {inventory_reduction} days", f"Target DPO extension of {payables_extension} days via Vale / BHP / Glencore negotiation", f"Target CCC: {opt_ccc} days", "Total NWC reduction from all three levers", f"Savings on Rs {cash_freed} Cr at {financing_rate}% cost of capital"]
    })

    def color_wc_table(row):
        if row["Category"] in ["Current Summary", "Optimised Summary"]:
            return ["font-weight: 700; background: #f8fafc"] * len(row)
        if row["Category"] == "Impact":
            col = "#15803d" if isinstance(row["Rs Cr"], (int, float)) and row["Rs Cr"] > 0 else "#b91c1c"
            return [f"font-weight: 600; color: {col}"] * len(row)
        return [""] * len(row)

    st.dataframe(wc_schedule.style.apply(color_wc_table, axis=1).format({"Rs Cr": "{:.2f}"}), use_container_width=True, hide_index=True)
    st.markdown(f'<div class="footnote">Working capital financing cost applied at {financing_rate}%/yr. Receivables reduction assumes tighter credit terms with auto, construction, and white goods OEMs. Inventory reduction reflects JIT procurement aligned to forward contract delivery schedules. Payables extension targets Vale, BHP, Glencore, and POSCO International — Indian integrated producers typically have leverage to negotiate 45-60 day terms given volume.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Break-Even and Operating Leverage Analysis</div>', unsafe_allow_html=True)
    k1b, k2b, k3b, k4b, k5b = st.columns(5)
    k1b.metric("Break-Even Volume", f"{int(bep_units):,} MT", help="Minimum production to cover all fixed costs")
    k2b.metric("Break-Even Revenue", f"Rs {bep_revenue:.1f} Cr", help="Revenue at break-even production")
    k3b.metric("Contribution Margin", f"{cm_ratio*100:.1f}%", help="Revenue remaining after all variable costs")
    k4b.metric("Margin of Safety", f"{mos_pct:.1f}%", delta=f"{int(mos_units):,} MT buffer", delta_color="normal" if mos_pct > 20 else "inverse")
    k5b.metric("Degree of Op. Leverage", f"{dol:.2f}x", help="1% revenue change causes this multiple EBITDA change")

    vol_range = np.linspace(0, units * 1.5, 200)
    rev_line = vol_range * selling_price / 1e7
    vc_line = vol_range * variable_cost_unit / 1e7
    fc_line = np.full_like(vol_range, fixed_costs)
    total_cost_line = vc_line + fc_line
    profit_line = rev_line - total_cost_line

    fig_be = make_subplots(rows=1, cols=2, subplot_titles=["Break-Even Chart (Rs Cr)", "Profit / Loss at Each Volume Level (Rs Cr)"], horizontal_spacing=0.1)
    fig_be.add_trace(go.Scatter(x=vol_range/1000, y=rev_line, name="Revenue", line=dict(color="#16a34a", width=2.5)), row=1, col=1)
    fig_be.add_trace(go.Scatter(x=vol_range/1000, y=total_cost_line, name="Total Cost", line=dict(color="#dc2626", width=2.5)), row=1, col=1)
    fig_be.add_trace(go.Scatter(x=vol_range/1000, y=vc_line, name="Variable Cost", line=dict(color="#f59e0b", width=1.5, dash="dot")), row=1, col=1)
    fig_be.add_trace(go.Scatter(x=vol_range/1000, y=fc_line, name="Fixed Cost", line=dict(color="#94a3b8", width=1.5, dash="dot")), row=1, col=1)
    fig_be.add_vline(x=bep_units/1000, line_dash="dash", line_color="#7c3aed", line_width=2, annotation_text=f"BEP: {int(bep_units):,} MT", annotation_font=dict(size=11, color="#7c3aed"), row=1, col=1)
    fig_be.add_vline(x=units/1000, line_dash="dot", line_color="#1d4ed8", line_width=1.5, annotation_text=f"Current: {units:,} MT", annotation_font=dict(size=11, color="#1d4ed8"), row=1, col=1)
    profit_colors = ["rgba(22,163,74,0.12)" if v >= 0 else "rgba(220,38,38,0.08)" for v in profit_line]
    fig_be.add_trace(go.Scatter(x=vol_range/1000, y=profit_line, name="Profit / Loss", mode="lines", line=dict(color="#7c3aed", width=2.5), fill="tozeroy", fillcolor="rgba(124,58,237,0.07)"), row=1, col=2)
    fig_be.add_hline(y=0, line_color="#374151", line_width=1.5, annotation_text="Break-Even", annotation_position="right", annotation_font=dict(size=11), row=1, col=2)
    fig_be.add_vline(x=bep_units/1000, line_dash="dash", line_color="#7c3aed", line_width=1.5, row=1, col=2)
    fig_be.add_vline(x=units/1000, line_dash="dot", line_color="#1d4ed8", line_width=1.5, row=1, col=2)
    fig_be.update_layout(height=420, plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11, color="#374151"), legend=dict(orientation="h", y=-0.16, font=dict(size=10)), margin=dict(t=40, b=60), xaxis_title="Production Volume ('000 MT)", xaxis2_title="Production Volume ('000 MT)", yaxis_title="Rs Cr", yaxis2_title="Profit / Loss (Rs Cr)")
    fig_be.update_xaxes(showgrid=False, linecolor="#e5e7eb")
    fig_be.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
    st.plotly_chart(fig_be, use_container_width=True)
    st.markdown(f'<div class="footnote">Contribution margin of Rs {cm:,.0f}/MT ({cm_ratio*100:.1f}%) and fixed costs of Rs {fixed_costs} Cr/month determine a break-even production volume of {int(bep_units):,} MT. The current margin of safety of {mos_pct:.1f}% ({int(mos_units):,} MT above BEP) indicates {"healthy" if mos_pct > 25 else "moderate" if mos_pct > 15 else "tight"} downside protection. Degree of Operating Leverage of {dol:.2f}x means a 10% revenue decline causes a {dol*10:.1f}% EBITDA decline — reflecting steel\'s high fixed-cost intensity.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">DOL Sensitivity — EBITDA Response to Revenue Change</div>', unsafe_allow_html=True)
    revenue_change_range = np.arange(-30, 31, 2)
    ebitda_response = []
    current_ebitda = ebitda if ebitda != 0 else 1
    for delta_pct in revenue_change_range:
        new_rev = revenue * (1 + delta_pct/100)
        new_vc = (spot_coal/1000 + spot_ore/1000) * units * (1 + delta_pct/100 * 0.7)
        new_ebitda = new_rev - new_vc - fixed_costs
        ebitda_response.append(round(new_ebitda, 1))

    fig_dol = go.Figure()
    bar_colors_dol = ["#16a34a" if v > current_ebitda else "#dc2626" for v in ebitda_response]
    fig_dol.add_trace(go.Scatter(x=revenue_change_range, y=ebitda_response, mode="lines+markers", line=dict(color="#1d4ed8", width=2.5), marker=dict(size=6, color=["#16a34a" if v > 0 else "#dc2626" for v in ebitda_response], line=dict(color="white", width=1)), fill="tozeroy", fillcolor="rgba(29,78,216,0.07)", name="EBITDA Response"))
    fig_dol.add_vline(x=0, line_color="#94a3b8", line_width=1.5, annotation_text="Base Case", annotation_font=dict(size=11))
    fig_dol.add_hline(y=0, line_color="#dc2626", line_width=1.5, annotation_text="EBITDA Break-Even", annotation_position="right", annotation_font=dict(size=11, color="#dc2626"))
    fig_dol.add_hline(y=current_ebitda, line_dash="dot", line_color="#7c3aed", line_width=1.5, annotation_text=f"Current EBITDA: Rs {current_ebitda:.1f} Cr", annotation_position="right", annotation_font=dict(size=11, color="#7c3aed"))
    fig_dol.update_layout(height=340, plot_bgcolor="#fafafa", paper_bgcolor="white", font=dict(family="Inter, sans-serif", size=11, color="#374151"), xaxis_title="Revenue Change (%)", yaxis_title="EBITDA (Rs Cr)", showlegend=False, margin=dict(t=20, b=20))
    fig_dol.update_xaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb", ticksuffix="%")
    fig_dol.update_yaxes(showgrid=True, gridcolor="#f1f5f9", linecolor="#e5e7eb")
    st.plotly_chart(fig_dol, use_container_width=True)

    st.markdown('<div class="section-header">Treasury and Working Capital Memorandum</div>', unsafe_allow_html=True)
    ccc_vs_tata = ccc - 62
    ccc_vs_top = ccc - 55
    lever_priority = []
    if payables_extension > 0: lever_priority.append(f"(1) Payables extension of {payables_extension} days with key mining counterparties — Rs {pay_freed:.1f} Cr release")
    if inventory_reduction > 0: lever_priority.append(f"({'2' if lever_priority else '1'}) Inventory reduction of {inventory_reduction} days through JIT procurement alignment — Rs {inv_freed:.1f} Cr release")
    if receivables_reduction > 0: lever_priority.append(f"({'3' if len(lever_priority)==2 else '2' if lever_priority else '1'}) Receivables reduction of {receivables_reduction} days through tighter credit terms or factoring — Rs {rec_freed:.1f} Cr release")

    st.markdown(f"""
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:8px;padding:28px 32px;font-family:'Inter',sans-serif;line-height:1.85;font-size:14px;color:#374151;">
        <div style="font-size:11px;font-weight:600;color:#9ca3af;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #f3f4f6;">TREASURY AND WORKING CAPITAL COMMITTEE — OPERATIONAL EFFICIENCY MEMO</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:16px;margin-bottom:20px;">
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Current CCC</span><div style="font-weight:600;color:#111827;">{ccc} days ({ccc_rating})</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Target CCC</span><div style="font-weight:600;color:#111827;">{opt_ccc} days</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Cash Released</span><div style="font-weight:600;color:#15803d;">Rs {cash_freed} Cr</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Annual Saving</span><div style="font-weight:600;color:#15803d;">Rs {annual_financing_saving} Cr</div></div>
        </div>
        <p style="margin:0 0 12px;"><strong>Situation.</strong> The company's current Cash Conversion Cycle of <strong>{ccc} days</strong> (DSO {rec_days}d + DIO {inv_days}d - DPO {pay_days}d) represents a Net Working Capital position of <strong>Rs {nwc} Cr</strong>. This is {"above" if ccc_vs_tata > 0 else "below"} Tata Steel India's benchmark of 62 days by {abs(ccc_vs_tata)} days, and {"above" if ccc_vs_top > 0 else "below"} the top-quartile global threshold of 55 days by {abs(ccc_vs_top)} days.</p>
        <p style="margin:0 0 12px;"><strong>Opportunity.</strong> Three working capital levers — payables extension, inventory reduction, and receivables reduction — can reduce the CCC to <strong>{opt_ccc} days</strong>, releasing <strong>Rs {cash_freed} Cr</strong> in cash. At the firm's cost of working capital financing of {financing_rate}%, this represents an annual saving of <strong>Rs {annual_financing_saving} Cr</strong>. The improvement does not require capital expenditure — it is a pure treasury and procurement management initiative.</p>
        <p style="margin:0 0 12px;"><strong>Recommended Levers in Priority Order.</strong> {" ".join(lever_priority) if lever_priority else "Configure optimisation targets in the sidebar to generate specific lever recommendations."}</p>
        <p style="margin:0 0 12px;"><strong>Break-Even Context.</strong> The break-even production volume of <strong>{int(bep_units):,} MT/month</strong> represents a margin of safety of <strong>{mos_pct:.1f}%</strong> against current production of {units:,} MT. With a Degree of Operating Leverage of <strong>{dol:.2f}x</strong>, a 10% revenue decline translates to a {dol*10:.1f}% EBITDA decline — reinforcing the importance of maintaining production volumes above break-even through demand cycle management.</p>
        <p style="margin:0;"><strong>Risk Considerations.</strong> Payables extension beyond 45 days with key miners (Vale, BHP, Glencore) requires long-term relationship management and may attract early-payment discount forfeiture. Inventory reduction below 45 days of COGS introduces supply disruption risk during port congestion or shipping delays — a material risk for Indian integrated producers dependent on seaborne coal imports. Receivables factoring, if used, should be evaluated against the cost differential versus internal financing rate of {financing_rate}%.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div style="padding: 80px 40px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 20px; text-align: center;">
        <div style="font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;">Working Capital Intelligence Engine</div>
        <h2 style="font-size: 22px; font-weight: 600; color: #1e293b; margin: 0 0 12px;">Configure operating parameters to run working capital analysis</h2>
        <p style="font-size: 14px; color: #64748b; max-width: 640px; margin: 0 auto 32px; line-height: 1.6;">Comprehensive working capital intelligence covering Cash Conversion Cycle benchmarking against Indian steel peers, three-lever optimisation quantification, break-even analysis, Degree of Operating Leverage, and board-ready treasury memorandum.</p>
        <div style="display: inline-grid; grid-template-columns: repeat(3, 1fr); gap: 16px; text-align: left; max-width: 640px; margin: 0 auto;">
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 20px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Live Coal</div>
                <div style="font-weight: 700; color: #1e293b; font-size: 18px; margin-top: 4px;">${spot_coal:.1f}/T</div>
                <div style="font-size: 12px; color: #64748b;">World Bank API</div>
            </div>
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 20px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Live Ore</div>
                <div style="font-weight: 700; color: #1e293b; font-size: 18px; margin-top: 4px;">${spot_ore:.1f}/T</div>
                <div style="font-size: 12px; color: #64748b;">World Bank API</div>
            </div>
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 20px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Bain Benchmark</div>
                <div style="font-weight: 700; color: #15803d; font-size: 18px; margin-top: 4px;">10d CCC = Rs 1,000 Cr</div>
                <div style="font-size: 12px; color: #64748b;">Cash release potential</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)