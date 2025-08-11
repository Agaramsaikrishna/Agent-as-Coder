def create_prompt(state) -> str:
    lines = [
        "Write a Python function `parse(pdf_path: str) -> pd.DataFrame` that extracts transactions from a bank statement PDF.",
        "Rules:",
        "- Use ONLY: pandas, pdfplumber, re, numpy.",
        "- Output must EXACTLY match the provided CSV schema & values.",
        f"- Expected columns: {state['csv_columns']}",
        f"- Expected rows: {state['csv_shape'][0]}",
        "- Strip whitespace from all string columns.",
        "- Format all date columns as DD-MM-YYYY.",
        "- Convert numeric columns to float.",
        "",
        "Note: Output only valid and complete Python code with proper indentation.",
        "Don't include markdown formatting like ```python.",
        "**CSV sample:**"
    ]
    for r in state['csv_sample']:
        lines.append("  - " + ", ".join(f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}" for k, v in r.items()))
    if state['pdf_sample']:
        lines.append(f"\n**PDF sample text:**\n{state['pdf_sample']}")
    if state['feedback_msg']:
        lines.append(f"\n**Previous test feedback:**\n{state['feedback_msg']}")
        lines.append("Fix these issues without changing the output format.")
    lines.append("\nReturn ONLY the Python code for the function, no markdown, no explanations.")
    return "\n".join(lines)
