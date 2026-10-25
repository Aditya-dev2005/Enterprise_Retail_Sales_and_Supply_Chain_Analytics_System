"""
Lets a user ask a plain-English question about the retail data
(e.g. "Which store sold the most last month?") and get back both the
generated SQL and a natural-language answer.

Flow:
  1. Send the question + a description of our database schema to an
     LLM via OpenRouter, asking it to write ONE read-only SQL SELECT
     query that answers it.
  2. Validate the generated SQL (SELECT-only, single statement, no
     destructive keywords) before running it anywhere near a real
     database.
  3. Execute the query and fetch the rows.
  4. Send the question + the resulting rows back to the LLM and ask
     for a short natural-language summary.

Security note: never execute LLM output blindly. The validation in
_validate_sql_is_safe() is a hard gate, not a suggestion - if a
generated query fails it, we reject it instead of trying to "fix" it.
"""

import re
import requests
from sqlalchemy import text

from configs.settings import OPENROUTER_API_KEY, OPENROUTER_MODEL
from database.database_connection import sessionLocal
from logger_config import logger

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

DB_SCHEMA_DESCRIPTION = """
Tables:

products(product_id VARCHAR, product_name VARCHAR, category VARCHAR, brand VARCHAR,
         unit_price FLOAT, supplier_id VARCHAR, status VARCHAR)

stores(store_id VARCHAR, store_name VARCHAR, city VARCHAR, state VARCHAR,
       store_manager VARCHAR, opening_date DATE, status VARCHAR)

customers(customer_id VARCHAR, customer_name VARCHAR, email VARCHAR, mobile VARCHAR,
          city VARCHAR, registration_date DATE, customer_type VARCHAR)

sales(sale_id VARCHAR, product_id VARCHAR REFERENCES products, store_id VARCHAR REFERENCES stores,
      customer_id VARCHAR REFERENCES customers, quantity INT, sale_date DATE,
      discount_percentage FLOAT, payment_mode VARCHAR)

inventory(inventory_id VARCHAR, product_id VARCHAR REFERENCES products,
          store_id VARCHAR REFERENCES stores, available_quantity INT,
          reorder_level INT, last_updated DATE)
"""

# Any generated SQL containing these keywords is rejected outright,
# regardless of casing or where they appear in the statement.
_BLOCKED_KEYWORDS = [
    "insert", "update", "delete", "drop", "alter", "truncate",
    "create", "grant", "revoke", "attach", "replace", "into outfile",
]


class AIQueryError(Exception):
    """Raised for any failure in the AI query flow (LLM call, unsafe
    SQL, or DB execution) so the API layer can turn it into a clean
    HTTP error."""
    pass


def _call_openrouter(messages: list, max_tokens: int = 400) -> str:
    if not OPENROUTER_API_KEY:
        raise AIQueryError(
            "OPENROUTER_API_KEY is not set. Add it to your environment or .env file."
        )

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        logger.exception(f"OpenRouter request failed: {e}")
        raise AIQueryError(f"Failed to reach OpenRouter API: {e}")
    except (KeyError, IndexError) as e:
        logger.exception(f"Unexpected OpenRouter response format: {e}")
        raise AIQueryError("Unexpected response format from OpenRouter API")


def _extract_sql(raw_text: str) -> str:
    """The model may wrap the query in a ```sql code block - strip that
    off if present, otherwise use the raw text."""
    match = re.search(r"```(?:sql)?\s*(.*?)```", raw_text, re.DOTALL | re.IGNORECASE)
    sql = match.group(1) if match else raw_text
    return sql.strip().rstrip(";").strip()


def _validate_sql_is_safe(sql: str) -> None:
    if not sql:
        raise AIQueryError("The model did not return a query.")

    if ";" in sql:
        raise AIQueryError("Only a single SQL statement is allowed.")

    if not sql.strip().lower().startswith("select"):
        raise AIQueryError("Only SELECT queries are allowed.")

    lowered = sql.lower()
    for keyword in _BLOCKED_KEYWORDS:
        if keyword in lowered:
            raise AIQueryError(
                f"Generated query contains a disallowed keyword ('{keyword}') and was rejected."
            )


def _generate_sql(question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a MySQL expert. Given a database schema and a question, "
                "write ONE single read-only SQL SELECT query that answers the "
                "question. Only use the tables and columns provided. "
                "Do not include any explanation - respond with ONLY the SQL query, "
                "wrapped in a ```sql code block.\n\n"
                f"Schema:\n{DB_SCHEMA_DESCRIPTION}"
            ),
        },
        {"role": "user", "content": question},
    ]

    raw = _call_openrouter(messages, max_tokens=300)
    sql = _extract_sql(raw)
    _validate_sql_is_safe(sql)
    return sql


def _run_sql(sql: str):
    session = sessionLocal()
    try:
        result = session.execute(text(sql))
        columns = list(result.keys())
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        return rows
    except Exception as e:
        logger.exception(f"Failed to execute AI-generated SQL: {e}")
        raise AIQueryError(f"Failed to execute the generated query: {e}")
    finally:
        session.close()


def _summarize_results(question: str, sql: str, rows: list) -> str:
    # Cap how much data we send back to the LLM to keep costs/latency down.
    preview_rows = rows[:20]

    messages = [
        {
            "role": "system",
            "content": (
                "You answer questions about retail data in 1-3 short sentences, "
                "based only on the SQL query and its results provided. "
                "Be direct and specific with numbers."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Question: {question}\n"
                f"SQL used: {sql}\n"
                f"Result rows (JSON): {preview_rows}\n"
                f"Total rows returned: {len(rows)}\n\n"
                "Answer the question in plain English."
            ),
        },
    ]

    return _call_openrouter(messages, max_tokens=200)


def answer_query(question: str) -> dict:
    logger.info(f"AI query received: {question}")

    sql = _generate_sql(question)
    rows = _run_sql(sql)
    answer = _summarize_results(question, sql, rows)

    logger.info(f"AI query completed. {len(rows)} row(s) returned.")

    return {
        "question": question,
        "sql_generated": sql,
        "row_count": len(rows),
        "data": rows,
        "answer": answer,
    }
