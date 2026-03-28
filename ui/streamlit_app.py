import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from loguru import logger

from workflows.financial_close_workflow import FinancialCloseWorkflow
from agents.orchestrator_agent import OrchestratorAgent


# ─────────────────────────────────────────────
# UI ENHANCEMENT: Page config with ET branding
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ET IntelliFinance Agent",
    page_icon="💰",
    layout="wide"
)

# ─────────────────────────────────────────────
# UI ENHANCEMENT: Global CSS — ET news-style
# Palette: #D0021B (ET Red), #1A1A1A (ink black),
#          #F5F5F5 (off-white), #666 (secondary grey)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ─────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+4:wght@400;600&family=DM+Sans:wght@400;500;600&display=swap');

/* ── Root Variables ───────────────────────── */
:root {
    --et-red:        #D0021B;
    --et-red-dark:   #A50016;
    --et-ink:        #1A1A1A;
    --et-body:       #2D2D2D;
    --et-muted:      #666666;
    --et-border:     #E0E0E0;
    --et-bg:         #F7F7F5;
    --et-card:       #FFFFFF;
    --et-accent-bg:  #FFF5F5;
    --radius:        4px;
    --shadow-sm:     0 1px 4px rgba(0,0,0,.08);
    --shadow-md:     0 4px 16px rgba(0,0,0,.10);
}

/* ── Base Reset ───────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--et-body);
    background-color: var(--et-bg) !important;
}

/* ── App Container ────────────────────────── */
.main .block-container {
    max-width: 1200px;
    padding: 0 2rem 4rem;
    background: var(--et-bg);
}

/* ── Masthead / Header ────────────────────── */
.et-masthead {
    background: var(--et-ink);
    color: #FFFFFF;
    padding: 0;
    margin: -1rem -2rem 0;
    border-bottom: 3px solid var(--et-red);
}
.et-masthead-inner {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    align-items: stretch;
    justify-content: space-between;
}
.et-logo-block {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 0;
    border-right: 1px solid rgba(255,255,255,.12);
    padding-right: 28px;
}
.et-logo-mark {
    width: 44px;
    height: 44px;
    background: var(--et-red);
    border-radius: 3px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 22px;
    color: #fff;
    letter-spacing: -1px;
    flex-shrink: 0;
}
.et-title-group h1 {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 900;
    color: #FFFFFF;
    margin: 0;
    letter-spacing: -0.3px;
    line-height: 1.1;
}
.et-title-group span {
    font-size: 11px;
    color: rgba(255,255,255,.55);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 500;
}
.et-badge {
    display: flex;
    align-items: center;
    padding-left: 28px;
    gap: 8px;
}
.et-hackathon-pill {
    background: var(--et-red);
    color: #fff;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 2px;
}
.et-year-tag {
    font-size: 11px;
    color: rgba(255,255,255,.4);
    font-weight: 500;
    letter-spacing: 0.5px;
}

/* ── Section Divider / Red Rule ──────────── */
.et-rule {
    height: 3px;
    background: var(--et-red);
    margin: 2rem 0 1.5rem;
    border: none;
}
.et-rule-thin {
    height: 1px;
    background: var(--et-border);
    margin: 1.5rem 0;
    border: none;
}

/* ── Section Heading (like ET section labels) */
.et-section-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
}
.et-section-label .et-section-tag {
    background: var(--et-red);
    color: #fff;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 2px;
}
.et-section-label h2 {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--et-ink);
    margin: 0;
    line-height: 1.2;
}

/* ── Cards ────────────────────────────────── */
.et-card {
    background: var(--et-card);
    border: 1px solid var(--et-border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1rem;
}
.et-card-accent {
    border-left: 3px solid var(--et-red);
}

/* ── Upload Zone ──────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--et-card) !important;
    border: 2px dashed var(--et-border) !important;
    border-radius: var(--radius) !important;
    padding: 1.5rem !important;
    transition: border-color .2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--et-red) !important;
}
[data-testid="stFileUploaderDropzone"] label {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--et-muted) !important;
}

/* ── Buttons ──────────────────────────────── */
[data-testid="stButton"] > button {
    background: var(--et-red) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.3px !important;
    padding: 10px 24px !important;
    transition: background .2s, transform .1s !important;
    box-shadow: 0 2px 6px rgba(208,2,27,.25) !important;
}
[data-testid="stButton"] > button:hover {
    background: var(--et-red-dark) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(208,2,27,.3) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Text Input ───────────────────────────── */
[data-testid="stTextInput"] input {
    border: 1px solid var(--et-border) !important;
    border-radius: var(--radius) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    background: var(--et-card) !important;
    color: var(--et-body) !important;
    transition: border-color .2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--et-red) !important;
    box-shadow: 0 0 0 2px rgba(208,2,27,.12) !important;
}

/* ── Dataframe ────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--et-border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
}

/* ── Metric Cards ─────────────────────────── */
[data-testid="stMetric"] {
    background: var(--et-card) !important;
    border: 1px solid var(--et-border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.25rem !important;
    box-shadow: var(--shadow-sm) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    color: var(--et-muted) !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    color: var(--et-ink) !important;
}

/* ── Alert / Info ─────────────────────────── */
[data-testid="stInfo"],
.stInfo {
    background: #EEF5FF !important;
    border-left: 3px solid #2563EB !important;
    border-radius: var(--radius) !important;
    font-family: 'Source Serif 4', serif !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    color: var(--et-body) !important;
}
[data-testid="stWarning"],
.stWarning {
    background: #FFFBEB !important;
    border-left: 3px solid #D97706 !important;
    border-radius: var(--radius) !important;
}
[data-testid="stSuccess"],
.stSuccess {
    background: #F0FDF4 !important;
    border-left: 3px solid #16A34A !important;
    border-radius: var(--radius) !important;
}
[data-testid="stError"],
.stError {
    background: #FFF5F5 !important;
    border-left: 3px solid var(--et-red) !important;
    border-radius: var(--radius) !important;
}

/* ── Spinner ──────────────────────────────── */
[data-testid="stSpinner"] {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--et-muted) !important;
}

/* ── Subheader overrides ──────────────────── */
h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--et-ink) !important;
}

/* ── JSON display ─────────────────────────── */
[data-testid="stJson"] {
    background: #FAFAFA !important;
    border: 1px solid var(--et-border) !important;
    border-radius: var(--radius) !important;
    font-size: 13px !important;
}

/* ── Sidebar ──────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--et-ink) !important;
}

/* ── Horizontal Rule ──────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--et-border) !important;
    margin: 2rem 0 !important;
}

/* ── Footer strip ─────────────────────────── */
.et-footer {
    background: var(--et-ink);
    color: rgba(255,255,255,.4);
    font-size: 11px;
    letter-spacing: 0.5px;
    text-align: center;
    padding: 12px 2rem;
    margin: 3rem -2rem -4rem;
    border-top: 3px solid var(--et-red);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# UI ENHANCEMENT: ET-style Masthead
# ─────────────────────────────────────────────
st.markdown("""
<div class="et-masthead">
    <div class="et-masthead-inner">
        <div class="et-logo-block">
            <div class="et-logo-mark">ET</div>
            <div class="et-title-group">
                <h1>IntelliFinance Agent</h1>
                <span>AI-powered Financial Compliance &amp; Insight System</span>
            </div>
        </div>
        <div class="et-badge">
            <span class="et-hackathon-pill">ET AI Hackathon 2026</span>
            <span class="et-year-tag">The Economic Times</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# UI ENHANCEMENT: Red rule beneath masthead
# ─────────────────────────────────────────────
st.markdown('<hr class="et-rule" style="margin-top:0">', unsafe_allow_html=True)


# ── Session state (UNCHANGED) ─────────────────
if "workflow_data" not in st.session_state:
    st.session_state.workflow_data = None


# ─────────────────────────────────────────────
# UI ENHANCEMENT: Upload section with ET label
# ─────────────────────────────────────────────
st.markdown("""
<div class="et-section-label">
    <span class="et-section-tag">Step 1</span>
    <h2>Upload Transaction Data</h2>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 Upload Transaction CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # ─────────────────────────────────────
        # UI ENHANCEMENT: Section label for data
        # ─────────────────────────────────────
        st.markdown('<hr class="et-rule-thin">', unsafe_allow_html=True)
        st.markdown("""
        <div class="et-section-label">
            <span class="et-section-tag">Preview</span>
            <h2>Uploaded Data</h2>
        </div>
        """, unsafe_allow_html=True)

        # UI ENHANCEMENT: Card wrapper for dataframe
        st.markdown('<div class="et-card">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ─────────────────────────────────────
        # UI ENHANCEMENT: CTA button row
        # ─────────────────────────────────────
        st.markdown('<hr class="et-rule-thin">', unsafe_allow_html=True)
        col_btn, _ = st.columns([2, 8])
        with col_btn:
            run_clicked = st.button("🚀 Run Analysis")

        if run_clicked:
            with st.spinner("Running financial analysis…"):

                # ── UNCHANGED LOGIC ──────────
                workflow = FinancialCloseWorkflow()
                result = workflow.execute(df)

                if result.get("status") == "success":
                    data = result["data"]
                    st.session_state.workflow_data = data

                    # ─────────────────────────
                    # UI ENHANCEMENT: Analysis results header
                    # ─────────────────────────
                    st.markdown('<hr class="et-rule">', unsafe_allow_html=True)
                    st.markdown("""
                    <div class="et-section-label">
                        <span class="et-section-tag">Analysis</span>
                        <h2>Results &amp; Insights</h2>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── Finance Summary ───────
                    st.markdown("""
                    <div class="et-section-label" style="margin-top:1.5rem">
                        <span class="et-section-tag">Finance</span>
                        <h2>Financial Summary</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="et-card et-card-accent">', unsafe_allow_html=True)
                    st.json(data.get("finance", {}).get("summary", {}))
                    st.markdown('</div>', unsafe_allow_html=True)

                    # ── Reconciliation ────────
                    st.markdown("""
                    <div class="et-section-label">
                        <span class="et-section-tag">Audit</span>
                        <h2>Reconciliation</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="et-card et-card-accent">', unsafe_allow_html=True)
                    st.json(data.get("finance", {}).get("reconciliation", {}))
                    st.markdown('</div>', unsafe_allow_html=True)

                    # ── Anomalies ─────────────
                    st.markdown("""
                    <div class="et-section-label">
                        <span class="et-section-tag" style="background:#B45309">Alerts</span>
                        <h2>Anomalies Detected</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="et-card" style="border-left:3px solid #D97706">', unsafe_allow_html=True)
                    st.json(data.get("finance", {}).get("anomalies", []))
                    st.markdown('</div>', unsafe_allow_html=True)

                    # ── Compliance ────────────
                    st.markdown("""
                    <div class="et-section-label">
                        <span class="et-section-tag">Compliance</span>
                        <h2>Compliance Result</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    compliance = data.get("compliance", {})
                    st.markdown('<div class="et-card et-card-accent">', unsafe_allow_html=True)
                    st.json(compliance)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # ── Compliance Explanation ─
                    st.markdown("""
                    <div class="et-section-label">
                        <span class="et-section-tag">AI</span>
                        <h2>Compliance Explanation</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    explanation = data.get("compliance_explanation", {}).get("explanation")
                    if explanation:
                        st.info(explanation)
                    else:
                        st.warning("No explanation available")

                    # ─────────────────────────
                    # RISK SECTION (UNCHANGED LOGIC)
                    # ─────────────────────────
                    st.markdown('<hr class="et-rule-thin">', unsafe_allow_html=True)
                    st.markdown("""
                    <div class="et-section-label">
                        <span class="et-section-tag" style="background:#D0021B">Risk</span>
                        <h2>Risk Assessment</h2>
                    </div>
                    """, unsafe_allow_html=True)

                    risk = data.get("risk", {})

                    if risk:
                        score = risk.get("risk_score", 0)
                        level = risk.get("risk_level", "UNKNOWN")
                        risk_explanation = risk.get("explanation", "")

                        # ── Risk Score / Level ─
                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric("Risk Score", f"{score}/10")

                        with col2:
                            if level == "LOW":
                                st.success(f"Risk Level: {level}")
                            elif level == "MEDIUM":
                                st.warning(f"Risk Level: {level}")
                            else:
                                st.error(f"Risk Level: {level}")

                        # ── Risk Explanation ───
                        st.markdown("""
                        <div class="et-section-label" style="margin-top:1rem">
                            <span class="et-section-tag">AI</span>
                            <h2>Risk Explanation</h2>
                        </div>
                        """, unsafe_allow_html=True)
                        if risk_explanation:
                            st.info(risk_explanation)
                        else:
                            st.warning("No risk explanation available")

                    # ── ET Insights ───────────
                    if compliance.get("is_compliant"):
                        st.markdown('<hr class="et-rule-thin">', unsafe_allow_html=True)
                        st.markdown("""
                        <div class="et-section-label">
                            <span class="et-section-tag">ET</span>
                            <h2>ET Insights</h2>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown('<div class="et-card" style="border-left:3px solid #16A34A">', unsafe_allow_html=True)
                        insights = data.get("insights", {}).get("insights", "")
                        st.write(insights)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.warning("Insights skipped due to compliance violations")

                    # ── Success Banner ─────────
                    st.markdown('<hr class="et-rule-thin">', unsafe_allow_html=True)
                    st.success("✅ Analysis Completed")

                else:
                    st.error("❌ Analysis Failed")
                    st.write(result)

    except Exception as e:
        logger.error(f"UI Error: {str(e)}")
        st.error(f"Error: {str(e)}")

else:
    # ─────────────────────────────────────────
    # UI ENHANCEMENT: Empty state hint
    # ─────────────────────────────────────────
    st.markdown("""
    <div class="et-card" style="text-align:center; padding:2.5rem; color:#999; border-style:dashed">
        <p style="font-size:2rem; margin:0">📂</p>
        <p style="font-family:'DM Sans',sans-serif; margin:.5rem 0 0; font-size:15px">
            Upload a CSV file to begin analysis
        </p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ASK FINANCE SECTION (UNCHANGED LOGIC)
# UI ENHANCEMENT: ET-style card + section label
# ─────────────────────────────────────────────
if st.session_state.workflow_data:
    st.markdown('<hr class="et-rule">', unsafe_allow_html=True)
    st.markdown("""
    <div class="et-section-label">
        <span class="et-section-tag">Step 2</span>
        <h2>Ask the Finance Agent</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="et-card et-card-accent">', unsafe_allow_html=True)

    user_query = st.text_input("Ask a question about the analysis:",
                               placeholder="e.g. What are the top anomalies and their impact?")

    col_ask, _ = st.columns([2, 8])
    with col_ask:
        ask_clicked = st.button("🧠 Get Answer")

    st.markdown('</div>', unsafe_allow_html=True)

    if ask_clicked:
        if user_query.strip() == "":
            st.warning("Please enter a query")
        else:
            with st.spinner("Analysing your question…"):

                # ── UNCHANGED LOGIC ──────────
                orchestrator = OrchestratorAgent()
                response = orchestrator.answer_query(
                    user_query,
                    st.session_state.workflow_data
                )

                if response.get("status") == "success":
                    st.success("✅ Answer")
                    # UI ENHANCEMENT: Card wrapper for answer
                    st.markdown('<div class="et-card" style="border-left:3px solid #2563EB">', unsafe_allow_html=True)
                    st.write(response.get("answer"))
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("❌ Failed to generate answer")
                    st.write(response)


# ─────────────────────────────────────────────
# UI ENHANCEMENT: Footer
# ─────────────────────────────────────────────
st.markdown("""
<div class="et-footer">
    ET IntelliFinance Agent &nbsp;·&nbsp; ET AI Hackathon 2026 &nbsp;·&nbsp; The Economic Times
</div>
""", unsafe_allow_html=True)