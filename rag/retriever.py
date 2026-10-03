import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class BankingRetriever:
    """Lightweight RAG retriever.

    This starter uses keyword retrieval to stay cloud-friendly. It is intentionally
    structured so it can later be replaced with FAISS/Chroma/pgvector embeddings.
    """

    def __init__(self):
        with open(ROOT / "data" / "banking_products.json", encoding="utf-8") as f:
            self.products = json.load(f)

    def search(self, query):
        q = query.lower()
        scored = []
        for item in self.products:
            text = json.dumps(item).lower()
            score = sum(1 for token in q.split() if token in text)
            if score:
                scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [x[1] for x in scored[:3]] or self.products[:2]
