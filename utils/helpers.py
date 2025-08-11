import pandas as pd
import pdfplumber
import re, traceback, importlib.util

def load_parser_module(bank: str):
    """
    Dynamically imports a custom parser module for the specified bank.

    This function loads a bank-specific parser module located at 
    'custom_parsers/{bank}_parser.py' using importlib's module loading capabilities.

    Args:
        bank (str): Name of the bank identifier (must match the base name of 
                    the parser module file without the '_parser.py' suffix)

    Returns:
        module: Imported Python module object containing the bank's parser implementation

    Example:
        >>> parser = load_parser_module("chase")
        >>> parser.parse(...)  # Would call the parse function from 'chase_parser.py'
    """
    spec = importlib.util.spec_from_file_location(f"{bank}_parser", f"custom_parsers/{bank}_parser.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def analyze_csv(csv_path: str):
    """
    Analyzes a CSV file and returns metadata and a sample.

    Args:
        csv_path (str): File system path to the CSV file

    Returns:
        dict: Dictionary containing:
              - "columns": List of column names
              - "shape": Tuple of (rows, columns)
              - "sample": First 3 rows as list of dictionaries

    Example:
        >>> analyze_csv('data/sample.csv')
        {
            "columns": ['Date', 'Amount', 'Description'],
            "shape": (1000, 3),
            "sample": [
                {'Date': '2023-09-01', 'Amount': '45.00', ...}
            ]
        }
    """
    df = pd.read_csv(csv_path)
    return {"columns": list(df.columns), "shape": df.shape, "sample": df.head(3).to_dict("records")}

def extract_pdf_sample(pdf_path: str):
    """
    Extracts up to 5 date-containing lines from a PDF's first two pages.

    This function:
    1. Opens the PDF file
    2. Scans page 0-1 for lines containing DD-MM-YYYY or DD/MM/YYYY date formats
    3. Returns the first 5 matching lines concatenated with newlines

    Args:
        pdf_path (str): File system path to the PDF file

    Returns:
        str: Sample text (up to 5 lines) or empty string if:
             - File can't be opened
             - No matching date lines are found
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            lines = []
            for page in pdf.pages[:2]:
                for l in (page.extract_text() or "").splitlines():
                    if re.match(r'\d{2}[-/]\d{2}[-/]\d{4}', l.strip()):
                        lines.append(l.strip())
                        if len(lines) >= 5:
                            break
                if len(lines) >= 5:
                    break
            return "\n".join(lines)
    except Exception:
        return ""

def detailed_compare(df1: pd.DataFrame, df2: pd.DataFrame) -> str:
    """
    Compares two DataFrames and returns detailed differences.

    Performs three types of comparison:
    1. Shape mismatch
    2. Column ordering/renaming differences
    3. Data mismatch in rows

    Args:
        df1: First DataFrame for comparison
        df2: Second DataFrame for comparison

    Returns:
        str: Human-readable comparison results with:
             - Shape differences (if any)
             - Column differences (if any)
             - First 5 row differences using pandas.DataFrame.compare()

    Example Output:
        Shape mismatch: (100, 3) vs (99, 3)
        Column mismatch: ['Date', 'Amount'] vs ['DATE', 'AMOUNT']
        Differences (sample):
            Date        0: 2023-09-01 vs 1: 2023-09-01
            Amount      0: 45.00      vs 1: 45.00
            ...
    """
    diffs = []
    if df1.shape != df2.shape:
        diffs.append(f"Shape mismatch: {df1.shape} vs {df2.shape}")
    if list(df1.columns) != list(df2.columns):
        diffs.append(f"Column mismatch: {list(df1.columns)} vs {list(df2.columns)}")
    try:
        comp = df1.compare(df2)
        diffs.append("Differences (sample):\n" + comp.head(5).to_string())
    except Exception:
        diffs.append("Could not compute row differences.")
    return "\n".join(diffs)

def test_parser(state) -> tuple[bool, str]:
    """
    Tests a bank parser implementation against a reference CSV.

    This function:
    1. Loads the bank-specific parser module
    2. Parses the provided PDF file
    3. Compares results to the expected output CSV
    4. Returns test results including detailed comparison data

    Args:
        state (dict): Dictionary containing:
                      - "bank": Bank identifier (filename base for parser module)
                      - "pdf_path": File path to test PDF file
                      - "csv_path": File path to expected CSV output

    Returns:
        tuple: (bool, str) where:
               First value is True if test passes, False otherwise
               Second value is either:
               - "ALL MATCH" when dataframes match exactly
               - Human-readable comparison output if not matching
               - ERROR DURING TEST: full error traceback if exception occurs

    Preprocessing steps:
    - Strips whitespace from all string columns
    - Normalizes date columns to d-m-Y format using dayfirst=True

    Example workflow:
        >>> state = {
        ...     "bank": "chase",
        ...     "pdf_path": "tests/test_chase.pdf",
        ...     "csv_path": "tests/expected_chase.csv"
        ... }
        >>> test_parser(state)
        (True, "ALL MATCH")
    """
    try:
        df_exp = pd.read_csv(state["csv_path"])
        parser_module = load_parser_module(state["bank"])
        df_parsed = parser_module.parse(state["pdf_path"])

        for col in df_parsed.select_dtypes(include=['object']).columns:
            df_parsed[col] = df_parsed[col].str.strip()
        for col in df_exp.select_dtypes(include=['object']).columns:
            df_exp[col] = df_exp[col].str.strip()

        date_cols = [c for c in df_parsed.columns if 'date' in c.lower()]
        for col in date_cols:
            df_parsed[col] = pd.to_datetime(df_parsed[col], dayfirst=True, errors='coerce').dt.strftime("%d-%m-%Y")
            df_exp[col] = pd.to_datetime(df_exp[col], dayfirst=True, errors='coerce').dt.strftime("%d-%m-%Y")

        if df_parsed.equals(df_exp):
            return True, "ALL MATCH"

        return False, detailed_compare(df_parsed, df_exp)

    except Exception as e:
        return False, f"ERROR DURING TEST: {e}\n{traceback.format_exc()}"