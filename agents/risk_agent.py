from groq import Groq
from loguru import logger
from typing import Dict, Any

from app.config import settings


class RiskAgent:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    def evaluate(self, finance_result: Dict[str, Any], compliance_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate risk score and generate explanation
        """

        logger.info("🚨 Calculating risk score...")

        try:
            # --- Rule-based scoring ---
            anomalies = len(finance_result.get("anomalies", []))
            duplicates = finance_result.get("reconciliation", {}).get("duplicate_count", 0)
            mismatches = finance_result.get("reconciliation", {}).get("mismatch_count", 0)
            violations = compliance_result.get("total_violations", 0)

            score = (
                anomalies * 1.5 +
                duplicates * 2 +
                mismatches * 1 +
                violations * 1
            )

            # Normalize to 0–10
            score = min(10, round(score, 2))

            # Risk level
            if score < 3:
                level = "LOW"
            elif score < 7:
                level = "MEDIUM"
            else:
                level = "HIGH"

            # --- LLM Explanation ---
            explanation = self._generate_explanation(score, level, finance_result, compliance_result)

            logger.info("✅ Risk evaluation complete")

            return {
                "status": "success",
                "risk_score": score,
                "risk_level": level,
                "explanation": explanation
            }

        except Exception as e:
            logger.error(f"❌ Risk Agent Error: {str(e)}")

            return {
                "status": "error",
                "message": str(e)
            }

    def _generate_explanation(self, score, level, finance_result, compliance_result):
        try:
            prompt = f"""
            Risk Score: {score}
            Risk Level: {level}

            Anomalies: {finance_result.get('anomalies')}
            Violations: {compliance_result.get('violations')}

            TASK:
            Explain why this risk level was assigned.
            Highlight key contributing factors.
            Keep it concise and professional.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial risk analyst."
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )

            return response.choices[0].message.content

        except Exception:
            return "Risk explanation unavailable"