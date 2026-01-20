# chatbot.py
import duckdb
import pandas as pd
import ollama
from pathlib import Path
import re

# ============================================
# CONFIG
# ============================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

OLLAMA_MODEL = "llama3.2:latest"

FORBIDDEN_SQL = ["insert", "update", "delete", "drop", "alter", "truncate"]

UNSUPPORTED_TERMS = [
    "forecast", "predict", "future", "2020", "2021", "2022", "2023",
    "last year", "next year"
]

# ============================================
# DATABASE INITIALIZATION
# ============================================

def initialize_db():
    con = duckdb.connect(database=":memory:")

    holdings_df = pd.read_csv(DATA_DIR / "holdings.csv")
    trades_df = pd.read_csv(DATA_DIR / "trades.csv")

    con.execute("CREATE TABLE holdings AS SELECT * FROM holdings_df")
    con.execute("CREATE TABLE trades AS SELECT * FROM trades_df")

    return con

# ============================================
# SYSTEM PROMPT
# ============================================
SYSTEM_PROMPT = """
You are a financial data SQL generator.

You have access to ONLY two DuckDB tables:
1) holdings
2) trades

RULES:
- Output ONLY valid DuckDB SQL OR NONE
- No explanations
- No markdown
- No hallucinated columns
- Use GROUP BY for aggregations
- Use ORDER BY for rankings
- Join tables ONLY if required
- Allowed JOIN keys: PortfolioName, SecurityId
- If not answerable → NONE

==============================
METRIC MAPPINGS
==============================

PERFORMANCE (holdings):
- profit, pnl, performance → PL_YTD
- unrealized pnl → PL_YTD
- daily pnl, today → PL_DTD
- monthly pnl, month → PL_MTD
- quarterly pnl, quarter → PL_QTD

VALUATION / EXPOSURE (holdings):
- market value, portfolio value, exposure → MV_Base
- local market value → MV_Local
- position size → MV_Base
- quantity, position quantity → Qty
- starting quantity → StartQty
- price → Price

TRADING ACTIVITY (trades):
- trades, number of trades → COUNT(*)
- buy trades → COUNT(*) WHERE TradeTypeName = 'Buy'
- sell trades → COUNT(*) WHERE TradeTypeName = 'Sell'
- traded quantity, volume → SUM(Quantity)
- average trade price → AVG(Price)

CASH FLOW (trades):
- trade value, cash → SUM(TotalCash)
- buy cash → SUM(TotalCash) WHERE TradeTypeName = 'Buy'
- sell cash → SUM(TotalCash) WHERE TradeTypeName = 'Sell'
- net cash flow → 
  SUM(
    CASE 
      WHEN TradeTypeName = 'Buy' THEN -TotalCash 
      ELSE TotalCash 
    END
  )

FEES & COSTS (trades):
- fees, transaction cost → SUM(AllocationFees)

PORTFOLIO SCOPING:
- by fund, by portfolio → GROUP BY PortfolioName
- by security → GROUP BY SecurityId
- by custodian → GROUP BY CustodianName

TABLE USAGE:
- Holdings & performance → holdings
- Trades, volume, cash → trades
"""


# ============================================
# SAFETY
# ============================================

def is_supported_question(question: str) -> bool:
    q = question.lower()
    return not any(term in q for term in UNSUPPORTED_TERMS)

def validate_sql(sql: str) -> bool:
    sql_lower = sql.lower()

    if any(word in sql_lower for word in FORBIDDEN_SQL):
        return False

    if not re.search(r"\bholdings\b|\btrades\b", sql_lower):
        return False

    return True

# ============================================
# SQL GENERATION
# ============================================

def generate_sql(question: str) -> str:
    if not is_supported_question(question):
        return "NONE"

    prompt = f"""
{SYSTEM_PROMPT}

User Question:
{question}

Return SQL or NONE:
"""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": "You generate SQL only."},
            {"role": "user", "content": prompt}
        ],
        options={"temperature": 0}
    )

    return response["message"]["content"].strip()

# ============================================
# EXECUTION
# ============================================

def ask_bot(con, question: str) -> str:
    sql = generate_sql(question)

    if sql == "NONE" or not validate_sql(sql):
        return "Sorry can not find the answer"

    try:
        df = con.execute(sql).fetchdf()
        if df.empty:
            return "Sorry can not find the answer"
        return df.to_string(index=False)
    except Exception:
        return "Sorry can not find the answer"
