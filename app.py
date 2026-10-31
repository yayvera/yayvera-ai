from PIL import Image
import streamlit as st
from groq import Groq
from tavily import TavilyClient
import urllib.parse
import random
import time
import requests

st.set_page_config(page_title="YAYVERA AI - Asla Uydurmaz", page_icon="⚽", layout="centered")
st.title("⚽ YAYVERA AI")
st.caption("Soru Sor + Fotoğraf Yap - YAYVERA Kurşun!")

# --- API KEYLER ---
groq_key = st.secrets.get("GROQ_API_KEY", "") if "GROQ_API_KEY" in st.secrets else ""
tavily_key = st.secrets.get("TAVILY_API_KEY", "") if "TAVILY_API_KEY" in st.secrets else ""
pollinations_token = st.secrets.get("POLLINATIONS_TOKEN", "") if "POLLINATIONS_TOKEN" in st.secrets else ""

with st.sidebar:
    st.header("⚙️ Ayarlar")
    if not groq_key:
        groq_key = st.text_input("GROQ_API_KEY", type="password")
    if not tavily_key:
        tavily_key = st.text_input("TAVILY_API_KEY", type="password")
    st.markdown("---")
    st.write("gturan126@gmail.com")
    if pollinations_token:
        st.success("✅ YAYVERA Kurşun Aktif! (Limitsiz)")
    else:
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
prompt_text = st.text_area("Ne yapsın?", placeholder="Örn: Arka plan Maldivler deniz manzarası, üzerinde siyah takım elbise, Çorum FK Stadyumunda")

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, width=350, caption="Yüklediğin referans fotoğraf")

if prompt_text:
    if st.button("✨ YAYVERA KURŞUN YAPSIN!", type="primary"):
        with st.spinner("YAYVERA kurşun yapıyor..."):
            try:
                encoded = urllib.parse.quote(prompt_text)
                seed = random.randint(1, 999999)
                
                if pollinations_token:
                    image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=turbo&nologo=true&seed={seed}"
                    headers = {"Authorization": f"Bearer {pollinations_token}"}
                    response = requests.get(image_url, headers=headers, timeout=90)
                    if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
                        st.image(response.content, caption="YAYVERA KURŞUN yaptı! ✅", width=400)
                        st.success("Oldu Gökhan! Limitsiz!")
                        st.balloons()
                    else:
                        # Bazen json hata döner, onu göster
                        st.error(f"Pollinations dedi: {response.text[:200]}")
                        st.image(image_url)
                else:
                    image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=turbo&nologo=true&seed={seed}"
                    my_bar = st.progress(0, text="45 sn bekleniyor...")
                    for percent in range(45):
                        time.sleep(1)
                        my_bar.progress((percent+1)/45, text=f"{45-percent} sn kaldı...")
                    my_bar.empty()
                    st.image(image_url, caption="YAYVERA KURŞUN yaptı! ✅", width=400)
                    st.balloons()

            except Exception as e:
                st.error(f"Hata: {e}")
