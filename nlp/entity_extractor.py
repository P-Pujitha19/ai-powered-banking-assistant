import re

def extract_entities(text: str):
    t = text.lower()
    result = {}

    amount_match = re.search(r'(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lakhs|crore|cr)?', t)
    if amount_match:
        raw = amount_match.group(1).replace(",", "")
        try:
            amount = float(raw)
            unit = amount_match.group(2)
            if unit in {"lakh", "lakhs"}:
                amount *= 100000
            elif unit == "crore" or unit == "cr":
                amount *= 10000000
            if amount >= 1000:
                result["amount"] = int(amount)
        except ValueError:
            pass

    for loan_type in ["personal loan", "home loan", "education loan", "car loan"]:
        if loan_type in t:
            result["loan_type"] = loan_type
            break

    tenure = re.search(r'(\d+)\s*(?:year|years|yr|yrs)', t)
    if tenure:
        result["tenure_years"] = int(tenure.group(1))

    rate = re.search(r'(\d+(?:\.\d+)?)\s*%', t)
    if rate:
        result["interest_rate"] = float(rate.group(1))

    if "savings" in t:
        result["account_type"] = "savings"

    if "fixed deposit" in t or "fd" in t:
        result["product"] = "fixed deposit"

    return result
