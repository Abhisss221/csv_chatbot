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

yaml
Copy code

---

## 📂 Project Structure

.
├── app.py # Flask application
├── bot3.py # SQL generation, validation & execution
├── data/
│ ├── holdings.csv # Portfolio holdings data
│ └── trades.csv # Trade data
├── templates/
│ └── index.html # Frontend UI
└── README.md

yaml
Copy code

---

## 🧠 How It Works

### 1. User Question
The user submits a natural language question through the UI or `/ask` API.

Example:
"What is total market value by portfolio?"

sql
Copy code

---

### 2. LLM → SQL Conversion
The LLM:
- Generates **only SQL**
- Uses strict column and metric mappings
- Returns `NONE` if the question is unsupported

Example SQL:
```sql
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
bash
Copy code
pip install flask duckdb pandas ollama
Start Server
bash
Copy code
python app.py
Open in Browser
arduino
Copy code
http://localhost:8000
🧪 API Example
POST /ask

json
Copy code
{
  "question": "Total net cash flow by portfolio"
}
Response

json
Copy code
{
  "answer": "PortfolioName  NetCash\nFundA  120000\nFundB  -45000"
}
🎯 Design Philosophy
LLM = Translator

DuckDB = Source of Truth

Flask = Orchestrator

This is not a chatbot that guesses —
It is a deterministic analytics engine with natural language input.
