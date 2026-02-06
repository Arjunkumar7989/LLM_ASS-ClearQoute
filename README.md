## Overview
This project converts natural language questions into SQL queries
and executes them on a SQLite database containing vehicle damage,
repair, and insurance quote data.

## Features
- Natural language to SQL conversion
- Rule-based fallback for deterministic results
- Optional LLM integration
- Robust CSV ingestion with real-world data handling

## Example
Question:
What is the average repair cost?

Generated SQL:
SELECT AVG(repair_cost) FROM repairs;

Output:
The average repair cost is ₹25,203.91
