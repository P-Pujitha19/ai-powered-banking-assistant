"""Generate additional synthetic banking customers and transactions."""
import json, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

names = ["Customer 001", "Customer 002", "Customer 003", "Customer 004", "Customer 005"]
customers = []
accounts = []
transactions = []

for i, name in enumerate(names, 1):
    cid = f"CUST{i:03d}"
    customers.append({
        "customer_id": cid,
        "name": name,
        "monthly_income": random.choice([35000, 45000, 60000, 80000, 100000]),
        "consent": True
    })
    accounts.append({
        "customer_id": cid,
        "account_type": "Savings",
        "account_number": f"90000000{i:04d}",
        "balance": random.randint(15000, 150000)
    })
    for j in range(1, 6):
        transactions.append({
            "transaction_id": f"TXN{i:03d}{j:03d}",
            "customer_id": cid,
            "date": f"2026-09-{j:02d}",
            "description": random.choice(["Grocery Store", "UPI Payment", "Salary Credit", "Utility Bill"]),
            "type": random.choice(["DEBIT", "DEBIT", "CREDIT"]),
            "amount": random.randint(500, 30000)
        })

for filename, obj in [
    ("customers.json", customers),
    ("accounts.json", accounts),
    ("transactions.json", transactions)
]:
    (DATA / filename).write_text(json.dumps(obj, indent=2), encoding="utf-8")

print("Synthetic data generated.")
