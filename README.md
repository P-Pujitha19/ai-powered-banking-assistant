# AI-Powered Banking Customer Query Assistant

A hybrid banking chatbot prototype combining:

- Python
- AIML / NLP
- TensorFlow intent classification
- GenAI / LLM response generation
- Agentic AI
- LangChain-compatible tool orchestration
- RAG-style banking knowledge retrieval
- Mock banking APIs
- Streamlit UI
- Synthetic customer/account/transaction data
- Privacy masking

## Architecture

Customer -> Streamlit -> Python -> TensorFlow/NLP -> Banking Agent
-> Mock APIs / RAG -> verified data -> GenAI -> privacy-safe response

## Important design principle

Financial facts such as balances, transactions, rates and eligibility are retrieved
from the application's mock tools/data. The LLM is not treated as the source of truth.

## Run locally

Python 3.11 is recommended.

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements-lite.txt
streamlit run app.py
```

The lite dependency set runs the complete demo using deterministic fallbacks.

## Enable TensorFlow intent classification

Install the full requirements:

```bash
pip install -r requirements.txt
python scripts/train_intent_model.py
streamlit run app.py
```

The trained model is automatically detected by `nlp/intent_classifier.py`.

## Enable optional GenAI

Set:

```bash
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
```

The response generator will use the LLM only after obtaining verified tool/RAG data.

If no key is available, the application still runs with deterministic responses.

## Generate more synthetic data

```bash
python scripts/generate_synthetic_data.py
```

## Example queries

- What is my account balance?
- Show my transactions
- What is the personal loan interest rate?
- Am I eligible for a 5 lakh personal loan?
- Calculate EMI for 5 lakh for 5 years
- Show my account details
- Tell me about fixed deposit

## Deployment

### Streamlit Cloud

Recommended for the Streamlit UI.

1. Push this repository to GitHub.
2. Create a Streamlit Cloud app.
3. Select `app.py`.
4. Use Python 3.11.
5. Add `OPENAI_API_KEY` in secrets if GenAI is enabled.

### Render

`render.yaml` is included. It uses the lightweight dependency set so the
Streamlit service remains relatively small.

### Vercel

Vercel is primarily designed around serverless web applications rather than
long-running Streamlit processes. If Vercel is required later, keep this project
architecture and expose the Python agent/API layer as a separate web service,
while deploying the Streamlit frontend elsewhere. Do not try to force the
Streamlit server directly into Vercel.

## Suggested future improvements

1. Replace keyword RAG with embeddings + FAISS/Chroma/pgvector.
2. Replace deterministic routing with a LangChain tool-calling agent.
3. Add authentication and customer consent checks.
4. Add API request logging and latency monitoring.
5. Add automated intent accuracy evaluation.
6. Add unit/integration tests.
7. Add a FastAPI layer for real REST endpoints.
8. Add a transaction date filter.
9. Add an EMI calculator tool with validation.
10. Add human-agent escalation for low-confidence or sensitive queries.

## Project deliverables

- Working Streamlit prototype
- Synthetic banking dataset
- TensorFlow training script
- Banking tools/API simulation
- Agentic orchestration layer
- RAG-style retriever
- Privacy masking
- README documentation
- Render/Docker deployment configuration
