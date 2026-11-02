import streamlit as st, urllib.parse, random, requests, base64, io
from PIL import Image, ImageDraw, ImageFont
from groq import Groq
from tavily import TavilyClient

st.set_page_config(page_title="BİLVERA", page_icon="💪", layout="wide")
if 'hak' not in st.session_state: st.session_state['hak'] = 999
if 'ai_image' not in st.session_state: st.session_state['ai_image'] = None

groq_key = st.secrets["GROQ_API_KEY"]
tavily_key = st.secrets["TAVILY_API_KEY"]
polli_token = st.secrets.get("POLLINATIONS_TOKEN","")

st.title("💪 BİLVERA")
st.caption(f"Kalan hakkın: {st.session_state['hak']} | İstediğin her şeyi yapar!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1️⃣ Soru Sor")
    soru = st.text_input("Sor", placeholder="Çorum FK maçı?", label_visibility="collapsed")
    if st.button("Sor", use_container_width=True):
        with st.spinner("Araştırıyor..."):
            tavily = TavilyClient(api_key=tavily_key)
            search = tavily.search(query=soru, max_results=5)
            context = "\n".join([r['content'] for r in search['results']])
            client = Groq(api_key=groq_key)
            comp = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"user","content":f"{context}\nSoru:{soru}"}])
            st.success(comp.choices[0].message.content)

with col2:
    st.subheader("2️⃣ Fotoğraf Yap")
    uploaded = st.file_uploader("Fotoğraf yükle", type=["jpg","png","jpeg"], label_visibility="collapsed")
    if uploaded: st.image(uploaded, width=200)

    prompt = st.text_area("Nasıl olsun?", placeholder="Örn: beni kaslı yap, Maldivler'de takım elbiseli, Çorum FK formasıyla...", height=100)
    yazi = st.text_input("Üzerine yazı (isteğe bağlı)", placeholder="Örn: VAZGEÇME!")
    
    if st.button(f"✨ YAP ({st.session_state['hak']} hak kaldı)", type="primary", use_container_width=True):
        if not prompt: st.warning("Ne istediğini yaz!")
        elif st.session_state['hak'] <= 0: st.error("Hakkın bitti! İleride burası paralı olacak.")
        else:
            face = ""
            if uploaded:
                try:
                    buf = io.BytesIO(); Image.open(uploaded).convert("RGB").save(buf, format="JPEG")
                    img_str = base64.b64encode(buf.getvalue()).decode()
                    client = Groq(api_key=groq_key)
                    v = client.chat.completions.create(model="meta-llama/llama-4-scout-17b-16e-instruct", messages=[{"role":"user","content":[{"type":"text","text":"Describe this person face hair beard detailed"},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{img_str}"}}]}])
                    face = v.choices[0].message.content + ", "
                except: face = "same person same face, "

            full = face + prompt + ", photorealistic, keep face identity, 8k"
            with st.spinner("BİLVERA yapıyor... 20 saniye"):
                url = f"https://gen.pollinations.ai/image/{urllib.parse.quote(full)}?width=1024&height=1024&model=flux&seed={random.randint(1,999999)}&nologo=true"
                r = requests.get(url, headers={"Authorization": f"Bearer {polli_token}"} if polli_token else {}, timeout=120)
                if r.status_code == 200:
                    img = Image.open(io.BytesIO(r.content)).convert("RGB")
                    if yazi:
                        draw = ImageDraw.Draw(img); W,H = img.size; fs = int(W*0.06)
                        try: font = ImageFont.truetype("arial.ttf", fs)
                        except: font = ImageFont.load_default()
                        bbox = draw.textbbox((0,0), yazi, font=font); x = W//2-(bbox[2]-bbox[0])//2; y = H-(bbox[3]-bbox[1])-50
                        draw.text((x+3,y+3), yazi, font=font, fill="black"); draw.text((x,y), yazi, font=font, fill="white")
                    
                    st.session_state['ai_image'] = img
                    st.session_state['hak'] -= 1
                    st.image(img, width=400)
                    buf = io.BytesIO(); img.save(buf, format="JPEG")
                    st.download_button("📥 İndir", buf.getvalue(), "bilvera.jpg", "image/jpeg", use_container_width=True)
                    st.success(f"Bitti! Kalan: {st.session_state['hak']}")
                else: st.error(r.text[:400])
    
    if st.session_state['ai_image'] is not None:
        st.image(st.session_state['ai_image'], caption="Son oluşturulan", width=400)

st.divider()
st.markdown("**BİLVERA** - İletişim: ("**BİLVERA** | © 2026")
