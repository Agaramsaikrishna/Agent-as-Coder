# 🧠 Agent-as-Coder: Bank Statement Parser

An autonomous LLM agent that generates Python parsers for bank PDF statements using minimal supervision.

🚀 Features
Automatically generate Python code to parse PDF bank statements.

Uses a LangGraph-based agent architecture to plan, generate, test, and self-fix.

Ensures output CSV matches expected schema and data.

Supports multiple banks with customizable parsers.

Minimal manual intervention required — runs autonomously until success or max iterations.


## ✅ How to Run

1. **Clone the repo**
```bash
https://github.com/Agaramsaikrishna/Agent-as-Coder.git
cd ai-agent-challenge
```

2.Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Add your API key**
```
Set CEREBRAS_API_KEY or configure in .env.
Note: I  used the cerebras instead of groq here 
```
 
5. **Run the agent**

```
python agent.py --target icici
```
-The agent will read the input PDF and CSV files from data/icici/.

-It will iteratively generate and test parser code.

-On success, the parser script will be saved to custom_parsers/icici_parser.py.


✅ Testing the Generated Parsers
You can run pytest on the test scripts to verify correctness:
```
pytest tests/test_icici.py
```


##🧠  Agent Architecture Diagram
```
┌────────────┐
│ plan       │ ← Analyze task and prepare prompt
└────┬───────┘
     ↓
┌────────────┐
│ generate   │ ← Generate parser code using LLM
└────┬───────┘
     ↓
┌────────────┐
│ test       │ ← Execute and validate generated parser
└────┬───────┘
     ↓
┌────────────┐
│ self-fix   │ ← Iterate with feedback until success or max iterations
└────────────┘

 ``` 

## 🧰 Project Structure
```
project-root/
├── agent.py                 # Main entrypoint script for running the agent
├── keys.py                  # API key storage (not committed)
├── data/
│   └── <bank_name>/
│       ├── <bank_name>_sample.pdf
│       └── result.csv       # Expected CSV output for verification
├── custom_parsers/          # Generated parser Python scripts saved here
├── src/
│   ├── state.py             # TypedDict and state definitions
│   └── graph.py             # Graph nodes and edges for LangGraph agent
└── utils/
    └── helpers.py           # Utility functions for CSV and PDF processing

```
📝 Notes
The project currently supports only certain banks based on data availability.

Parsers are tailored to the CSV schema and PDF format of each bank.

Customize or extend by adding new bank folders under data/ with sample PDFs and expected CSV results.





