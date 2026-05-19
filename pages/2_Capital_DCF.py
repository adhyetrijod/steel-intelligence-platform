import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from core.models import SteelFinancialEngine

st.set_page_config(page_title="Capital Allocation | ISFIP", layout="wide")
engine = SteelFinancialEngine()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    [data-testid="stMetricValue"] { font-size: 26px !important; font-weight: 600 !important; color: #ffffff !important; }
    [data-testid="stMetricLabel"] { font-size: 12px !important; color: #6b7280 !important; text-transform: uppercase; letter-spacing: 0.5px; }
    [data-testid="metric-container"] { background: #ffffff; border-radius: 8px; padding: 20px 24px; border: 1px solid #e5e7eb; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
    div[data-testid="stSidebar"] { background: #0f172a; border-right: 1px solid #1e293b; }
    div[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    div[data-testid="stSidebar"] .stSlider > div > div { background: #334155 !important; }
    .section-header { font-size: 13px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin: 24px 0 12px; border-bottom: 1px solid #f3f4f6; padding-bottom: 8px; }
    .data-table { font-size: 13px; }
    .verdict-box { border-radius: 6px; padding: 20px 24px; margin: 16px 0; }
    .footnote { font-size: 12px; color: #9ca3af; font-style: italic; margin-top: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding: 32px 0 8px 0; border-bottom: 2px solid #1e3a5f; margin-bottom: 28px;">
    <div style="font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px;">INTEGRATED FERRUM CAPITAL INTELLIGENCE</div>
    <h1 style="font-size: 26px; font-weight: 700; color: #f1f5f9; margin: 0; letter-spacing: -0.5px;">Capital Allocation Engine</h1>
    <div style="font-size: 14px; color: #64748b; margin-top: 6px;">Discounted Cash Flow Analysis — Free Cash Flow to Firm Methodology</div>
    <div style="display: flex; gap: 24px; margin-top: 16px; flex-wrap: wrap;">
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Model:</span> FCFF DCF + Gordon Growth Terminal Value</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Benchmark WACC:</span> Tata Steel 10.2% | JSW 10.8% | SAIL 11.5%</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Decision Rule:</span> NPV > 0 AND IRR > WACC</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Use Case:</span> BF Upgrade / DRI / EAF / Greenfield</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_ctx1, col_ctx2, col_ctx3, col_ctx4 = st.columns(4)
ctx_style = "background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:14px 16px;"
col_ctx1.markdown(f'<div style="{ctx_style}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">Method</div><div style="font-size:15px;font-weight:600;color:#1e293b;margin-top:4px;">FCFF Discounting</div><div style="font-size:12px;color:#64748b;">Unlevered free cash flow</div></div>', unsafe_allow_html=True)
col_ctx2.markdown(f'<div style="{ctx_style}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">Terminal Value</div><div style="font-size:15px;font-weight:600;color:#1e293b;margin-top:4px;">Gordon Growth</div><div style="font-size:12px;color:#64748b;">Perpetuity with stable growth</div></div>', unsafe_allow_html=True)
col_ctx3.markdown(f'<div style="{ctx_style}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">Tax Treatment</div><div style="font-size:15px;font-weight:600;color:#1e293b;margin-top:4px;">NOPAT Basis</div><div style="font-size:12px;color:#64748b;">Post-tax operating profit</div></div>', unsafe_allow_html=True)
col_ctx4.markdown(f'<div style="{ctx_style}"><div style="font-size:11px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">Standard</div><div style="font-size:15px;font-weight:600;color:#1e293b;margin-top:4px;">CFA / Damodaran</div><div style="font-size:12px;color:#64748b;">Institutional grade model</div></div>', unsafe_allow_html=True)

st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

st.sidebar.markdown('<div style="padding: 20px 0 12px; border-bottom: 1px solid #1e293b; margin-bottom: 16px;"><div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Capital Allocation Engine</div><div style="font-size: 15px; color: #f1f5f9; font-weight: 600; margin-top: 4px;">Investment Parameters</div></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Project Scale</div>', unsafe_allow_html=True)
investment = st.sidebar.number_input("Initial Investment (Rs Cr)", 100, 10000, 1000, 100)
annual_ebitda = st.sidebar.number_input("Year-1 EBITDA (Rs Cr/yr)", 50, 5000, 600, 50)
st.sidebar.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Growth and Discount Assumptions</div>', unsafe_allow_html=True)
growth_rate = st.sidebar.slider("Revenue Growth Rate (% per yr)", 0.0, 12.0, 3.0, 0.5)
wacc = st.sidebar.slider("WACC (%)", 6.0, 18.0, 10.0, 0.5)
tax_rate = st.sidebar.slider("Effective Tax Rate (%)", 10, 35, 25, 1)
term_growth = st.sidebar.slider("Terminal Growth Rate (%)", 1.0, 4.0, 2.5, 0.25)
years = st.sidebar.slider("Projection Horizon (years)", 5, 15, 10)
st.sidebar.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Cash Flow Adjustments</div>', unsafe_allow_html=True)
depreciation = st.sidebar.number_input("Annual Depreciation (Rs Cr)", 10, 500, 60, 10)
capex_maint = st.sidebar.number_input("Maintenance CapEx (Rs Cr/yr)", 5, 300, 30, 5)
delta_wc = st.sidebar.number_input("Delta Working Capital (Rs Cr/yr)", 0, 100, 10, 5)
st.sidebar.markdown(f'<div style="background:#1e293b;border-radius:6px;padding:12px;margin-top:16px;"><div style="font-size:11px;color:#64748b;margin-bottom:6px;">INDUSTRY WACC REFERENCE</div><div style="font-size:12px;color:#94a3b8;line-height:1.8;">Tata Steel India: ~10.2%<br>JSW Steel: ~10.8%<br>SAIL: ~11.5%<br>Terminal growth: 2.0-2.5%</div></div>', unsafe_allow_html=True)
run_btn = st.sidebar.button("Run DCF Analysis", type="primary", use_container_width=True)

if run_btn:
    dcf = engine.dcf_analysis(investment, annual_ebitda, growth_rate/100, wacc/100, tax_rate/100, depreciation, capex_maint, delta_wc, term_growth/100, years)
    invest = "INVEST" in dcf['decision']
    irr_spread = round(dcf['irr'] - wacc, 1)
    tv_pct = round(dcf['pv_terminal'] / (dcf['pv_cashflows'] + dcf['pv_terminal']) * 100, 1)

    if invest:
        verdict_bg = "#f0fdf4"
        verdict_border = "#16a34a"
        verdict_text = "#15803d"
        verdict_label = "INVEST"
        verdict_description = f"Project generates value above the cost of capital. IRR of {dcf['irr']}% exceeds WACC of {wacc}% by {irr_spread} percentage points. NPV of Rs {dcf['npv']:.0f} Cr represents net value created for shareholders. Recommended for board approval subject to execution risk review."
    else:
        verdict_bg = "#fef2f2"
        verdict_border = "#dc2626"
        verdict_text = "#b91c1c"
        verdict_label = "DO NOT INVEST"
        verdict_description = f"Project fails to clear the cost of capital hurdle. IRR of {dcf['irr']}% falls below WACC of {wacc}% by {abs(irr_spread)} percentage points. NPV of Rs {dcf['npv']:.0f} Cr represents value destruction. Project requires restructuring, cost reduction, or improved revenue assumptions before resubmission."

    st.markdown(f"""
    <div style="background:{verdict_bg};border-left:5px solid {verdict_border};border-radius:6px;padding:20px 24px;margin-bottom:24px;">
        <div style="font-size:11px;font-weight:600;color:{verdict_text};text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;">Investment Decision</div>
        <div style="font-size:22px;font-weight:700;color:{verdict_text};margin-bottom:8px;">{verdict_label}</div>
        <div style="font-size:14px;color:#374151;line-height:1.6;">{verdict_description}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Key Financial Metrics</div>', unsafe_allow_html=True)
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Net Present Value", f"Rs {dcf['npv']:.0f} Cr", delta=f"{'+'if dcf['npv']>0 else ''}{dcf['npv']:.0f} Cr", delta_color="normal" if dcf['npv'] > 0 else "inverse")
    k2.metric("Internal Rate of Return", f"{dcf['irr']}%", delta=f"{'+'if irr_spread>0 else ''}{irr_spread}% vs WACC", delta_color="normal" if irr_spread > 0 else "inverse")
    k3.metric("Payback Period", f"{dcf['payback_years']} years")
    k4.metric("PV of Cash Flows", f"Rs {dcf['pv_cashflows']:.0f} Cr")
    k5.metric("Terminal Value (PV)", f"Rs {dcf['pv_terminal']:.0f} Cr")

    st.markdown(f'<div class="footnote">Terminal value constitutes {tv_pct}% of total project value. {"Within normal range (40-70%) for long-cycle steel assets." if 40 < tv_pct < 75 else "Outside typical range — model is sensitive to terminal growth assumptions. Review with sensitivity analysis."} Projection horizon: {years} years at {wacc}% discount rate.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Cash Flow Analysis</div>', unsafe_allow_html=True)

    ebitda_series = [round(annual_ebitda * (1 + growth_rate/100)**t, 1) for t in range(1, years+1)]
    ebit_series = [round(e - depreciation, 1) for e in ebitda_series]
    nopat_series = [round(e * (1 - tax_rate/100), 1) for e in ebit_series]

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Annual Free Cash Flow to Firm (Rs Cr)", "Cumulative Discounted Cash Flow (Rs Cr)"], horizontal_spacing=0.1)

    bar_colors = ['#16a34a' if v > 0 else '#dc2626' for v in dcf['cashflows']]
    fig.add_trace(go.Bar(x=[f"Y{y}" for y in dcf['years']], y=dcf['cashflows'], marker_color=bar_colors, marker_line=dict(color='rgba(0,0,0,0.08)', width=1), text=[f"{v:.0f}" for v in dcf['cashflows']], textposition='outside', textfont=dict(size=10, color='#374151'), name='FCFF'), row=1, col=1)
    fig.add_hline(y=0, line_color='#94a3b8', line_width=1, row=1, col=1)

    cum_pv = []
    running = -investment
    for pv in dcf['pv_annual']:
        running += pv
        cum_pv.append(round(running, 1))

    line_color = ['#16a34a' if v >= 0 else '#dc2626' for v in cum_pv]
    fig.add_trace(go.Scatter(x=[f"Y{y}" for y in dcf['years']], y=cum_pv, mode='lines+markers', line=dict(color='#1d4ed8', width=2.5), marker=dict(size=7, color=['#16a34a' if v >= 0 else '#dc2626' for v in cum_pv], line=dict(color='white', width=1.5)), fill='tozeroy', fillcolor='rgba(29,78,216,0.06)', name='Cumulative PV'), row=1, col=2)
    fig.add_hline(y=0, line_dash='dot', line_color='#dc2626', line_width=1.5, annotation_text=f"Payback achieved at Y{dcf['payback_years']:.0f}", annotation_position="top right", annotation_font=dict(size=11, color='#dc2626'), row=1, col=2)
    fig.add_hline(y=-investment, line_dash='dot', line_color='#94a3b8', line_width=1, annotation_text=f"Initial outlay: Rs {investment} Cr", annotation_font=dict(size=10, color='#94a3b8'), row=1, col=2)

    fig.update_layout(height=420, showlegend=False, plot_bgcolor='#fafafa', paper_bgcolor='white', font=dict(family='Inter, sans-serif', size=12, color='#374151'), hoverlabel=dict(bgcolor='white', font_size=12, bordercolor='#e5e7eb'), margin=dict(t=40, b=20))
    fig.update_xaxes(showgrid=False, linecolor='#e5e7eb', tickfont=dict(size=11))
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', linecolor='#e5e7eb', tickfont=dict(size=11))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Detailed Cash Flow Schedule</div>', unsafe_allow_html=True)
    cf_df = pd.DataFrame({
        "Year": dcf['years'],
        "EBITDA (Rs Cr)": ebitda_series,
        "EBIT (Rs Cr)": ebit_series,
        "NOPAT (Rs Cr)": nopat_series,
        "FCFF (Rs Cr)": dcf['cashflows'],
        "Discount Factor": [round(1/(1+wacc/100)**t, 5) for t in dcf['years']],
        "PV of FCFF (Rs Cr)": dcf['pv_annual'],
        "Cumulative PV (Rs Cr)": [round(sum(dcf['pv_annual'][:i+1])-investment, 1) for i in range(len(dcf['years']))]
    })

    def color_cells(val):
        if isinstance(val, (int, float)):
            if val > 0: return 'color: #15803d; font-weight: 500'
            elif val < 0: return 'color: #b91c1c; font-weight: 500'
        return 'color: #374151'

    st.dataframe(cf_df.style.map(color_cells, subset=["FCFF (Rs Cr)", "NOPAT (Rs Cr)", "Cumulative PV (Rs Cr)"]).format({"EBITDA (Rs Cr)": "{:.1f}", "EBIT (Rs Cr)": "{:.1f}", "NOPAT (Rs Cr)": "{:.1f}", "FCFF (Rs Cr)": "{:.1f}", "Discount Factor": "{:.5f}", "PV of FCFF (Rs Cr)": "{:.1f}", "Cumulative PV (Rs Cr)": "{:.1f}"}), use_container_width=True, hide_index=True)
    st.markdown(f'<div class="footnote">FCFF = NOPAT + Depreciation (Rs {depreciation} Cr) - Maintenance CapEx (Rs {capex_maint} Cr) - Delta Working Capital (Rs {delta_wc} Cr). NOPAT = EBIT x (1 - {tax_rate}%). Tax shield on debt not included in FCFF model — reflected in WACC.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Sensitivity Analysis — NPV vs WACC and Growth Rate</div>', unsafe_allow_html=True)
    wacc_range = np.arange(6.0, 18.5, 0.5)
    growth_scenarios = [1.5, 2.5, 3.0, 4.0, 5.0]
    sens_fig = go.Figure()
    sens_colors = ['#94a3b8', '#64748b', '#1d4ed8', '#0891b2', '#0284c7']

    for g_rate, s_color in zip(growth_scenarios, sens_colors):
        npv_vals = []
        for w in wacc_range:
            try:
                res = engine.dcf_analysis(investment, annual_ebitda, g_rate/100, w/100, tax_rate/100, depreciation, capex_maint, delta_wc, term_growth/100, years)
                npv_vals.append(res['npv'])
            except:
                npv_vals.append(None)
        label_weight = 700 if g_rate == growth_rate else 400
        sens_fig.add_trace(go.Scatter(x=wacc_range, y=npv_vals, mode='lines', name=f"Growth {g_rate}%", line=dict(color=s_color, width=3 if g_rate == growth_rate else 1.5, dash='solid' if g_rate == growth_rate else 'dot')))

    sens_fig.add_vline(x=wacc, line_dash='dash', line_color='#dc2626', line_width=1.5, annotation_text=f"Current WACC: {wacc}%", annotation_font=dict(size=11, color='#dc2626'))
    sens_fig.add_hline(y=0, line_color='#374151', line_width=1.5, annotation_text="NPV Breakeven", annotation_position="right", annotation_font=dict(size=11))
    sens_fig.update_layout(height=360, plot_bgcolor='#fafafa', paper_bgcolor='white', font=dict(family='Inter, sans-serif', size=12), xaxis_title="WACC (%)", yaxis_title="NPV (Rs Cr)", legend=dict(orientation='h', y=-0.2, font=dict(size=11)), margin=dict(t=20, b=60), hoverlabel=dict(bgcolor='white', font_size=12))
    sens_fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9', linecolor='#e5e7eb')
    sens_fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', linecolor='#e5e7eb')
    st.plotly_chart(sens_fig, use_container_width=True)
    st.markdown('<div class="footnote">Sensitivity chart shows NPV across a WACC range of 6-18% for five revenue growth scenarios. Bold blue line represents base case assumptions. Curves crossing the NPV=0 axis indicate the WACC at which the project breaks even (the IRR).</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Board Memorandum — Capital Allocation Committee</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:8px;padding:28px 32px;font-family:'Inter',sans-serif;line-height:1.8;font-size:14px;color:#374151;">
        <div style="font-size:11px;font-weight:600;color:#9ca3af;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #f3f4f6;">CAPITAL ALLOCATION COMMITTEE — INVESTMENT MEMO</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px;">
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Project Capex</span><div style="font-weight:600;color:#111827;">Rs {investment} Cr</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Decision</span><div style="font-weight:600;color:{verdict_text};">{verdict_label}</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">NPV at {wacc}% WACC</span><div style="font-weight:600;color:#111827;">Rs {dcf['npv']:.0f} Cr</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Project IRR</span><div style="font-weight:600;color:#111827;">{dcf['irr']}% ({'+' if irr_spread>0 else ''}{irr_spread}% spread vs WACC)</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Payback Period</span><div style="font-weight:600;color:#111827;">{dcf['payback_years']} years</div></div>
            <div><span style="font-size:11px;color:#9ca3af;text-transform:uppercase;">Terminal Value Contribution</span><div style="font-weight:600;color:#111827;">{tv_pct}% of total project value</div></div>
        </div>
        <div style="border-top:1px solid #f3f4f6;padding-top:16px;">
            <p style="margin:0 0 10px;"><strong>Situation.</strong> The board is evaluating a Rs {investment} Cr capital investment in steel production capacity. The project is projected to generate Rs {annual_ebitda} Cr EBITDA in Year 1, growing at {growth_rate}% per annum over a {years}-year horizon at an effective tax rate of {tax_rate}%.</p>
            <p style="margin:0 0 10px;"><strong>Analysis.</strong> Applying the firm's cost of capital of {wacc}% as the discount rate, the project yields a Net Present Value of <strong>Rs {dcf['npv']:.0f} Cr</strong> and an Internal Rate of Return of <strong>{dcf['irr']}%</strong>. The IRR-WACC spread of {irr_spread} percentage points {'provides adequate buffer above the hurdle rate' if irr_spread > 2 else 'is narrow and leaves limited margin for execution risk' if irr_spread > 0 else 'indicates the project does not clear the cost of capital'}. Terminal value at {tv_pct}% of total project value is {'within' if 40 < tv_pct < 75 else 'outside'} the normal 40-70% range for long-cycle steel assets.</p>
            <p style="margin:0;"><strong>Recommendation.</strong> {verdict_description}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="padding: 80px 40px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 20px; text-align: center;">
        <div style="font-size: 13px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;">Capital Allocation Engine</div>
        <h2 style="font-size: 22px; font-weight: 600; color: #1e293b; margin: 0 0 12px;">Configure investment parameters in the sidebar to run DCF analysis</h2>
        <p style="font-size: 14px; color: #64748b; max-width: 600px; margin: 0 auto 32px; line-height: 1.6;">This model evaluates steel sector capex decisions using free cash flow to firm methodology with Gordon Growth terminal value — the standard approach used by bulge-bracket advisors and steel sector strategists.</p>
        <div style="display: inline-grid; grid-template-columns: repeat(4,1fr); gap: 16px; text-align: left; margin-top: 8px;">
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 20px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Asset Type</div>
                <div style="font-weight: 600; color: #1e293b; margin-top: 4px;">Blast Furnace</div>
                <div style="font-size: 12px; color: #64748b;">Rs 800 - 2000 Cr</div>
            </div>
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 20px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Asset Type</div>
                <div style="font-weight: 600; color: #1e293b; margin-top: 4px;">EAF Transition</div>
                <div style="font-size: 12px; color: #64748b;">Rs 400 - 1200 Cr</div>
            </div>
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 20px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Asset Type</div>
                <div style="font-weight: 600; color: #1e293b; margin-top: 4px;">DRI Plant</div>
                <div style="font-size: 12px; color: #64748b;">Rs 600 - 1800 Cr</div>
            </div>
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px 20px;">
                <div style="font-size: 11px; color: #94a3b8; text-transform: uppercase; font-weight: 600;">Asset Type</div>
                <div style="font-weight: 600; color: #1e293b; margin-top: 4px;">Pellet Plant</div>
                <div style="font-size: 12px; color: #64748b;">Rs 300 - 800 Cr</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)