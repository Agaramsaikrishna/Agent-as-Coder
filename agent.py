"""
agent.py

Entry point script for the Agent-as-Coder system that automatically generates
and tests a Python parser for bank statement PDFs.

Usage:
    python agent.py --target <bank_name>

Arguments:
    --target: The bank name to process (e.g., "icici", "sbi"). This determines
              the input PDF and CSV files under the `data/<bank>/` directory.

Functionality:
- Validates presence of the required PDF and CSV files.
- Loads CSV schema and sample data for test verification.
- Extracts sample text from the PDF for prompt generation.
- Initializes the agent state with all necessary info.
- Builds and runs the LangGraph-based agent to generate, test, and refine
  the custom parser code.
- Prints final status and saves the generated parser under
  `custom_parsers/<bank>_parser.py`.

This script requires the following modules in the project structure:
- utils.helpers: For CSV analysis and PDF sample extraction.
- src.state: Contains AgentState TypedDict definition.
- src.graph: Constructs and returns the compiled LangGraph agent.

Example:
    python agent.py --target icici

"""

import argparse, os, sys
from utils.helpers import analyze_csv, extract_pdf_sample
from src.state import AgentState
from src.graph import build_graph

def main():
    p = argparse.ArgumentParser(description="Agent-as-Coder for PDF bank statement parsing.")
    p.add_argument("--target", required=True, help="Bank name (e.g., icici, sbi)")
    args = p.parse_args()

    bank = args.target.lower()
    pdf = f"data/{bank}/{bank}_sample.pdf"
    csvp = f"data/{bank}/result.csv"

    if not os.path.exists(pdf) or not os.path.exists(csvp):
        print(f"Error: Missing {pdf} or {csvp}")
        sys.exit(1)

    info = analyze_csv(csvp)
    state: AgentState = {
        "bank": bank,
        "pdf_path": pdf,
        "csv_path": csvp,
        "code": "",
        "iterations": 0,
        "success": False,
        "error_msg": "",
        "feedback_msg": "",
        "csv_columns": info["columns"],
        "csv_shape": info["shape"],
        "csv_sample": info["sample"],
        "pdf_sample": extract_pdf_sample(pdf),
    }

    agent = build_graph()
    print(f"Starting agent for bank: {bank}...\n")
    result = agent.invoke(state)

    print(f"Parser saved to custom_parsers/{bank}_parser.py")
    print(f"\n✅ FINAL: SUCCESS in {result['iterations']} iterations")

if __name__ == "__main__":
    main()
