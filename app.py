from PIL import Image
import streamlit as st
from groq import Groq
from tavily import TavilyClient
import urllib.parse
import random
import requests
import base64
import io

st.set_page_config(page_title="YAYVERA AI - Asla Uydurmaz", page_icon="⚽", layout="centered")
st.title("⚽ YAYVERA AI")
st.caption("Soru Sor + Fotoğraf Yap - YAYVERA Kurşun!")

groq_key = st.secrets.get("GROQ_API_KEY", "") if "GROQ_API_KEY" in st.secrets else ""
tavily_key = st.secrets.get("TAVILY_API_KEY", "") if "TAVILY_API_KEY" in st.secrets else ""
pollinations_token = st.secrets.get("POLLINATIONS_TOKEN", "") if "POLLINATIONS_TOKEN" in st.secrets else ""

with st.sidebar:
    st.header("⚙️ Ayarlar")
    st.write("gturan126@gmail.com")
    if pollinations_token:
        st.success("✅ Limitsiz Aktif!")

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
                comp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role":"user","content":prompt}])
                st.success(comp.choices[0].message.content)
            except Exception as e:
                st.error(str(e))

st.markdown("---")
st.subheader("2️⃣ 📸 YAYVERA KURŞUN - Fotoğraf Yapar")
st.write("Yüzünü koruyarak yapar!")

uploaded = st.file_uploader("Fotoğraf yükle", type=["jpg","jpeg","png"])
prompt_text = st.text_area("Ne yapsın?", placeholder="Örn: Arka plan Maldivler, üzerinde siyah takım elbise, Çorum FK Stadyumunda")

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, width=350, caption="Referans sensin!")

if prompt_text:
    if st.button("✨ YAYVERA KURŞUN YAPSIN!", type="primary"):
        with st.spinner("Yüzünü tanıyor, sonra çiziyor..."):
            try:
                final_prompt = prompt_text
                
                # Eğer fotoğraf yüklendiyse, Groq Vision ile yüzü tarif et
                if uploaded and groq_key:
                    try:
                        # Fotoğrafı base64 yap
                        buffered = io.BytesIO()
                        img.save(buffered, format="JPEG")
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        
                        client = Groq(api_key=groq_key)
                        vision_resp = client.chat.completions.create(
                            model="meta-llama/llama-4-scout-17b-16e-instruct",
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Bu fotoğraftaki adamı detaylı tarif et: saç, sakal, yüz şekli, ten rengi, yaş. Sadece tarif, yorum yok."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
                                ]
                            }]
                        )
                        face_desc = vision_resp.choices[0].message.content
                        final_prompt = f"{face_desc} olan adam, {prompt_text}, photorealistic, ultra detailed, same face, keep identity"
                        st.caption(f"Yüz tarifi: {face_desc}")
                    except Exception as e:
                        st.caption(f"Yüz okuma atlandı: {e}")
                        final_prompt = f"Same man as reference, {prompt_text}"

                encoded = urllib.parse.quote(final_prompt)
                seed = random.randint(1, 999999)
                image_url = f"https://gen.pollinations.ai/image/{encoded}?width=1024&height=1024&model=flux&nologo=true&seed={seed}"
                headers = {"Authorization": f"Bearer {pollinations_token}"} if pollinations_token else {}
                
                response = requests.get(image_url, headers=headers, timeout=120)
                if response.status_code == 200:
                    st.image(response.content, caption="YAYVERA KURŞUN yaptı! ✅", width=400)
                    st.success("Oldu Gökhan! Bu sefer sensin!")
                    st.balloons()
                else:
                    st.error(f"Hata {response.status_code}: {response.text[:500]}")
            except Exception as e:
                st.error(f"Hata: {e}")
