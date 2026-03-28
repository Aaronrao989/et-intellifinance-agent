import os
import json
from datetime import datetime
from loguru import logger
from typing import Dict, Any

from app.config import settings


class AuditAgent:
    def __init__(self):
        self.log_file = os.path.join(settings.LOG_DIR, "audit_log.json")
        self.error_file = os.path.join(settings.LOG_DIR, "error_log.json")

    def log(
        self,
        input_data: Any,
        finance_result: Dict[str, Any],
        compliance_result: Dict[str, Any],
        insights: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Logs full audit trail:
        - Input
        - Decisions
        - Outputs
        """

        logger.info("🧾 Writing audit log...")

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "input_summary": self._summarize_input(input_data),
            "finance_result": finance_result,
            "compliance_result": compliance_result,
            "insights": insights,
        }

        try:
            existing_logs = self._read_json(self.log_file)
            existing_logs.append(record)
            self._write_json(self.log_file, existing_logs)

            logger.info("✅ Audit log saved")

            return record

        except Exception as e:
            logger.error(f"❌ Audit Logging Error: {str(e)}")
            return {"status": "error", "message": str(e)}

    def log_error(self, error_message: str):
        """
        Logs system errors separately
        """

        logger.warning("⚠️ Logging error...")

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "error": error_message,
        }

        try:
            existing_logs = self._read_json(self.error_file)
            existing_logs.append(record)
            self._write_json(self.error_file, existing_logs)

        except Exception as e:
            logger.error(f"❌ Error Logging Failed: {str(e)}")

    def _read_json(self, path: str):
        if not os.path.exists(path):
            return []

        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _write_json(self, path: str, data):
        """
        Safe JSON writer that converts non-serializable objects
        like pandas.Timestamp into strings
        """

        def default_serializer(obj):
            # Handle datetime-like objects
            if hasattr(obj, "isoformat"):
                return obj.isoformat()

            # Fallback: convert everything else to string
            return str(obj)

        with open(path, "w") as f:
            json.dump(data, f, indent=4, default=default_serializer)

    def _summarize_input(self, data: Any) -> Dict[str, Any]:
        """
        Avoid logging full raw data (for performance + clarity)
        """

        try:
            if hasattr(data, "shape"):  # pandas DataFrame
                return {
                    "type": "DataFrame",
                    "rows": data.shape[0],
                    "columns": data.shape[1],
                }

            elif isinstance(data, dict):
                return {
                    "type": "dict",
                    "keys": list(data.keys())
                }

            elif isinstance(data, str):
                return {
                    "type": "file_path",
                    "path": data
                }

            return {"type": "unknown"}

        except Exception:
            return {"type": "unreadable"}