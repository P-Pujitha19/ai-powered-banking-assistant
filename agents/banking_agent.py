from nlp.intent_classifier import IntentClassifier
from nlp.entity_extractor import extract_entities
from agents.tools import BankingTools
from rag.retriever import BankingRetriever
from utils.privacy import mask_sensitive_data
from utils.response_generator import generate_response


class BankingAssistant:
    """Hybrid banking assistant.

    Flow:
    query -> TensorFlow/ML intent layer -> entity extraction
          -> LangChain-compatible tools -> RAG -> GenAI response
    """

    def __init__(self):
        self.classifier = IntentClassifier()
        self.tools = BankingTools()
        self.retriever = BankingRetriever()

    def answer(self, query: str, customer_id: str):
        intent, confidence, classifier_source = self.classifier.predict(query)
        entities = extract_entities(query)

        # Agent/tool routing. This is deliberately explicit and deterministic
        # for the prototype so financial facts come from tools rather than LLM guesses.
        tool_result = None
        tool_name = None

        if intent == "CHECK_BALANCE":
            tool_name = "get_account_balance"
            tool_result = self.tools.get_account_balance(customer_id)

        elif intent == "TRANSACTION_HISTORY":
            tool_name = "get_transaction_history"
            tool_result = self.tools.get_transaction_history(customer_id)

        elif intent == "ACCOUNT_DETAILS":
            tool_name = "get_account_details"
            tool_result = self.tools.get_account_details(customer_id)

        elif intent == "LOAN_ELIGIBILITY":
            tool_name = "check_loan_eligibility"
            amount = entities.get("amount", 500000)
            loan_type = entities.get("loan_type", "personal")
            tool_result = self.tools.check_loan_eligibility(customer_id, loan_type, amount)

        elif intent in {"LOAN_INTEREST_RATE", "PRODUCT_INFORMATION", "INTEREST_RATE"}:
            tool_name = "search_banking_knowledge"
            product = entities.get("loan_type") or entities.get("product") or "personal loan"
            docs = self.retriever.search(product)
            tool_result = {"product": product, "documents": docs}

        elif intent == "EMI_CALCULATION":
            tool_name = "calculate_emi"
            amount = entities.get("amount", 500000)
            rate = entities.get("interest_rate", 11.5)
            tenure = entities.get("tenure_years", 5)
            tool_result = self.tools.calculate_emi(amount, rate, tenure)

        else:
            tool_name = "search_banking_knowledge"
            tool_result = {"documents": self.retriever.search(query)}

        safe_result = mask_sensitive_data(tool_result)
        response = generate_response(query, intent, safe_result)

        debug = {
            "intent": intent,
            "confidence": round(confidence, 3),
            "classifier": classifier_source,
            "entities": entities,
            "selected_tool": tool_name,
        }

        return {"response": response, "debug": debug}
