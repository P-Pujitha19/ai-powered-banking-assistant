import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class BankingAPI:
    """Mock banking API backed by synthetic JSON data."""

    def __init__(self):
        self.customers = self._load("customers.json")
        self.accounts = self._load("accounts.json")
        self.transactions = self._load("transactions.json")
        self.products = self._load("banking_products.json")

    def _load(self, name):
        with open(ROOT / "data" / name, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_balance(self, customer_id):
        account = next(a for a in self.accounts if a["customer_id"] == customer_id)
        return {
            "customer_id": customer_id,
            "account_type": account["account_type"],
            "available_balance": account["balance"],
            "currency": "INR",
            "account_number": account["account_number"],
        }

    def get_transactions(self, customer_id):
        rows = [t for t in self.transactions if t["customer_id"] == customer_id]
        return {"customer_id": customer_id, "transactions": rows}

    def get_account(self, customer_id):
        account = next(a for a in self.accounts if a["customer_id"] == customer_id)
        return account

    def check_loan_eligibility(self, customer_id, loan_type, amount):
        customer = next(c for c in self.customers if c["customer_id"] == customer_id)
        product = next((p for p in self.products if p["product"].lower() == loan_type.lower()), None)
        max_amount = product["maximum_amount_inr"] if product else 2000000
        eligible = bool(customer["monthly_income"] >= 40000 and amount <= max_amount)
        return {
            "customer_id": customer_id,
            "loan_type": loan_type,
            "requested_amount": amount,
            "eligible": eligible,
            "reason": "Meets demo income and requested-amount rules." if eligible else "Does not meet demo eligibility rules.",
        }
