from PIL import Image
import streamlit as st
from groq import Groq
from tavily import TavilyClient
import urllib.parse
import random

st.set_page_config(page_title="YAYVERA AI - Asla Uydurmaz", page_icon="⚽", layout="centered")
st.title("⚽ YAYVERA AI")
st.caption("Soru Sor + Fotoğraf Yap - YAYVERA Kurşun!")

# --- API KEYLER ---
groq_key = st.secrets.get("GROQ_API_KEY", "") if "GROQ_API_KEY" in st.secrets else ""
tavily_key = st.secrets.get("TAVILY_API_KEY", "") if "TAVILY_API_KEY" in st.secrets else ""

with st.sidebar:
    st.header("⚙️ Ayarlar")
    if not groq_key:
        groq_key = st.text_input("GROQ_API_KEY", type="password")
    if not tavily_key:
        tavily_key = st.text_input("TAVILY_API_KEY", type="password")
    st.markdown("---")
    st.write("gturan126@gmail.com")
    st.success("✅ YAYVERA Kurşun Aktif!")

# --- 1. SORU SORMA ---
st.subheader("1️⃣ Sor bakalım:")
soru = st.text_input("soru", placeholder="Örn: Çorum FK maçı kaç kaç bitti?", label_visibility="collapsed")
if st.button("Sor"):
    if not groq_key or not tavily_key:
        st.error("Groq ve Tavily keyleri gir!")
    else:
        with st.spinner("Araştırıyor..."):
            try:
                tavily = TavilyClient(api_key=tavily_key)
                search = tavily.search(query=soru, search_depth="advanced", max_results=5)
                context = "\n".join([r['content'] for r in search['results']])
                client = Groq(api_key=groq_key)
                prompt = f"Sen YAYVERA AI'sın, asla uydurmazsın. Sadece şu internet sonuçlarına göre cevap ver:\n{context}\nSoru: {soru}"
                comp = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role":"user","content":prompt}])
                st.success(comp.choices[0].message.content)
            except Exception as e:
                st.error(str(e))

st.markdown("---")

# --- 2. YAYVERA KURŞUN - FOTOĞRAF ---
st.subheader("2️⃣ 📸 YAYVERA KURŞUN - Fotoğraf Yapar")
st.write("Fotoğrafını yükle, ne istediğini yaz, YAYVERA sıfırdan yapsın!")

uploaded = st.file_uploader("Fotoğraf yükle (isteğe bağlı)", type=["jpg","jpeg","png"])
prompt_text = st.text_area("Ne yapsın?", placeholder="Örn: Arka plan Maldivler deniz manzarası, üzerinde siyah takım elbise, Çorum FK Stadyumunda\nÖrn: Sarışın bir adam, arkasında deniz")

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, width=350, caption="Yüklediğin referans fotoğraf")

if prompt_text:
    if st.button("✨ YAYVERA KURŞUN YAPSIN!", type="primary"):
        with st.spinner("YAYVERA kurşun yapıyor... yoğunluk varsa tekrar dene..."):
            try:
                encoded = urllib.parse.quote(prompt_text)
                seed = random.randint(1, 999999)
                image_url_flux = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=flux&nologo=true&seed={seed}&enhance=true"
                image_url_turbo = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=turbo&nologo=true&seed={seed}"
                
                st.image(image_url_flux, caption="YAYVERA KURŞUN yaptı! ✅", width=400)
                st.success("Oldu Gökhan!")
                st.balloons()
                st.markdown(f"[📥 İndir]({image_url_flux}) | Olmazsa: [Turbo ile dene]({image_url_turbo})")
                st.caption("Yoğunluk olursa F5 yapıp 10 sn sonra tekrar dene.")

            except Exception as e:
                st.error(f"Hata: {e}")
