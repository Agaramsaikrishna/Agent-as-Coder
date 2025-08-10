
from typing import TypedDict

class AgentState(TypedDict):
    bank: str
    pdf_path: str
    csv_path: str
    code: str
    iterations: int
    success: bool
    error_msg: str
    feedback_msg: str
    csv_columns: list
    csv_shape: tuple
    csv_sample: list
    pdf_sample: str
