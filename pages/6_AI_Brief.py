# pages/6_AI_Brief.py
# ═══════════════════════════════════════════════════════
# GenAI Executive Brief Generator — GPT-4o powered
# The feature that makes this "hire on spot" material
# ═══════════════════════════════════════════════════════

import streamlit as st
import os

st.set_page_config(page_title="AI Executive Brief", layout="wide")

st.title("GenAI Executive Brief Generator")
st.caption("GPT-4o powered · Board-ready narrative · Bain SCRR framework")

# ── Check OpenAI key ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("API Configuration")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Get from platform.openai.com — needed for GPT-4o"
    )
    model = st.selectbox("Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"])
    temperature = st.slider("Creativity", 0.0, 1.0, 0.2,
                            help="Lower = more precise. Keep at 0.2 for board briefs.")

    st.markdown("---")
    st.markdown("""
    **What this does:**
    Takes your financial model outputs and generates
    a board-ready Bain SCRR brief using GPT-4o —
    the same structure Bain partners use in steel
    sector client presentations.
    """)

st.markdown("""
<div style="background:#e3f2fd; border-left:4px solid #1565c0;
            padding:16px; border-radius:8px; margin-bottom:20px;">
    <b>How to use this page:</b><br>
    1. Run your financial models on any previous page<br>
    2. Enter the key outputs below manually (or auto-populate after running models)<br>
    3. Click Generate → GPT-4o writes the board brief<br>
    4. Download as Markdown or copy to PowerPoint
</div>
""", unsafe_allow_html=True)

# ── Input Panel ───────────────────────────────────────────────────────────────
st.subheader("Financial Model Inputs")
st.caption("Enter outputs from your model runs — or leave defaults to demo")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Risk Engine (Monte Carlo)**")
    mean_ebitda   = st.number_input("Mean EBITDA (₹ Cr/mo)",  value=85.0)
    var_95        = st.number_input("VaR 95% (₹ Cr/mo)",      value=-42.0)
    prob_loss     = st.number_input("Loss Probability (%)",    value=8.3)
    std_ebitda    = st.number_input("EBITDA Std Dev (₹ Cr)",  value=31.0)

with col2:
    st.markdown("**Capital Decisions (DCF)**")
    npv           = st.number_input("NPV (₹ Cr)",             value=342.0)
    irr           = st.number_input("IRR (%)",                value=14.2)
    wacc          = st.number_input("WACC (%)",               value=10.0)
    payback       = st.number_input("Payback (years)",        value=6.4)

with col3:
    st.markdown("**Operations**")
    proc_saving   = st.number_input("Procurement Saving (₹ Cr/mo)", value=12.3)
    proc_pct      = st.number_input("Saving vs Spot (%)",            value=4.2)
    ccc           = st.number_input("Cash Conv. Cycle (days)",        value=72.0)
    wc_freed      = st.number_input("WC Freed (₹ Cr)",               value=94.0)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("**Scenario P&L**")
    bear_ebitda = st.number_input("Bear EBITDA (₹ Cr/mo)", value=38.0)
    base_ebitda = st.number_input("Base EBITDA (₹ Cr/mo)", value=85.0)
    bull_ebitda = st.number_input("Bull EBITDA (₹ Cr/mo)", value=142.0)

with col5:
    st.markdown("**EBITDA Margins**")
    bear_margin = st.number_input("Bear Margin (%)", value=9.2)
    base_margin = st.number_input("Base Margin (%)", value=17.0)
    bull_margin = st.number_input("Bull Margin (%)", value=24.1)

with col6:
    st.markdown("**Context**")
    company     = st.text_input("Company", value="Tata Steel India")
    audience    = st.selectbox("Audience", ["Board of Directors", "CFO", "CEO", "Strategy Committee"])
    focus       = st.selectbox("Strategic Focus", [
        "Cost Reduction", "Capital Allocation", 
        "Risk Management", "Procurement Optimization"
    ])

# ── Generate ──────────────────────────────────────────────────────────────────
st.markdown("---")
generate_btn = st.button("🚀 Generate Executive Brief (GPT-4o)", type="primary", use_container_width=True)

if generate_btn:
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
        st.stop()

    with st.spinner("GPT-4o writing board-ready brief..."):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            system_prompt = """You are a senior Bain & Company partner with 20 years of 
            experience in steel sector consulting. You write crisp, quantified, 
            board-ready executive briefs in the Situation-Complication-Resolution-
            Recommendation (SCRR) framework. Every claim must be supported by a number. 
            Language is confident, direct, and consulting-grade. No filler words."""

            user_prompt = f"""
Write a board-level executive brief for {company}'s {audience} on the topic of {focus}.
Use the Bain SCRR framework (Situation, Complication, Resolution, Recommendation).

Financial model outputs (from integrated analytics platform):

RISK:
- Monthly EBITDA mean: ₹{mean_ebitda} Cr | Std dev: ₹{std_ebitda} Cr
- VaR at 95% confidence (30-day): ₹{var_95} Cr
- Probability of EBITDA loss: {prob_loss}%

CAPITAL:
- DCF NPV: ₹{npv} Cr | IRR: {irr}% | WACC: {wacc}% | Payback: {payback} yrs
- Decision: {"INVEST — IRR exceeds WACC" if irr > wacc else "REJECT — IRR below WACC"}

OPERATIONS:
- LP procurement optimization saving: ₹{proc_saving} Cr/month ({proc_pct}% vs spot)
- Annual procurement saving: ₹{proc_saving * 12:.0f} Cr
- Cash Conversion Cycle: {ccc} days (industry benchmark: 65 days)
- Working capital freed via payables optimization: ₹{wc_freed} Cr

SCENARIOS:
- Bear: ₹{bear_ebitda} Cr EBITDA ({bear_margin}% margin)
- Base: ₹{base_ebitda} Cr EBITDA ({base_margin}% margin)
- Bull: ₹{bull_ebitda} Cr EBITDA ({bull_margin}% margin)
- EBITDA range: ₹{bear_ebitda} Cr to ₹{bull_ebitda} Cr

Requirements:
1. SITUATION: 2 sentences — current state of {company}'s cost structure
2. COMPLICATION: 2 sentences — what the data reveals as the core risk/opportunity
3. RESOLUTION: 3 sentences — what the analytics show is possible, with specific numbers
4. RECOMMENDATION: 3 prioritized actions with specific timelines and expected impact
5. End with a one-line "Bottom Line" that a board member would remember

Tone: Board of a Sensex-listed company. Direct. Quantified. No hedging.
Length: ~300 words.
"""

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=700
            )

            brief_text = response.choices[0].message.content

            # ── Display ───────────────────────────────────────────────────────
            st.markdown("---")
            st.subheader("GPT-4o Generated Executive Brief")

            st.markdown(f"""
            <div style="background:#fffbf0; border-left:5px solid #e65100;
                        padding:24px; border-radius:10px; font-family:Georgia,serif;
                        font-size:14px; line-height:1.9; box-shadow:0 2px 12px rgba(0,0,0,0.08);">
                {brief_text.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            # ── Download ──────────────────────────────────────────────────────
            st.markdown("")
            col_d1, col_d2, col_d3 = st.columns(3)
            with col_d1:
                st.download_button(
                    "📥 Download as Markdown",
                    brief_text,
                    file_name=f"{company.replace(' ','_')}_executive_brief.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col_d2:
                st.download_button(
                    "📄 Download as Text",
                    brief_text,
                    file_name=f"{company.replace(' ','_')}_executive_brief.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col_d3:
                st.info("💡 Copy to PowerPoint for board deck")

            # ── Token usage ───────────────────────────────────────────────────
            usage = response.usage
            st.caption(
                f"Tokens used: {usage.prompt_tokens} prompt + "
                f"{usage.completion_tokens} completion = {usage.total_tokens} total | "
                f"Model: {model}"
            )

        except Exception as e:
            st.error(f"API Error: {e}")
            st.info("Check your API key and ensure you have GPT-4o access.")

else:
    st.markdown("""
    <div style="text-align:center; padding:60px; color:#888;">
        <h2>🤖</h2>
        <p>Configure inputs above and click <b>Generate Executive Brief</b></p>
        <p style="font-size:13px;">GPT-4o will write a board-ready Bain SCRR brief from your model outputs</p>
    </div>
    """, unsafe_allow_html=True)