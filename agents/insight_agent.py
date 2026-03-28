from groq import Groq
from loguru import logger
from typing import Dict, Any

from app.config import settings


class InsightAgent:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    def generate(self, finance_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates ET-style financial insights using LLM
        """

        logger.info("🧠 Insight Agent: Generating insights...")

        try:
            summary = finance_result.get("summary", {})
            anomalies = finance_result.get("anomalies", [])
            reconciliation = finance_result.get("reconciliation", {})

            prompt = self._build_prompt(summary, anomalies, reconciliation)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a financial analyst writing insights for Economic Times. "
                            "Provide professional, concise, and business-relevant insights."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
            )

            output_text = response.choices[0].message.content

            logger.info("✅ Insights generated")

            return {
                "status": "success",
                "insights": output_text
            }

        except Exception as e:
            logger.error(f"❌ Insight Agent Error: {str(e)}")

            return {
                "status": "error",
                "message": str(e)
            }

    def _build_prompt(self, summary, anomalies, reconciliation) -> str:
        """
        Builds structured prompt for ET-style insights
        """

        prompt = f"""
        Financial Summary:
        - Total Transactions: {summary.get('total_transactions')}
        - Total Amount: {summary.get('total_amount')}
        - Average Transaction: {summary.get('average_transaction')}

        Anomalies Detected: {len(anomalies)}

        Duplicate Transactions: {reconciliation.get('duplicate_count')}
        Mismatched Transactions: {reconciliation.get('mismatch_count')}

        TASK:
        1. Write a headline like Economic Times
        2. Provide 2-3 key business insights
        3. Highlight risks (if any)
        4. Keep it concise and professional
        """

        return prompt.strip()