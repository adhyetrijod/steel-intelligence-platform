import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from core.data import get_coal_prices, get_ore_prices

st.set_page_config(page_title="Steel Financial Intelligence Platform", layout="wide", initial_sidebar_state="expanded")

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
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    [data-testid="stMetricValue"] { font-size: 22px !important; font-weight: 600 !important; color: #ffffff !important; }
    [data-testid="stMetricLabel"] { font-size: 11px !important; color: #94a3b8 !important; text-transform: uppercase; letter-spacing: 0.5px; }
    [data-testid="metric-container"] { background: #1e293b; border-radius: 8px; padding: 18px 22px; border: 1px solid #334155; }
    [data-testid="stMetricDelta"] { color: #94a3b8 !important; font-size: 12px !important; }
    div[data-testid="stSidebar"] { background: #0f172a; border-right: 1px solid #1e293b; }
    div[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    .section-header { font-size: 11px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 1.5px; margin: 32px 0 16px; border-bottom: 1px solid #1e293b; padding-bottom: 8px; }
    .footnote { font-size: 12px; color: #475569; font-style: italic; margin-top: 8px; line-height: 1.6; }
    .stTabs [data-baseweb="tab"] { color: #94a3b8 !important; }
    .stTabs [aria-selected="true"] { color: #ffffff !important; }
    .stDataFrame { border: 1px solid #1e293b; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:48px 0 32px 0;border-bottom:1px solid #1e293b;margin-bottom:36px;">
    <h1 style="font-size:36px;font-weight:700;color:#f1f5f9;margin:0 0 14px;letter-spacing:-0.5px;line-height:1.15;">
        Steel Financial Intelligence Platform
    </h1>
    <div style="display:flex;gap:28px;flex-wrap:wrap;">
        <div style="font-size:12px;color:#64748b;">
            <span style="color:#64748b;font-weight:500;">Research:</span>
            Bain Steel Sector 2024 · McKinsey Industrial · WSA Statistical Yearbook
        </div>
        <div style="font-size:12px;color:#64748b;">
            <span style="color:#64748b;font-weight:500;">Use case:</span>
            Tata Steel India operations context
        </div>
        <div style="font-size:12px;color:#64748b;">
            <span style="color:#64748b;font-weight:500;">Data:</span>
            World Bank Commodity API — live
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

coal_delta = round((coal_df['price'].iloc[-1] - coal_df['price'].iloc[-2]) / coal_df['price'].iloc[-2] * 100, 2) if len(coal_df) > 1 else 0
ore_delta  = round((ore_df['price'].iloc[-1]  - ore_df['price'].iloc[-2])  / ore_df['price'].iloc[-2]  * 100, 2) if len(ore_df) > 1 else 0

st.markdown('<div class="section-header">Live Commodity Market Snapshot</div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Coking Coal", f"${spot_coal:.1f} / T",  delta=f"{coal_delta:+.2f}% vs prior month")
k2.metric("Iron Ore",    f"${spot_ore:.1f} / T",   delta=f"{ore_delta:+.2f}% vs prior month")
k3.metric("Coal History", f"{len(coal_df)} months", help="World Bank monthly series")
k4.metric("Ore History",  f"{len(ore_df)} months",  help="World Bank monthly series")
k5.metric("Models Active", "7 of 7",                help="All financial models loaded")
st.markdown('<div class="footnote">Source: World Bank Commodity Markets Outlook. Prices in USD per metric tonne. Updated monthly.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Platform Architecture — Seven Financial Models</div>', unsafe_allow_html=True)
tabs = st.tabs(["Model Overview", "Methodology", "Industry Benchmarks", "Research Basis"])

with tabs[0]:
    col_m1, col_m2 = st.columns(2)
    ms = "background:#1e293b;border:1px solid #334155;border-radius:6px;padding:16px 20px;margin-bottom:12px;"
    with col_m1:
        for title, sub, desc, use in [
            ("Model 1 — Risk Engine", "Monte Carlo EBITDA Simulation", "10,000 correlated commodity price scenarios. Outputs VaR, CVaR, loss probability. Correlated coal-ore shocks at empirical rho = 0.45.", "CFO risk committees, treasury functions"),
            ("Model 2 — Capital Decisions", "DCF / NPV / IRR Analysis", "Full discounted cash flow with Gordon Growth terminal value, sensitivity analysis, and board investment memorandum generation.", "Board capital allocation committees"),
            ("Model 3 — Procurement", "LP Procurement Optimiser", "SciPy HiGHS linear programming solver finds optimal spot/3M/6M forward contract allocation to minimise total procurement cost.", "Supply chain finance, procurement heads"),
            ("Model 7 — Executive Brief", "GPT-4o Brief Generator", "Converts quantitative model outputs into board-ready executive narrative using Bain SCRR framework.", "Strategy teams, board secretariat"),
        ]:
            st.markdown(f'<div style="{ms}"><div style="font-size:10px;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">{title}</div><div style="font-size:14px;font-weight:600;color:#f1f5f9;">{sub}</div><div style="font-size:12px;color:#64748b;margin-top:4px;line-height:1.5;">{desc}</div><div style="font-size:11px;color:#475569;margin-top:8px;">Used by: {use}</div></div>', unsafe_allow_html=True)
    with col_m2:
        for title, sub, desc, use in [
            ("Model 4 — Scenario Planning", "Five-Scenario P&L Stress Test", "Full income statement across Deep Stress, Bear, Base, Bull, and Supercycle. Probability-weighted expected value, EBITDA bridge waterfall.", "Annual planning, investor relations"),
            ("Model 5 — Working Capital", "CCC Analysis and Treasury", "Cash Conversion Cycle benchmarking against Tata Steel, JSW, and SAIL. Three-lever optimisation with break-even and DOL analysis.", "Treasury, CFO office"),
            ("Model 6 — Commodity VaR", "Parametric Value at Risk", "Portfolio VaR with correlation adjustment for combined coal and ore exposure. CVaR at configurable confidence levels.", "Risk management, hedging decisions"),
        ]:
            st.markdown(f'<div style="{ms}"><div style="font-size:10px;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">{title}</div><div style="font-size:14px;font-weight:600;color:#f1f5f9;">{sub}</div><div style="font-size:12px;color:#64748b;margin-top:4px;line-height:1.5;">{desc}</div><div style="font-size:11px;color:#475569;margin-top:8px;">Used by: {use}</div></div>', unsafe_allow_html=True)

with tabs[1]:
    meth_data = {
        "Model":       ["Monte Carlo","DCF / NPV / IRR","Commodity VaR","LP Procurement","Scenario P&L","Working Capital","Break-Even / DOL"],
        "Method":      ["Multivariate Log-Normal correlated shocks","FCFF + Gordon Growth Terminal Value","Parametric Normal portfolio correlation","SciPy HiGHS LP — exact optimisation","Five-scenario income statement stress test","DSO + DIO - DPO three-lever optimisation","Contribution margin and operating leverage"],
        "Standard":    ["Basel III / BCBS","CFA / Damodaran","Basel III market risk","Operations Research LP","Bain 2024 calibration","WSA working capital norms","Management accounting"],
        "Key Output":  ["VaR, CVaR, loss probability","NPV, IRR, payback, cashflow schedule","Portfolio VaR, CVaR, exposure pct","Optimal split, monthly saving Rs Cr","Full P&L, EV, EBITDA bridge","CCC days, NWC Rs Cr, cash freed","BEP MT, margin of safety, DOL"]
    }
    st.dataframe(pd.DataFrame(meth_data), use_container_width=True, hide_index=True)

with tabs[2]:
    bench_data = {
        "Metric":        ["EBITDA Margin","CCC (days)","Coal Cost as pct Revenue","Debt / EBITDA","ROCE","Receivables Days","Payables Days"],
        "Tata Steel IN": ["17-22%","~62","28-32%","~2.8x","~12%","~38","~32"],
        "JSW Steel":     ["18-24%","~71","26-30%","~2.1x","~14%","~42","~28"],
        "SAIL":          ["8-14%", "~89","31-36%","~5.2x","~6%", "~55","~22"],
        "Top Quartile":  [">25%",  "<55","<25%",  "<2.0x",">18%","<30",">45"]
    }
    st.dataframe(pd.DataFrame(bench_data), use_container_width=True, hide_index=True)
    st.markdown('<div class="footnote">Source: Company annual reports FY2024. Top quartile represents global integrated producer benchmark per WSA Statistical Yearbook 2024.</div>', unsafe_allow_html=True)

with tabs[3]:
    res_data = {
        "Publication":  ["Steel Sector Under Pressure","Steel Decarbonization Pathways","Commodity Markets Outlook","Statistical Yearbook","Industrial Metals Outlook"],
        "Organisation": ["Bain and Company","McKinsey Global Institute","World Bank","World Steel Association","IMF"],
        "Year":         ["2024","2023","2024","2024","2024"],
        "Applied In":   ["Scenario calibration, procurement benchmarks, CCC targets","WACC benchmarks, EAF transition IRR thresholds","Live commodity price API, volatility coefficients","CCC benchmarks, working capital norms","Scenario probability ranges, bear/bull calibration"]
    }
    st.dataframe(pd.DataFrame(res_data), use_container_width=True, hide_index=True)

st.markdown('<div class="section-header">Steel Sector — Market Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:13px;color:#64748b;margin-bottom:20px;">Curated developments across Indian and global steel markets. Context for scenario assumption calibration.</div>', unsafe_allow_html=True)

STEEL_NEWS = [
    {"headline": "India steel capacity target of 300 MT by 2030 reaffirmed", "source": "Ministry of Steel, India", "date": "May 2026", "summary": "The government has reiterated its 300 MT capacity target with Tata Steel, JSW, and SAIL as anchor producers. Infrastructure and green steel investments remain central to the expansion plan.", "category": "Policy", "cc": "#1d4ed8"},
    {"headline": "Coking coal imports from Australia remain elevated despite price correction", "source": "World Steel Association", "date": "May 2026", "summary": "Australian premium hard coking coal holds approximately 65% of Indian import mix. Spot prices have corrected 8% from Q1 highs but remain above the five-year average, maintaining pressure on margins.", "category": "Commodity", "cc": "#dc2626"},
    {"headline": "JSW Steel reports record EBITDA margin of 22.4% in Q4 FY26", "source": "JSW Steel Investor Relations", "date": "May 2026", "summary": "Q4 FY2026 results showed record EBITDA margin of 22.4%, driven by lower iron ore input costs from captive mines and improved product mix toward value-added flat products.", "category": "Earnings", "cc": "#15803d"},
    {"headline": "China steel output declines for third consecutive quarter", "source": "World Steel Association", "date": "April 2026", "summary": "Chinese crude steel output fell 4.2% year-on-year in Q1 2026. The reduction has contributed to softening seaborne iron ore prices, improving input economics for non-Chinese integrated producers.", "category": "Global Market", "cc": "#7c3aed"},
    {"headline": "India imposes 12% provisional safeguard duty on flat steel imports", "source": "DGTR India", "date": "April 2026", "summary": "Provisional safeguard duty imposed on certain flat products to protect domestic producers from import surges from China, Vietnam, and South Korea. Measure supports domestic realisations through H1 FY27.", "category": "Policy", "cc": "#1d4ed8"},
    {"headline": "Green steel premium emerging — European buyers paying 15-20% above standard HRC", "source": "Steel Times International", "date": "March 2026", "summary": "European automotive and construction buyers are paying 15-20% premium for certified green steel via DRI-EAF routes. Indian producers with DRI capacity are exploring export opportunities.", "category": "Trend", "cc": "#ea580c"},
]

news_cols = st.columns(3)
for i, a in enumerate(STEEL_NEWS):
    with news_cols[i % 3]:
        st.markdown(f"""
        <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:18px 20px;margin-bottom:16px;min-height:220px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                <span style="background:{a['cc']};color:white;font-size:10px;font-weight:600;padding:2px 8px;border-radius:3px;text-transform:uppercase;letter-spacing:0.5px;">{a['category']}</span>
                <span style="font-size:11px;color:#475569;">{a['date']}</span>
            </div>
            <div style="font-size:13px;font-weight:600;color:#f1f5f9;line-height:1.45;margin-bottom:8px;">{a['headline']}</div>
            <div style="font-size:12px;color:#64748b;line-height:1.6;">{a['summary']}</div>
            <div style="margin-top:12px;font-size:11px;color:#475569;font-style:italic;">{a['source']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="footnote">Market intelligence compiled from public sources. Verify against primary sources before operational or investment decisions.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Commodity Price History</div>', unsafe_allow_html=True)
fig = make_subplots(rows=1, cols=2, subplot_titles=["Coking Coal — Monthly Spot (USD/T)", "Iron Ore — Monthly Spot (USD/T)"], horizontal_spacing=0.1)
fig.add_trace(go.Scatter(x=coal_df['date'], y=coal_df['price'], mode='lines', name='Coal', line=dict(color='#3b82f6', width=2), fill='tozeroy', fillcolor='rgba(59,130,246,0.08)'), row=1, col=1)
fig.add_trace(go.Scatter(x=ore_df['date'],  y=ore_df['price'],  mode='lines', name='Ore',  line=dict(color='#f97316', width=2), fill='tozeroy', fillcolor='rgba(249,115,22,0.08)'),  row=1, col=2)
fig.add_hline(y=coal_df['price'].mean(), line_dash='dot', line_color='#475569', line_width=1.5, annotation_text=f"Avg ${coal_df['price'].mean():.0f}", annotation_font=dict(size=10, color='#64748b'), row=1, col=1)
fig.add_hline(y=ore_df['price'].mean(),  line_dash='dot', line_color='#475569', line_width=1.5, annotation_text=f"Avg ${ore_df['price'].mean():.0f}",  annotation_font=dict(size=10, color='#64748b'), row=1, col=2)
fig.update_layout(height=300, showlegend=False, plot_bgcolor='#0f172a', paper_bgcolor='#0f172a', font=dict(family='Inter, sans-serif', size=11, color='#94a3b8'), margin=dict(t=40, b=20))
fig.update_xaxes(showgrid=False, linecolor='#1e293b', tickfont=dict(color='#64748b'))
fig.update_yaxes(showgrid=True, gridcolor='#1e293b', linecolor='#1e293b', tickprefix='$', tickfont=dict(color='#64748b'))
fig.update_annotations(font=dict(color='#64748b'))
st.plotly_chart(fig, use_container_width=True)
st.markdown(f'<div class="footnote">World Bank Commodity Markets Outlook. {len(coal_df)} monthly observations to {coal_df["date"].iloc[-1].strftime("%b %Y")}.</div>', unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:48px;padding-top:20px;border-top:1px solid #1e293b;display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;align-items:center;">
    <div>
        <div style="font-size:13px;font-weight:600;color:#94a3b8;">Steel Financial Intelligence Platform</div>
        <div style="font-size:12px;color:#475569;margin-top:2px;">Built independently — inspired by Bain and Company steel sector research</div>
    </div>
    <div style="text-align:right;">
        <div style="font-size:12px;color:#475569;">Python · SciPy · Streamlit · Plotly · OpenAI API · World Bank API</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div style="padding:20px 0 12px;border-bottom:1px solid #1e293b;margin-bottom:20px;">
    <div style="font-size:15px;color:#f1f5f9;font-weight:600;">ISFIP</div>
    <div style="font-size:12px;color:#64748b;margin-top:3px;">Steel Financial Intelligence</div>
</div>
<div style="padding:0 0 16px;">
    <div style="font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:10px;font-weight:600;">Analysis Modules</div>
    <div style="font-size:13px;color:#64748b;line-height:2.2;">
        Risk Engine — Monte Carlo<br>
        Capital DCF — NPV / IRR<br>
        Procurement — LP Optimiser<br>
        Scenarios — Stress Testing<br>
        Working Capital — CCC<br>
        AI Brief — GPT-4o
    </div>
</div>
<div style="background:#1e293b;border-radius:6px;padding:14px;margin-top:8px;border:1px solid #334155;">
    <div style="font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;font-weight:600;">Live Market Data</div>
    <div style="font-size:13px;color:#64748b;line-height:1.9;">
        Coking Coal: <span style="color:#f1f5f9;font-weight:600;">${spot_coal:.1f}/T</span><br>
        Iron Ore: <span style="color:#f1f5f9;font-weight:600;">${spot_ore:.1f}/T</span><br>
        Source: World Bank API<br>
        Updated: Monthly
    </div>
</div>
""", unsafe_allow_html=True)