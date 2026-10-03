from agents.banking_agent import BankingAssistant

def test_balance():
    result = BankingAssistant().answer("What is my balance?", "CUST001")
    assert "72,450" in result["response"]

def test_transactions():
    result = BankingAssistant().answer("Show my transactions", "CUST001")
    assert "transactions" in result["response"]

def test_loan():
    result = BankingAssistant().answer("Am I eligible for a 5 lakh personal loan?", "CUST001")
    assert result["debug"]["intent"] == "LOAN_ELIGIBILITY"
