from groq import Groq
from loguru import logger
from typing import Dict, Any

from app.config import settings


class ComplianceExplainerAgent:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    def explain(self, compliance_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate human-readable explanation of compliance result
        """

        logger.info("⚖️ Generating compliance explanation...")

        try:
            prompt = self._build_prompt(compliance_result)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a financial compliance expert. "
                            "Explain compliance results in simple, professional language. "
                            "Highlight key violations, risks, and overall status."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )

            explanation = response.choices[0].message.content

            logger.info("✅ Compliance explanation generated")

            return {
                "status": "success",
                "explanation": explanation
            }

        except Exception as e:
            logger.error(f"❌ Compliance Explainer Error: {str(e)}")

            return {
                "status": "error",
                "message": str(e)
            }

    def _build_prompt(self, compliance_result: Dict[str, Any]) -> str:
        return f"""
        Compliance Status: {compliance_result.get('is_compliant')}
        Total Violations: {compliance_result.get('total_violations')}

        Violations:
        {compliance_result.get('violations')}

        TASK:
        1. Explain whether the dataset is compliant or not
        2. Summarize key issues (if any)
        3. Highlight risks
        4. Keep it concise and professional
        """