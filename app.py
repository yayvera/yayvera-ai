if prompt_text:
    if st.button("✨ YAYVERA KURŞUN YAPSIN!", type="primary"):
        with st.spinner("YAYVERA kurşun yapıyor..."):
            try:
                import requests
                encoded = urllib.parse.quote(prompt_text)
                seed = random.randint(1, 999999)
                
                # Doğru link
                if pollinations_token:
                    image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=turbo&nologo=true&seed={seed}"
                    headers = {"Authorization": f"Bearer {pollinations_token}"}
                    # Token ile gizlice çekiyoruz
                    response = requests.get(image_url, headers=headers, timeout=60)
                    if response.status_code == 200:
                        st.image(response.content, caption="YAYVERA KURŞUN yaptı! ✅", width=400)
                        st.success("Oldu Gökhan! Limitsiz oldu!")
                        st.balloons()
                    else:
                        st.error(f"Pollinations hatası: {response.status_code}")
                        st.image(image_url) # yedek
                else:
                    # Token yoksa eski yöntem
                    image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=turbo&nologo=true&seed={seed}"
                    progress_text = "Pollinations 45 sn kuralı için bekleniyor..."
                    my_bar = st.progress(0, text=progress_text)
                    for percent in range(45):
                        time.sleep(1)
                        my_bar.progress((percent+1)/45, text=f"{45-percent} saniye kaldı...")
                    my_bar.empty()
                    st.image(image_url, caption="YAYVERA KURŞUN yaptı! ✅", width=400)

            except Exception as e:
                st.error(f"Hata: {e}")
