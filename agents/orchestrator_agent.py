from loguru import logger
from typing import Dict, Any

# Import agents
from agents.finance_agent import FinanceAgent
from agents.compliance_agent import ComplianceAgent
from agents.insight_agent import InsightAgent
from agents.audit_agent import AuditAgent
from agents.query_agent import QueryAgent
from agents.compliance_explainer_agent import ComplianceExplainerAgent
from agents.risk_agent import RiskAgent  # 🔥 NEW


class OrchestratorAgent:
    def __init__(self):
        self.finance_agent = FinanceAgent()
        self.compliance_agent = ComplianceAgent()
        self.insight_agent = InsightAgent()
        self.audit_agent = AuditAgent()
        self.query_agent = QueryAgent()
        self.compliance_explainer = ComplianceExplainerAgent()
        self.risk_agent = RiskAgent()  # 🔥 NEW

    def run_financial_workflow(self, data) -> Dict[str, Any]:
        """
        Main workflow:
        1. Financial Analysis
        2. Compliance Check
        3. Compliance Explanation
        4. Risk Evaluation (NEW)
        5. Insight Generation
        6. Audit Logging
        """

        logger.info("🚀 Starting Financial Workflow")

        workflow_log = {}

        try:
            # STEP 1: Financial Analysis
            logger.info("📊 Running Finance Analysis...")
            finance_result = self.finance_agent.analyze(data)
            workflow_log["finance"] = finance_result

            # STEP 2: Compliance Check
            logger.info("⚖️ Running Compliance Checks...")
            compliance_result = self.compliance_agent.validate(finance_result)
            workflow_log["compliance"] = compliance_result

            # STEP 3: Compliance Explanation
            logger.info("🧠 Generating Compliance Explanation...")
            compliance_explanation = self.compliance_explainer.explain(compliance_result)
            workflow_log["compliance_explanation"] = compliance_explanation

            # 🔥 STEP 4: Risk Evaluation (NEW)
            logger.info("🚨 Evaluating Risk...")
            risk_result = self.risk_agent.evaluate(finance_result, compliance_result)
            workflow_log["risk"] = risk_result

            # STEP 5: Insight Generation
            insights = None
            if compliance_result.get("is_compliant", False):
                logger.info("🧠 Generating Insights...")
                insights = self.insight_agent.generate(finance_result)
                workflow_log["insights"] = insights
            else:
                logger.warning("⚠️ Skipping insights due to compliance issues")

            # STEP 6: Audit Logging
            logger.info("🧾 Logging Audit Trail...")
            audit_record = self.audit_agent.log(
                input_data=data,
                finance_result=finance_result,
                compliance_result=compliance_result,
                insights=insights,
            )

            workflow_log["audit"] = audit_record

            logger.success("✅ Workflow Completed Successfully")

            return {
                "status": "success",
                "data": workflow_log
            }

        except Exception as e:
            logger.error(f"❌ Workflow Failed: {str(e)}")

            self.audit_agent.log_error(str(e))

            return {
                "status": "error",
                "message": str(e)
            }

    # 🔥 Query Handling
    def answer_query(self, query: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Answer user queries based on workflow results
        """

        logger.info("💬 Handling user query...")

        try:
            response = self.query_agent.answer(query, workflow_data)
            return response

        except Exception as e:
            logger.error(f"❌ Query Handling Error: {str(e)}")

            return {
                "status": "error",
                "message": str(e)
            }