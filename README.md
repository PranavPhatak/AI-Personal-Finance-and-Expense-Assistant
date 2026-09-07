# AI Personal Finance & Expense Assistant

An AI-powered personal finance assistant that lets you manage, track, and analyze your income, expenses, and budgets using natural language — no SQL, no forms, no manual navigation.

```
"I spent ₹1,500 on shopping today."
"Show me my recent expenses."
"How much have I spent on food?"
"Set my food budget for September 2026 to ₹5,000."
"What is my remaining balance?"
```

The agent interprets your request, interacts with a SQLite database through SQL tools, performs the required operation, and returns a clean, human-readable response.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Database Design](#database-design)
- [Getting Started](#getting-started)
- [Testing the Application](#testing-the-application)
- [Data Safety](#data-safety)
- [Current Limitations](#current-limitations)
- [Future Improvements](#future-improvements)
- [What I Learned](#what-i-learned)
- [License](#license)

---

## Overview

Traditional finance apps require you to learn their forms, buttons, and filters. This project flips that model — you simply talk to your finances in plain English, and the AI agent handles the underlying database work.

The application is built around a **Streamlit** chat interface backed by a **LangGraph** agent, which uses **ChatGroq** as its LLM and a **SQLDatabaseToolkit** to safely read from and write to a local **SQLite** database.

---

## Features

### Natural Language Interaction
No SQL or database knowledge required — describe what you want, and the agent determines the right operation automatically.

### Expense Management
- Add, view, update, and delete expenses
- Filter by date or category
- Calculate total spending
- Analyze category-wise spending
- Identify the highest spending category

### Income Management
- Add, view, update, and delete income records
- Filter by date or source
- Calculate total income

### Budget Management
- Create and manage category-based monthly budgets
- Compare actual spending against budgets
- Detect over-budget categories

### Financial Analysis
- Total income and expenses
- Remaining balance
- Category-wise breakdowns
- Monthly summaries
- Budget vs. actual comparisons

### Streaming Responses
Responses stream progressively with a natural typing effect instead of appearing all at once.

### Hidden SQL Execution
The agent generates and executes SQL internally, but users only ever see clean, formatted results — never raw queries.

**Example:**

| ID | Category | Amount | Description |
|----|----------|--------|-------------|
| 8  | Food     | ₹100   | Pani Puri |
| 3  | Food     | ₹250   | — |
| 4  | Shopping | ₹1,500 | Bought some clothes |

---

## Architecture

```
                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │  Streamlit  │
                    │     UI      │
                    └──────┬──────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    LangGraph Agent  │
                │                     │
                │    create_agent()   │
                └──────────┬──────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         ChatGroq      SQL Tools    Checkpointer
           LLM       SQLDatabase     InMemorySaver
              │        Toolkit
              │            │
              │            ▼
              │       SQLite Database
              │            │
              │     ┌──────┼──────┐
              │     ▼      ▼      ▼
              │  Expenses Budgets Income
              │
              ▼
        Final AI Response
              │
              ▼
            USER
```

### Request Flow

1. User enters a question or command
2. Streamlit passes the input to the LangGraph agent
3. The LLM interprets intent
4. The agent determines the required database operation
5. `SQLDatabaseToolkit` provides the necessary tools
6. SQLite is queried or updated
7. The database returns a result
8. The LLM interprets the result
9. The user receives a natural-language response

The user only ever sees the final response — every intermediate step is abstracted away.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | LLM application framework |
| LangGraph | Agent execution and state management |
| ChatGroq | LLM integration |
| SQLite | Local relational database |
| SQLDatabaseToolkit | Database interaction tools |
| Streamlit | Web-based user interface |
| python-dotenv | Environment variable management |
| uv | Python project/dependency management |

---

## Project Structure

```
AI-Personal-Finance-and-Expense-Assistant/
│
├── agent.py              # AI agent configuration
├── app.py                 # Streamlit application and chat interface
├── database.py             # SQLite setup and LangChain DB connection
├── prompt.py               # System prompt and agent instructions
├── personal_finance.db     # SQLite financial database
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Python dependencies
├── uv.lock                 # Locked dependency versions
├── .gitattributes
├── .gitignore
├── .python-version
└── LICENSE
```

### File Responsibilities

**`app.py`** — Streamlit interface: chat input, chat history, response streaming, typing effect, and processing indicators.

**`agent.py`** — Agent configuration: ChatGroq model, SQLDatabaseToolkit, database tools, LangGraph checkpointer, and system prompt wiring. Kept separate from the UI layer.

**`database.py`** — Creates the SQLite database and required tables, and connects SQLite to LangChain's SQL database interface.

**`prompt.py`** — System instructions governing database operations, expense/income/budget management, SQL safety, result formatting, currency formatting, date handling, and prevention of fabricated data.

---

## Database Design

The application uses a SQLite database with three core tables.

### Expenses

| Column | Type | Description |
|---|---|---|
| `Id` | INTEGER | Primary key |
| `Category` | TEXT | Expense category |
| `Amount` | REAL | Expense amount |
| `Description` | TEXT | Description of the expense |
| `Expense_Date` | TIMESTAMP | Date and time of the expense |

### Budgets

| Column | Type | Description |
|---|---|---|
| `Id` | INTEGER | Primary key |
| `Category` | TEXT | Budget category |
| `Amount` | REAL | Budget amount |
| `Month` | INTEGER | Budget month |
| `Year` | INTEGER | Budget year |

### Income

| Column | Type | Description |
|---|---|---|
| `Id` | INTEGER | Primary key |
| `Amount` | REAL | Income amount |
| `Source` | TEXT | Income source |
| `Income_Date` | DATE | Income date |

### Financial Calculations

```
Total Expenses     = SUM(Expenses.Amount)
Total Income        = SUM(Income.Amount)
Remaining Balance   = Total Income - Total Expenses
```

Budget comparisons are made by evaluating actual category spending against the assigned budget for that category and month.

### Currency Handling

All amounts are treated as **Indian Rupees (INR)**. Values are stored numerically in the database and displayed using the `₹` symbol (e.g., `₹100`, `₹1,500`, `₹1,00,000`). USD is not supported.

---

## Getting Started

### Prerequisites

- Python 3.x
- A Groq API key
- Git
- Internet connection (for LLM API calls)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Personal-Finance-and-Expense-Assistant.git
cd AI-Personal-Finance-and-Expense-Assistant
```

### 2. Create a Virtual Environment

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Or using `uv`:
```bash
uv sync
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

> **Important:** Never commit your API key. Confirm `.env` is listed in `.gitignore`.

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser.

---

## Testing the Application

With a fresh database, try the following sequence:

**Add Income**
```
I received my salary of ₹50,000 on September 1, 2026.
I also received ₹5,000 from freelance work on September 3, 2026.
```

**Add Expenses**
```
I spent ₹250 on food today.
I spent ₹1,500 on shopping today. I bought some clothes.
I spent ₹800 on transportation today.
I paid ₹2,000 for my electricity bill today.
I spent ₹300 on food today for dinner with my family.
```

**Add Budgets**
```
Set my food budget for September 2026 to ₹5,000.
Set my shopping budget for September 2026 to ₹8,000.
Set my transportation budget for September 2026 to ₹3,000.
```

**Run Analysis**
```
Give me a summary of my finances.
What is my highest spending category?
How much have I spent on food?
Am I over budget anywhere?
```

---

## Data Safety

Financial data is stored locally in `personal_finance.db`. The LLM interprets requests and determines the appropriate database operation, while SQLite handles the actual data persistence.

**Security practices to follow:**
- Never commit `.env` or any file containing API credentials
- For production use, additionally implement:
  - User authentication and authorization
  - Encrypted storage
  - Secure secrets management
  - Database access controls
  - Input validation
  - Audit logging

---

## Current Limitations

This project is primarily a learning and portfolio piece. Known limitations:

- Single local SQLite database (no multi-user support)
- No user authentication
- Local-only conversation state
- No cloud database
- No dedicated financial dashboard
- No bank account integration or transaction syncing
- Financial outputs should be independently verified before use in real decisions

---

## Future Improvements

- **Financial Dashboard** — visualizations for monthly expenses, category breakdowns, income vs. expenses, and budget utilization
- **Spending Trends** — historical trend analysis (e.g., "How has my food spending changed over 6 months?")
- **Savings Goals** — goal-setting and progress tracking
- **Budget Alerts** — notifications at defined budget thresholds (e.g., 80% used, budget exceeded)
- **User Authentication** — per-user agents and databases
- **Cloud Database** — migration to PostgreSQL, MySQL, Supabase, or Cloud SQL
- **Exportable Reports** — CSV, PDF, and Excel exports for monthly summaries, expenses, budgets, and income

---

## What I Learned

This project was built to explore how LLMs can interact with structured data to perform real-world operations, including:

- LangChain and LangGraph agent design
- SQL database agents and `SQLDatabaseToolkit`
- Tool calling and LLM-driven database interaction
- Prompt engineering for structured financial operations
- Agent state management and conversation memory
- Streamlit development, streaming responses, and session state
- SQLite and environment variable management
- Python project management with `uv`

---

## Author

**Pranav Phatak**
B.Tech Computer Engineering

Interests: Generative AI · AI Agents · LangChain · LangGraph · RAG Systems · Python · Machine Learning · Software Development

---

## Support

If you found this project useful:
- Star the repository
- Fork it and build on it
- Open an issue for bugs or ideas
- Contribute improvements via pull request

---

## License

This project is available under the license included in the [LICENSE](LICENSE) file.

---

<div align="center">

**Talk to your finances. Let AI handle the database.**

Built with Python · LangChain · LangGraph · ChatGroq · SQLite · Streamlit

</div>
