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




##🧠  Agent Architecture Diagram
```
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
 ``` 

## 🧰 Project Structure
```
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
```

