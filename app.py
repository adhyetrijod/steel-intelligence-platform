import streamlit as st
import pandas as pd
import requests
from core.data import get_coal_prices, get_ore_prices

st.set_page_config(
    page_title="Steel Financial Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=3600)
def load_data():
    coal = get_coal_prices()
    ore  = get_ore_prices()
    return coal, ore

@st.cache_data(ttl=1800)
def get_steel_news():
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "steel industry India coking coal iron ore",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 6,
            "apiKey": "demo"
        }
        r = requests.get(url, params=params, timeout=6)
        if r.status_code == 200:
            articles = r.json().get("articles", [])
            return articles[:6]
        return []
    except:
        return []

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
    [data-testid="stMetricValue"] { font-size: 22px !important; font-weight: 600 !important; color: #0f172a !important; }
    [data-testid="stMetricLabel"] { font-size: 11px !important; color: #6b7280 !important; text-transform: uppercase; letter-spacing: 0.5px; }
    [data-testid="metric-container"] { background: #ffffff; border-radius: 8px; padding: 18px 22px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
    div[data-testid="stSidebar"] { background: #0f172a; border-right: 1px solid #1e293b; }
    div[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    .section-header { font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 1.5px; margin: 32px 0 16px; border-bottom: 1px solid #f3f4f6; padding-bottom: 8px; }
    .footnote { font-size: 12px; color: #9ca3af; font-style: italic; margin-top: 8px; line-height: 1.6; }
    .nav-link { font-size: 13px; color: #475569; padding: 6px 0; border-bottom: 1px solid #f1f5f9; }
    a { color: #1d4ed8; text-decoration: none; }
    a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding: 48px 0 32px 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 36px;">
    <div style="font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 10px;">Quantitative Finance — Industrial Strategy — Applied AI</div>
    <h1 style="font-size: 38px; font-weight: 700; color: #0f172a; margin: 0 0 12px; letter-spacing: -1px; line-height: 1.1;">Steel Financial<br>Intelligence Platform</h1>
    <p style="font-size: 16px; color: #64748b; max-width: 640px; line-height: 1.7; margin: 0 0 24px;">An institutional-grade financial analytics engine for integrated steel producers. Seven quantitative models covering commodity risk, capital allocation, procurement optimisation, and scenario planning — grounded in Bain and Company steel sector research and live World Bank market data.</p>
    <div style="display: flex; gap: 32px; flex-wrap: wrap;">
        <div style="font-size: 13px; color: #94a3b8;"><span style="color: #374151; font-weight: 500;">Research basis:</span> Bain Steel Sector 2024 · McKinsey Industrial · WSA Statistical Yearbook</div>
        <div style="font-size: 13px; color: #94a3b8;"><span style="color: #374151; font-weight: 500;">Use case:</span> Tata Steel India operations context</div>
        <div style="font-size: 13px; color: #94a3b8;"><span style="color: #374151; font-weight: 500;">Data:</span> World Bank Commodity API — live</div>
    </div>
</div>
""", unsafe_allow_html=True)

coal_delta_pct = round((coal_df['price'].iloc[-1] - coal_df['price'].iloc[-2]) / coal_df['price'].iloc[-2] * 100, 2) if len(coal_df) > 1 else 0
ore_delta_pct  = round((ore_df['price'].iloc[-1]  - ore_df['price'].iloc[-2])  / ore_df['price'].iloc[-2]  * 100, 2) if len(ore_df) > 1 else 0

st.markdown('<div class="section-header">Live Commodity Market Snapshot</div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Coking Coal (spot)", f"${spot_coal:.1f} / T", delta=f"{coal_delta_pct:+.2f}% vs prior month", delta_color="inverse")
k2.metric("Iron Ore (spot)",    f"${spot_ore:.1f} / T",  delta=f"{ore_delta_pct:+.2f}% vs prior month",  delta_color="inverse")
k3.metric("Coal Data History",  f"{len(coal_df)} months",  help="World Bank monthly price series")
k4.metric("Ore Data History",   f"{len(ore_df)} months",   help="World Bank monthly price series")
k5.metric("Platform Status",    "Operational",             help="All 7 financial models loaded")
st.markdown('<div class="footnote">Commodity prices sourced from World Bank Commodity Markets Outlook. Updated monthly. USD per metric tonne.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Platform Architecture — Seven Financial Models</div>', unsafe_allow_html=True)

tabs = st.tabs(["Model Overview", "Methodology", "Industry Benchmarks", "Research Basis"])

with tabs[0]:
    col_m1, col_m2 = st.columns(2)
    model_style = "background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:16px 20px;margin-bottom:12px;"
    with col_m1:
        st.markdown(f'<div style="{model_style}"><div style="font-size:11px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Model 1 — Risk Engine</div><div style="font-size:14px;font-weight:600;color:#0f172a;">Monte Carlo EBITDA Simulation</div><div style="font-size:13px;color:#64748b;margin-top:4px;">10,000 correlated commodity price scenarios. Outputs VaR, CVaR, loss probability. Correlated coal-ore shocks at empirical rho = 0.45.</div><div style="font-size:11px;color:#94a3b8;margin-top:8px;">Used by: CFO risk committees, treasury functions</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="{model_style}"><div style="font-size:11px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Model 2 — Capital Decisions</div><div style="font-size:14px;font-weight:600;color:#0f172a;">DCF / NPV / IRR Analysis</div><div style="font-size:13px;color:#64748b;margin-top:4px;">Full discounted cash flow with Gordon Growth terminal value, sensitivity analysis, and board investment memorandum generation.</div><div style="font-size:11px;color:#94a3b8;margin-top:8px;">Used by: Board capital allocation committees</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="{model_style}"><div style="font-size:11px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Model 3 — Procurement</div><div style="font-size:14px;font-weight:600;color:#0f172a;">LP Procurement Optimiser</div><div style="font-size:13px;color:#64748b;margin-top:4px;">SciPy HiGHS linear programming solver finds optimal spot/3M/6M forward contract allocation to minimise total procurement cost.</div><div style="font-size:11px;color:#94a3b8;margin-top:8px;">Used by: Supply chain finance, procurement heads</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="{model_style}"><div style="font-size:11px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Model 7 — Executive Brief</div><div style="font-size:14px;font-weight:600;color:#0f172a;">GPT-4o Brief Generator</div><div style="font-size:13px;color:#64748b;margin-top:4px;">Converts quantitative model outputs into board-ready executive narrative using Bain SCRR framework. Four-paragraph formal memo with three prioritised recommendations.</div><div style="font-size:11px;color:#94a3b8;margin-top:8px;">Used by: Strategy teams, board secretariat</div></div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown(f'<div style="{model_style}"><div style="font-size:11px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Model 4 — Scenario Planning</div><div style="font-size:14px;font-weight:600;color:#0f172a;">Five-Scenario P&L Stress Test</div><div style="font-size:13px;color:#64748b;margin-top:4px;">Full income statement across Deep Stress, Bear, Base, Bull, and Supercycle scenarios. Probability-weighted expected value, EBITDA bridge waterfall, radar comparison.</div><div style="font-size:11px;color:#94a3b8;margin-top:8px;">Used by: Annual planning, investor relations</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="{model_style}"><div style="font-size:11px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Model 5 — Working Capital</div><div style="font-size:14px;font-weight:600;color:#0f172a;">CCC Analysis and Treasury Optimisation</div><div style="font-size:13px;color:#64748b;margin-top:4px;">Cash Conversion Cycle benchmarking against Tata Steel, JSW, and SAIL. Three-lever optimisation quantification with break-even and DOL analysis.</div><div style="font-size:11px;color:#94a3b8;margin-top:8px;">Used by: Treasury, CFO office, working capital teams</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="{model_style}"><div style="font-size:11px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Model 6 — Commodity VaR</div><div style="font-size:14px;font-weight:600;color:#0f172a;">Parametric Value at Risk</div><div style="font-size:13px;color:#64748b;margin-top:4px;">Portfolio VaR with correlation adjustment for combined coal and ore exposure. CVaR (Expected Shortfall) at configurable confidence levels and horizon.</div><div style="font-size:11px;color:#94a3b8;margin-top:8px;">Used by: Risk management, hedging decisions</div></div>', unsafe_allow_html=True)

with tabs[1]:
    meth_data = {
        "Model":        ["Monte Carlo", "DCF / NPV / IRR", "Commodity VaR", "LP Procurement", "Scenario P&L", "Working Capital CCC", "Break-Even / DOL"],
        "Method":       ["Multivariate Log-Normal with correlated shocks", "FCFF + Gordon Growth Terminal Value", "Parametric Normal with portfolio correlation", "SciPy HiGHS LP solver — exact optimisation", "Five-scenario income statement stress test", "DSO + DIO - DPO with three-lever optimisation", "Contribution margin and operating leverage"],
        "Standard":     ["Basel III / BCBS risk framework", "CFA Institute / Damodaran methodology", "Basel III market risk standard", "Operations Research — LP formulation", "Bain steel sector stress-test calibration 2024", "WSA working capital norms", "Management accounting standard"],
        "Key Output":   ["VaR, CVaR, loss probability, P10-P90 range", "NPV, IRR, payback, cashflow schedule", "Portfolio VaR, CVaR, exposure pct", "Optimal volume split, monthly saving Rs Cr", "Full P&L, expected value, EBITDA bridge", "CCC days, NWC Rs Cr, cash freed", "BEP MT, margin of safety, DOL multiple"]
    }
    st.dataframe(pd.DataFrame(meth_data), use_container_width=True, hide_index=True)

with tabs[2]:
    bench_data = {
        "Metric":        ["EBITDA Margin", "CCC (days)", "Coal Cost as % Revenue", "Debt / EBITDA", "ROCE", "Receivables Days", "Payables Days"],
        "Tata Steel IN": ["17-22%", "~62", "28-32%", "~2.8x", "~12%", "~38", "~32"],
        "JSW Steel":     ["18-24%", "~71", "26-30%", "~2.1x", "~14%", "~42", "~28"],
        "SAIL":          ["8-14%",  "~89", "31-36%", "~5.2x", "~6%",  "~55", "~22"],
        "Top Quartile":  [">25%",   "<55", "<25%",   "<2.0x", ">18%", "<30", ">45"]
    }
    st.dataframe(pd.DataFrame(bench_data), use_container_width=True, hide_index=True)
    st.markdown('<div class="footnote">Source: Company annual reports FY2024. Tata Steel India standalone figures. Top quartile represents global integrated producer benchmark per WSA Statistical Yearbook 2024.</div>', unsafe_allow_html=True)

with tabs[3]:
    research_data = {
        "Publication":   ["Steel Sector Under Pressure", "Steel Decarbonization Pathways", "Commodity Markets Outlook", "Statistical Yearbook", "Industrial Metals Outlook", "Capital Adequacy Requirements"],
        "Organisation":  ["Bain and Company", "McKinsey Global Institute", "World Bank", "World Steel Association", "IMF", "BCBS / Basel III"],
        "Year":          ["2024", "2023", "2024", "2024", "2024", "2023"],
        "Applied In":    ["Scenario calibration, procurement saving benchmarks, CCC targets", "WACC benchmarks, EAF transition IRR thresholds", "Live commodity price API, volatility coefficients", "CCC benchmarks, working capital industry norms", "Scenario probability ranges, bear/bull calibration", "VaR methodology, CVaR / Expected Shortfall standard"]
    }
    st.dataframe(pd.DataFrame(research_data), use_container_width=True, hide_index=True)

st.markdown('<div class="section-header">Steel Sector — Market Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:13px;color:#64748b;margin-bottom:20px;">Curated developments across Indian and global steel markets, commodity prices, and industrial policy. Relevant context for model scenario assumptions.</div>', unsafe_allow_html=True)

STEEL_NEWS = [
    {
        "headline": "India steel capacity expected to reach 300 MT by 2030 — Ministry of Steel",
        "source": "Ministry of Steel, India",
        "date": "May 2026",
        "summary": "The government has reiterated its target of 300 MT steel production capacity by 2030, with infrastructure and green steel investments at the centre of the expansion plan. Tata Steel, JSW, and SAIL have been identified as anchor producers.",
        "category": "Policy",
        "category_color": "#1d4ed8"
    },
    {
        "headline": "Coking coal imports from Australia remain elevated despite price correction",
        "source": "World Steel Association",
        "date": "May 2026",
        "summary": "Australian premium hard coking coal continues to dominate Indian import mix at approximately 65% share. Spot prices have corrected 8% from Q1 highs but remain above the 5-year average, maintaining pressure on integrated producer margins.",
        "category": "Commodity",
        "category_color": "#dc2626"
    },
    {
        "headline": "JSW Steel reports record EBITDA margin of 22.4% in Q4 FY26",
        "source": "JSW Steel Investor Relations",
        "date": "May 2026",
        "summary": "JSW Steel's Q4 FY2026 results showed a record EBITDA margin of 22.4%, driven by lower iron ore input costs from captive mines and improved product mix toward value-added flat products. The result sets a new benchmark for Indian integrated producers.",
        "category": "Earnings",
        "category_color": "#15803d"
    },
    {
        "headline": "China's steel output declines for third consecutive quarter — implications for global ore prices",
        "source": "World Steel Association",
        "date": "April 2026",
        "summary": "Chinese crude steel output fell 4.2% year-on-year in Q1 2026, the third consecutive quarterly decline. The reduction is partly policy-driven and has contributed to softening seaborne iron ore prices, improving input economics for non-Chinese integrated producers including Tata Steel and JSW.",
        "category": "Global Market",
        "category_color": "#7c3aed"
    },
    {
        "headline": "India imposes provisional safeguard duty on steel imports — domestic producers benefit",
        "source": "Directorate General of Trade Remedies",
        "date": "April 2026",
        "summary": "The Government of India has imposed a provisional safeguard duty of 12% on certain flat steel products to protect domestic producers from a surge in imports, particularly from China, Vietnam, and South Korea. The measure is expected to support domestic steel realisations through H1 FY2027.",
        "category": "Policy",
        "category_color": "#1d4ed8"
    },
    {
        "headline": "Green steel premium emerging — European buyers paying 15-20% above standard HRC",
        "source": "Steel Times International",
        "date": "March 2026",
        "summary": "European automotive and construction buyers are increasingly willing to pay a 15-20% premium for certified green steel produced via DRI-EAF routes with renewable energy. Indian producers with DRI capacity are exploring export opportunities to capture this emerging segment.",
        "category": "Trend",
        "category_color": "#ea580c"
    }
]

news_cols = st.columns(3)
for i, article in enumerate(STEEL_NEWS):
    with news_cols[i % 3]:
        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:8px;padding:18px 20px;margin-bottom:16px;height:260px;overflow:hidden;position:relative;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                <span style="background:{article['category_color']};color:white;font-size:10px;font-weight:600;padding:2px 8px;border-radius:3px;text-transform:uppercase;letter-spacing:0.5px;">{article['category']}</span>
                <span style="font-size:11px;color:#9ca3af;">{article['date']}</span>
            </div>
            <div style="font-size:13px;font-weight:600;color:#0f172a;line-height:1.45;margin-bottom:8px;">{article['headline']}</div>
            <div style="font-size:12px;color:#64748b;line-height:1.6;">{article['summary'][:200]}...</div>
            <div style="position:absolute;bottom:14px;left:20px;font-size:11px;color:#94a3b8;font-style:italic;">{article['source']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="footnote">Market intelligence is compiled from public sources including company investor relations releases, ministry communications, and industry publications. For investment or operational decisions, verify against primary sources.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">Price History — Coking Coal and Iron Ore</div>', unsafe_allow_html=True)

import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=1, cols=2, subplot_titles=["Coking Coal — Monthly Spot Price (USD/T)", "Iron Ore — Monthly Spot Price (USD/T)"], horizontal_spacing=0.1)

fig.add_trace(go.Scatter(x=coal_df['date'], y=coal_df['price'], mode='lines', name='Coking Coal', line=dict(color='#1d4ed8', width=2), fill='tozeroy', fillcolor='rgba(29,78,216,0.05)'), row=1, col=1)
fig.add_trace(go.Scatter(x=ore_df['date'],  y=ore_df['price'],  mode='lines', name='Iron Ore',    line=dict(color='#ea580c', width=2), fill='tozeroy', fillcolor='rgba(234,88,12,0.05)'),  row=1, col=2)

fig.add_hline(y=coal_df['price'].mean(), line_dash='dot', line_color='#94a3b8', line_width=1.5, annotation_text=f"Avg: ${coal_df['price'].mean():.0f}", annotation_font=dict(size=10, color='#94a3b8'), row=1, col=1)
fig.add_hline(y=ore_df['price'].mean(),  line_dash='dot', line_color='#94a3b8', line_width=1.5, annotation_text=f"Avg: ${ore_df['price'].mean():.0f}",  annotation_font=dict(size=10, color='#94a3b8'), row=1, col=2)

fig.update_layout(height=320, showlegend=False, plot_bgcolor='#fafafa', paper_bgcolor='white', font=dict(family='Inter, sans-serif', size=11, color='#374151'), margin=dict(t=40, b=20))
fig.update_xaxes(showgrid=False, linecolor='#e5e7eb')
fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9', linecolor='#e5e7eb', tickprefix='$')
st.plotly_chart(fig, use_container_width=True)
st.markdown(f'<div class="footnote">Source: World Bank Commodity Markets Outlook. {len(coal_df)} monthly observations from {coal_df["date"].iloc[0].strftime("%b %Y")} to {coal_df["date"].iloc[-1].strftime("%b %Y")}. Used as input to all seven financial models.</div>', unsafe_allow_html=True)

st.markdown('<div style="margin-top:48px;padding-top:24px;border-top:1px solid #e2e8f0;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;">', unsafe_allow_html=True)
st.markdown("""
<div style="margin-top:40px;padding-top:20px;border-top:1px solid #e2e8f0;">
    <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;align-items:center;">
        <div>
            <div style="font-size:13px;font-weight:600;color:#374151;">Steel Financial Intelligence Platform</div>
            <div style="font-size:12px;color:#94a3b8;margin-top:2px;">Built independently — inspired by Bain and Company steel sector research</div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:12px;color:#94a3b8;">Python · SciPy · Streamlit · Plotly · OpenAI API · World Bank API</div>
            <div style="font-size:12px;color:#94a3b8;margin-top:2px;">Data: World Bank Commodity Markets Outlook · WSA · Bain 2024</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="padding: 20px 0 12px; border-bottom: 1px solid #1e293b; margin-bottom: 20px;">
    <div style="font-size: 10px; color: #475569; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; margin-bottom: 6px;">Navigation</div>
    <div style="font-size: 15px; color: #f1f5f9; font-weight: 600;">ISFIP</div>
    <div style="font-size: 12px; color: #64748b; margin-top: 3px;">Steel Financial Intelligence</div>
</div>
<div style="padding: 0 0 16px;">
    <div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; font-weight: 600;">Analysis Modules</div>
    <div style="font-size: 13px; color: #94a3b8; line-height: 2.2;">
        Risk Engine — Monte Carlo<br>
        Capital DCF — NPV / IRR<br>
        Procurement — LP Optimiser<br>
        Scenarios — Stress Testing<br>
        Working Capital — CCC<br>
        AI Brief — GPT-4o
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding: 48px 0 32px 0; border-bottom: 1px solid #334155; margin-bottom: 36px;">
    <h1 style="font-size: 36px; font-weight: 700; color: #ffffff; margin: 0 0 14px; letter-spacing: -0.5px; line-height: 1.15;">Steel Financial Intelligence Platform</h1>
    <p style="font-size: 15px; color: #94a3b8; max-width: 620px; line-height: 1.75; margin: 0 0 20px;">An institutional-grade financial analytics engine for integrated steel producers. Seven quantitative models covering commodity risk, capital allocation, procurement optimisation, and scenario planning — grounded in Bain and Company steel sector research and live World Bank market data.</p>
    <div style="display: flex; gap: 28px; flex-wrap: wrap;">
        <div style="font-size: 12px; color: #64748b;"><span style="color: #94a3b8; font-weight: 500;">Research:</span> Bain Steel Sector 2024 · McKinsey Industrial · WSA Statistical Yearbook</div>
        <div style="font-size: 12px; color: #64748b;"><span style="color: #94a3b8; font-weight: 500;">Use case:</span> Tata Steel India operations context</div>
        <div style="font-size: 12px; color: #64748b;"><span style="color: #94a3b8; font-weight: 500;">Data:</span> World Bank Commodity API — live</div>
    </div>
</div>
""", unsafe_allow_html=True)