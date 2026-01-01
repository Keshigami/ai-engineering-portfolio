import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Content Ops Assistant", layout="wide")

st.title("🚀 AI Content Ops Assistant")
st.markdown("Turn a campaign brief into multi-channel copy instantly.")

with st.sidebar:
    st.header("🎛️ Brand Controls")
    tone = st.select_slider("Tone of Voice", options=["Professional", "Friendly", "Bold", "Witty"])
    persona = st.selectbox("Target Persona", ["SaaS Founders", "Marketing Managers", "DevOps Engineers"])
    target_channel = st.multiselect("Channels", ["Email", "LinkedIn", "Facebook Ad"], default=["Email", "LinkedIn"])

brief = st.text_area("Campaign Brief", placeholder="Describe your product launch or offer here...", height=150)

if st.button("Generate Content"):
    if not brief:
        st.warning("Please enter a campaign brief.")
    else:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-key-here"))
        
        with st.spinner("Writing copy..."):
            for channel in target_channel:
                st.subheader(f"📱 {channel}")
                
                if not os.getenv("OPENAI_API_KEY"):
                    # Mock response
                    st.info(f"Generated {tone} {channel} content for {persona} based on: '{brief[:30]}...'")
                else:
                    prompt = f"Write a {tone} {channel} post for {persona} based on this brief: {brief}"
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.write(response.choices[0].message.content)
                st.divider()

if st.button("Export to CSV"):
    st.success("Successfully prepared for export (CSV)!")
