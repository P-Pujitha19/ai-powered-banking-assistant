import streamlit as st
from agents.banking_agent import BankingAssistant

st.set_page_config(page_title="AI Banking Assistant", page_icon="🏦", layout="centered")

st.title("🏦 AI-Powered Banking Customer Query Assistant")
st.caption("Hybrid AIML + TensorFlow + GenAI + Agentic AI banking prototype")

@st.cache_resource
def get_assistant():
    return BankingAssistant()

assistant = get_assistant()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Demo Customer")
    customer_id = st.selectbox("Customer ID", ["CUST001", "CUST002", "CUST003"])
    st.info("Synthetic data only. No real banking information is used.")
    st.markdown("### Try asking")
    st.markdown("- What is my account balance?")
    st.markdown("- Show my transactions")
    st.markdown("- What is the personal loan interest rate?")
    st.markdown("- Am I eligible for a 5 lakh personal loan?")
    show_debug = st.checkbox("Show developer details", value=False)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("debug") and show_debug:
            st.json(message["debug"])

query = st.chat_input("Ask your banking question...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Processing your request..."):
            result = assistant.answer(query, customer_id)
        st.markdown(result["response"])
        if show_debug:
            st.json(result["debug"])

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["response"],
        "debug": result["debug"]
    })
