import json
from pathlib import Path
from api.banking_api import BankingAPI

ROOT = Path(__file__).resolve().parents[1]

class BankingTools:
    """Banking tools exposed to the agent layer."""

    def __init__(self):
        self.api = BankingAPI()

    def get_account_balance(self, customer_id):
        return self.api.get_balance(customer_id)

    def get_transaction_history(self, customer_id):
        return self.api.get_transactions(customer_id)

    def get_account_details(self, customer_id):
        return self.api.get_account(customer_id)

    def check_loan_eligibility(self, customer_id, loan_type, amount):
        return self.api.check_loan_eligibility(customer_id, loan_type, amount)

    def calculate_emi(self, amount, annual_rate, tenure_years):
        p = float(amount)
        r = float(annual_rate) / 12 / 100
        n = int(tenure_years * 12)
        emi = p * r * (1 + r) ** n / ((1 + r) ** n - 1) if r else p / n
        return {
            "principal": p,
            "annual_interest_rate": annual_rate,
            "tenure_years": tenure_years,
            "monthly_emi": round(emi, 2),
        }
