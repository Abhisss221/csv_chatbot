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

