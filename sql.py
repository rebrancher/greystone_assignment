from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import sqlite3
# from main import User, Loan

def create_or_check_db():
    engine = create_engine("sqlite:///mydb.db", echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)

    print(database_exists(engine.url))

def create_tables():
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (uuid TEXT, 
                 first_name TEXT, 
                 last_name TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS loans
                    (uuid TEXT, 
                    amount REAL, 
                    annual_interest_rate REAL, 
                    loan_term_in_months REAL 
                    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS loan_assignments
                    (loan_id TEXT, 
                    user_id TEXT
                    )''')
    conn.commit()

def get_tables():
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return c.fetchall()

# def get_users():
#     conn = sqlite3.connect('mydb.db')
#     c = conn.cursor()
#     c.execute("SELECT * FROM users")
#     return c.fetchall()

