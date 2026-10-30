import streamlit as st
import os
from groq import Groq
from tavily import TavilyClient

st.set_page_config(page_title="YAYVERA AI", page_icon="🤖")
st.title("🤖 YAYVERA AI")
st.write("Merhaba! Ben YAYVERA AI, senin yapay zeka asistanın!")

# API Keys
groq_key = st.secrets.get("GROQ_API_KEY", "")
tavily_key = st.secrets.get("TAVILY_API_KEY", "")

if not groq_key:
    st.warning("API anahtarı eklenmemiş. Streamlit Secrets kısmına ekle.")
else:
    client = Groq(api_key=groq_key)
    
    user_input = st.text_input("Bana bir şey sor:")
    
    if user_input:
        with st.spinner("YAYVERA düşünüyor..."):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Sen YAYVERA AI'sın. Türkçe, samimi ve yardımsever bir asistansın."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content)
