# ai-agent-challenge
Coding agent challenge which write custom parsers for Bank statement PDF.


# 🧠 Agent-as-Coder: Bank Statement Parser

An autonomous LLM agent that generates Python parsers for bank PDF statements using minimal supervision.

## ✅ How to Run

1. **Clone the repo**
```bash
[git clone https://github.com/your-fork/ai-agent-challenge.git](https://github.com/Agaramsaikrishna/Agent-as-Coder.git)
cd ai-agent-challenge
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. Add your API key
Set OPENAI_API_KEY or configure in .env.

4. Run the agent

python agent.py --target icici


Run the agent

bash
Copy
Edit
python agent.py --target icici
Inspect results
Generated parser is saved at:

bash
Copy
Edit
custom_parsers/icici_parser.py
Run tests:

bash
Copy
Edit
pytest tests/test_icici.py


🧠  Agent Architecture Diagram
┌────────────┐
│ plan       │ ← Analyze task
└────┬───────┘
     ↓
┌────────────┐
│ generate   │ ← pdf_parser_tool (via LLM)
└────┬───────┘
     ↓
┌────────────┐
│ test       │ ← test_runner_tool (Pytest)
└────┬───────┘
     ↓
┌────────────┐
│ self-fix   │ ← Retry with feedback
└────────────┘


🧰 Project Structure
.
project-root/
├── agent.py
├── keys.py                # API keys storage
├── data/
│   └── <bank_name>/
│       ├── <bank_name>_sample.pdf
│       └── result.csv
├── custom_parsers/        # Generated parser output
├── src/
│   ├── state.py
│   └── graph.py
└── utils/
    └── helpers.py


graph TD
    Plan[AI Code Generation] --> Execute[Code Execution]
    Execute --> Test[Test Validation]
    Test --> Decision{Success?}
    Decision -- No --> Plan

    Decision -- Yes --> End
