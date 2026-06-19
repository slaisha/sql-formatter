# ⚡ SQL Formatter & Analyzer

A beautiful, fast tool to format messy SQL queries and analyze their complexity. Built for analytics engineers who want clean, readable SQL.

## Features

- **Instant Formatting**: Transform messy SQL into clean, properly indented queries
- **Syntax Highlighting**: Professional code highlighting with custom theme
- **Complexity Analysis**: Understand your query's complexity at a glance
  - Table count
  - Join operations
  - CTEs (Common Table Expressions)
  - Subquery depth
  - Column count
  - WHERE condition count
- **Copy to Clipboard**: One-click copy of formatted SQL
- **Sample Queries**: Pre-loaded examples to try

## Tech Stack

- **Streamlit**: Fast web app framework
- **sqlparse**: SQL parsing and formatting
- **Pygments**: Syntax highlighting
- **Zero external APIs**: All processing happens locally

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Then:
1. Paste your messy SQL query
2. Click "Format & Analyze"
3. Get beautifully formatted SQL with complexity metrics
4. Copy and use in your project

## Why This Tool?

- **Zero AI costs**: Pure Python parsing, no LLM needed
- **Privacy-first**: All processing happens locally
- **Fast**: Instant results
- **Analytics-focused**: Metrics that matter for data engineers

## Sample Queries Included

- Simple SELECT
- Multiple JOINs
- Complex CTEs
- Nested subqueries

## Design

Custom gradient theme with plum (#5A3050) and teal (#0F766E) brand colors. Glassmorphism design with smooth animations.

---

Built with ❤️ for analytics engineers
