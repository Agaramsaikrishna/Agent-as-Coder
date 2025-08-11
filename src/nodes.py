"""
Core workflow functions for AI-powered parser generation and execution

Key features:
- Uses Cerebras AI for code generation
- Implements a 3-iteration maximum planning loop
- Generates bank-specific parser modules
- Automates testing with custom validation
- Adds required imports to generated code
"""

import os, re
from langchain_cerebras import ChatCerebras
from utils.prompt import create_prompt
from utils.helpers import test_parser
from keys import GEMINI_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI


def plan_generate(state):
    """
    Core workflow functions for AI-powered parser generation and execution

    Key features:
    - Uses Cerebras AI for code generation
    - Implements a 3-iteration maximum planning loop
    - Generates bank-specific parser modules
    - Automates testing with custom validation
    - Adds required imports to generated code
    """
    state["iterations"] += 1
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, api_key=GEMINI_API_KEY)

    prompt = create_prompt(state)
    resp = llm.invoke([("user", prompt)])
    code = resp.content.strip()

    code = re.sub(r"^```python", "", code)
    code = re.sub(r"^```", "", code)
    code = re.sub(r"```$", "", code).strip()

    required_imports = ["import pandas as pd", "import pdfplumber", "import re", "import numpy as np"]
    for imp in reversed(required_imports):
        if imp not in code:
            code = imp + "\n" + code

    state["code"] = code
    return state

def execute_test(state):
    """
    Core workflow functions for AI-powered parser generation and execution

    Key features:
    - Uses Cerebras AI for code generation
    - Implements a 3-iteration maximum planning loop
    - Generates bank-specific parser modules
    - Automates testing with custom validation
    - Adds required imports to generated code
    """
    os.makedirs("custom_parsers", exist_ok=True)
    with open(f"custom_parsers/{state['bank']}_parser.py", "w") as f:
        f.write(state["code"])
    ok, fb = test_parser(state)
    state["success"] = ok
    state["feedback_msg"] = fb
    return state

def decide_next(state):
    """
    Core workflow functions for AI-powered parser generation and execution

    Key features:
    - Uses Cerebras AI for code generation
    - Implements a 3-iteration maximum planning loop
    - Generates bank-specific parser modules
    - Automates testing with custom validation
    - Adds required imports to generated code
    """
    return "end" if state["success"] or state["iterations"] >= 3 else "plan"
