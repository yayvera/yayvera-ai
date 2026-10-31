from PIL import Image
import streamlit as st
import os
from groq import Groq
from tavily import TavilyClient

st.set_page_config(page_title="YAYVERA AI - Asla Uydurmaz", page_icon="⚽", layout="centered")

st.title("⚽ YAYVERA AI - Asla Uydurmaz")
st.caption("Bilgisayar, Telefon ve Tablet uyumlu - İnternete bağlı")

# --- API KEYLER ---
# Streamlit secrets'dan alıyor, yoksa yan menüden soruyor
groq_key = st.secrets.get("GROQ_API_KEY", "") if "GROQ_API_KEY" in st.secrets else ""
tavily_key = st.secrets.get("TAVILY_API_KEY", "") if "TAVILY_API_KEY" in st.secrets else ""

with st.sidebar:
    st.header("⚙️ Ayarlar")
    if not groq_key:
        groq_key = st.text_input("Groq API Key (gsk_...)", type="password")
    if not tavily_key:
        tavily_key = st.text_input("Tavily API Key (tvly_...)", type="password")
    st.markdown("---")
    st.write("gturan126@gmail.com")
    st.markdown("[YAYVERA Link](https://yayvera-ai.streamlit.app)")

# --- 1. SORU SORMA KISMI ---
st.subheader("Sor bakalım:")
soru = st.text_input("", placeholder="Örn: Çorum FK Iğdır FK maçı kaç kaç bitti?", label_visibility="collapsed")

if st.button("Sor"):
    if not soru:
        st.warning("Bir soru yaz Gökhan!")
    elif not groq_key or not tavily_key:
        st.error("API keyleri ayarlardan gir!")
    else:
        with st.spinner("YAYVERA araştırıyor, asla uydurmuyor..."):
            try:
                # 1. Tavily ile internetten ara
                tavily = TavilyClient(api_key=tavily_key)
                search = tavily.search(query=soru, search_depth="advanced", max_results=5)
                context = "\n".join([r['content'] for r in search['results']])
                
                # 2. Groq ile cevap ver
                client = Groq(api_key=groq_key)
                prompt = f"""Sen YAYVERA AI'sın, asla uydurmazsın. Sadece aşağıdaki internet sonuçlarına göre cevap ver. Eğer bilgi yoksa 'Bilmiyorum' de, uydurma.
                
                İnternet Sonuçları:
                {context}
                
                Soru: {soru}
                Cevap (Türkçe, kısa ve net):"""
                
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                cevap = completion.choices[0].message.content
                st.success(cevap)
                st.caption(f"Kaynak: {search['results'][0]['url'] if search['results'] else 'İnternet'}")
            except Exception as e:
                st.error(f"Hata: {e}")

# --- 2. YENİ ÖZELLİK: FOTOĞRAF ARKA PLAN DEĞİŞTİRME ---
st.markdown("---")
st.subheader("📸 YAYVERA - Fotoğraf Arka Plan Değiştir")
st.write("Fotoğrafını yükle, YAYVERA arka planı değiştirsin!")

uploaded = st.file_uploader("Fotoğrafını yükle", type=["jpg","png","jpeg"], key="photo")

bg = st.selectbox("Arka plan seç", ["Çorum FK Stadyumu", "Çorum Kalesi", "Orman", "Deniz Manzarası", "Şehir"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Senin fotoğrafın", width=350)
    
    if st.button("🎨 Arka Planı Değiştir!", type="primary"):
        with st.spinner("YAYVERA arka planı değiştiriyor..."):
            colors = {
                "Çorum FK Stadyumu": (0, 128, 0),
                "Çorum Kalesi": (139, 115, 85),
                "Orman": (34, 139, 34),
                "Deniz Manzarası": (30, 144, 255),
                "Şehir": (70, 70, 70)
            }
            bg_color = colors.get(bg, (0,0,0))
            # Yeni arka plan
            new_img = Image.new("RGB", img.size, bg_color)
            # Fotoğrafı ortaya küçült
            w, h = img.size
            scale = 0.75
            small = img.resize((int(w*scale), int(h*scale)))
            x = (w - small.size[0]) // 2
            y = (h - small.size[1]) // 2
            new_img.paste(small, (x, y))
            
            st.image(new_img, caption=f"YAYVERA yaptı! Arka plan: {bg}", width=350)
            st.success(f"YAYVERA yaptı! ✅ Arka plan: {bg}")
            st.balloons()
