from groq import Groq
from loguru import logger
from typing import Dict, Any

from app.config import settings


class QueryAgent:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    def answer(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Answer user queries based on financial analysis context
        """

        logger.info("💬 Query Agent: Processing user query...")

        try:
            prompt = self._build_prompt(query, context)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a financial analyst assistant. "
                            "Answer user queries based strictly on provided financial data. "
                            "Be clear, concise, and professional."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )

            answer_text = response.choices[0].message.content

            logger.info("✅ Query answered")

            return {
                "status": "success",
                "query": query,
                "answer": answer_text
            }

        except Exception as e:
            logger.error(f"❌ Query Agent Error: {str(e)}")

            return {
                "status": "error",
                "message": str(e)
            }

    def _build_prompt(self, query: str, context: Dict[str, Any]) -> str:
        """
        Build structured prompt using system outputs
        """

        finance = context.get("finance", {})
        compliance = context.get("compliance", {})

        prompt = f"""
        USER QUERY:
        {query}

        FINANCIAL DATA:
        Summary: {finance.get('summary')}
        Anomalies: {finance.get('anomalies')}
        Reconciliation: {finance.get('reconciliation')}

        COMPLIANCE:
        Is Compliant: {compliance.get('is_compliant')}
        Violations: {compliance.get('violations')}

        TASK:
        Answer the user query based ONLY on this data.
        Do not hallucinate.
        """

        return prompt.strip()