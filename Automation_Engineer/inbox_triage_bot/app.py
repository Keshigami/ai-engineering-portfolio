import streamlit as st
import os
from triage_bot import triage_email
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Ops Inbox Triage Bot", layout="wide")

st.title("🤖 Ops Inbox Triage Bot")
st.markdown("""
Automatically classify and route incoming emails to the right department.
**Goal**: Reduce manual triage time by 70%.
""")

if not os.getenv("OPENAI_API_KEY"):
    st.sidebar.warning("⚠️ OpenAI API Key not found. Running in DEMO mode.")

email_text = st.text_area("Paste the email body below:", height=200, placeholder="e.g., Hi, I want to buy your enterprise plan...")

if st.button("Triage Email"):
    if not email_text:
        st.warning("Please paste an email.")
    else:
        with st.spinner("Analyzing email..."):
            result = triage_email(email_text)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Category", result.category)
            with col2:
                st.metric("Priority", result.priority)
            with col3:
                st.metric("Route To", result.route_to)
            
            st.markdown("### 📝 Summary")
            st.info(result.summary)
            
            st.success(f"Email successfully routed to {result.route_to}")
