import re

class IntentClassifier:
    """TensorFlow-ready intent classifier.

    If a trained TensorFlow model exists at models/intent_classifier/intent_model.keras
    it can be loaded here. The included fallback is deterministic so the project runs
    immediately without downloading a large ML model.
    """

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.labels = None
        self._try_load_tensorflow_model()

    def _try_load_tensorflow_model(self):
        try:
            import tensorflow as tf
            from pathlib import Path
            base = Path(__file__).resolve().parents[1] / "models" / "intent_classifier"
            model_path = base / "intent_model.keras"
            tokenizer_path = base / "tokenizer.json"
            labels_path = base / "labels.json"
            if model_path.exists() and tokenizer_path.exists() and labels_path.exists():
                self.model = tf.keras.models.load_model(model_path)
                from tensorflow.keras.preprocessing.text import tokenizer_from_json
                self.tokenizer = tokenizer_from_json(tokenizer_path.read_text())
                self.labels = labels_path.read_text()
                import json
                self.labels = json.loads(self.labels)
        except Exception:
            self.model = None

    def predict(self, text):
        if self.model is not None:
            import tensorflow as tf
            from tensorflow.keras.preprocessing.sequence import pad_sequences
            seq = self.tokenizer.texts_to_sequences([text.lower()])
            x = pad_sequences(seq, maxlen=30, padding="post")
            probs = self.model.predict(x, verbose=0)[0]
            idx = int(probs.argmax())
            return self.labels[idx], float(probs[idx]), "TensorFlow"

        t = text.lower()
        rules = [
            ("CHECK_BALANCE", ["balance", "how much money", "available amount"]),
            ("TRANSACTION_HISTORY", ["transaction", "transactions", "statement", "spent", "spending"]),
            ("LOAN_ELIGIBILITY", ["eligible", "eligibility", "qualify", "can i get", "loan"]),
            ("LOAN_INTEREST_RATE", ["loan interest", "interest rate", "rate for", "loan rate"]),
            ("EMI_CALCULATION", ["emi", "monthly payment", "installment"]),
            ("ACCOUNT_DETAILS", ["account details", "account number", "account type"]),
            ("INTEREST_RATE", ["interest rate", "fd rate", "deposit rate"]),
            ("PRODUCT_INFORMATION", ["savings account", "fixed deposit", "credit card", "personal loan", "home loan"]),
        ]
        for intent, phrases in rules:
            if any(p in t for p in phrases):
                return intent, 0.90, "Rule-based fallback"
        return "GENERAL_BANKING", 0.55, "Rule-based fallback"
