def calculate_monthly_payment(amount: float, annual_interest_rate: float, loan_term_months: int) -> float:
    monthly_interest_rate = annual_interest_rate / 12 / 100
    monthly_payment = amount * (monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -loan_term_months))
    return monthly_payment

def generate_loan_schedule(amount: float, annual_interest_rate: float, loan_term_months: int):
    monthly_payment = calculate_monthly_payment(amount, annual_interest_rate, loan_term_months)
    schedule = []
    for month in range(1, loan_term_months + 1):
        remaining_balance = amount * (1 + annual_interest_rate / 12 / 100) ** month - monthly_payment * ((1 + annual_interest_rate / 12 / 100) ** month - 1) / (annual_interest_rate / 12 / 100)
        schedule.append({
            "month": month,
            "remaining_balance": round(remaining_balance, 2),
            "monthly_payment": round(monthly_payment, 2)
        })
    return schedule


