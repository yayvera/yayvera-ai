import streamlit as st
from groq import Groq
from tavily import TavilyClient

st.set_page_config(page_title="YAYVERA AI", page_icon="⚽")
st.title("⚽ YAYVERA AI - Gerçek Futbol Bilgisi")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def ara_ve_cevapla(soru):
    arama = tavily_client.search(query=soru, max_results=5, include_answer=True)
    gercek_bilgi = arama.get("answer","") + "\n".join([r["content"][:400] for r in arama["results"]])
    prompt = f"Sen YAYVERA AI'sın. SADECE şu GERÇEK BİLGİYE göre cevap ver, ASLA UYDURMA. GERÇEK BİLGİ: {gercek_bilgi} SORU: {soru}"
    chat = groq_client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":prompt}], temperature=0.1)
    return chat.choices[0].message.content

soru = st.text_input("Sor bakalım:", "Çorum FK Iğdır FK maçı kaç kaç bitti?")
if st.button("Sor"):
    with st.spinner("Gerçek kaynaklardan arıyorum..."):
        st.success(ara_ve_cevapla(soru))
