from loguru import logger
from typing import Any, Dict

from agents.orchestrator_agent import OrchestratorAgent


class FinancialCloseWorkflow:
    """
    High-level workflow wrapper for financial close process
    """

    def __init__(self):
        self.orchestrator = OrchestratorAgent()

    def execute(self, data: Any) -> Dict:
        """
        Runs the full financial close workflow
        """

        logger.info("🏁 Starting Financial Close Workflow...")

        try:
            result = self.orchestrator.run_financial_workflow(data)

            if result.get("status") == "success":
                logger.success("✅ Financial Close Workflow Completed")
            else:
                logger.error("❌ Financial Close Workflow Failed")

            return result

        except Exception as e:
            logger.error(f"❌ Workflow Execution Error: {str(e)}")

            return {
                "status": "error",
                "message": str(e)
            }