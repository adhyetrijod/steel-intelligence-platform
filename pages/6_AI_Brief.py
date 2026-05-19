import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st

st.set_page_config(page_title="Executive Brief | ISFIP", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    [data-testid="stMetricValue"] { font-size: 22px !important; font-weight: 600 !important; color: #1a1a2e !important; }
    [data-testid="stMetricLabel"] { font-size: 11px !important; color: #6b7280 !important; text-transform: uppercase; letter-spacing: 0.5px; }
    [data-testid="metric-container"] { background: #ffffff; border-radius: 8px; padding: 16px 20px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
    div[data-testid="stSidebar"] { background: #0f172a; border-right: 1px solid #1e293b; }
    div[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    div[data-testid="stSidebar"] input { background: #1e293b !important; border: 1px solid #334155 !important; border-radius: 6px !important; color: #f1f5f9 !important; }
    .section-header { font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 1.5px; margin: 28px 0 14px; border-bottom: 1px solid #f3f4f6; padding-bottom: 8px; }
    .footnote { font-size: 12px; color: #9ca3af; font-style: italic; margin-top: 8px; line-height: 1.6; }
    .brief-output { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 28px 32px; font-family: 'Inter', sans-serif; line-height: 1.85; font-size: 14px; color: #374151; }
    stTextInput input { font-family: 'Inter', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding: 32px 0 8px 0; border-bottom: 2px solid #1e3a5f; margin-bottom: 28px;">
    <div style="font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px;">INTEGRATED STEEL FINANCIAL INTELLIGENCE PLATFORM</div>
    <h1 style="font-size: 26px; font-weight: 700; color: #f1f5f9; margin: 0; letter-spacing: -0.5px;">Executive Brief Generator</h1>
    <div style="font-size: 14px; color: #64748b; margin-top: 6px;">GPT-4o Powered — Bain SCRR Framework — Board-Ready Narrative from Model Outputs</div>
    <div style="display: flex; gap: 24px; margin-top: 16px; flex-wrap: wrap;">
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Framework:</span> Situation — Complication — Resolution — Recommendation</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Model:</span> GPT-4o (OpenAI)</div>
        <div style="font-size: 12px; color: #94a3b8;"><span style="color: #475569; font-weight: 500;">Output:</span> Board memo, downloadable as Markdown</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div style="padding: 20px 0 12px; border-bottom: 1px solid #1e293b; margin-bottom: 16px;"><div style="font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">Executive Brief Generator</div><div style="font-size: 15px; color: #f1f5f9; font-weight: 600; margin-top: 4px;">API Configuration</div></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;">OpenAI API Key</div>', unsafe_allow_html=True)
api_key = st.sidebar.text_input("", type="password", placeholder="sk-...", label_visibility="collapsed")
st.sidebar.markdown('<div style="font-size:11px;color:#475569;margin-top:4px;line-height:1.6;">Get your key at platform.openai.com. The key is never stored — used only for this session.</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
model = st.sidebar.selectbox("Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], label_visibility="visible")
temperature = st.sidebar.slider("Response Precision (lower = more precise)", 0.0, 1.0, 0.2, 0.05)
st.sidebar.markdown(f'<div style="background:#1e293b;border-radius:6px;padding:12px;margin-top:16px;"><div style="font-size:11px;color:#64748b;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Model Reference</div><div style="font-size:12px;color:#94a3b8;line-height:1.9;">GPT-4o: Best quality, higher cost<br>GPT-4-turbo: Fast, good quality<br>GPT-3.5-turbo: Fast, lower cost<br><br>Recommended: GPT-4o for board briefs.<br>Temperature 0.2 = precise, factual output.</div></div>', unsafe_allow_html=True)

if not api_key:
    st.markdown("""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:24px 28px;margin-bottom:24px;">
        <div style="font-size:11px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:12px;">Setup Required</div>
        <div style="font-size:15px;font-weight:600;color:#1e293b;margin-bottom:8px;">Enter your OpenAI API key to activate brief generation</div>
        <div style="font-size:14px;color:#64748b;line-height:1.7;margin-bottom:16px;">
            This page connects to OpenAI's GPT-4o model to generate board-ready executive briefs 
            from your financial model outputs. Your API key is used only within this session 
            and is never logged or stored.
        </div>
        <div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:6px;padding:16px 20px;">
            <div style="font-size:12px;font-weight:600;color:#374151;margin-bottom:8px;">How to get your API key:</div>
            <div style="font-size:13px;color:#64748b;line-height:1.8;">
                1. Go to <strong>platform.openai.com</strong><br>
                2. Sign in or create an account<br>
                3. Navigate to API Keys section<br>
                4. Click "Create new secret key"<br>
                5. Copy the key (starts with sk-...) and paste in the sidebar
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-header">Financial Model Inputs</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:13px;color:#64748b;margin-bottom:20px;">Enter outputs from your model runs on previous pages — or use the default values to generate a demonstration brief.</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div style="font-size:12px;font-weight:600;color:#374151;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid #f3f4f6;">Risk Engine — Monte Carlo</div>', unsafe_allow_html=True)
    mean_ebitda  = st.number_input("Mean EBITDA (Rs Cr/mo)", value=85.0, step=1.0)
    var_95       = st.number_input("VaR 95% (Rs Cr/mo)", value=-42.0, step=1.0)
    prob_loss    = st.number_input("Loss Probability (%)", value=8.3, step=0.1)
    std_ebitda   = st.number_input("EBITDA Std Dev (Rs Cr)", value=31.0, step=1.0)

with col2:
    st.markdown('<div style="font-size:12px;font-weight:600;color:#374151;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid #f3f4f6;">Capital Decisions — DCF</div>', unsafe_allow_html=True)
    npv          = st.number_input("NPV (Rs Cr)", value=342.0, step=1.0)
    irr          = st.number_input("IRR (%)", value=14.2, step=0.1)
    wacc         = st.number_input("WACC (%)", value=10.0, step=0.1)
    payback      = st.number_input("Payback Period (years)", value=6.4, step=0.1)

with col3:
    st.markdown('<div style="font-size:12px;font-weight:600;color:#374151;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid #f3f4f6;">Operations</div>', unsafe_allow_html=True)
    proc_saving  = st.number_input("Procurement Saving (Rs Cr/mo)", value=12.3, step=0.1)
    proc_pct     = st.number_input("Saving vs Spot (%)", value=4.2, step=0.1)
    ccc          = st.number_input("Cash Conv. Cycle (days)", value=72.0, step=1.0)
    wc_freed     = st.number_input("Working Capital Freed (Rs Cr)", value=94.0, step=1.0)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown('<div style="font-size:12px;font-weight:600;color:#374151;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid #f3f4f6;">Scenario P&L</div>', unsafe_allow_html=True)
    bear_ebitda  = st.number_input("Deep Stress EBITDA (Rs Cr/mo)", value=12.0, step=1.0)
    base_ebitda  = st.number_input("Base EBITDA (Rs Cr/mo)", value=85.0, step=1.0)
    bull_ebitda  = st.number_input("Supercycle EBITDA (Rs Cr/mo)", value=162.0, step=1.0)

with col5:
    st.markdown('<div style="font-size:12px;font-weight:600;color:#374151;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid #f3f4f6;">EBITDA Margins</div>', unsafe_allow_html=True)
    bear_margin  = st.number_input("Deep Stress Margin (%)", value=3.2, step=0.1)
    base_margin  = st.number_input("Base Margin (%)", value=17.0, step=0.1)
    bull_margin  = st.number_input("Supercycle Margin (%)", value=29.1, step=0.1)

with col6:
    st.markdown('<div style="font-size:12px;font-weight:600;color:#374151;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid #f3f4f6;">Context</div>', unsafe_allow_html=True)
    company      = st.text_input("Company Name", value="Tata Steel India")
    audience     = st.selectbox("Primary Audience", ["Board of Directors", "CFO", "CEO", "Strategy Committee", "Capital Allocation Committee"])
    focus        = st.selectbox("Strategic Focus", ["Cost Reduction and Procurement", "Capital Allocation", "Risk Management", "Working Capital Optimisation", "Full Financial Overview"])

st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
generate_btn = st.button("Generate Executive Brief", type="primary", use_container_width=False, key="ai_brief_generate")

if generate_btn:
    if not api_key:
        st.markdown("""
        <div style="background:#fef2f2;border-left:4px solid #dc2626;border-radius:6px;padding:14px 18px;margin-top:16px;">
            <div style="font-size:13px;font-weight:600;color:#b91c1c;">API key required</div>
            <div style="font-size:13px;color:#374151;margin-top:4px;">Enter your OpenAI API key in the sidebar to generate the brief. See setup instructions above.</div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    with st.spinner("Generating board-ready brief via GPT-4o..."):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            system_prompt = """You are a senior Bain and Company partner with 20 years of experience 
in steel sector strategy consulting. You write precise, quantified, board-ready executive briefs 
in the Situation-Complication-Resolution-Recommendation framework. Every analytical claim must 
be supported by a specific number from the data provided. Language is direct, formal, and 
consulting-grade. No filler sentences. No hedging language. No bullet points — continuous 
well-structured prose only."""

            irr_spread = round(irr - wacc, 1)
            irr_verdict = f"exceeds WACC by {irr_spread} percentage points" if irr > wacc else f"falls short of WACC by {abs(irr_spread)} percentage points"
            ebitda_swing = round(bull_ebitda - bear_ebitda, 1)

            user_prompt = f"""Write a board-level executive brief for {company} addressed to the {audience} on the topic of {focus}.

Use the Bain SCRR framework: Situation, Complication, Resolution, Recommendation.

Financial model data (all outputs from quantitative analysis):

RISK AND PROBABILITY:
- Monthly EBITDA expected value: Rs {mean_ebitda} Cr | Standard deviation: Rs {std_ebitda} Cr
- Value at Risk at 95% confidence (30-day): Rs {var_95} Cr
- Probability of EBITDA loss in any given month: {prob_loss}%

CAPITAL ALLOCATION:
- DCF Net Present Value: Rs {npv} Cr at {wacc}% WACC
- Internal Rate of Return: {irr}% — {irr_verdict}
- Investment payback period: {payback} years

PROCUREMENT AND OPERATIONS:
- LP optimisation monthly saving: Rs {proc_saving} Cr ({proc_pct}% vs all-spot strategy)
- Annualised procurement saving: Rs {round(proc_saving * 12, 1)} Cr
- Cash Conversion Cycle: {ccc} days (Tata Steel India benchmark: 62 days)
- Working capital released via payables optimisation: Rs {wc_freed} Cr

SCENARIO STRESS TEST:
- Deep Stress scenario EBITDA: Rs {bear_ebitda} Cr/month ({bear_margin}% margin)
- Base case EBITDA: Rs {base_ebitda} Cr/month ({base_margin}% margin)
- Supercycle EBITDA: Rs {bull_ebitda} Cr/month ({bull_margin}% margin)
- Full EBITDA range (Deep Stress to Supercycle): Rs {ebitda_swing} Cr

Requirements:
- Four paragraphs: Situation, Complication, Resolution, Recommendation
- Each paragraph 3-5 sentences of dense, quantified analysis
- Every claim must reference a specific number from the data above
- Final paragraph must include exactly three prioritised actions with estimated timelines and quantified impact
- End with one sentence labelled "Bottom Line" that a board member will remember
- Tone: Formal, direct, confident. Written for senior executives, not analysts.
- No bullet points. No lists. Continuous prose only.
- Do not use the word "leverage" or "synergy"
- Length: 320-380 words"""

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=800
            )

            brief_text = response.choices[0].message.content
            usage = response.usage

            st.markdown('<div class="section-header">Generated Executive Brief</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="brief-output">
                <div style="font-size:11px;font-weight:600;color:#9ca3af;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #f3f4f6;">
                    {audience.upper()} — {focus.upper()} — {company.upper()}
                </div>
                <div style="font-size:14px;color:#1e293b;line-height:1.95;white-space:pre-wrap;">{brief_text}</div>
                <div style="margin-top:24px;padding-top:16px;border-top:1px solid #f3f4f6;font-size:11px;color:#9ca3af;">
                    Generated by {model} — {usage.total_tokens} tokens ({usage.prompt_tokens} prompt + {usage.completion_tokens} completion) — Temperature {temperature}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
            col_d1, col_d2 = st.columns([1, 3])
            with col_d1:
                st.download_button(
                    label="Download Brief (.md)",
                    data=f"# Executive Brief — {company}\n\n**Audience:** {audience}\n**Focus:** {focus}\n\n---\n\n{brief_text}",
                    file_name=f"{company.replace(' ', '_')}_executive_brief.md",
                    mime="text/markdown",
                    key="download_brief"
                )

            st.markdown(f'<div class="footnote">Brief generated using {model} at temperature {temperature}. Total token consumption: {usage.total_tokens}. Estimated cost at standard GPT-4o pricing: approximately ${round(usage.prompt_tokens * 0.000005 + usage.completion_tokens * 0.000015, 4)}. All financial figures are model outputs — validate against management accounts before board submission.</div>', unsafe_allow_html=True)

        except Exception as e:
            error_msg = str(e)
            if "api_key" in error_msg.lower() or "authentication" in error_msg.lower() or "invalid" in error_msg.lower():
                st.markdown("""
                <div style="background:#fef2f2;border-left:4px solid #dc2626;border-radius:6px;padding:16px 20px;">
                    <div style="font-size:13px;font-weight:600;color:#b91c1c;">Invalid API Key</div>
                    <div style="font-size:13px;color:#374151;margin-top:4px;">The API key provided was not accepted by OpenAI. Check that the key is complete and has not expired. Keys start with "sk-" and are approximately 50 characters long.</div>
                </div>
                """, unsafe_allow_html=True)
            elif "quota" in error_msg.lower() or "billing" in error_msg.lower():
                st.markdown("""
                <div style="background:#fffbeb;border-left:4px solid #f59e0b;border-radius:6px;padding:16px 20px;">
                    <div style="font-size:13px;font-weight:600;color:#92400e;">Quota Exceeded</div>
                    <div style="font-size:13px;color:#374151;margin-top:4px;">Your OpenAI account has insufficient credits. Add billing at platform.openai.com/billing. GPT-4o costs approximately $0.005 per brief generation.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#fef2f2;border-left:4px solid #dc2626;border-radius:6px;padding:16px 20px;">
                    <div style="font-size:13px;font-weight:600;color:#b91c1c;">Generation Failed</div>
                    <div style="font-size:13px;color:#374151;margin-top:4px;">{error_msg}</div>
                </div>
                """, unsafe_allow_html=True)

else:
    if api_key:
        st.markdown("""
        <div style="padding: 48px 40px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 20px; text-align: center;">
            <div style="font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;">Ready to Generate</div>
            <h2 style="font-size: 20px; font-weight: 600; color: #1e293b; margin: 0 0 10px;">API key accepted — configure inputs above and click Generate</h2>
            <p style="font-size: 14px; color: #64748b; max-width: 560px; margin: 0 auto; line-height: 1.6;">The brief will follow Bain's SCRR framework in formal board-level prose — no bullet points, every claim quantified, ending with three prioritised actions and a bottom-line statement.</p>
        </div>
        """, unsafe_allow_html=True)