# DEBUG İÇİN - NEREDE TAKILIYOR GÖRELİM
import streamlit as st
import os
from groq import Groq
from tavily import TavilyClient

st.set_page_config(page_title="YAYVERA DEBUG", page_icon="🚀")
st.title("DEBUG MODU")

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY", "")

st.write(f"Groq var mı? {'EVET' if GROQ_API_KEY else 'HAYIR'} - {GROQ_API_KEY[:10]}...")
st.write(f"Tavily var mı? {'EVET' if TAVILY_API_KEY else 'HAYIR'} - {TAVILY_API_KEY[:10]}...")

if st.button("Tavily Test Et"):
    try:
        tavily = TavilyClient(api_key=TAVILY_API_KEY)
        res = tavily.search("Şenol Güneş nereli", max_results=2)
        st.success("Tavily çalışıyor!")
        st.json(res)
    except Exception as e:
        st.error(f"Tavily HATASI: {e}")
