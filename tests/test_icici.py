import os
import pandas as pd
from custom_parsers.icici_parser import parse

def test_icici_parser():
    # Paths to input and expected output
    pdf_path = "data/icici/icici_sample.pdf"
    expected_csv_path = "data/icici/result.csv"

    assert os.path.exists(pdf_path), f"Missing PDF file: {pdf_path}"
    assert os.path.exists(expected_csv_path), f"Missing expected CSV file: {expected_csv_path}"

    # Load expected output
    expected_df = pd.read_csv(expected_csv_path)

    # Run the parser
    result_df = parse(pdf_path)

    # Normalize both DataFrames before comparison
    for col in result_df.select_dtypes(include=['object']).columns:
        result_df[col] = result_df[col].str.strip()
        expected_df[col] = expected_df[col].str.strip()

    # Normalize date format
    date_cols = [col for col in result_df.columns if 'date' in col.lower()]
    for col in date_cols:
        result_df[col] = pd.to_datetime(result_df[col], dayfirst=True, errors='coerce').dt.strftime('%d-%m-%Y')
        expected_df[col] = pd.to_datetime(expected_df[col], dayfirst=True, errors='coerce').dt.strftime('%d-%m-%Y')

    # Sort if needed to avoid row order issues (optional)
    result_df = result_df.sort_values(by=result_df.columns.tolist()).reset_index(drop=True)
    expected_df = expected_df.sort_values(by=expected_df.columns.tolist()).reset_index(drop=True)

    # Assertion
    assert result_df.equals(expected_df), "Parsed data does not match expected CSV output"
