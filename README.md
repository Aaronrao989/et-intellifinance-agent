<div align="center">

# 💰 ET IntelliFinance Agent

### AI-Powered Financial Compliance, Risk & Insight System

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)
[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)

**🚀 Built for ET Gen AI Hackathon 2026 — Team Neuralink**

[Live Frontend](https://etfrontend.vercel.app/) • [Backend API Docs](https://et-intellifinance-agent-1.onrender.com/docs)

</div>

---

## 📌 Problem Statement

Modern financial workflows are manual, error-prone, and lack real-time intelligence:

| Pain Point | Impact |
|---|---|
| Manual reconciliation | 2–3 hours per cycle |
| No real-time compliance checks | Costly violations |
| No anomaly detection | Hidden financial risks |
| No actionable insights | Slower decision-making |

---

## 💡 Solution

**ET IntelliFinance Agent** is a domain-specific, multi-agent AI system that transforms how financial data is processed:

- ✅ **Automates** financial analysis and reconciliation
- ✅ **Enforces** compliance guardrails before insights are generated
- ✅ **Detects** anomalies and quantifies risk
- ✅ **Generates** Economic Times-style business insights
- ✅ **Enables** natural language interaction with your financial data

---

## 🏗️ System Architecture

```
Frontend (Vercel — HTML Dashboard)
              │
              ▼
   FastAPI Backend (Render)
              │
              ▼
    Multi-Agent AI System
    ┌─────────────────────────────┐
    │  ├── 📊 Finance Agent       │
    │  ├── ⚖️  Compliance Agent   │
    │  ├── 🧠 Explainer Agent     │
    │  ├── 🚨 Risk Agent          │
    │  ├── 📰 Insight Agent       │
    │  ├── 💬 Query Agent         │
    │  └── 🧾 Audit Agent         │
    └─────────────────────────────┘
```

---

## 🚀 Features

### 📊 Financial Analysis
- Transaction parsing and summary metrics
- Automated reconciliation

### ⚖️ Compliance Guardrails
- Rule-based validation engine
- Duplicate detection
- Negative transaction checks
- Threshold violation alerts

### 🧠 Explainable Compliance
- LLM-generated, human-readable explanations
- Audit-friendly outputs — no black boxes

### 🚨 Risk Intelligence
- **Risk Score** — 0 to 10 numeric scale
- **Risk Level** — LOW / MEDIUM / HIGH classification
- AI-generated narrative explanation per risk finding

### 📰 ET-Style Insights
- Business headline generation
- Market-style commentary
- Risk narrative summaries

### 💬 Natural Language Queries
Ask the Finance Agent questions like:
> *"Why is compliance failing?"*
> *"What are the top risks in this dataset?"*
> *"Summarize the anomalies detected."*

### 🧾 Full Audit Trail
- Complete input → output decision logging
- JSON-safe, fully traceable audit records

---

## ⚡ How It Works

```
1. Upload CSV  →  2. Finance Agent analyzes data
                        │
                  3. Compliance Agent validates rules
                        │
                  4. Risk Agent calculates risk score
                        │
                  5. Insight Agent generates ET-style insights
                        │
                  6. Query Agent enables user interaction
                        │
                  7. Audit Agent logs entire workflow
```

---

## 📊 Impact Model

| Metric | Before | After | Improvement |
|---|---|---|---|
| Reconciliation Time | 2–3 hours | < 5 seconds | **~95% reduction** |
| Compliance Checks | Manual | Automated | **Real-time** |
| Risk Visibility | None | Scored & Explained | **Full coverage** |
| Decision Speed | Slow | Instant insights | **Significant boost** |

---

## 🖥️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | FastAPI, Python, Pandas, Groq API (LLM), Gunicorn |
| **Frontend** | HTML, CSS, JavaScript |
| **Deployment** | Render (Backend), Vercel (Frontend) |

---

## 📂 Project Structure

```
et-intellifinance-agent/
│
├── app/
│   ├── api.py
│   └── config.py
│
├── agents/
│   ├── finance_agent.py
│   ├── compliance_agent.py
│   ├── compliance_explainer_agent.py
│   ├── risk_agent.py
│   ├── insight_agent.py
│   ├── query_agent.py
│   ├── audit_agent.py
│   └── orchestrator_agent.py
│
├── tools/
├── workflows/
├── ui/
│   └── index.html
├── data/
├── requirements.txt
└── start.sh
```

---

## 🎬 Demo Scenarios

### Case 1 — Non-Compliant Data
> Detects anomalies → Shows violations → Blocks insights until resolved

### Case 2 — Clean Data
> Passes compliance → Generates ET-style insights → Enables full query interaction

---

## 🧠 Key Innovations

| Innovation | Description |
|---|---|
| Multi-Agent Architecture | Specialized agents handle distinct tasks in a coordinated pipeline |
| Compliance-First AI | Insights are gated behind compliance — no hallucination risk |
| Explainable Intelligence | Every decision comes with a human-readable explanation |
| Interactive Finance Agent | Natural language queries on your own financial data |

---

## 🛠️ Local Setup & Run Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/et-intellifinance-agent.git
cd et-intellifinance-agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # Mac / Linux
venv\Scripts\activate        # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

### 5. Run the Backend (FastAPI)

```bash
uvicorn app.api:app --reload
```

API docs available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 6. Run the Frontend

**Option A — Recommended (local server):**

```bash
cd ui
python -m http.server 5500
```

Open in browser: [http://localhost:5500](http://localhost:5500)

**Option B — Quick open:**

```bash
open ui/index.html
```

### 7. Test the System

1. Upload a CSV file
2. Click **Run Analysis**
3. Review: Financial Summary · Compliance Status · Risk Score · Insights
4. Use **Ask Finance Agent** 💬 to query your data in natural language

> ⚠️ **Notes:**
> - Ensure the backend is running before launching the frontend
> - Update API URLs in `index.html` if using a custom host
> - Sample datasets are available in the `/data` folder

---

## ☁️ Deployment

### Backend — Render

```
Build Command:  pip install -r requirements.txt
Start Command:  bash start.sh
```

### Frontend — Vercel

```
Root Directory:  ui
Build Required:  No
```

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key |
| `GROQ_MODEL` | Model to use (e.g. `llama-3.1-8b-instant`) |

---

## 🏆 Why This Stands Out

- Real-world financial workflow — not a toy demo
- Compliance guardrails enforced before insights surface
- Fully explainable AI decisions, audit-ready
- End-to-end deployable system, production-ready

---

## 📌 Future Scope

- Real-time financial data feeds
- ERP system integration
- Multi-language support
- Advanced ML-based anomaly detection

---

<div align="center">

**👨‍💻 Team Neuralink** · Built with ❤️ for **ET Gen AI Hackathon 2026**

</div>