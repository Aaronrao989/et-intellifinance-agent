import sys
from loguru import logger

from workflows.financial_close_workflow import FinancialCloseWorkflow


def run_pipeline(input_path: str):
    """
    Runs the full financial workflow pipeline
    """

    logger.info("🚀 ET IntelliFinance Agent Started")

    workflow = FinancialCloseWorkflow()

    result = workflow.execute(input_path)

    if result.get("status") == "success":
        logger.success("🎉 Pipeline executed successfully")

        # Pretty print output
        print("\n===== FINAL OUTPUT =====\n")
        print(result["data"])

    else:
        logger.error("❌ Pipeline execution failed")
        print(result)

    return result


if __name__ == "__main__":
    """
    Usage:
    python app/main.py data/sample_transactions.csv
    """

    if len(sys.argv) < 2:
        print("❗ Please provide input file path")
        print("Example: python app/main.py data/sample_transactions.csv")
        sys.exit(1)

    input_file = sys.argv[1]

    run_pipeline(input_file)