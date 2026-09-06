from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///personal_finance.db")

print("Database created successfully")