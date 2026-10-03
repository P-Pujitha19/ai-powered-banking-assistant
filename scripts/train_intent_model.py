"""Train a small TensorFlow intent classifier.

Run:
    python scripts/train_intent_model.py

The model is intentionally small for demonstration. It uses synthetic examples
and can later be replaced with a larger labeled banking-query dataset.
"""
import json
from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "models" / "intent_classifier"
OUT.mkdir(parents=True, exist_ok=True)

samples = {
    "CHECK_BALANCE": [
        "what is my balance", "show my account balance", "how much money do I have",
        "what is my available balance", "tell me my savings balance"
    ],
    "TRANSACTION_HISTORY": [
        "show my transactions", "show recent transactions", "give me my statement",
        "what did I spend last month", "show my transaction history"
    ],
    "LOAN_ELIGIBILITY": [
        "am I eligible for a loan", "can I get a personal loan",
        "do I qualify for a loan", "check my loan eligibility"
    ],
    "LOAN_INTEREST_RATE": [
        "what is the personal loan interest rate", "tell me home loan rates",
        "what rate do you charge for a loan", "loan interest rate"
    ],
    "EMI_CALCULATION": [
        "calculate my emi", "what is my monthly payment", "calculate installment",
        "emi for five lakh loan"
    ],
    "ACCOUNT_DETAILS": [
        "show my account details", "what type of account do I have",
        "tell me my account number"
    ],
    "PRODUCT_INFORMATION": [
        "tell me about savings account", "what is a fixed deposit",
        "what are personal loan features", "tell me about credit card"
    ],
}

texts, labels = [], []
label_names = list(samples.keys())
for label, rows in samples.items():
    for row in rows:
        texts.append(row)
        labels.append(label_names.index(label))

vectorizer = layers.TextVectorization(output_mode="int", output_sequence_length=30)
vectorizer.adapt(texts)

model = tf.keras.Sequential([
    tf.keras.Input(shape=(1,), dtype=tf.string),
    vectorizer,
    layers.Embedding(len(vectorizer.get_vocabulary()) + 1, 64),
    layers.Bidirectional(layers.LSTM(32)),
    layers.Dense(32, activation="relu"),
    layers.Dense(len(label_names), activation="softmax")
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(texts, labels, epochs=60, verbose=0)

model.save(OUT / "intent_model.keras")
(OUT / "labels.json").write_text(json.dumps(label_names, indent=2))

# Save a portable vocabulary tokenizer representation.
tokenizer = {"vocabulary": vectorizer.get_vocabulary()}
(OUT / "tokenizer.json").write_text(json.dumps(tokenizer, indent=2))

print("Saved TensorFlow model to:", OUT)
