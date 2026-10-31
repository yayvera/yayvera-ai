from PIL import Image
import streamlit as st
import google.generativeai as genai
from groq import Groq
from tavily import TavilyClient
import io

st.set_page_config(page_title="YAYVERA AI - Asla Uydurmaz", page_icon="⚽", layout="centered")
st.title("⚽ YAYVERA AI")
st.caption("Soru Sor + Fotoğraf Düzenle - Asla Uydurmaz")

# --- API KEYLER ---
groq_key = st.secrets.get("GROQ_API_KEY", "") if "GROQ_API_KEY" in st.secrets else ""
tavily_key = st.secrets.get("TAVILY_API_KEY", "") if "TAVILY_API_KEY" in st.secrets else ""
google_key = st.secrets.get("GOOGLE_API_KEY", "") if "GOOGLE_API_KEY" in st.secrets else ""

with st.sidebar:
    st.header("⚙️ Ayarlar")
    if not google_key:
        google_key = st.text_input("GOOGLE_API_KEY (aistudio.google.com)", type="password")
    if not groq_key:
        groq_key = st.text_input("GROQ_API_KEY", type="password")
    if not tavily_key:
        tavily_key = st.text_input("TAVILY_API_KEY", type="password")
    st.markdown("---")
    st.write("gturan126@gmail.com")

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

# --- 2. SENİN İSTEDİĞİN: FOTO + YAZI ---
st.subheader("2️⃣ 📸 Fotoğraf + Yazı = YAYVERA Yapar")
st.write("Fotoğrafını yükle, ne istediğini yaz!")

uploaded = st.file_uploader("Fotoğraf yükle", type=["jpg","jpeg","png"])
prompt_text = st.text_area("Ne yapsın?", placeholder="Örn: Arka planı deniz manzaralı yap, Maldivler olsun. Üstümdeki kıyafet aynı kalsın.\nVeya: Üstüme siyah takım elbise giydir, arka plan Çorum FK Stadyumu olsun.")

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, width=350, caption="Yüklediğin fotoğraf")

if uploaded and prompt_text:
    if st.button("✨ YAYVERA YAPSIN!", type="primary"):
        if not google_key:
            st.error("Google API Key gir! aistudio.google.com'dan ücretsiz al")
        else:
            with st.spinner("YAYVERA yapıyor... 15-20 saniye bekle..."):
                try:
                    genai.configure(api_key=google_key)
                    model = genai.GenerativeModel("gemini-2.5-flash-image-preview")
                    
                    # Foto + Yazı gönder
                    response = model.generate_content([prompt_text, img])
                    
                    # Resim var mı kontrol et
                    new_image = None
                    for part in response.candidates[0].content.parts:
                        if part.inline_data is not None:
                            image_data = part.inline_data.data
                            new_image = Image.open(io.BytesIO(image_data))
                            break
                    
                    if new_image:
                        st.image(new_image, caption="YAYVERA yaptı! ✅", width=400)
                        st.success("Oldu Gökhan! İşte istediğin gibi!")
                        st.balloons()
                        # İndirme butonu
                        buf = io.BytesIO()
                        new_image.save(buf, format="PNG")
                        st.download_button("📥 İndir", buf.getvalue(), file_name="yayvera_yapti.png", mime="image/png")
                    else:
                        # Bazen text döner
                        st.write(response.text)
                        st.warning("Resim üretilemedi, promptu daha net yaz. Örn: 'Keep the person same, change background to beach'")

                except Exception as e:
                    st.error(f"Hata: {e}")
                    st.info("Model: gemini-2.5-flash-image-preview - API key doğru mu kontrol et")
