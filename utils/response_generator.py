import os
import json

def _fallback(query, intent, data):
    if intent == "CHECK_BALANCE":
        return f"Your current available balance is ₹{data['available_balance']:,.2f}."
    if intent == "TRANSACTION_HISTORY":
        txns = data.get("transactions", [])
        if not txns:
            return "I couldn't find any transactions for this customer."
        total = sum(abs(t["amount"]) for t in txns if t["type"] == "DEBIT")
        return f"I found {len(txns)} recent transactions. The total debit amount in the available sample is ₹{total:,.2f}."
    if intent == "LOAN_ELIGIBILITY":
        status = "eligible" if data["eligible"] else "not eligible"
        return f"Based on the demo eligibility rules, you are {status} for the requested {data['loan_type']} amount of ₹{data['requested_amount']:,.0f}. {data['reason']}"
    if intent == "EMI_CALCULATION":
        return f"For a principal of ₹{data['principal']:,.0f} at {data['annual_interest_rate']}% for {data['tenure_years']} years, the estimated monthly EMI is ₹{data['monthly_emi']:,.2f}."
    if intent in {"LOAN_INTEREST_RATE", "INTEREST_RATE", "PRODUCT_INFORMATION"}:
        docs = data.get("documents", [])
        if docs:
            p = docs[0]
            return f"{p['product']} information: interest rate {p['interest_rate']}, maximum amount ₹{p['maximum_amount_inr']:,.0f}, tenure {p['tenure']}."
        return "I couldn't find matching banking product information."
    if intent == "ACCOUNT_DETAILS":
        return f"Your demo account is a {data['account_type']} account ending in {data['account_number'][-4:]}."
    return "I can help with balances, transactions, account details, loan information, interest rates, eligibility and EMI calculations."

def generate_response(query, intent, data):
    """Optional LLM generation. Falls back to deterministic responses.

    To enable an LLM, set OPENAI_API_KEY and install the relevant LangChain
    provider package. Financial facts should remain grounded in tool results.
    """
    if os.getenv("OPENAI_API_KEY"):
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate
            llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a banking assistant. Use ONLY the supplied tool result for financial facts. Never invent balances, rates, eligibility or transactions. Be concise and state when information is unavailable."),
                ("human", "Customer query: {query}\nIntent: {intent}\nVerified tool result: {data}")
            ])
            chain = prompt | llm
            return chain.invoke({"query": query, "intent": intent, "data": json.dumps(data)}).content
        except Exception:
            pass
    return _fallback(query, intent, data)
