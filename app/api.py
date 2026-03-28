from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

from workflows.financial_close_workflow import FinancialCloseWorkflow
from agents.orchestrator_agent import OrchestratorAgent


app = FastAPI(
    title="ET IntelliFinance Agent API",
    description="AI-powered financial compliance & insight system",
    version="1.0.0"
)

# 🔥 Enable CORS (IMPORTANT for HTML frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for hackathon (allow all)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow = FinancialCloseWorkflow()
orchestrator = OrchestratorAgent()


@app.get("/")
def root():
    return {"message": "ET IntelliFinance Agent API is running 🚀"}


# =========================
# 📊 ANALYZE ENDPOINT
# =========================
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        result = workflow.execute(df)

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# =========================
# 💬 QUERY ENDPOINT
# =========================
@app.post("/query")
def query_endpoint(payload: dict):
    try:
        query = payload.get("query")
        data = payload.get("data")

        if not query or not data:
            return {
                "status": "error",
                "message": "Query or data missing"
            }

        response = orchestrator.answer_query(query, data)

        return response

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }