from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from sql import create_or_check_db, create_tables, get_tables
from uuid import uuid4
import sqlite3
from loan_functions import calculate_monthly_payment, generate_loan_schedule

app = FastAPI()

print(create_or_check_db())
create_tables()
print(get_tables())

class User(BaseModel):
    uuid: str = None
    first_name: str
    last_name: str

class Loan(BaseModel):
    uuid: str = None
    amount: float
    annual_interest_rate: float
    loan_term_in_months: float

class LoanAssignment(BaseModel):
    uuid: str = None
    loan_id: str
    user_id: str

def get_loan(loan_id: str):
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute("SELECT * FROM loans WHERE uuid = ?", (loan_id,))
    loan = c.fetchone()
    return Loan(uuid=loan[0], amount=loan[1], annual_interest_rate=loan[2], loan_term_in_months=loan[3])

@app.post("/users/create")
async def create_user(user: User):
    user.uuid = str(uuid4())
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (user.uuid, user.first_name, user.last_name))
    conn.commit()
    return user


@app.post("/loan/create/")
async def create_loan(loan: Loan):
    loan.uuid = str(uuid4())

    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute("INSERT INTO loans VALUES (?, ?, ?, ?)", (loan.uuid, loan.amount, loan.annual_interest_rate, loan.loan_term_in_months))
    conn.commit()
    return loan

@app.post("/loan/assign")
async def assign_loan(loanAssignment: LoanAssignment):
    conn = sqlite3.connect('mydb.db')
    loan_assignment_number = uuid4()
    c = conn.cursor()
    c.execute("INSERT INTO loan_assignments VALUES (?, ?, ?)", (loanAssignment.loan_assignment_number, loanAssignment.loan_id, loanAssignment.user_id))
    conn.commit()
    return {
        "loan_id": loanAssignment.loan_id,
        "user_id": loanAssignment.user_id
    }

@app.get("/users")
def get_users():
    print("get_users")
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    print(users)
    for user in users:
        print(user)
    return {
        "user_id": user[0],
        "first_name": user[1],
        "last_name": user[2]
    }

@app.get("/loans")
def get_loans():
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute("SELECT uuid FROM loans")
    loans = c.fetchall()
    arr = []

    for loan in loans:
        arr.append(loan[0])

    return {
        "loans": arr
    }


@app.post("/loan/schedule", response_model=list[dict])
async def loan_schedule(loan: Loan):
    schedule = generate_loan_schedule(loan.amount, loan.annual_interest_rate, loan.loan_term_in_months)
    return schedule

@app.get("/loan/summary/{loan_id}/{month}")
async def loan_summary(loan_id: str, month: str):
    loan = get_loan(loan_id)

    month = int(month)
    if month < 1 or month > loan.loan_term_in_months:
        raise HTTPException(status_code=404, detail="Month is out of range")
    
    schedule = generate_loan_schedule(loan.amount, loan.annual_interest_rate, loan.loan_term_in_months)
    selected_month = schedule[month-1]
    principal_paid = sum(item['monthly_payment'] - (item['remaining_balance'] * loan.annual_interest_rate / 12 / 100) for item in schedule[:month])
    interest_paid = sum(item['monthly_payment'] for item in schedule[:month]) - principal_paid
    
    return {
        "current_principal_balance": selected_month['remaining_balance'],
        "aggregate_principal_paid": round(principal_paid, 2),
        "aggregate_interest_paid": round(interest_paid, 2)
    }