<<<<<<< HEAD
# Financial CSV Chatbot (Flask + DuckDB + Ollama)

This project lets you ask natural-language questions about two financial CSV files (**holdings** and **trades**) through a simple Flask web UI.  
It uses **Ollama** to generate **DuckDB SQL**, executes the query locally, and returns the result.

## Project structure

- `app.py`: Flask server (serves UI + `/ask` API)
- `bot3.py`: Loads CSVs into DuckDB, generates SQL via Ollama, executes SQL safely
- `templates/index.html`: Single-page chat UI
- `data/holdings.csv`: Holdings dataset
- `data/trades.csv`: Trades dataset

## Prerequisites

- Python 3.10+ (works with Python 3.11)
- Ollama installed and running
  - Install: see Ollama docs (`https://ollama.com`)
  - Start the server: `ollama serve`
  - Pull the model used by this repo (default in `bot3.py` is `llama3.2:latest`):
    - `ollama pull llama3.2:latest`

## Install (Python deps)

Create a virtual environment (recommended) and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -U pip
pip install flask duckdb pandas ollama
```

## Run the web app

From the project root (`D:\csv_chatbot`):

```bash
python app.py
```

Then open:

- `http://localhost:8000`

## How it works (high level)

- On startup, `app.py` calls `initialize_db()` from `bot3.py`.
- `bot3.py` loads:
  - `data/holdings.csv` → DuckDB table `holdings`
  - `data/trades.csv` → DuckDB table `trades`
- When you ask a question:
  - Ollama generates SQL (or `NONE`) using a strict system prompt.
  - SQL is validated (blocks dangerous statements) and executed in DuckDB.
  - Results are returned as a plain text table.

## Common issues / fixes

### Ollama connection error

- Make sure Ollama is running:
  - `ollama serve`
- Make sure the model exists:
  - `ollama list`
  - `ollama pull llama3.2:latest`

### CSV file not found

The app expects these exact files:

- `data/holdings.csv`
- `data/trades.csv`

### “Sorry can not find the answer”

This happens when:

- The question isn’t answerable from the two tables, or
- Ollama returns invalid/unsafe SQL, or
- The SQL executes but returns zero rows, or
- There is an execution error (caught and returned as the same message)

## Example questions

- “Which fund has the highest YTD P&L?”
- “Total number of trades by PortfolioName”
- “Top 10 securities by market value”
- “Net cash flow by portfolio”

=======
# Financial Data Chatbot (LLM + DuckDB + Flask)

A secure, production-style **natural language financial analytics chatbot** built using **Flask, DuckDB, and an LLM**.  
The chatbot converts user questions into **read-only SQL**, executes them on real portfolio data, and returns **verified answers**.

> **LLM generates SQL only. DuckDB guarantees correctness.**

---

## ✨ Features

- Natural language → SQL query generation
- In-memory analytical database using DuckDB
- Strict SQL safety and validation
- No hallucinated data or numbers
- Fast aggregations on CSV data
- Simple Flask API + UI
- Production-oriented architecture

---

## 🏗 Architecture Overview

User (UI / API)
↓
Flask Server
↓
LLM (SQL Generator Only)
↓
DuckDB (Single Source of Truth)
↓
Validated Tabular Response


---

## 📂 Project Structure
project-root/
├── app.py # Flask application
├── bot3.py # SQL generation, validation & execution
├── data/
│ ├── holdings.csv # Portfolio holdings data
│ └── trades.csv # Trade data
├── templates/
│ └── index.html # Frontend UI
└── README.md



## 🧠 How It Works

### 1. User Question
The user submits a natural language question through the UI or `/ask` API.

Example:
"What is total market value by portfolio?"


---

### 2. LLM → SQL Conversion
The LLM:
- Generates **only SQL**
- Uses strict column and metric mappings
- Returns `NONE` if the question is unsupported

Example SQL:

SELECT PortfolioName, SUM(MV_Base)
FROM holdings
GROUP BY PortfolioName;
3. SQL Validation
Before execution, SQL is checked for:

❌ Write operations (INSERT, UPDATE, DELETE, DROP)

❌ Invalid tables or hallucinated columns

❌ Unsupported queries (forecasting, future dates)

Invalid queries are rejected safely.

4. DuckDB Execution
DuckDB executes the validated SQL on in-memory data loaded from CSV files.

Why DuckDB?

Columnar OLAP engine

Extremely fast aggregations

Zero setup

Pandas-native

Perfect for financial analytics

5. Safe Response
Valid result → returned as a table

Empty / invalid / failed query → safe fallback message

arduino
Copy code
"Sorry can not find the answer"
🔐 Safety & Guardrails
Read-only SQL execution

Explicit forbidden SQL keywords

Strict table access (holdings, trades)

No free-form LLM answers

Deterministic output backed by real data

📊 Supported Question Types
Holdings
Market value / exposure

Quantity / position size

Daily, monthly, quarterly, yearly PnL

Portfolio-level summaries

Trades
Number of trades

Buy vs sell counts

Traded volume

Cash flow and net cash

Average trade price

❌ Unsupported Queries
Forecasting or predictions

Future performance

Questions outside available data

Non-financial or vague queries

⚙️ Running the Project
Install Dependencies

pip install flask duckdb pandas ollama
Start Server
python app.py

Open in Browser
http://localhost:8000

🧪 API Example
POST /ask


{
  "question": "Total net cash flow by portfolio"
}
Response


{
  "answer": "PortfolioName  NetCash\nFundA  120000\nFundB  -45000"
}
🎯 Design Philosophy
LLM = Translator

DuckDB = Source of Truth

Flask = Orchestrator
