from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///personal_finance.db")

db.run("""
    CREATE TABLE IF NOT EXISTS Expenses(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Category TEXT NOT NULL,
        Amount REAL NOT NULL,
        Description TEXT,
        Expense_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

db.run("""
    CREATE TABLE IF NOT EXISTS Budgets(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Category TEXT NOT NULL,
        Amount REAL NOT NULL CHECK(Amount > 0),
        Month INTEGER NOT NULL CHECK(Month BETWEEN 1 AND 12),
        Year INTEGER NOT NULL CHECK(Year BETWEEN 2000 AND 2100),
        UNIQUE (Category, Month, Year)
    );
""")

db.run("""
    CREATE TABLE IF NOT EXISTS Income(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Amount INTEGER NOT NULL,
        Source TEXT NOT NULL,
        Income_Date DATE NOT NULL 
    );
""")

print("Tables created successfully")